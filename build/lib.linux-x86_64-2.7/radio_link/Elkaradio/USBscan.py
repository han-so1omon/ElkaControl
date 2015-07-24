import os, sys, usb, logging, logging.config, sys

i = 0
for i in range(125):
    print "#: {}".format(i)
    dev = usb.core.find(idVendor = 0x1915,  idProduct = 0x7777)
    if dev is None:
        raise ValueError('Device not found')
    dev.ctrl_transfer(usb.TYPE_VENDOR, 0x01, i, 0, ())
    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]
    ep = usb.util.find_descriptor(intf, find_all=1)
    for a in ep:
        print "EP: {}".format(a)
