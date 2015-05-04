"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: ETP 
Module: elkaDriver.py 

Driver for base station of Elka autopilot.

Takes inputs from a joystick controller and converts them to data packets.
Data packets are sent via Elkaradio wireless link to tethered Elka inertial
quadrotor autopilot system. Receives acks from tethered Elka (or any compatible
nRF24L01p as specified in ElkaradioTRX.py) 

"""

import sys, os
sys.path.append(os.getcwd()) 
import Queue, threading, struct, logging, math

from time import sleep
from IPython import embed

from Elkaradio.elkaradioTRX import Elkaradio
from Inputs.joystickCtrl import * 
from ETP.dataPacket import DataPacket
from Utils.exceptions import *

############################## Set up loggers ##################################
logger = logging.getLogger('main.elkaDriver')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
log_acks = logging.getLogger('acks')
################################################################################

########## ElkaDriver Class ##########
class ElkaDriver(object):
    def __init__(self, dev = None):
        """ Create the link driver """
        self.dev = dev
        self.eradio = None
        
        self.joystick = None
        self.axes = None
    
        # queue access must be atomic
        self.in_queue = None 

        self.ack_queue = None 
        
        # driver runs joystick_ctrl and driver threads
        self._threads = []

    def start(self):
        # Initialize eradio and joystick
        try:
            try: # connect to eradio
                self.connect()
                logger.debug('\nElkaradio is connected')
            except LinkEstablished: # already a link in place
                logger.debug('\nLink is already in place')

            #connect to joystick
            j = JoystickCtrl(self.in_queue)
            self.axes = Axes(j.ctrlr_name)

            logger.debug('\n{0} joystick has been'.format(j.ctrlr_name) + ' initialized') 

            self._threads.append(j)
            j.daemon = True
            j.start()
        except JoystickNotFound as e:
            raise
        except LinkException as e:
            raise
        except KeyboardInterrupt as e:
            raise
        except Exception as e:
            raise

    def restart(self):
        i = 0
        for t in self._threads:
            # check for live thread
            if not t.isAlive():
            # restart threads
                if i == 0:
                    t = JoystickCtrl()
                    self.axes_enum = Axes(t.ctrlr_name)
                elif i == 1:
                    t= ElkaDriverThread(self.eradio, self,in_queue, 
                            self.ack_queue)
                t.daemon = True
                t.start()
            logger.debug('\nElkaDriverThread thread has restarted')
            i += 1

    def close(self):
        if self.eradio is not None:
            self.eradio.close()

        self.eradio = None

        logger.debug('\nElkaDriver is closed')
        #also flush in_queue and out_queue contents

    def connect(self):
        channel = 40
        datarate = Elkaradio.DR_250KPS
        if self.eradio is None:
            try:
                self.eradio = Elkaradio(self.dev)
            except ElkaradioNotFound as e:
                raise
        else:
            raise Exception ("Link already open!") 

        # prepare the inter-thread communication queue
        self.ack_queue = Queue.Queue()
        self.in_queue = Queue.Queue()
        '''
        # limited size out queue to avoid 'Readback effect'
        self.out_queue = Queue.Queue(50)
        '''

        t = ElkaDriverThread(self.eradio, self.in_queue, self.ack_queue)
                             
        self._threads.append(t)
        
        # start thread as daemon because packet handling occurs
        # passively
        t.daemon = True
        t.start()
        logger.debug('\nBase node is beginning transmission')

    def get_status(self):
        if self.eradio is None:
            try:
                self.eradio = Elkaradio()
            except USBError as e:
                return "Cannot open Elkaradio. Permission problem?"\
                       " ({})".format(str(e))
            except Exception as e:
                return str(e)

        mode = None
        if self.eradio.radio_mode == 0:
            mode = 'MODE_PTX'
        elif self.eradio.radio_mode == 1:
            mode = 'MODE_PTX_SYNCHRONOUS'
        elif self.eradio.radio_mode == 2:
            mode = 'MODE_PRX'
        elif self.eradio.radio_mode == 3:
            mode = 'MODE_HYBRID' 
        logger.debug('\nElkaradio versio {} in {}'.format(
                        self.eradio.version, mode))
            
        return "Elkaradio version {} in {}".format(
                        self.eradio.version, mode)

    @property
    def name(self):
        return "radio"

########## End of ElkaDriver Class ##########

########## ElkaDriverThread Class ##########
class ElkaDriverThread(threading.Thread):
    """ Radio link receiver thread used to read data from the Elkaradio
        USB driver. """

    def __init__(self, eradio, inQueue, ackQueue):
        """ Create the object """
        threading.Thread.__init__(self)
        self.eradio = eradio
        self.in_queue = inQueue
        self.ack_queue = ackQueue
        '''
        #FIXME no longer using outQueue
        self.out_queue = outQueue
        '''
        self.sp = False

    def receive_packet(self, time=0):
        """
        receive a packet though the link. this call is blocking but will
        timeout and return none if a timeout is supplied.
        """
        pk = None
        if time == 0:
            try:
                pk = self.ack_queue.get(False)
                log_acks.info('\n{0}'.format(pk))
                return pk
            except Queue.Empty:
                return None
        elif time < 0:
            try:
                pk = self.ack_queue.get(True)
                log_acks.info('\n{0}'.format(pk))
            except Queue.Empty:
                return None
        else:
            try:
                pk = self.ack_queue.get(True, time)
                log_acks.info('\n{0}'.format(pk))
            except Queue.Empty:
                return None

    @staticmethod
    def convert_raw(raw):
        ''' Convert from floating pt number range [-1 1] to 16 bit number '''
        out = []
        to_datum = 1
        trans = 1000
        for i in range(len(raw)):
            if i == 0: # transform to [1000 2000]
                out.append(int((1.5 + raw[i]) * 1000))
            else: # transform to [-1000 1000]
                out.append(int(raw[i]*1000))

        return out

    def run(self):
        """ Run the receiver thread """
        logger.debug('\nElkaDriverThread running')

        while not self.sp:
            ackIn = None
            header = [4, 255, 255]
            data_out_h = struct.pack('B' * len(header), *header) # pack header

            # get raw data from controller
            raw = self.in_queue.get()

            data = ElkaDriverThread.convert_raw(raw)
            
            data_out_d = ''
            for d in data:
                d1 = (d >> 8) & 0xff
                d2 = d & 0xff
                data_out_d += struct.pack('B', d1) # data
                data_out_d += struct.pack('B', d2) # data

            data_out = data_out_h + data_out_d
            while len(data_out) < 32:
                data_out += struct.pack('B', 0)

            # log formatted output. data size includes padded zeros
            log_outputs.info('\nheader : {0}\ndata: {1}'.format(header, data))

            ackIn = self.eradio.send_packet(data_out)

            # Sixth bit in the status register (read from register) will always
            # be one. Read the 6th bit in the status register until a good
            # packet has been received.

            ''' Length of ackIn will be 1 (e.g. single 0) if an invalid packet
            is read
            '''

            while len(ackIn) == 1:
                try:
                    ackIn = self.dev.read(0x81, 64, 1000)
                except Exception as e:
                    raise

            log_acks.info('ackIn data: {0}'.format(
                    ackIn))
            self.ack_queue.put(ackIn)
########## End of ElkaDriverThread Class ##########
