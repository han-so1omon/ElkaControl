#!/usr/bin/python

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.sp=False
    def run(self):
      while not self.sp:
        print self.name
    def stop(self):
      self.sp=True

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

def chk_thread(x):
  if x.isAlive():
    x.join(1)

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

t = [thread1,thread2]

i=0
try:
  while(i<1000):
    map(lambda x: chk_thread(x),t)
    i+=1
    print i
except:
  map(lambda x: x.stop(), t)
