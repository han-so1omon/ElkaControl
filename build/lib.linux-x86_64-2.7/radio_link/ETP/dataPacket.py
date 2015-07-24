"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: ETP
Module: dataPacket.py


Data packet for ETP

"""

import struct, sys, logging, math
from IPython import embed

############################## Set up loggers ##################################
logger = logging.getLogger('main.dataPacket')
################################################################################

class DataPacket(object):

    def __init__(self, header = [0]*3, data = [0]*4):
        '''
        Constructor
        '''
        self._size = len(header) + len(data) 

        self.header = header 
        self.data = data 

    @staticmethod
    def convert_raw(raw):
        ''' Convert from floating pt number range [-1 1] to 12 bit number range
            [0 4000]
        '''
        orig = []
        to_datum = 1
        trans = 2000
        for r in raw:
            orig.append(int(((r + to_datum)*trans)))

        wrd_orig_sz = 12
        wrd_trans_sz = 8

        trans = DataPacket.convert_array_wrd_sz(orig, wrd_orig_sz, wrd_trans_sz)
        return trans 

    @staticmethod
    def convert_array_wrd_sz(a, wrd_a_sz, wrd_b_sz):
        ''' converts array a of word size wrd_a_sz into array b of word size
            wrd_b_sz ''' 
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

   
    @classmethod
    def ack(cls, data = None):
        if data:
            return cls([0]*3, data)
        else:
            return cls()

    @classmethod
    def output(cls, header = None, raw = None):
        '''
        packs 3 8-bit ints header and 4 12-bit ints data into binary structs
        '''
        if raw:
            data = DataPacket.convert_raw(raw)
            if header is not None:
                ret = cls(header, data)
                #embed()
                logger.debug('ret: {0}'.format(ret))
                return ret
            else:
                return cls([0]*3, data)
        else:
            return cls([0]*3, [0]*6)
        
    @property
    def header(self):
        """ Get header """
        return self._header
    
    @header.setter
    def header(self, header):
        """ Set requests to send """
        if type(header) == list:
            self._header = header
        else:
            raise WrongDataTypeException("Header must be list")

     #Some python madness to access different format of the data    
    def _get_data(self):
        """ Get packet data """
        return self._data
    
    def _set_data(self, data):
        if type(data) == list:
            self._data = data
        else:
            raise WrongDataTypeException("Data must be list")
        
    def _get_data_l(self):
        """ Get the data in the packet as a list """
        return list(self._get_data_t())
    
    def _get_data_t(self):
        """ Get the data in the packet as a tuple """
        return struct.unpack("B" * len(self._data), self._data)
    
    def __str__(self):
        """ Get a string representation of the packet """
        return "{}".format(self.datat)
    
    data = property(_get_data, _set_data)
    datal = property(_get_data_l, _set_data)
    datat = property(_get_data_t, _set_data)
