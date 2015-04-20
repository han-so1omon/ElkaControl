"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: Elkaradio 
Module: elkaDriver.py 

"""

import os, sys, usb, usb.core, usb.util, logging

from IPython import embed

sys.path.append(os.getcwd())

############################## Set up loggers ##################################
logger = logging.getLogger('main.elkaradioTRX')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
log_acks = logging.getLogger('acks')
################################################################################

from Utils.exceptions import ElkaradioNotFound
from ETP.dataPacket import DataPacket

#USB parameters
CRADIO_VID = 0x1915
CRADIO_PID = 0x7777

# Dongle configuration requests
#See http://wiki.bitcraze.se/projects:crazyradio:protocol for documentation
SET_RADIO_CHANNEL = 0x01
SET_RADIO_ADDRESS = 0x02
SET_DATA_RATE = 0x03
SET_RADIO_POWER = 0x04
SET_RADIO_ARD = 0x05
SET_RADIO_ARC = 0x06
ACK_ENABLE = 0x10
SET_CONT_CARRIER = 0x20
SCANN_CHANNELS = 0x21
RADIO_MODE = 0x22 # Additional firmware compatible flag to set radio mode
LAUNCH_BOOTLOADER = 0xFF

def _find_devices():
    """
    Returns a list of Elkaradio devices currently connected to the computer
    """
    ret = []

    dev = usb.core.find(idVendor=0x1915, idProduct=0x7777, find_all=1)
    if dev is not None:
        ret = dev

    return ret

class Elkaradio(object):
    """ Used for communication with the Elkaradio USB dongle """
    #configuration constants
    DR_250KPS = 0
    DR_1MPS = 1
    DR_2MPS = 2

    P_M18DBM = 0
    P_M12DBM = 1
    P_M6DBM = 2
    P_0DBM = 3

    MODE_PTX = 0
    MODE_PTX_SYNCHRONOUS = 1
    MODE_PRX = 2
    MODE_HYBRID = 3

    def __init__(self, device=None, devid=0):
        """ Create object and scan for USB dongle if no device is supplied """
        if device is None:
            try:
                devices = _find_devices() # polls for device if none provided
                #FIXME continue scanning for a device not in use
                device = next(devices, None)
            except Exception:
                raise ElkaradioNotFound("Cannot find an open Elkaradio Dongle")

        
        log_acks.debug("well at least we can write to the logs")

        self.dev = device
        self.dev.set_configuration(1)
        self.version = float("{0:x}.{1:x}".format(self.dev.bcdDevice >> 8,
        				self.dev.bcdDevice & 0x0FF))
        self.set_data_rate(Elkaradio.DR_250KPS)
        self.set_channel(40)
        self.set_cont_carrier(False)
        self.set_address((0x34, 0x43, 0x10, 0x10, 0x01))
        self.set_power(Elkaradio.P_M12DBM)
        self.set_arc(3)
        self.set_ard_bytes(32)
        
        self.radio_mode = Elkaradio.MODE_HYBRID

    def close(self):
        self.set_radio_mode(Elkaradio.MODE_PTX)
        self.dev.reset()
        self.dev = None
        logger.debug('\nElkaradio is closed')

    ### Dongle configuration ###
    def set_channel(self, channel):
        """ Set the radio channel to be used """
        self._send_vendor_setup(SET_RADIO_CHANNEL, channel, 0, ())

    def set_address(self, address):
        """ Set the radio address to be used"""
        if len(address) != 5:
            raise Exception("Elkaradio: the radio address shall be 5"
							" bytes long")

        self._send_vendor_setup(SET_RADIO_ADDRESS, 0, 0, address)

    def set_data_rate(self, datarate):
        """ Set the radio datarate to be used """
        self._send_vendor_setup(SET_DATA_RATE, datarate, 0, ())

    def set_power(self, power):
        """ Set the radio power to be used """
        self._send_vendor_setup(SET_RADIO_POWER, power, 0, ())

    def set_arc(self, arc):
        """ Set the ACK retry count for radio communication """
        self._send_vendor_setup(SET_RADIO_ARC, arc, 0, ())
        self.arc = arc

    def set_ard_time(self, us):
        """ Set the ACK retry delay for radio communication """
        # Auto Retransmit Delay:
        # 0000 - Wait 250uS
        # 0001 - Wait 500uS
        # 0010 - Wait 750uS
        # ........
        # 1111 - Wait 4000uS

        # Round down, to value representing a multiple of 250uS
        t = int((us / 250) - 1)
        if (t < 0):
            t = 0
        if (t > 0xF):
            t = 0xF
        self._send_vendor_setup(SET_RADIO_ARD, t, 0, ())

    def set_ard_bytes(self, nbytes):
        self._send_vendor_setup(SET_RADIO_ARD, 0x80 | nbytes, 0, ())

    def set_cont_carrier(self, active):
        if active:
            self._send_vendor_setup(SET_CONT_CARRIER, 1, 0, ())
        else:
            self._send_vendor_setup(SET_CONT_CARRIER, 0, 0, ())

    def set_radio_mode(self, mode):
        self._send_vendor_setup(RADIO_MODE, mode, 0, ())
        if mode == 0:
            self.radio_mode = 'MODE_PTX'
        elif mode == 1:
            self.radio_mode = 'MODE_PTX_SYNCHRONOUS'
        elif mode == 2:
            self.radio_mode = 'MODE_PRX'
        elif mode == 3:
            self.radio_mode = 'MODE_HYBRID'

    def scan_channels(self, start, stop, packet):
        # Slow PC-driven scann
        result = tuple()
        for i in range(start, stop + 1):
            self.set_channel(i)
            status = self.send_packet(packet)
            if status and status.ack:
                result = result + (i,)
        return result

    ### Data transfers ###
    def send_packet(self, dataOut):
        """ Send a packet and receive the ack from the radio dongle
            The ack contains information about the packet transmition
            and a data payload if the ack packet contained any """
        ackIn = None
        data = None
        #self.ep_write(dataOut, 10)
        #data = self.ep_read(64, 10)

        self.dev.write(1, dataOut, 1000)
        
        try:
            data = self.dev.read(0x81, 64, 1000)
        except usb.USBError as e:
            logger.exception(e)

        return data


    #Private utility functions
    def _send_vendor_setup(self, request, value, index, data):
        self.dev.ctrl_transfer(usb.TYPE_VENDOR, request, wValue=value,
    							wIndex=index, timeout=1000, data_or_wLength=data)
    
    def _get_vendor_setup(self, request, value, index, length):
        return self.dev.ctrl_transfer(usb.TYPE_VENDOR | 0x80, request,
    			                        wValue=value, wIndex=index, timeout=1000,
    			                        data_or_wLength=length)