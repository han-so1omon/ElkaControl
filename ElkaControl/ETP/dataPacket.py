"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: ETP
Module: dataPacket.py


Data packet for ETP

"""

import struct, sys, logging, math

############################## Set up loggers ##################################
logger = logging.getLogger('main.dataPacket')
################################################################################

class DataPacket(object):
    '''
    packs 3 8-bit ints header and 4 12-bit ints data into binary structs
    '''

    def __init__(self, header = [0]*3, data = [0]*4):
        '''
        Constructor
        '''
        # size in bytes using each header element as an 8-bit int and each 
        # data element as a 10-bit int
        self._size = sys.getsizeof(header)*8 + sys.getsizeof(data)*10

        self._header = header 
        self._data = data 

    @staticmethod
    def convert_raw(raw):
        ''' Convert from floating pt number range [-1 1] to 12 bit number range
            [0 4000]
        '''
        orig = []
        to_datum = 1
        trans = 4000
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
    def ack(cls, header, data):
        return DataPacket(header, data)

    @classmethod
    def output(cls, header, raw):
        data = DataPacket.convert_raw(raw)
        return DataPacket(header, data)
        
    @property
    def header(self):
        """ Get header """
        return self._header
    
    @header.setter
    def header(self, header):
        """ Set requests to send """
        self._update_header(header)
    
    @classmethod
    def _update_header(cls, header):
        ''' Update the header with gains or pilot inputs '''
        if type(header) == str:
            self._header = header
        elif type(header) == list or type(header) == tuple:
            if len(header) == 1:
                self._header = struct.pack('B', header[0])
            elif len(header) > 1:
                self._header = struct.pack('B' * len(header), *header)
            else:
                self._header = ''
        else:
            raise WrongDataTypeException("Header must be str, tuple," +
                                         "or list type")

    

    #Some python madness to access different format of the data    
    def _get_data(self):
        """ Get packet data """
        return self._data
    
    def _set_data(self, data):
        if type(data) == str:
            self._data = data
        elif type(data) == list or type(data) == tuple:
            if len(data) == 1:
                self._data = struct.pack("B"*2, data[0])
            elif len(data) > 1:
                self._data = struct.pack("B" * len(data), *data)
            else:
                self._data = ""
        else:
            raise WrongDataTypeException("Data must be str, tuple, or list type"
                                        )
        
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
