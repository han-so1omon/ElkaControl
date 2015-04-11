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
import Queue, threading, array, logging

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
        #FIXME no longer using out_queue
        self.out_queue = None 
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

    def pause(self):
        for t in self._threads:
            t.stop()
            t = None

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
                            self.ack_queue, self.out_queue)
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
        channel = 2
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
        # limited size out queue to avoid 'Readback effect'
        self.out_queue = Queue.Queue(50)

        t = ElkaDriverThread(self.eradio, self.in_queue, self.ack_queue,
                             self.out_queue)
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

    RETRYCNT_BEFORE_DISCONNECT = 10

    def __init__(self, eradio, inQueue, ackQueue, outQueue):
        """ Create the object """
        threading.Thread.__init__(self)
        self.eradio = eradio
        self.in_queue = inQueue
        self.ack_queue = ackQueue
        #FIXME no longer using outQueue
        self.out_queue = outQueue
        self.sp = False
        self.retry_before_disconnect = self.RETRYCNT_BEFORE_DISCONNECT

    def receive_packet(self, time=0):
        """
        receive a packet though the link. this call is blocking but will
        timeout and return none if a timeout is supplied.
        """
        pk = None
        if time == 0:
            try:
                pk = self.ack_queue.get(False)
                log_acks.info('{0}'.format(pk))
                return pk
            except Queue.Empty:
                return None
        elif time < 0:
            try:
                pk = self.ack_queue.get(True)
                log_acks.info('{0}'.format(pk))
            except Queue.Empty:
                return None
        else:
            try:
                pk = self.ack_queue.get(True, time)
                log_acks.info('{0}'.format(pk))
            except Queue.Empty:
                return None

    def package_data(self):
        """ form packet and send to out_queue """
        #FIXME fix header
        #FIXME problem with self.in_queue.get()
        header = [0, 255, 255] 
        try:
            pk = DataPacket.output(header, self.in_queue.get())
        except Queue.Empty:
            pk = DataPacket.output(header) 



        '''
        try:
            self.out_queue.put(pk, true, 2)
        except Queue.Full:
            raise QueueFullException()
        '''

        return pk
   
    def stop(self):
        """ Stop the thread """
        self.sp = True
        try:
            self.join()
        except Exception:
            pass

    def run(self):
        """ Run the receiver thread """
        data_out = array.array('B', [0x00])
        wait_time = 0
        empty_ctr = 0
        
        logger.debug('\nElkaDriverThread running')
        while not self.sp:
            try:
                ack_status = self.eradio.send_packet(data_out)
            except Exception as e:
                raise

            if ack_status is None:
                # primitive version of Bitcraze callbacks
                log_acks.debug('No ack received')
                continue

            if ack_status.ack is False:
                self.retry_before_disconnect -= 1

                #FIXME fix decrementing and resetting retry_before_disconnect
                if self.retry_before_disconnect == 0:
                    continue
            self.retry_before_disconnect = self.RETRYCNT_BEFORE_DISCONNECT

            data = ack_status.data

            # If there is a copter in range, the packet is analyzed and
            # the next packet is prepared
            if (len(data) > 0):
                ack_packet = DataPacket.ack(data[0:3], list(data[3:]))
                log_acks.info('{0},{1}'.format(
                    ack_packet.header, ack_packet.data))
                # print "<- " + ackPacket.__str__()
                self.ack_queue.put(ack_packet)
                wait_time = 0
                empty_ctr = 0
            else:
                empty_ctr += 1
                if (empty_ctr > 10):
                    empty_ctr = 10
                    # Relaxation time if the last 10 packets were empty
                    wait_time = .01
                else:
                    wait_time = 0

            '''
            #FIXME not able to retrieve from queue
            out = self.out_queue.get(True, waitTime)
            self.package_data(out)
            '''
            pk = self.package_data() 

            #out_packet = self.package_data(self.out_queue.get(True, waitTime))

            data_out = array.array('B', *pk.) # 
            if out_packet:
                # print "-> " + outPacket.__str__()
                for h in out_packet.header:
                    data_out.put(h)
                for x in out_packet.data:
                    if type(x) == int:
                        data_out.put(x)
                    else:
                        data_out.put(ord(x))
            else:
                data_out.put(0x00)

########## End of ElkaDriverThread Class ##########
