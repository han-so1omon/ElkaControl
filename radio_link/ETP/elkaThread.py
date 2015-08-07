"""
Author: Eric Solomon
Project: Elkaradio Control 
Lab: Alfred Gessow Rotorcraft Center
Package: ETP
Module: elkaThread.py

Contains methods for converting joystick inputs and running elka.
"""

import sys, os, Queue, threading, logging, traceback
sys.path.append(os.getcwd()) 

from collections import deque
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
#FIXME tune this
def convert_raw(raw):
  out = []
  to_datum = 1
  trans = 1000
  for i in range(len(raw)):
    if i == 0: # transform thrust to [1000 2000]
      out.append(int((3 + raw[i]) * 500))
    else: # transform roll,pitch,yaw to [-1000 1000]
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
    self.gains = [chr(5),chr(255),chr(255)]
    self.sensitivity = [chr(6),chr(255),chr(255)]
    self.trim = [chr(4),chr(255),chr(255)]

############## driver thread class #################
""" New way to run the receiver thread """
class DriverThread(ExThread):
  def __init__(self,eradio,init_gains=[10,0,200,10,0,200,200],
      in_queue_arg=deque(maxlen=50)):
    ExThread.__init__(self)
    self.eradio = eradio
    self.sp = False
    self.in_queue = in_queue_arg
    self.header = Headers()
    # gains format: kppitch, kipitch, kdpitch, kproll, kiroll, kdroll, kpyaw
    self.gains = init_gains
    logger.debug('gains: {}'.format(init_gains))

  def run_w_exc(self):
    pitch_gains = split_bytes(self.gains[0]) +\
                  split_bytes(self.gains[1]) +\
                  split_bytes(self.gains[2])
    roll_gains = split_bytes(self.gains[3]) +\
                 split_bytes(self.gains[4]) +\
                 split_bytes(self.gains[5])
    yaw_gains = split_bytes(self.gains[6])

    # Initial packet with gains
    payload = pitch_gains + roll_gains + yaw_gains
    payload = map(chr,payload)
    payload = self.header.gains + payload
    # Format payload as string to comply with pyusb standards
    payload.insert(0,chr(len(payload)))
    payload = ''.join(payload)
    
    ackIn = None
    ackIn = self.eradio.send(payload)

    payload = map(ord,list(payload))
    log_outputs.info('{}'.format(payload))
    log_acks.info('{}'.format(ackIn))

    # New header for control inputs
    header = self.header.trim

    while not self.sp:
      ackIn = None

      # get raw data from controller
      raw = self.in_queue.pop()
      
      payload = header + map(chr,flatten(map(split_bytes, convert_raw(raw))))
      payload.insert(0,chr(len(payload)))
      payload = ''.join(payload)

      #''' New way to send and receive packets '''
      ackIn = self.eradio.send(payload)
      # convert payload back to readable format
      payload = map(ord,list(payload))
      log_outputs.info('{}'.format(payload))
      log_acks.info('{}'.format(ackIn))
          
  def stop(self):
    self.sp = True

################## main run function ########################
# specify default gains
def run_elka(init_gains):
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
  if init_gains:
    t = DriverThread(eradio,init_gains=init_gains,in_queue_arg=in_queue)
  else:
    t = DriverThread(eradio,in_queue_arg=in_queue)
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
