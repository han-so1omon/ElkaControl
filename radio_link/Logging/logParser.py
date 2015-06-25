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
        # store in, out, and ack data parsed from logs
        self.inp = {}
        self.out = {}
        self.acks = {}

    """ Save a log file to the appropriate location """
    def save_file(self, fstr=None, nm=None):
      pth = None

      if not fstr:
        raise OSError(
            'File not able to be copied. Invalid file name given')
      else:
        #matches filename.extension
        r = re.compile(r'(?<=[/|\\])([\w|\d|\-|\_]+).([\w|\d]+)\Z')
        m_in = r.findall(fstr) 

      #FIXME clean this up
      if (not nm) and m_in:
        d = datetime.datetime.fromtimestamp(time.time())
        m_out = '{0}-{1}-{2}-{3}_{4}_{5}_{6}.{7}'.format(
          m_in[0][0],d.year,d.month,d.day,d.hour,d.minute,d.second,
          m_in[0][1])
        try:
          os.mkdir('{}/Logging/PrevLogs'.format(os.getcwd()))
        except OSError:
          pass # directory already exists
        m_out = './Logging/PrevLogs/' + m_out
      else:
        m_out = r.findall(nm)
        pth = nm.split('/') #requires that path splits with '/'
        pth = [pth[i] for i in range(0,len(pth)-1)]
        pth = '/'.join(pth) # return path without filename
        try:
          os.mkdir(pth)
        except OSError:
          pass # directory already exists
        m_out = pth + '/' + '{0}.{1}'.format(m_out[0][0], m_out[0][1])
        print m_out

      shutil.copy2(fstr, m_out)

    """ Parse inputs log. Store time and raw data as tuples
        in self.inp dict. """
    def parse_in(self, ipf='./Logging/Logs/inputs.log'):
        r = re.compile(r'((\d+):(\d+):(\d+.\d+)),'
                r'\[((\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+))\]')
        el = [None] * 2
        with open(ipf, 'r') as inf:c
            for l in inf:
                el = r.match(l)
                if el[0] is not None:
                    print el
                else:
                    print "re not matched"

    """ Parse outputs log. Store time and transformed data as tuples
        in self.out dict. """
    def parse_out(self, otf ='./Logging/Logs/outputs.log'):
      #FIXME this process should be done by reading the header
      self.out['gains'] = []
      self.out['p_in'] = [] # pilot inputs

      rp = re.compile(r'(\d+):(\d+):(\d+)\.(\d+),\[(((\d+),?\s?){11})\]')
      rg = re.compile(r'(\d+):(\d+):(\d+)\.(\d+),\[(((\d+),?\s?){15})\]')
      with open(otf, 'r') as outf:
        print 'here'
        for l in outf:
          m = None
          m = rp.match(l)
          if m:
            t = int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001
            out = map(int,m.group(5).split(', '))
            self.out['p_in'].append([t] +
                  [out[i] for i in range(3,11)])
          else:
            m = rg.match(l)
            t = int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001
            out = map(int,m.group(5).split(', '))
            self.out['gains'].append([t] +
                  [out[i] for i in range(3,15)])
      return self.out

    """ Parse acks log. Store gyro, euler angles, and commands  as tuples
        in self.acks dict. """
    def parse_ack(self, acf ='./Logging/Logs/acks.log'):
        #FIXME this process should be done by reading the header
        self.acks['gyro'] = []
        self.acks['euler'] = []
        self.acks['commanded'] = []
        self.acks['none'] = []

        # capture valid ack from ELKA
        r = re.compile(
          r'(\d+):(\d+):(\d+)\.(\d+),array\(\'B\',\s\[((\d+,?\s?){27})\]\)')
        ralt1 = re.compile(
          r'(\d+):(\d+):(\d+)\.(\d+),array\(\'B\',\s\[((\d+?\s?))\]\)')
        ralt2 = re.compile(r'(\d+):(\d+):(\d+)\.(\d+),(None)')
        with open(acf, 'r') as ackf:
          for l in ackf:
            m = None
            m = r.match(l)
            if not m: #Line must be None, [0], or some invalid list
              # capture [0]
              m = ralt1.match(l)
              if not m: # capture None
                m = ralt2.match(l)
              self.acks['none'].append(int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001)
            else:
              t = int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001
              rec = map(int,m.group(5).split(', '))
              self.acks['gyro'].append([t] +
                    [rec[i] for i in range(0,6)])
              self.acks['euler'].append([t] +
                    [rec[i] for i in range(6,9)])
              self.acks['commanded'].append([t] +
                    [rec[i] for i in range(9,len(rec))])
          return self.acks
        raise IOError('file not found')
########## End of LogParser Class ##########
