import sys, os
sys.path.append(os.getcwd()) 

from Elkaradio.elkaradioTRX import *

p = ''.join([chr(30), chr(101)])

eradio = Elkaradio()

ack = (eradio.send(p))

print ack
