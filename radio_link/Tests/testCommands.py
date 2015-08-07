"""
Author: Eric Solomon
Project: Elkaradio Control
Lab: Alfred Gessow Rotorcraft Center
Package: Tests 
Module: testCommands.py

Tests inputs vs received commands from ack
"""

import sys, os, re, shutil, datetime, time, unittest,\
    numpy as np, matplotlib.pyplot as plt
sys.path.append(os.getcwd()) 

from Logging.logParser import LogParser

############################### Set up loggers ##################################
# clear previous contents of logging files
open('./../Logging/testCmds.log', 'w').close()

# create logger with 'testCTRL'
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('testCmds')

logger.debug('Tests capabilities of edited Crazyflie interface for '
+ 'wireless communications and data transfer\n')
################################################################################

class TestCommands(unittest.TestCase):
  # Plots thrust, roll, pitch, and yaw before and after being processed by ELKA.
  # Converts 'after' to 'before' and compares.
  def plt_cmd_diff():
    lp = LogParser()

    ins = lp.parse_out('./Logging/PrevLogs/t_ins.log')
    outs = lp.parse_out('./Logging/PrevLogs/t_outs.log')
    acks = lp.parse_out('./Logging/PrevLogs/t_acks.log')
    
    
