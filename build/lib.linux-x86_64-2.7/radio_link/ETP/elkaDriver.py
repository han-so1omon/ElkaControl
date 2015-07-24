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

from Elkaradio.elkaradioTRX import *
from Inputs.joystickCtrl import * 
#from ETP.exceptionThread import ExThread
from Utils.exceptions import *

############################## Set up loggers ##################################
logger = logging.getLogger('main.elkaDriver')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
log_acks = logging.getLogger('acks')
################################################################################

########## Utility methods  ##########
""" Convert list of floating pt numbers ranging [-1 1] to 8 bit integer list
"""
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

""" Flatten list into single array """
def flatten(l):
  res = []
  for r in l:
    if isinstance(r, list):
      res.extend(flatten(r))
    else:
      res.append(r)
  return res

""" Convert list of 16-bit numbers into 2 8-bit numbers """
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

########## ElkaDriver Class ##########
class ElkaDriver(object):
  def __init__(self, dev = None):
    """ Create the link driver """
    self.dev = dev
    self.eradio = None

    self.joystick = None
    self.axes = None

    self.in_queue = None 
    self.ack_queue = None 

    # driver runs joystick_ctrl and driver threads
    self._threads = []

    '''
    #FIXME debugging
    class mockT(ExThread):
      def run_w_exc():
        while True:
          pass
    et = mockT()
    et.start()
    logger.debug('test thread is alive?:{}'.format(et.isAlive()))
    '''
 
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
      #j.daemon = True #FIXME necessary?
      j.start()
    except JoystickNotFound:
      raise
    except LinkException:
      raise
    except KeyboardInterrupt:
      raise
    except:
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
        self.dev = self.eradio.dev # if none given
      except ElkaradioNotFound:
        raise
    else:
      raise LinkEstablished("Link already open!") 

    # prepare the inter-thread communication queue
    self.ack_queue = Queue.Queue()
    self.in_queue = Queue.Queue()

    t = ElkaDriverThread(self.eradio, self.in_queue, self.ack_queue)
    self._threads.append(t)
    t.start()
    if t.isAlive():
      logger.debug('\nBase node is beginning transmission')
    else:
      raise LinkException('ElkaDriverThread failed to start')

  def get_status(self):
    if self.eradio is None:
      try:
        self.eradio = Elkaradio()
      except USBError:
        raise 
      except Exception:
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

############## ExThread class ####################
class ExThread(threading.Thread):
  """ Defines a thread capable of passing exceptions """
  def __init__(self):
      threading.Thread.__init__(self)
      self.__status_queue = Queue.Queue()

  def run_w_exc(self):
      raise NotImplementedError

  def run(self):
      try:
          self.run_w_exc()
      except KeyboardInterrupt:
          self.__status_queue.put(sys.exc_info())
      except:
          self.__status_queue.put(sys.exc_info())
      self.__status_queue.put(None)

  def wait_for_exc_info(self):
      return self.__status_queue.get()

  def join_w_exc(self):
      ex_info = self.wait_for_exc_info()
      if ex_info is None:
          print 'none hurr'
          return
      else:
          raise ex_info[1]

########## ElkaDriverThread Class ##########
class ElkaDriverThread(ExThread):
  """ Radio link receiver thread used to read data from the Elkaradio
      USB driver. """

  def __init__(self, eradio, inQueue, ackQueue):
    """ Create the object """
    ExThread.__init__(self)
    #threading.Thread.__init__(self)
    self.eradio = eradio
    self.in_queue = inQueue
    self.ack_queue = ackQueue
    self.sp = False

  """ New way to run the receiver thread """
  def run_w_exc():
    logger.debug('\nElkaDriverThread running')

    #FIXME temp
    kppitch = 1
    kdpitch = 1
    kproll = 1
    kdroll = 1
    kpyaw = 1
    kdyaw = 1

    header = [chr(0),chr(255),chr(255)]
    pitch_gains = split_bytes(kppitch) +\
                  split_bytes(kdpitch)
    roll_gains = split_bytes(kproll) +\
                 split_bytes(kdroll)
    yaw_gains = split_bytes(kpyaw) +\
                split_bytes(kdyaw)

    # Initial packet with gains
    payload = pitch_gains + roll_gains + yaw_gains
    payload = map(chr,payload)
    payload = header + payload
    # Format payload as string to comply with pyusb standards
    payload = ''.join(payload)
    
    log_outputs.info('\nGains\n{0}'.format(payload))

    ackIn = None
    ackIn = eradio.send(payload)
    if ackIn:
      log_acks.info('ackIn data: {0}'.format(ackIn))
      self.ack_queue.put(ackIn)
    else:
      log_acks.debug('no ack received')

    #time.sleep(0.1) # tune this as necessary

    # New header for control inputs
    header = [chr(0),chr(255),chr(255)]

    while not self.sp:
      ackIn = None

      # get raw data from controller
      raw = self.in_queue.get() 
      payload = header + map(chr,flatten(map(split_bytes, convert_raw(raw))))
      #print payload
      payload = ''.join(payload)

      ''' New way to send and receive packets '''
      ackIn = eradio.send(payload)
      #time.sleep(0.1)
      if ackIn:
        log_acks.info('ackIn data: {0}'.format(ackIn))
        self.ack_queue.put(ackIn)
      else:
        log_acks.debug('no ack received')

  """ Stop the thread. Should only be called from another thread """
  def stop(self):
    self.sp = True
########## End of ElkaDriverThread Class ##########

