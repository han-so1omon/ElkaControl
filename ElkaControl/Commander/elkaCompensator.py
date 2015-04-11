"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: Elkaradio 
Module: elkaDriver.py 

"""

import os, sys, usb, usb.core, usb.util, logging

sys.path.append(os.getcwd())

############################## Set up loggers ##################################
logger = logging.getLogger('main.elkaradioTRX')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
log_acks = logging.getLogger('acks')
################################################################################


