import pygame
import time
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

def get():
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    out1 = 0
    it = 0 #iterator
    pygame.event.pump()
    
    #Read input from the two joysticks       
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it+=1
    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
        #out[it] = j.get_button(i)
        it+=1
    out1 = j.get_numaxes()
    return out

while True:
    #pub = get()
    throttle = int((1.0-get()[1])*500.0)
    print throttle
    print '\n'
