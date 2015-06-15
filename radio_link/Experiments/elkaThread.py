import sys, os, threading, traceback, Queue
sys.path.append(os.getcwd()) 

from Elkaradio.elkaradioTRX import *


############### utility functions ###############
def convert_raw(raw):
  out = []
  to_datum = 1
  trans = 1000
  for i in range(len(raw)):
    if i == 0: # transform to [1000 2000]
      out.append(int((1.5 + raw[i]) * 1000))
    else: # transform to [-1000 1000]
      out.append(int(raw[i]*1000))
  split_bytes(out)
  return out

def flatten(l):
  res = []
  for r in l:
    if isinstance(r, list):
      res.extend(flatten(r))
    else:
      res.append(r)
  return res

def split_bytes(vals):
  l = []
  if isinstance(vals, list):
    for v in vals:
      l.append((v>>8)&0xff)
      l.append(v&0xff)
  else:
    l.append((vals>>8)&0xff)
    l.append(vals&0xff)
  return l

############## exception thread class ####################
class ExThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__status_queue = Queue.Queue()

    def run_w_exc(self):
        raise NotImplementedError

    def run(self):
        try:
            self.run_w_exc()
        except KeyboardInterrupt:
            self.__status_queue.put(sys.exc_info())
        except:
            self.__status_queue.put(sys.exc_info())
        self.__status_queue.put(None)

    def wait_for_exc_info(self):
        return self.__status_queue.get()

    def join_w_exc(self):
        ex_info = self.wait_for_exc_info()
        if ex_info is None:
            print 'none hurr'
            return
        else:
            raise ex_info[1]

############## driver thread class #################
""" New way to run the receiver thread """
class DriverThread(ExThread):
    def __init__(self, eradio):
        ExThread.__init__(self)
        self.eradio = eradio
        self.sp = False

    def run_w_exc(self):
        #FIXME temp
        kppitch = 1
        kdpitch = 1
        kproll = 1
        kdroll = 1
        kpyaw = 1
        kdyaw = 1

        header = [chr(0),chr(255),chr(255)]
        pitch_gains = split_bytes(kppitch) +\
                      split_bytes(kdpitch)
        roll_gains = split_bytes(kproll) +\
                     split_bytes(kdroll)
        yaw_gains = split_bytes(kpyaw) +\
                    split_bytes(kdyaw)

        # Initial packet with gains
        payload = pitch_gains + roll_gains + yaw_gains
        payload = map(chr,payload)
        payload = header + payload
        # Format payload as string to comply with pyusb standards
        payload = ''.join(payload)
        
        ackIn = None
        ackIn = self.eradio.send(payload)
        #print ackIn
        #time.sleep(0.1) # FIXME tune this as necessary

        # New header for control inputs
        header = [chr(0),chr(255),chr(255)]

        while not self.sp:
            ackIn = None

            # get raw data from controller
            raw = [-.5, -.3, .2, .1]

            payload = header + map(chr,flatten(map(split_bytes, convert_raw(raw))))
            payload = ''.join(payload)

            #''' New way to send and receive packets '''
            ackIn = self.eradio.send(payload)
            print ackIn
            #time.sleep(0.1)

    def stop(self):
        self.sp = True

def main():
    eradio = Elkaradio()

    t = DriverThread(eradio)
    t.start()

    try:
        while t.isAlive():
            t.join(1)
    except:
        t.stop()
        print traceback.format_exc()
        usb.util.dispose_resources(eradio.dev)

if __name__ == '__main__':
    main()
