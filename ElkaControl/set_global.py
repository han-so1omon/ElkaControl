class _radio_ack(object):
    ack = False
    powerDet = False
    retry = 0
    data = ()

some_data = _radio_ack() 
some_data.data = (2, 22)
print some_data.data
