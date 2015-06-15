import sys, os, Queue, threading, logging, traceback
sys.path.append(os.getcwd()) 

from Elkaradio.elkaradioTRX import *
from Inputs.joy_read import JoyThread 
from Utils.exceptions import *
from Utils.exThread import ExThread

############################## Set up loggers ##################################
logger = logging.getLogger('main.elkaThread')
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
      out.append(int((1.5 + raw[i]) * 1000))
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

############## driver thread class #################
""" New way to run the receiver thread """
class DriverThread(ExThread):
  def __init__(self, eradio, inQueue=None):
    ExThread.__init__(self)
    self.eradio = eradio
    self.sp = False
    self.in_queue = inQueue

  def run_w_exc(self):
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
    log_outputs.info('{}'.format(payload))
    
    ackIn = None
    ackIn = self.eradio.send(payload)

    log_acks.info('{}'.format(ackIn))

    # New header for control inputs
    header = [chr(0),chr(255),chr(255)]

    while not self.sp:
      ackIn = None

      # get raw data from controller
      raw = self.in_queue.get()
      
      payload = header + map(chr,flatten(map(split_bytes, convert_raw(raw))))
      payload = ''.join(payload)
      log_outputs.info('{}'.format(payload))

      #''' New way to send and receive packets '''
      ackIn = self.eradio.send(payload)
      log_acks.info('{}'.format(ackIn))
          
  def stop(self):
    self.sp = True

################## main run function ########################
def run_elka():
  def chk_thread(t):
    if t.isAlive():
      t.join(1)

  def stop_thread(t):
    t.stop()
    logger.debug('\nThread {0} stopped'.format(t.name))

  eradio = Elkaradio()
  in_queue = Queue.Queue()

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
