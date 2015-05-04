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
        
        self.inl = open('./Logging/Logs/inputs.log')
        self.outl = open('./Logging/Logs/outputs.log')
        self.ackl = open('./Logging/Logs/acks.log')

        # each element is a 5 element array of format:
        # [del_t, axis1, axis2, axis3, axis4]
        self.inputs = []

        # each element is a 6 element array of format:
        # [del_t, header, data1, data2, data3, data4]
        self.outputs = []

        # each element is a 28 element array of format:
        # [del_t, data1, ... , data27]
        self.acks = []

    # parse a list of floating point numbers
    def parse_ln(self, line):
        return re.findall(r'[+-]?\d*\.*\d+', line)

    def parse_log(self, log):
        # while not EOF send to parse_ln
        if log == 'inputs':
            for l in self.inl:
                self.inputs.append(self.parse_ln(l))
            print self.inputs
        elif log == 'outputs':
            # parse whether header or data
            for l in self.outl:
                self.outputs.append(self.parse_ln(l))
        elif log == 'acks':
            for l in self.ackl:
                self.acks.append(self.parse_ln(l))
########## End of Parser Class ##########
