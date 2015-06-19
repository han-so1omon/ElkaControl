"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: Logging
Module: logParser.py 

Parses inputs, outputs, and acks logs into usable data sets
"""

import sys, os, re, shutil, datetime, time
sys.path.append(os.getcwd()) 

########## Parser Class ##########
class LogParser(object):
    def __init__(self):
        self.inl = open('./Logging/Logs/inputs.log', 'r')
        self.outl = open('./Logging/Logs/outputs.log', 'r')
        self.ackl = open('./Logging/Logs/acks.log', 'r')

        # store most recently parsed input times and data
        self.in_epoch = None
        self.in_ic = []
        self.input_t = []
        self.input_d = []

        # store most recently parsed output times, header, and data
        self.out_epoch = None
        self.out_ic = []
        self.output_t = []
        self.output_h = []
        self.output_d = []

        # store most recently parsed ack times and imudata
        self.ack_epoch = None
        self.ack_ic = []
        self.ack_t = []
        self.ack_accel = []
        self.ack_euler = []
        self.ack_commanded = []

    """ Parse a file
    def parse(self, fpath):
        f = open(fpath, 'r')
        r = re.compile(r'((\d+):(\d+):(\d+.\d+)),(\W+)'
        head = f.readline()
        """
        

    """ Save a log file to the appropriate location
    def save(self, fstr=None, nm=None, loc=None):
      m = None
      fstr = './Logging/Logs/inputs.log'

      if not fstr:
        raise OSError(
            'File not able to be copied. Invalid file name given')
      else:
        r = re.compile(.(?<=[/|\\])(\w+)+.(\w+))
        # first match is directories, second match is file
        m = re.findall(fstr) 

      if (not nm) and (m is not None):
        d = datetime.datetime.fromtimestamp(time.time())
        if len(m) = 2:
          nm = '{0}-{1}-{2}-{3}_{4}_{5}_{6}.log'.format(
              m[1][1],d.year,d.month,d.day,d.hour,d.minute,d.second)
        else:
          nm = '{0}-{1}-{2}-{3}_{4}_{5}_{6}.log'.format(
              m[0][1],d.year,d.month,d.day,d.hour,d.minute,d.second)


      if not loc:
        try:
          os.mkdir('{}/Logging/PrevLogs'.format(os.getcwd()))
        except OSError:
          pass # directory already exists
        nm = './Logging/PrevLogs/' + nm

      shutil.copy2(fstr, nm)
      print nm
      """

    def parse_in(self):
        r = re.compile(r'((\d+):(\d+):(\d+.\d+)),'
                r'\[((\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+))\]')
        el = [None] * 2
        with open('./Logging/Logs/inputs.log', 'r') as inf:
            for l in inf:
                el = r.match(l)
                if el[0] is not None:
                    print el
                else:
                    print "re not matched"

    def parse_out(self):
        with open('./Logging/Logs/outputs.log', 'r') as outf:
            for l in outf:
                pass

    def parse_ack(self):
        with open('./Logging/Logs/acks.log', 'r') as ackf:
            for l in ackf:
                pass

########## End of Parser Class ##########
