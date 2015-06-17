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
p = os.path.join(os.getcwd(), 'Logging/Logs')
sys.path.append(p)

from Elkaradio.elkaradioTRX import Elkaradio
from Elkaradio.elkaradioTRX import _find_devices 
from Utils.exceptions import *
from Logging.logParser import LogParser
from Logging.dataPlotter import DataPlotter

from ETP.elkaThread import run_elka

############################## Set up loggers ##################################
# clear previous contents of logging files
open('./Logging/Logs/main.log', 'w').close()
open('./Logging/Logs/inputs.log', 'w').close()
open('./Logging/Logs/outputs.log', 'w').close()

logging.config.fileConfig('./Logging/Logs/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')
log_inputs = logging.getLogger('inputs')
log_outputs = logging.getLogger('outputs')
log_acks = logging.getLogger('acks')

logger.debug('\nRuns Elka Transfer Protocol (ETP) for a base node and a receive'+
             ' node\n')

# Stream file headers:
# datefmt
# stream name ',' lines per entry, num el per line 1/.../num el per line n
log_inputs.info('\nInputs, 1, 4')
log_outputs.info('\nOutputs, 2, 3/4')
log_acks.info('\nAcks, 1, 27')
################################################################################

######################### Define helper functions ##############################
def parse_raw_cmd(r_cmd):
    r_cmd = r_cmd.strip()
    if r_cmd:
        return [word.strip(string.punctuation) for word in r_cmd.split()]
    else:
        return 'Invalid command' 

""" Old run elka base station. Communicates with anything on the other end of the
    radio link
def run_elka_control(base=None):
  def chk_thread(t):
    if t.isAlive():
      t.join(1)

  def stop_thread(t):
    t.stop()
    logger.debug('\nThread {0} stopped'.format(t.name))

  if base is not None:
      base.start()
  else:
      raise ElkaradioNotFound('Base could not start because no radio is found')

  # should show 3 threads running
  logger.debug('\n{0} active threads:\n {1}'.format(threading.active_count(),
            threading.enumerate()))
  try:
    while(True):
      map(lambda t: chk_thread(t), base._threads)
  except:
    map(lambda t: stop_thread(t), base._threads)
    base.close()
    logger.debug('\nBase node closed')
    raise
"""
""" New way """
def run_elka_control():
   run_elka()

def run_two_radios(rx=[]):
    ''' Demonstrate ETP with two ElkaRadios '''
    i = 0
    for r in rx:
      r.set_radio_mode(Elkaradio.MODE_PRX)
      i += 1
      logger.debug('\nElkaradio number {0} is set to primary receive mode'\
                   .format(i))

    run_elka_control()

def parse_logs():
    # Display displays set names, export sends to spreadsheet,
    # Plot plots with x,y,z as axes values
    # Return returns to Main
    p_options = ('\nDisplay available data sets <display>'
                '\nExport data to formatted file <export>'
                '\nPlot data <plot(x,y)>/<plot(x,y,z)>'
                '\nReturn to main menu <return>')

    lp = LogParser()
    dp = DataPlotter()
    
    # parse logs
    lp.parse_in()
    lp.parse_out()
    lp.parse_ack()

    while not sp:
        # prompt next step
        print '\nParse Logs:\nWhat would you like to do?'
        print p_options

        r_cmd = raw_input('<')
        cmd = parse_raw_cmd(r_cmd)

        if cmd[0] == 'display' and len(cmd) == 1:
            pass
        elif cmd[0] == 'plot' and len(cmd) == 1:
            # output able to plot the following: 
            pass
        elif cmd[0] == 'plot' and len(cmd) > 1:
            # send to grapher
            pass
        elif cmd[0] == 'return' and len(cmd) == 1:
            break
        else:
            print 'Invalid command'
            continue
################################################################################

################################ Main method ###################################
def main():
  sp = False
  try:
      base = None # base node

      options = ('\nExit <exit>\nRun ElkaControl with Elka <run elka>\n'
                'Run ElkaControl with two ElkaRadios <run radios>\n'
                'Parse log files <parse>')
      while not sp:
          print '\nMain:\nWhat would you like to do?'
          print options
          
          r_cmd = raw_input('< ')
          cmd = parse_raw_cmd(r_cmd)

          if cmd[0] == 'exit':
              sp = True
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
              run_two_radios(rx) 
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
