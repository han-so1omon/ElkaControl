import traceback, os, sys, usb, usb.core, usb.util, logging, logging.config

sys.path.append(os.getcwd())

from ETP.elkaDriver import ElkaDriver
from Elkaradio.elkaradioTRX import Elkaradio
from Utils.exceptions import *

open('./Logging/testCtrl.log', 'w').close()
logging.config.fileConfig('./Logging/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('testCtrl')

base = None

try:
    base = Elkaradio()

    pk = [0,2,3,4,5,4,3,2,1,1,2,3,4,5]

    logger.debug('pk: {}'.format(pk))
    ack = base.send_packet(pk)
    
    logger.debug('ack: {0}'.format(ack))
except Exception as e:
    logger.debug('exit via exception')
finally:
    base.close()
    logger.debug('{}'.format(traceback.format_exc()))
