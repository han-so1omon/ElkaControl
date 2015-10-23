import sys, os, Queue, threading, logging, traceback, logging.config, logging.handlers
sys.path.append(os.getcwd()) 

from collections import deque
from Elkaradio.elkaradioTRX import *
from Inputs.joy_read import JoyThread 
from Utils.exceptions import *
from Utils.exThread import ExThread

############################## Set up loggers ##################################
logging.config.fileConfig('./Logging/Logs/logging1.conf', disable_existing_loggers=False)
logger = logging.getLogger('main.elkaThread')
#logger = logging.getLogger('main')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
log_acks = logging.getLogger('acks')
################################################################################

############### utility functions ###############
def convert_raw(raw):
  out = []
  to_datum = 1
  trans = 1000
  for i in range(len(raw)):
    if i == 0: # transform to [1000 2000]
      out.append(int((1-raw[i]) * 1000))
    else: # transform to [-1000 1000]
      out.append(int(raw[i]*1000))
  split_bytes(out)
  return out

def flatten(l):
  res = []
  for r in l:
    if isinstance(r, list):
      res.extend(flatten(r))
    else:
      res.append(r)
  return res

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

############## gains enum class ###################
class Headers(object):
  def __init__(self):
    self.debug = [chr(0),chr(255),chr(255)]
    self.gains = [chr(1),chr(255),chr(255)]
    self.pilot_inputs = [chr(4),chr(255),chr(255)]

############## driver thread class #################
""" New way to run the receiver thread """
class DriverThread(ExThread):
  def __init__(self, eradio, inQueue=None):
    ExThread.__init__(self)
    self.eradio = eradio
    self.sp = False
    self.in_queue = inQueue
    self.header = Headers()

  def run_w_exc(self):
    #FIXME temp
    kppitch = 10
    kdpitch = 200
    kproll = 10
    kdroll = 200
    kpyaw = 200
    kdyaw = 0

    pitch_gains = split_bytes(kppitch) +\
                  split_bytes(kdpitch)
    roll_gains = split_bytes(kproll) +\
                 split_bytes(kdroll)
    yaw_gains = split_bytes(kpyaw) +\
                split_bytes(kdyaw)

    # Initial packet with gains
    payload = pitch_gains + roll_gains + yaw_gains
    payload = map(chr,payload)


    # Send gains first
    header_gains = self.header.gains
    header_pilot = self.header.pilot_inputs
    payload = header_gains+ map(chr,pitch_gains+roll_gains+yaw_gains)
    payload.insert(0,chr(len(payload)))
    payload = ''.join(payload)
    ackIn = self.eradio.send(payload)
  
    while not self.sp:
      ackIn = None

      # get raw data from controller
      raw = self.in_queue.pop()
      
      payload = header_pilot + map(chr,flatten(map(split_bytes, convert_raw(raw))))
      #payload = header + map(chr,flatten(map(convert_raw(raw))))
      payload.insert(0,chr(len(payload)))
      payload = ''.join(payload)

      #''' New way to send and receive packets '''
      ackIn = self.eradio.send(payload)
      # convert payload back to readable format
      payload = map(ord,list(payload))
      
      log_outputs.info('{}'.format(payload))
      log_acks.info('{}'.format(ackIn))
      logger.debug('{}'.format(ackIn))
          
  def stop(self):
    self.sp = True

################## main run function ########################
def run_elka():
  def chk_thread(t):
    if t.isAlive():
      t.join(1)

  def stop_thread(t):
    t.stop()
    logger.debug('\n{0} stopped'.format(t.name))

  eradio = Elkaradio()

  #limit queue size to prevent command buffer from forming
  in_queue = deque(maxlen=50)
  threads = []
  joy = JoyThread(in_queue)
  joy.start()
  threads.append(joy)
  t = DriverThread(eradio,in_queue)
  t.start()
  threads.append(t)

  # Check if thread threw an Exception and should terminate
  try:
    while(True):
      map(lambda t: chk_thread(t), threads)
  except:
    map(lambda t: stop_thread(t), threads)
    usb.util.dispose_resources(eradio.dev)
    raise

if __name__ == '__main__':
    run_elka()
