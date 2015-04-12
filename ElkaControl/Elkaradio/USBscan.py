import os, sys, usb, logging, logging.config, sys

i = 0
for i in range(125):
    print "#: {}".format(i)
    dev = usb.core.find(idProduct = 0x7777)
    dev.ctrl_transfer(usb.TYPE_VENDOR, 0x01, i, 0, ())
    cfj = dev.get_active_configuration()
    inf = cfj[(0,0)]
    ep = usb.util.find_descriptor(inf, find_all=1)
    for a in ep:
        print "EP: {}".format(a)
