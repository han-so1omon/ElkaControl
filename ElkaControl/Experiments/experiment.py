import Queue, threading, traceback, os, struct, random, math

""" how does threading work with queues?

class base():
    def __init__(self):
        self.queue = Queue.Queue()
        self.thread = None
        self.cnt = 0

    def connect(self):
        self.thread = sub(self.queue)
        self.thread.daemon = True
        self.thread.start()

    def add(self):
        self.queue.put("from base {0}".format(self.cnt))
        self.cnt += 1
    
    def receive(self):
        print(self.queue.get(True))

class sub(threading.Thread):
    def __init__(self, queue):
        super(sub, self).__init__()
        self.queue = queue
        self.cnt = 0

    def run(self):
        while True:
            self.queue.put("from thread {0}".format(self.cnt))
            self.cnt += 1

try:
    b = base()
    b.connect()
    while True:
        b.add()
        b.receive()
except KeyboardInterrupt as e:
    print "Keyboard Interrupt"
finally:
    print traceback.format_exc()
"""

""" How to form lists of a set length

l = [None] * 4
print l

"""

""" how to add logging module to program path

(fpath, fname) = os.path.split(os.getcwd())
print fpath 
"""

''' how to pack and unpack array of 12-bit ints into binary struct

def convert_array_sz(a, wrd_a_sz, wrd_b_sz):
    in_t = int(math.ceil((float(wrd_a_sz)/float(wrd_b_sz))*len(a)))

    b = [0] * in_t

    k = 0
    for i in range(len(a)):
        for j in range(wrd_a_sz):
            b_idx = int(math.floor(k/wrd_b_sz)) 
            if j == 0 or (k % wrd_b_sz) == 0: # if at beginning of a[i] or b[i]
                shift = (wrd_a_sz - j) - (wrd_b_sz - (k % wrd_b_sz))
            mask = 1 << ((wrd_a_sz - 1) - j)
            if shift >= 0:
                b[b_idx] |= (a[i] & mask) >> shift
            else:
                b[b_idx] |= (a[i] & mask) << abs(shift)
            k += 1

    return b


wrd_a_sz = 12
wrd_b_sz = 8 

a = []
for i in range(4):
    a.append(random.randint(0, 4000))
print a

for i in range(4):
    print '\na: {0:b}'.format(a[i])

b = convert_array_sz(a, wrd_a_sz, wrd_b_sz)

print b
for i in range(len(b)):
    b[i] = int(b[i])
    print '\nb: {0:b}'.format(b[i])

# '*' is unpack list operator in python
data = struct.pack('B'*len(b), *b)
'''

''' filling list up to 32B
#FIXME figure this out
def fill(x = [0]*8):
    print x

fill([3])
'''

''' pass around queues '''
def worker1():
    try:
        while not Queue.Empty:
            item = q.get()
            print "from w1: {}".format(item)
    except KeyboardInterrupt:
        raise

def worker2():
    try:
        i = 0
        while i < 10000:
            q.put(i)
            print 'from w2: {}'.format(i)
            i += 1
    except KeyboardInterrupt:
        raise

def close(t):
    t.join()

q = Queue.Queue()

t1 = threading.Thread(target=worker1)
t1.daemon = True
t1.start()

t2 = threading.Thread(target=worker2)
t2.daemon = True
t2.start()


try:
    t1.join()
    t2.join()
    print "done"
except KeyboardInterrupt:
    print 'active threads: ', threading.active_count(), 'kbint\n'
    print 'curr', threading.current_thread()

