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
        ''' 
        #FIXME no longer using out_queue
        self.out_queue = None 
        '''
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
                            self.ack_queue, self.out_queue)
                t.daemon = True
                t.start()
            logger.debug('\nElkaDriverThread thread has restarted')
            i += 1

    def close(self):
        for t in self._threads:
            t.stop()
            t = None

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

    RETRYCNT_BEFORE_DISCONNECT = 10

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

    @staticmethod
    def convert_raw(raw):
        ''' Convert from floating pt number range [-1 1] to 12 bit number range
            [0 4000]
        '''
        orig = []
        to_datum = 1
        trans = 2000
        for r in raw:
            orig.append(int(((r + to_datum)*trans)))

        wrd_orig_sz = 12
        wrd_trans_sz = 8

        trans = ElkaDriverThread.convert_array_wrd_sz(orig, wrd_orig_sz, wrd_trans_sz)
        return trans 

    @staticmethod
    def convert_array_wrd_sz(a, wrd_a_sz, wrd_b_sz):
        ''' converts array a of word size wrd_a_sz into array b of word size
            wrd_b_sz ''' 
        in_t = int(math.ceil((float(wrd_a_sz)/float(wrd_b_sz))*len(a)))

        b = [0] * in_t

        k = 0
        for i in range(len(a)):
            for j in range(wrd_a_sz):
                b_idx = int(math.floor(k/wrd_b_sz)) 
                if j == 0 or (k % wrd_b_sz) == 0: # if at beginning of a[i] or b[i]
                    shift = (wrd_a_sz - j) - (wrd_b_sz - (k % wrd_b_sz))
                mask = 1 << ((wrd_a_sz - 1) - j)
                if shift >= 0:
                    b[b_idx] |= (a[i] & mask) >> shift
                else:
                    b[b_idx] |= (a[i] & mask) << abs(shift)
                k += 1
        
        return b


    def stop(self):
        """ Stop the thread """
        self.sp = True
        try:
            self.join()
        except Exception:
            pass

    def run(self):
        """ Run the receiver thread """
        logger.debug('\nElkaDriverThread running')
        while not self.sp:
            ackIn = None
                        
            # Grabs data from in_queue
            # pk = self.package_data() 

            header = [0, 255, 255]
            # array must be unpacked singularly
            data_out_h = struct.pack('B' * len(header), *header) # pack header
            p = self.in_queue.get()
            trans = ElkaDriverThread.convert_raw(p)
            data_out_d = struct.pack('B' * len(trans), *trans) # pack data
            data_out = data_out_h + data_out_d
            log_outputs.info('\nheader : {0}\ndata: {1}\nsize: {2}'.format(header,
                trans, len(data_out)))
   
            # Takes DataPacket and attempts to send it, will wait
            # on empty data packets
            while self.retry_before_disconnect and ackIn is None:
                try:
                    ackIn = self.eradio.send_packet(data_out) # ackIn is raw imu
                                                              # data in a struct
                except Exception as e:
                    raise

                if ackIn is None:
                    # primitive version of Bitcraze callbacks
                    log_acks.debug('No ack received, RBDct = ' + self.retry_before_disconnect)
                    self.retry_before_disconnect -= 1
                    if not self.retry_before_disconnect:
                            self.sp = True
                else:
                    log_acks.info('ackIn data: {0}'.format(
                            ackIn))
                    self.ack_queue.put(ackIn)
                    
            self.retry_before_disconnect = self.RETRYCNT_BEFORE_DISCONNECT
########## End of ElkaDriverThread Class ##########
