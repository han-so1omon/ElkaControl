"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: Logging
Module: logParser.py 

Parses inputs, outputs, and acks logs into usable data sets
"""

import sys, os, re, shutil, datetime, time, numpy as np,\
    matplotlib.pyplot as plt
sys.path.append(os.getcwd()) 

# combines adjacent array bytes in arrays
def combine_arr_bytes(a):
  sz = len(a)/2
  return [((a[2*i]<<8)+a[2*i+1]) for i in range(sz)]

########## Parser Class ##########
class LogParser(object):
    def __init__(self):
        # store in, out, gains, acks, and dropped data parsed from logs
        self.inp = None
        self.out = None
        self.gains = None
        self.acks = None
        self.drops = None
        self.rfile = re.compile(r'(?<=[/|\\])([\w|\d|\-|\_]+).([\w|\d]+)\Z')
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
        m_in = self.rfile.findall(fstr) 

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
        m_out = self.rfile.findall(nm)
        if '/' in nm:
          pth = nm.split('/') #requires that path splits with '/'
        elif '\\'in nm:
          pth = nm.split('\\') #requires that path splits with '\'
        else: pth = ['./']
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
            self.inp = np.float32(raw)
            first = False
          else:
            self.inp = np.vstack((self.inp, raw))
      return self.inp

    """ Parse outputs log. Store time and transformed data as tuples
        in self.out dict. """
    def parse_out(self, otf ='./Logging/Logs/outputs.log'):
      # 0 for all arrays, 1 for gains, 2 for p_in, -1 for none
      firstG = True; firstP = True
      rp = re.compile(r'(\d+):(\d+):(\d+)\.(\d+),\[(((\d+),?\s?){12})\]')
      rg = re.compile(r'(\d+):(\d+):(\d+)\.(\d+),\[(((\d+),?\s?){18})\]')
      with open(otf, 'r') as outf:
        for l in outf:
          m = None
          m = rp.match(l)
          if m:
            t = int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001
            out = np.float32([t]+combine_arr_bytes(
              map(int,m.group(5).split(',')))[4:])
            if firstP:
              self.out = np.float32(out)
              firstP = False
            else:
                self.out = np.vstack((self.out,out))
          else:
            m = rg.match(l)
            if not m:
              raise IOError('unexpected line read in {}'.format(outf))
            t = int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001
            out = np.float32([t]+combine_arr_bytes(
              map(int,m.group(5).split(','))[4:]))
            if firstG:
              self.gains = np.float32(out)
              firstG = False
            else:
              self.gains = np.vstack((self.gains,out))
      return self.out, self.gains

    """ Parse acks log. Store gyro, euler angles, and commands  as tuples
        in self.acks dict. """
    def parse_ack(self, acf ='./Logging/Logs/acks.log'):
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
                self.drops = np.hstack((
                    [int(m.group(1))*3600 + int(m.group(2))*60 +
                    int(m.group(3)) + int(m.group(4))*.001],
                    [drop_ctr]))
                drop_ctr += 1
                firstI = False
              else:
                self.drops = np.vstack((self.drops,
                    np.hstack(([int(m.group(1))*3600 + int(m.group(2))*60
                    + int(m.group(3)) + int(m.group(4))*.001],
                    [drop_ctr]))))
                drop_ctr += 1
            else:
              t = int(m.group(1))*3600 + int(m.group(2))*60 \
                    + int(m.group(3)) + int(m.group(4))*.001
              rec = combine_arr_bytes(map(int,m.group(5).split(','))[1:])
              if firstV:
                self.acks = np.hstack(([t],rec))
                firstV = False
              else:
                self.acks = np.vstack((self.acks,np.hstack(([t],rec))))
            if not m:
              raise IOError('unexpected line read in {}'.format(ackf))
        return self.acks, self.drops

    """
    Pass up to four arrays and specify a plot style.
    Line styles and plot styles are specified at:
      http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
    
    Returns matplotlib.pyplot figure
    """
    def plot_data(self,fdata,arrs,style):
      f = plt.figure(num=self.fig_num)
      self.fig_num += 1
      ax = plt.subplot(111)
      if fdata:
        for d in fdata.keys():
          self.pdets[d](fdata[d])
      if style:
        plt.plot(*arrs,**style)
      else:
        plt.plot(*arrs)
      plt.show()
      return f

    """
    Pass an array, header, and delimiter to save a numpy ndarray to a text
    file.
    """
    def export_arr(self,arr=None,header=None,delimiter=",",filename='tmp.csv'):
      if '/' in filename:
        pth = filename.split('/') #path splits with '/'
        pth = [pth[i] for i in range(0,len(pth)-1)]
        pth = '/'.join(pth) # return path without filename
      elif '\\'in nm:
        pth = filename.split('\\') #path splits with '\'
        pth = [pth[i] for i in range(0,len(pth)-1)]
        pth = '/'.join(pth) # return path without filename
      else: pth = '.' # last element is a dummy
      try:
        os.mkdir(pth)
      except OSError:
        pass # directory already exists
      filename = self.rfile.findall(filename)
      filename = pth + '/' + '{0}.{1}'.format(filename[0][0],filename[0][1])

      np.savetxt(filename,arr,delimiter=delimiter,header=header)
      print 'Saved to {}'.format(filename)     

########## End of LogParser Class ##########
