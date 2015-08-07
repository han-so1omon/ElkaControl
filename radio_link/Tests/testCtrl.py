"""
Author: Eric Solomon
Project: Elkaradio control of quadrotors
Lab: Alfred Gessow Rotorcraft Center
Package: Tests
Module: testCTRL.py 


Data packet for ETP
"""

import sys, os
sys.path.append(os.getcwd())
os.chdir(os.path.join(os.getcwd(), "Tests"))

import unittest, logging, logging.config, logging.handlers, re 

from Utils.exceptions import JoystickNotFound
from Elkaradio.elkaradioTRX import Elkaradio
from Elkaradio.elkaradioTRX import _find_devices
from ETP.dataPacket import DataPacket
from ETP.elkaDriver import ElkaDriver
from Inputs.joystickCtrl import JoystickCtrl

############################### Set up loggers ##################################
# clear previous contents of logging files
open('./../Logging/testCtrl.log', 'w').close()
open('./../Logging/inputs.log', 'w').close()
open('./../Logging/outputs.log', 'w').close()

# create logger with 'testCTRL'
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('testCtrl')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')

logger.debug('Tests capabilities of edited Crazyflie interface for '
+ 'wireless communications and data transfer\n')
################################################################################

eradios = []

class Test(unittest.TestCase):
    """ Use _find_devices to find local elkaradios and log their id """
    def testFinderadios(self):
        logger.debug('\n\ttestFinderadios')

        eradio_array = self.find_eradios()
        
        logger.debug('\n%s Elkaradios found\n',
                     len(eradio_array))

        
    """ Instantiate a elkaradio from the elkaradio driver
    in PTX mode and log its identifier """
    def testInstantiateTXeradio(self):
        logger.debug('\n\ttestInstantiateTXeradio')
        
        eradio_array = self.find_eradios()
        
        sRepr = ''
        
        for i in range(len(eradio_array)): 
            eradios.append(Elkaradio(eradio_array[i]))
            if sRepr != '':
                sRepr += '\n'
            sRepr += str(eradios[i]) + '\n\t' \
            + 'Serial Number: ' + str(eradios[i].dev.serial_number)
        logger.debug('\nElkaradio identifiers:\n' + sRepr + '\n')


    """ Send a specific type of data from one elkaradio to another and receive
    an ack confirming that the correct data was received """
    def testSendData(self):
        logger.debug('\n\ttestSendData')
        
        eradio_array = self.find_eradios()
        
        #add eradios to array
        for i in range(len(eradio_array)):
            eradios.append(Elkaradio(eradio_array[i]))
        
        #use default radio channels & radio addresses
        #set data rate to 250 Kbps
        for i in range(len(eradios)):
            eradios[i].set_data_rate(0)
        
        #set second eradio found to PRX mode
        if len(eradios) > 2:
            eradios[1].set_radio_mode(Elkaradio.MODE_PRX)
        
        for h in range(10):
            toSend = []
            for i in range(26):
                toSend.append(0x00 + h)
            data = DataPacket(0, toSend)
            assert (data.datal == toSend)

            log_outputs.debug('Packet: {0}'.format(data.datat))
            
            ack = None
            if len(eradios) > 2:
                ack = eradios[0].send_packet(data.data)
            if ack is not None:
                logger.debug('Received ack {0}'.format(ack))
            
        if len(eradios) > 2:
            eradios[1].close()


    """ Initialize joystick and send inputs. Track and log inputs to inputs.log
    """
    def testJoystickInputs(self):
        logger.debug("\n\ttestJoystickInputs")
        log_inputs.debug('Inputs\n')
        try:
            with JoystickCtrl() as ctrlr:
                logger.debug("Initializing joystick controller\n")
                try:
                    ctrlr.get_inputs()
                except KeyboardInterrupt:
                    logger.debug("End of inputs\n")
        except JoystickNotFound:
            logger.debug("No joysticks found!")

    """ Send a specific type of data from one elkaradio to another and process
    that data. Send back an ack with the processed data """
    def testProcessData(self):
        pass

    """ Send arbitrary data from one elkaradio to another and receive an ack
    confirming that data was received """
    def testAck(self):
        pass

    """ Send arbitrary data from one elkaradio to another and receive an ack
    confirming that the correct data was received """
    def testAckConsistent(self):
        pass

    """ Send a specific type of data from one elkaradio to another and process
    that data. Send back an ack with the correctly processed data """
    def testProcessDataConsistent(self):
        pass
    
    """ Starts a elkaradio in TX mode and switches it it RX mode """
    def testWirelessRX(self):
        pass
    
    """ Sends a packet from a elkaradio in TX mode attached to the basestation
    to a elkaradio in RX mode through wireless radio communication """
    def testWirelessComm(self):
        pass
    
    #################### Setup & Tear Down Methods############
    
    """
    def tearDown(self):
        if len(eradios) is not None:
            for cr in eradios:
                cr.close()
    """
    
############################Utility Methods#####################################
    """ Wrapper for Elkaradio driver class' _find_devices() method """
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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
