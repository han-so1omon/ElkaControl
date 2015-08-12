import os, sys, serial
sys.path.append(os.getcwd())

from Elkaradio.elkaradioTRX import _find_serial_port

s_port = _find_serial_port()
print s_port

ser = serial.Serial(port=s_port, baudrate=115200)
print ser
