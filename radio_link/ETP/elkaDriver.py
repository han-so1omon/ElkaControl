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

Logging is done with hex representations of numbers so that they do not have to
be converted back into decimal numbers. This increases execution speed.
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
        logger.debug('\nElkaradio is connected to base station CPU')
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
        raise 
      except Exception as e:
        raise

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

  """ Convert list of floating pt numbers ranging [-1 1] to 8 bit integer list
  """
  @staticmethod
  def convert_raw(raw):
    out = []
    to_datum = 1
    trans = 1000
    for i in range(len(raw)):
      if i == 0: # transform to [1000 2000]
        out.append(int((1.5 + raw[i]) * 1000))
      else: # transform to [-1000 1000]
        out.append(int(raw[i]*1000))
    split_bytes(out)
    return out

  @staticmethod
  def flatten(l):
    res = []
    for r in l:
      if isinstance(r, list):
        res.extend(flatten(r))
      else:
        res.append(r)
    return res

  @staticmethod
  def split_bytes(vals):
    l = []
    if isinstance(vals, list):
      for v in vals:
        l.append((v>>8)&0xff)
        l.append(v&0xff)
    else:
      l.append((vals>>8)&0xff)
      l.append(vals&0xff)
    return l

  #FIXME
  """ New way to run the receiver thread """
  def run(self):
    try:
      logger.debug('\nElkaDriverThread running')

      #FIXME temp
      kppitch = 1
      kdpitch = 1
      kproll = 1
      kdroll = 1
      kpyaw = 1
      kdyaw = 1

      header = [chr(0),chr(255),chr(255)]
      pitch_gains = ElkaDriverThread.split_bytes(kppitch) +\
                    ElkaDriverThread.split_bytes(kdpitch)
      roll_gains = ElkaDriverThread.split_bytes(kproll) +\
                   ElkaDriverThread.split_bytes(kdroll)
      yaw_gains = ElkaDriverThread.split_bytes(kpyaw) +\
                  ElkaDriverThread.split_bytes(kdyaw)


      # Initial packet with gains
      payload = pitch_gains + roll_gains + yaw_gains
      payload = map(chr,payload)
      payload = header + payload
      # Format payload as string to comply with pyusb standards
      payload = ''.join(payload)

      log_outputs.info('\nGains\n{0}'.format(payload))

      ackIn = None
      ackIn = self.eradio.send(payload)
      time.sleep(0.1) # FIXME tune this as necessary
      if ackIn:
        log_acks.info('ackIn data: {0}'.format(ackIn))
        self.ack_queue.put(ackIn)
      else:
        log_acks.debug('no ack received')

      # Switch to control inputs
      log_outputs.info('\nControls')

      # New header for control inputs
      header = [chr(0),chr(255),chr(255)]

      logger.debug('\nSending control inputs')
      while not self.sp:
        ackIn = None

        # get raw data from controller
        raw = self.in_queue.get()

        payload = header + ElkaDriverThread.convert_raw(raw)
        payload = ''.join(payload)

        # log output
        log_outputs.info('{0}'.format(payload))

        ''' New way to send and receive packets '''
        ackIn = self.eradio.send(payload)
        time.sleep(0.1)

        if ackIn:
          log_acks.info('ackIn data: {0}'.format(ackIn))
          self.ack_queue.put(ackIn)
        else:
          log_acks.debug('no ack received')

    except Exception as e:
      raise
    finally:
      self.join()

  """ Old way to run receiver thread
  def run(self):
    # Size data_out to fit Enhanced Shockburst packet
    data_out = '\0' * 32
    header = (str(x) for x in [0,255,255])
    # pack header
    log_outputs.debug('data out: {}'.format(data_out))
    for i in range(3):
      data_out += struct.pack('B', header[i])    

    # get raw data from controller
    raw = self.in_queue.get()

    data = ElkaDriverThread.convert_raw(raw)

    # Convert data into 8-bit numbers
    # Fill data_out
    for i in range(3,7):
      d1 = (d >> 8) & 0xff
      d2 = d & 0xff
      data_out[i] = struct.pack('B', d1) # data
      data_out[i+1] = struct.pack('B', d2) # data

    # log output
    log_outputs.info('{0}{1}'.format(header, data))

    self.eradio.dev.write(1, dataOut, 1000)

    ''' Length of ackIn will be 1 (e.g. single 0) if an invalid packet
    is read
    '''
    #while not ackIn or len(ackIn) == 1:
    while not ackIn:
      try:
        ackIn = self.dev.read(0x81, 64, 1000)
      except Exception as e:
        raise
  """

  def stop(self):
    """ Stop the thread. Should only be called from another thread """
    self.sp = True
########## End of ElkaDriverThread Class ##########
