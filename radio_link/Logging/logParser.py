"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: Logging
Module: logParser.py 

Parses inputs, outputs, and acks logs into usable data sets
"""

import sys, os
sys.path.append(os.getcwd()) 

import re

########## Parser Class ##########
class LogParser(object):
    def __init__(self):
        
        self.inl = open('./Logging/Logs/inputs.log', 'r')
        self.outl = open('./Logging/Logs/outputs.log', 'r')
        self.ackl = open('./Logging/Logs/acks.log', 'r')

        # store input times and data
        self.in_epoch = None
        self.in_ic = []
        self.input_t = []
        self.input_d = []

        # store output times, header, and data
        self.out_epoch = None
        self.out_ic = []
        self.output_t = []
        self.output_h = []
        self.output_d = []

        # store ack times and imudata
        self.ack_epoch = None
        self.ack_ic = []
        self.ack_t = []
        self.ack_accel = []
        self.ack_euler = []
        self.ack_commanded = []

    # parse a list of floating point numbers from a text string
    def parse_ln(self, line):
        return re.findall(r'[+-]?\d*\.*\d+', line)

    def parse_in(self):
        init = 2
        for l in self.inl:
            ln = self.par_ln(l)
            if init == 2:
                init -= 1 

    def parse_out(self):
        init = 2
        for l in self.outl:
            ln = self.par_ln(l)
            if init == 2:
                init -= 1 
                self.out_epoch = sum(ln)
            elif init == 1:
                init -= 1
                self.out_ic = ln
            else:
                pass

    def parse_ack(self):
        for l in self.ackl:
            self.acks.append(self.parse_ln(l))

########## End of Parser Class ##########
