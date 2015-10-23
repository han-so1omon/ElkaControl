import time,sys
import elkatalk
import string
import serial
from elkatalk import splitbytes,flatten
from elkaradioTRX import _find_serial_port
#from input_gains import *

kppitch = 1
kdpitch = 1
kproll = 1
kdroll = 1
kpyaw = 1
kdyaw = 1

header = ['0','255','255']
pitch_gains = flatten([splitbytes(kppitch),splitbytes(kdpitch)])
roll_gains = flatten([splitbytes(kproll),splitbytes(kdroll)])
yaw_gains = flatten([splitbytes(kpyaw),splitbytes(kdyaw)]) 

payload = flatten([pitch_gains,roll_gains,yaw_gains])
payload = [str(c) for c in payload] #convert uint_8's to strings:
payload = flatten([header,payload])

# will prompt user for password
e = elkatalk.elkatalk(_find_serial_port())
time.sleep(2)

file = open('test.txt',"w")
print payload


while True:
    sent = e.send(payload)
    received = e.receive(26)
    
    millis = int(round(time.time()*1000))
    received = received+','+ ''.join(repr(millis))+"\n"
    file.write(received)
    time.sleep(0.1)
