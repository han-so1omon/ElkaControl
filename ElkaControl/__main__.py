"""
Author: Eric Solomon
Project: Elkaradio Control 
Lab: Alfred Gessow Rotorcraft Center
Package: ElkaControl 
Module: __main__.py

Contains main function for Elka Control
"""

import os, sys, traceback, logging, logging.config, logging.handlers, threading, re

from IPython import embed

#add logging module to path
p = os.path.join(os.path.split(os.getcwd())[0], 'Logging')
sys.path.append(p)

from Inputs.joystickCtrl import *
from ETP.elkaDriver import ElkaDriver
from Elkaradio.elkaradioTRX import Elkaradio
from Elkaradio.elkaradioTRX import _find_devices 
from Utils.exceptions import *

############################## Set up loggers ##################################
# clear previous contents of logging files
open('./Logging/main.log', 'w').close()
open('./Logging/inputs.log', 'w').close()
open('./Logging/outputs.log', 'w').close()

logging.config.fileConfig('./Logging/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
log_acks = logging.getLogger('acks')

logger.debug('\nRuns Elka Transfer Protocol (ETP) for a base node and a receive'+
             ' node\n')

# Each stream file is headed with the stream name ',' and number of elements per
# line
log_inputs.info('Inputs, 4')
log_outputs.info('Outputs, 6')
#FIXME fix acks elements per line
log_acks.info('Acks, 6')
################################################################################

""" Demonstrate ETP with two ElkaRadios 
try:
    i = 0
    erads = []
    base = None # single base node
    rx = [] # array of receive nodes
    for e in _find_devices():
        erads.append(e)
        if i == 0:
            base = ElkaDriver(erads[i])
        else:
            rx.append(Elkaradio(erads[i]))
        i += 1

    i = 1
    for r in rx:
        r.set_radio_mode(Elkaradio.MODE_PRX)
        i += 1
        logger.debug('\nElkaradio number {0} is set to primary receive mode'\
                     .format(i))

    if base is not None:
        base.start()
    else:
        raise ElkaradioNotFound()
"""

base = None

try:
    base = ElkaDriver()
    
    if base is not None:
        base.start()
    else:
        raise ElkaradioNotFound()

    logger.debug('\n{0} active threads:\n {1}'.format(threading.active_count(),
            threading.enumerate()))

    while True:
        pass

    for t in base._threads:
        t.join()

except JoystickNotFound as e:
    print "Joystick not found"
    logger.exception(e)
except KeyboardInterrupt as e:
    print "Keyboard Interrupt"
    logger.exception(e)
except ElkaradioNotFound as e:
    print "Elkaradio not found"
    logger.exception(e)
except LinkException as e:
    print "Exception in comm link" 
    logger.exception(e)
except Exception as e:
    print "Exception"
    logger.exception(e)
finally:
    if base is not None:
        base.close()
        logger.debug('\nBase node closed')
    print traceback.format_exc()
    print threading.enumerate()
