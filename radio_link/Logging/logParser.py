"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: Logging
Module: logParser.py 

Parses inputs, outputs, and acks logs into usable data sets
"""

import sys, os, re, shutil, datetime, time
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(os.getcwd()) 

########## Parser Class ##########
class LogParser(object):
    def __init__(self):
        # store in, out, and ack data parsed from logs
        self.inp = {}
        self.out = {}
        self.acks = {}
        plt.ion()
        self.fig_num = 1
        self.pdets = dict(zip([
          'title', 'xlabel', 'ylabel', 'text', 'axis', 'grid'
          ],
          [
          plt.title, plt.xlabel, plt.ylabel, plt.text, plt.axis, plt.grid
          ]))

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
        print 'Saved to {}'.format(m_out)

      shutil.copy2(fstr, m_out)

    """ Parse inputs log. Store time and raw data as tuples
        in self.inp dict. """
    def parse_in(self, ipf='./Logging/Logs/inputs.log'):
      first = True
      r = re.compile(
            r'(\d+):(\d+):(\d+)\.(\d+),\[((-?\d+\.\d+(e-?\d+)?,?\s?){4})\]')
      with open(ipf, 'r') as inf:
        for l in inf:
          m = None
          m = r.match(l)
          if not m:
            raise IOError('unexpected line read in {}'.format(inf))
          t = int(m.group(1))*3600 + int(m.group(2))*60 \
                + int(m.group(3)) + int(m.group(4))*.001
          raw = np.float32([t] + map(float,m.group(5).split(', ')))
          if first:
            # change this if float32 is too small
            self.inp['raw'] = np.float32(raw)
            first = False
          else:
            self.inp['raw'] = np.vstack((self.inp['raw'], raw))
      return self.inp

    """ Parse outputs log. Store time and transformed data as tuples
        in self.out dict. """
    def parse_out(self, otf ='./Logging/Logs/outputs.log'):
      # 0 for all arrays, 1 for gains, 2 for p_in, -1 for none
      firstG = True; firstP = True
      rp = re.compile(r'(\d+):(\d+):(\d+)\.(\d+),\[(((\d+),?\s?){12})\]')
      rg = re.compile(r'(\d+):(\d+):(\d+)\.(\d+),\[(((\d+),?\s?){16})\]')
      with open(otf, 'r') as outf:
        for l in outf:
          m = None
          m = rp.match(l)
          if m:
            t = int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001
            out = np.float32([t]+map(int,m.group(5).split(', ')))
            if firstP:
              self.out['trans'] = np.hstack((out[0],out[5:13]))
              firstP = False
            else:
                self.out['trans'] = np.vstack((self.out['trans'],
                      np.hstack((out[0],out[5:13]))))
          else:
            m = rg.match(l)
            if not m:
              raise IOError('unexpected line read in {}'.format(outf))
            t = int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001
            out = np.float32([t]+map(int,m.group(5).split(', ')))
            if firstG:
              self.out['gains'] = np.hstack((out[0],out[5:17]))
              firstG = False
            else:
              self.out['gains'] = np.vstack((self.out['gains'],
                    np.hstack((out[0],out[5:17]))))
      return self.out

    """ Parse acks log. Store gyro, euler angles, and commands  as tuples
        in self.acks dict. """
    def parse_ack(self, acf ='./Logging/Logs/acks.log'):
        self.acks['gyro'] = []
        self.acks['euler'] = []
        self.acks['commanded'] = []
        self.acks['none'] = []
        firstV = True; firstI = True

        # capture valid ack from ELKA
        r = re.compile(
          r'(\d+):(\d+):(\d+)\.(\d+),array\(\'B\',\s\[((\d+,?\s?){27})\]\)')
        ralt1 = re.compile(
          r'(\d+):(\d+):(\d+)\.(\d+),array\(\'B\',\s\[((\d+?\s?))\]\)')
        ralt2 = re.compile(r'(\d+):(\d+):(\d+)\.(\d+),(None)')
        with open(acf, 'r') as ackf:
          drop_ctr = 1 
          for l in ackf:
            m = None
            m = r.match(l)
            if not m: #Line must be None, [0], or some invalid list
              m = ralt1.match(l) # capture [0]
              if not m: 
                m = ralt2.match(l) # capture None
              if not m:
                raise IOError('unexpected line read in {}'.format(ackf))
              if firstI:
                self.acks['none'] = np.hstack((
                    [int(m.group(1))*3600 + int(m.group(2))*60 +
                    int(m.group(3)) + int(m.group(4))*.001],
                    [drop_ctr]))
                drop_ctr += 1
                firstI = False
              else:
                self.acks['none'] = np.vstack((self.acks['none'],
                    np.hstack(([int(m.group(1))*3600 + int(m.group(2))*60
                    + int(m.group(3)) + int(m.group(4))*.001],
                    [drop_ctr]))))
                drop_ctr += 1
            else:
              t = int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001
              rec = map(int,m.group(5).split(', '))
              if firstV:
                self.acks['gyro'] = np.hstack(([t],rec[1:7]))
                self.acks['euler'] = np.hstack(([t],rec[7:10]))
                self.acks['commanded'] = np.hstack(([t],rec[10:len(rec)]))
                firstV = False
              else:
                self.acks['gyro'] = np.vstack((self.acks['gyro'],
                                    np.hstack(([t],rec[1:7]))))
                self.acks['euler'] = np.vstack((self.acks['euler'],
                                    np.hstack(([t],rec[7:10]))))
                self.acks['commanded'] = np.vstack((self.acks['commanded'],
                                    np.hstack(([t],rec[10:len(rec)]))))
            if not m:
              raise IOError('unexpected line read in {}'.format(ackf))
        return self.acks

    """
    Pass up to four arrays and specify a plot style.
    Line styles and plot styles are specified at:
      http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
    
    Returns matplotlib.pyplot figure
    """
    def plot_data(self,fdata,arrs,style):
      print fdata
      f = plt.figure(num=self.fig_num)
      self.fig_num += 1
      ax = plt.subplot(111)
      for d in fdata.keys():
        self.pdets[d](fdata[d])
      if style:
        plt.plot(*arrs,**style)
      else:
        plt.plot(*arrs)
      plt.show()
      return f

########## End of LogParser Class ##########
