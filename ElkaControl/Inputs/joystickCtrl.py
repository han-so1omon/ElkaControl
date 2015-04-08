"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: Inputs
Module: joystickCtrl.py 

"""

import sys, os, subprocess, pygame, logging, threading
sys.path.append(os.getcwd())

import Queue

from ETP.dataPacket import DataPacket
from Utils.exceptions import JoystickNotFound

############################## Set up loggers ##################################
logger = logging.getLogger('main.joystickCtrl')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
################################################################################
    
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption(" Crazyradio Inputs ")

########## InputDisp class ##########
class InputDisp(object):
    """
    This is a simple class that will help us display to the screen.
    It has nothing to do with the joysticks, just outputting the
    information.
    """
    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)
 
    def disp(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, BLACK)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height
 
    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15

    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10
 
    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10

########## End of InputDisp ##########

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
        if joystick_name == 'Generic X-Box pad':
            self.LeftHL = 0
            self.LeftVU = 1
            self.LeftIO = 2
            self.RightHL = 3
            self.RightVU = 4
            self.RightIO = 5
        elif joystick_name == 'Sony PLAYSTATION(R)3 Controller':
            self.LeftHL = 0
            self.LeftVU = 1
            self.RightHL = 2
            self.RightVU = 3
            self.Left2IO = 12
            self.Right2IO = 13
            self.Left1IO = 14
            self.Right1IO = 15

########## End of Axes() ##########

########## JoystickCtrl class ##########
class JoystickCtrl(threading.Thread):
    def __init__(self, inQueue):
        pygame.joystick.init()
        
        super(JoystickCtrl, self).__init__()

        self.ctrlr = None 
        self.axes = []
        self.hats = []
        self.inDisp = InputDisp()
        self.ctrlr_name = None

        self.numaxes = None 
        self.numbuttons = None
        self.numhats = None

        # loop control
        self.sp = False

        self.in_queue = inQueue

        if (pygame.joystick.get_count() != 0):
            self.ctrlr = pygame.joystick.Joystick(0)
            self.ctrlr.init()

            self.ctrlr_name = self.ctrlr.get_name()
            self.numaxes = self.ctrlr.get_numaxes()
            self.numbuttons = self.ctrlr.get_numbuttons()
            self.numhats = self.ctrlr.get_numhats()
            
            #initialize axes, buttons, and hats arrays
            self.axes = [None] * self.numaxes
            self.buttons = [None] * self.numbuttons
            self.hats = [None] * self.numhats

        else:
            raise JoystickNotFound()

    def close(self):
        # clean up pygame
        pygame.joystick.quit()
        pygame.quit()
        logger.debug('\nJoystick controller closed\n')

    # Get inputs indefinitely
    def run(self):
        try:
            logger.debug('\nJoystick thread running')
            axes_enum = Axes(self.ctrlr_name) 
            while not self.sp:

                # DRAWING STEP
                # First, clear the screen to white. Don't put other drawing commands
                # above this, or they will be erased with this command.
                screen.fill(WHITE)
                self.inDisp.reset()
                
                # Event processing step
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: # If user clicked close
                        self.sp = True

                # Possible joystick actions:
                # JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
                # JOYBUTTONUP JOYHATMOTION
                
                self.inDisp.disp(screen, "Joystick {}".format(
                                 self.ctrlr_name))

                self.inDisp.disp(screen, "\t- AXES -")

                for i in range(self.numaxes):
                    self.axes[i] = self.ctrlr.get_axis(i)
                    self.inDisp.disp(screen, "Axis {0}: {1}".format(
                                     i, self.axes[i]))

                self.inDisp.disp(screen, "\t - BUTTONS -")

                for i in range(self.ctrlr.get_numbuttons()):
                    self.buttons[i] = self.ctrlr.get_button(i)
                    self.inDisp.disp(screen, "Button {0}: {1}".format(
                                     i, self.buttons[i]))

                self.inDisp.disp(screen, "\t - HATS -")

                for i in range(self.ctrlr.get_numhats()):
                    self.hats[i] = self.ctrlr.get_hat(i)
                    self.inDisp.disp(screen, "Hat {0}: {1}".format(
                                     i, self.hats[i]))

                pygame.display.flip()

                raw = [None] * 4
                # send back raw data
                raw[0] = self.axes[axes_enum.RightHL]
                raw[1] = self.axes[axes_enum.RightVU]
                raw[2] = self.axes[axes_enum.LeftVU]
                raw[3] = self.axes[axes_enum.LeftHL]
                self.in_queue.put(raw)
                log_inputs.info('{0}'.format(raw))

        except KeyboardInterrupt as e:
            raise
        except Exception, e:
            raise
        finally:
            #Quit pygame and close screen
            self.close()
            
    def stop(self):
        """ Stop the thread """
        self.sp = True
        try:
            self.join()
        except Exception:
            pass

########## End of JoystickCtrl class ##########
