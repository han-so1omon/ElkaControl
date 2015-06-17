import sys, os, pygame, threading, Queue, logging
sys.path.append(os.getcwd()) 

from collections import deque
from Utils.exceptions import *
from Utils.exThread import ExThread

############################## Set up loggers ##################################
logger = logging.getLogger('main.joy_read')
log_inputs = logging.getLogger('inputs')
################################################################################

########## Axes() class #########
class Axes(object):
    def __init__(self, joystick_name):
        
        # Define joystick axes based off of pad name
        # Naming scheme as follows:
        #   Axis location = {Left[1/2], Right[1/2]}
        #   Axis direction = {H[orizontal], V[ertical], I[n/Out]
        #       This gives the movement direction
        #   Axis zero = {L[eft], R[ight], I[n], O[ut]

        # For current implementation, only use the following:
        #   LeftHL, LeftVU, RightHL, RightVU
        if joystick_name == 'Generic X-Box pad' or\
           joystick_name == 'Controller (Gamepad F310)':
            self.LeftHL = 0
            self.LeftVU = 1
            self.RightHL = 3
            self.RightVU = 4
        elif joystick_name == 'Sony PLAYSTATION(R)3 Controller':
            self.LeftHL = 0
            self.LeftVU = 1
            self.RightHL = 2
            self.RightVU = 3

########### JoyThread class #############
class JoyThread(ExThread):
  def __init__(self, in_queue):
    ExThread.__init__(self)
    self.in_queue = in_queue
    self.sp = False
    pygame.init()
    if (pygame.joystick.get_count() != 0):
      self.j = pygame.joystick.Joystick(0)
      self.j.init()
      self.ctrlr_name = self.j.get_name()
      self.axes_enum = Axes(self.ctrlr_name) 
      self.numaxes = self.j.get_numaxes()
      #self.axes = [None] * self.numaxes
      self.raw = [None] * 4
      logger.debug('\nJoystick: {0}'.format(self.ctrlr_name))
    else:
      raise JoystickNotFound()

  # sift through pygame events and get axes to send as determined by
  # axes_enum
  def get(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT: # If user clicked close
        self.sp = True

    self.raw[0] = self.j.get_axis(self.axes_enum.LeftVU)
    self.raw[1] = self.j.get_axis(self.axes_enum.RightHL)
    self.raw[2] = self.j.get_axis(self.axes_enum.RightVU)
    self.raw[3] = self.j.get_axis(self.axes_enum.LeftHL)
    self.in_queue.append(self.raw)

  def run_w_exc(self):
    logger.debug('\nJoystick thread running')
    raw = [None] * 4
    while not self.sp:
      self.get()
      log_inputs.info('{}'.format(self.raw))

  def stop(self):
    self.sp = True

