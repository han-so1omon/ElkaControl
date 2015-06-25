"""
Author: Eric Solomon
Project: Elkaradio Control 
Lab: Alfred Gessow Rotorcraft Center
Package: ElkaControl 
Module: __main__.py

Contains main function for Elka Control
"""

import os, sys, traceback, logging, logging.config, logging.handlers,\
       threading, re, string

from IPython import embed # debugging

#add logging module to path
sys.path.append(os.path.join(os.getcwd(), 'Logging/Logs'))

from Elkaradio.elkaradioTRX import Elkaradio
from Elkaradio.elkaradioTRX import _find_devices 
from Utils.exceptions import *
from Logging.logParser import LogParser
from Logging.dataPlotter import DataPlotter
from ETP.elkaThread import run_elka

########################### Set up loggers ##############################
""" Log headers are <name>: tuple1[<tuple1 elements>] tuple2[<tuple2 elements>]... """

#Establish loggers as module level globals
logger = None
log_inputs = None
log_outputs = None
log_acks = None

open('./Logging/Logs/main.log', 'w').close()
open('./Logging/Logs/inputs.log', 'w').close()
open('./Logging/Logs/outputs.log', 'w').close()
logging.config.fileConfig('./Logging/Logs/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
log_acks = logging.getLogger('acks')
logger.debug('\nLog files cleared')
#log_inputs.info('raw_in[4]')
#log_outputs.info('controls[8]/gains[8]') # also contains gains
#log_acks.info('gyro[6] euler[4] commanded[16]')

######################### Define helper functions ##############################
r = re.compile(r'(\S+)') # global re for raw parse
def parse_raw_cmd(r_cmd):
  global r
  return r.findall(r_cmd)

""" Run elka control """
def run_elka_control(rx=None):
  global logger, log_inputs, log_outputs, log_acks
  if rx:
    setup_radios(rx)
  logger.debug('Running Elka Control')
  ''' Headers... necessary?
  log_inputs.info('inputs: [3][4]')
  log_outputs.info('outputs: [][]')
  log_acks.info('acks: [][]')
  '''
  run_elka()

def setup_radios(rx=[]):
  global logger
  logger.debug('Setting up radios')
  ''' Demonstrate ETP with two ElkaRadios '''
  i = 0
  for r in rx:
    r.set_radio_mode(Elkaradio.MODE_PRX)
    i += 1
    logger.debug('\nElkaradio number {0} is set to primary receive mode'\
                 .format(i))

def parse_logs():
  # Display displays set names, export sends to spreadsheet,
  # Plot plots with x,y,z as axes values
  # Return returns to Main
  p_options = ('\nHelp <help>'
               '\nDisplay available data sets <display>'
              '\nSave data file <save <./path/to/file.bar>>'
              '\nExport data to formatted file <export>'
              '\nPlot data <plot(x,y)>/<plot(x,y,z)>'
              '\nParse log file <parse <logtype> <./path/to/x.log>>'
              '\nReturn to main menu <return>')

  lp = LogParser()
  dp = DataPlotter()
 
  sp = False
  while not sp:
    # prompt next step
    print '\nParse Logs:\nWhat would you like to do?'
    print p_options

    r_cmd = raw_input('<')
    cmd = parse_raw_cmd(r_cmd)

    if cmd[0] == 'help':
        #FIXME display options
        pass
    elif cmd[0] == 'display' and len(cmd) == 1:
      print 'Input data: {}'.format(ind)
      print 'Output data: {}'.format(outd)
      print 'Ack data: {}'.format(ackd)
    elif cmd[0] == 'plot':
      pass
    elif cmd[0] == 'return' and len(cmd) == 1:
      break
    elif cmd[0] == 'save':
        if len(cmd) > 2:
            lp.save_file(cmd[1], cmd[2])
        else:
            lp.save_file(cmd[1], None)
    elif cmd[0] == 'parse':
      # parse logs
      if cmd[1] == 'input' and len(cmd) == 3:
        ind = lp.parse_in(cmd[2])
      elif cmd[1] == 'output' and len(cmd) == 3:
        outd = lp.parse_out(cmd[2])
        print outd
      elif cmd[1] == 'ack' and len(cmd) == 3:
        ackd = lp.parse_ack(cmd[2])
        print ackd
      else: print 'could not parse {}'.format(
              [cmd[i] for i in range(1,len(cmd))])
    else:
      print 'Invalid command'
################################################################################

################################ Main method ###################################
def main():
  global logger
  sp = False
  try:
    base = None

    options = ('\nHelp <help>\n'
               'Exit <exit>\n'
               'Run ElkaControl with Elka <run elka>\n'
              'Run ElkaControl with two ElkaRadios <run radios>\n'
              'Parse log files <parse>')
    while not sp:
      print '\nMain:\nWhat would you like to do?'
      print options
      
      r_cmd = raw_input('< ')
      cmd = parse_raw_cmd(r_cmd)

      """ main option tree """
      if cmd[0] == 'exit':
        sp = True
      elif cmd[0] == 'help':
          #FIXME print options
          pass
      elif cmd[0] == 'run' and cmd[1] == 'elka':
        run_elka_control()
      elif cmd[0] == 'run' and cmd[1] == 'radios':
        # mainly for debugging
        i = 0
        erads = []
        rx = [] # array of receive nodes
        for e in _find_devices():
          erads.append(e)
          if i != 0:
            rx.append(Elkaradio(erads[i]))
          i += 1
        run_elka_control(rx=rx) 
      elif cmd[0] == 'parse':
        parse_logs()
      else:
        print 'Invalid command'
        continue

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
  except JoystickThreadFinished as e:
    print 'Joystick thread has stopped'
    logger.exception(e)
  except Exception as e:
    print "Exception"
    logger.exception(e)
  finally:
    logger.debug(traceback.format_exc())
    # should only show main thread as alive
    logger.debug(threading.enumerate()) 
    if not sp:
      main()

if __name__ == '__main__':
    main()
