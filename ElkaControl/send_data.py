''' send data '''
import sys, os
sys.path.append(os.getcwd()) 
import unittest, Queue, threading, array, logging, logging.config

from Elkaradio.elkaradioTRX import Elkaradio
from Utils.exceptions import JoystickNotFound
from Elkaradio.elkaradioTRX import Elkaradio
from Elkaradio.elkaradioTRX import _find_devices
from ETP.dataPacket import DataPacket
from ETP.elkaDriver import ElkaDriver
from Inputs.joystickCtrl import JoystickCtrl

############################## Set up loggers ##################################
# clear previous contents of logging files
open('./Logging/testCtrl.log', 'w').close()
open('./Logging/inputs.log', 'w').close()
open('./Logging/outputs.log', 'w').close()

logging.config.fileConfig('./Logging/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('testCtrl')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
log_acks = logging.getLogger('acks')

logger.debug('\nTests sending data and passing data by Queue\n')
###############################################################################

eradios = []

class Test(unittest.TestCase):
    def test_send_data(self):
        logger.debug("Test: send_data")
        log_outputs.info('Test: send_data')

        eradio_array = self.find_eradios()
        
        #add eradios to array
        for i in range(len(eradio_array)):
            eradios.append(Elkaradio(eradio_array[i]))
            #FIXME make sure that eradios are starting correctly
            logger.debug('Elkaradio {0}: {1}'.format(i, eradios[i]))
        
        #use default radio channels & radio addresses
        #set data rate to 250 Kbps
        for i in range(len(eradios)):
            eradios[i].set_data_rate(0)
        
        #set second eradio found to PRX mode
        if len(eradios) > 2:
            #FIXME make sure that one radio is set to PRX mode
            eradios[1].set_radio_mode(Elkaradio.MODE_PRX)
        
        for h in range(10):
            toSend = []
            for i in range(26):
                toSend.append(0x00 + h)
            #FIXME make sure that outputs are being formed correctly
            data = DataPacket.output(0, toSend)

            log_outputs.info('Packet {0}: {1}'.format(h, data.data))
        
            ack = None
            if len(eradios) > 1:
                ack = eradios[0].send_packet(data.data)

            if ack is not None:
                log_acks.info('Ack {0}: {1}'.format(h, ack))
            else:
                log_acks.info('Ack {0}: No ack received'.format(h))
            
        if len(eradios) > 2:
            eradios[1].close()

############################Utility Methods#####################################
    """ Wrapper for Crazyradio driver class' _find_devices() method """
    def find_eradios(self):
        eradios = _find_devices()
        eradio_array = []
        i = 0
        curr = next((eradios), None)
        while(curr != None):
            eradio_array.append(curr)
            i += 1
            curr = next((eradios), None)
        return eradio_array
               
    def get_inputs(self, ctrlr):            
        try:
            while (True):
                ctrlr.get_axes()
        except KeyboardInterrupt as e:
            raise


''' pass around queues 
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
'''

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
