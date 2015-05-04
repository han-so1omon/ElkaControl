import sys, os, subprocess, pygame, logging, threading

eztext_s = 'Inputs/eztext/'
home, garb = os.path.split(os.getcwd())
eztext_p = os.path.join(home, eztext_s)
sys.path.append(eztext_p)
sys.path.append(os.getcwd())
print sys.path

import eztext

from pygame.locals import *


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the width and height of the screen [width,height]
size = [500, 700]

########## InputDisp class ##########
class InputDisp(object):
    """
    This is a simple class that will help us display to the screen.
    It has nothing to do with the joysticks, just outputting the
    information.
    """
    pygame.init()

    def __init__(self):
        """ Constructor """
        self.screen = pygame.display.set_mode(size)

        pygame.display.set_caption(" Elkaradio Input ")
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg = self.bg.convert()
        self.bg.fill(WHITE)
        
        
        pygame.display.flip()

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

# sample runner 
disp = InputDisp()

txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt='type here: ')

disp.screen.blit(disp.bg, (0,0))
clock = pygame.time.Clock()

sp = False
while not sp:
    clock.tick(30)

    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            print 'quitting time\n'
            sp = True   

    # clear the screen
    disp.screen.fill((255,255,255))
    txtbx.update(events)
    txtbx.draw(disp.screen)
    pygame.display.flip()
