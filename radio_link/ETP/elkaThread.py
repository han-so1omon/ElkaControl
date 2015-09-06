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

from pygame.joystick import init, get_count, quit
from collections import deque
from Elkaradio.elkaradioTRX import *
from Inputs.joy_read import JoyThread 
from Utils.exceptions import *
from Utils.exThread import ExThread

############################## Set up loggers ##################################
logger = logging.getLogger('main.elkaThread')
log_inputs = logging.getLogger('input')
log_outputs = logging.getLogger('output')
log_acks = logging.getLogger('ack')
################################################################################

############### utility functions ###############
#FIXME outputting between 0 and 65535
def convert_raw(raw):
  out = []
  to_datum = 1
  trans = 1000
  for i in range(len(raw)):
    if i == 0: # transform thrust to [1000 2000]
      out.append(int((3 + raw[i])*500))
    else: # transform roll,pitch,yaw to [-1000 1000]
      out.append(int(raw[i]*1000))
  out = split_bytes(out)
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
    l.extend(flatten(map(split_bytes,vals)))
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
""" Run the receiver thread """
JSCTRL = 0
KBCTRl = 1

class DriverThreadKeyboard(ExThread):
  def __init__(self,eradio,kb_in=[0,0,0,0],init_gains=[10,0,200,10,0,200,200]):
    ExThread.__init__(self)
    self.eradio = eradio
    self.sp = False
    self.header = Headers()
    self.kb_in=kb_in
    # gains format: kppitch, kipitch, kdpitch, kproll, kiroll, kdroll, kpyaw
    self.default_gains = [10,0,200,10,0,200,200]
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
      payload = header + map(chr,flatten(self.kb_in))
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

class DriverThreadJoystick(ExThread):
  def __init__(self,eradio,init_gains=[10,0,200,10,0,200,200],
      in_queue_arg=deque(maxlen=50)):

    ExThread.__init__(self)
    self.eradio = eradio
    self.sp = False
    self.in_queue = in_queue_arg
    self.header = Headers()
    # gains format: kppitch, kipitch, kdpitch, kproll, kiroll, kdroll, kpyaw
    self.default_gains = [10,0,200,10,0,200,200]
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
      
      payload = header + map(chr,flatten(convert_raw(raw)))
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
  init()
  if get_count() > 0:
    self.ctrl_mode = JSCTRL
    print 'Starting in Joystick Control Mode'
    logger.debug('\nStarting in Joystick Control Mode')

    in_queue = deque(maxlen=50)
    threads = []
    joy = JoyThread(in_queue)
    joy.start()
    threads.append(joy)
  else:
    self.ctrl_mode = KBCTRL
    print 'Starting in Keyboard Control Mode'
    logger.debug('\nStarting in Keyboard Control Mode')
    kb_in = map(int,raw_input('Enter default values for thrust [0,2000],'
            'roll [-1000,1000], pitch [-1000, 1000], yaw [-1000,'
            '1000]\n').split(','))

  if init_gains && self.ctrl_mode == JSCTRL:
    t = DriverThreadJoystick(eradio,init_gains=init_gains,
        in_queue_arg=in_queue)
  elif init_gains && self.ctrl_mode == KBCTRL:
    t = DriverThreadKeyboard(eradio,init_gains=init_gains,kb_in=kb_in)
  elif self.ctrl_mode = JSCTRL:
    t = DriverThreadJoystick(eradio,in_queue_arg=in_queue)
  elif self.ctrl_mode = KBCTRL:
    t = DriverThreadKeyboard(eradio,kb_in=kb_in) 

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
