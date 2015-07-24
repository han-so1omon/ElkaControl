'''
TODO:
scan serial ports for vendor id 1915, device id 0x7777
use this port as serial port to communicate with
'''
import time, sys
import serial
import string

def flatten(l):
  res = []
  for r in l:
    if isinstance(r, list):
      res.extend(flatten(r))
    else:
      res.append(r)
  return res

def splitbytes(val):
    val_dh = (val>>8)&0xff
    val_dl = val&0xff
    l = [val_dh,val_dl]
    return l

class elkatalk:
    def __init__(self,sport = "/dev/ttyUSB0"):
	self.ser = serial.Serial(sport,115200)

    def send(self,bytes):
	bytes = flatten(bytes)
        bytes.insert(0,len(bytes))
        bytes = [int(c) for c in bytes]
        output_str = ''.join(map(chr,bytes))
        self.ser.write(output_str)
        return output_str

    def receive(self,length):
	bytes = self.ser.read(length)
	bytes = ",".join([str(ord(c)) for c in bytes])
        return bytes


