import random, collections

class K(object):
    def __init__(self, queue):
        self.queue = queue
        self.raw = [None]*4

    def get(self):
        self.raw = [random.random() for i in self.raw]
        self.queue.append(self.raw)

q = collections.deque()
k = K(q)

k.get()
print k.raw
print k.queue.popleft()
k.get()
print k.raw
print k.queue.popleft()

