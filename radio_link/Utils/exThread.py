import sys, os, threading, Queue
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

