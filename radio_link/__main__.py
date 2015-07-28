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

### set up parsed data arrays
ind = []
outd = []
ackd = []
data_available = False # true after parse call

######################### Define helper functions ##############################
# Global regexps for slight time efficiency
r = re.compile(r'(\S+)')
# use re.findall for these
#sty = re.compile(r'(\S+)\s*=\s*(\S+)')
sty = re.compile(r'(\S+)\s*=\s*([^,]+\s*)+')
data_arrs = re.compile(r'\s*(\w+)\s+(\w+)\s+(\d+)\s+\'(\S+)\',?')

def parse_raw_cmd(r_cmd):
  global r
  return r.findall(r_cmd)

def parse_plot(fcmd,cmd,ind,outd,ackd):
  global sty, data_arrs
  arrs = None; style = None
    
  def parse_style(scmd):
    matches = sty.findall(scmd)
    if matches:
      return dict([(m[0],m[1].strip(',')) for m in matches])

  def parse_arrs(acmd,ind,outd,ackd):
    matches = data_arrs.findall(acmd)
    arr_idx = dict(zip([
        ('in','thrust'),('in','roll'),('in','pitch'),('in','yaw'),
        ('out','thrust'),('out','roll'),('out','pitch'),('out','yaw'),
        ('ack','gyro1'),('ack','gyro2'),('ack','gyro3'),('ack','gyro4'),
        ('ack','gyro5'),('ack','gyro6'),('ack','euler1'),('ack','euler2'),
        ('ack','euler3'),('ack','euler4'),('ack','commanded1'),
        ('ack','commanded2'),('ack','commanded3'),('ack','commanded4'),
        ('ack','commanded5'),('ack','commanded6'),('ack','commanded7'),
        ('ack','commanded8'),('ack','commanded9'),('ack','commanded10'),
        ('ack','commanded11'),('ack','commanded12'),('ack','commanded13'),
        ('ack','commanded14'),('ack','commanded15'),('ack','commanded16'),
        ('ack','dropped')
        ],[
        ('raw',0,1),('raw',0,2),('raw',0,3),('raw',0,4),('trans',0,1),
        ('trans',0,2),('trans',0,3),('trans',0,4),('gyro',0,1),
        ('gyro',0,2),('gyro',0,3),('gyro',0,4),('gyro',0,5),('gyro',0,6),
        ('euler',0,1),('euler',0,2),('euler',0,3),('euler',0,4),
        ('commanded',0,1),('commanded',0,2),('commanded',0,3),
        ('commanded',0,4),('commanded',0,5),('commanded',0,6),
        ('commanded',0,7),('commanded',0,8),('commanded',0,9),
        ('commanded',0,10),('commanded',0,11),('commanded',0,12),
        ('commanded',0,13),('commanded',0,14),('commanded',0,15),
        ('commanded',0,16),('none',0,1)
        ]))
    arrs = []
    if matches:
      for m in matches:
        # append x, then y, then style
        idx = arr_idx[m[0:2]]
        if m[0] == 'in':
          arrs.append(ind[int(m[2])][idx[0]][:,idx[1]])
          arrs.append(ind[int(m[2])][idx[0]][:,idx[2]])
        elif m[0] == 'out':
          arrs.append(outd[int(m[2])][idx[0]][:,idx[1]])
          arrs.append(outd[int(m[2])][idx[0]][:,idx[2]])
        elif m[0] == 'ack':
          arrs.append(ackd[int(m[2])][idx[0]][:,idx[1]])
          arrs.append(ackd[int(m[2])][idx[0]][:,idx[2]])
        else:
          raise InvalidCommand('Plot must be of type in, out, or ack')
        arrs.append(m[3]) # append line style
    else: raise InvalidCommand('Incorrect plot lines specified. '
            'Must specify between one and four valid lines.')
    return arrs
  
  return parse_style(fcmd), parse_arrs(cmd,ind,outd,ackd), parse_style(cmd)

def retrieve_arr(arr_typ,arr_num):
  ret_arr_idx = dict(zip([
    'in','out','gyro','euler','commanded','dropped'
    ],[
    (ind,'raw','t=time;th=thrust;r=roll;p=pitch;y=yaw\n'
         't1,th1,r1,p1,y1'),
    (outd,'trans','t=time;th=thrust;r=roll;p=pitch;y=yaw\n'
         't1,th1,r1,p1,y1'),
    (ackd,'gyro','t=time;g=gyro\nt1,g1,g2,g3,g4,g5,g6'),
    (ackd,'euler','t=time;e=euler\nt1,e1,e2,e3,e4'),
    (ackd,'commanded','t=time;c=commanded\nt1,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10'
        'c11,c12,c13,c14,c15,c16'),
    (ackd,'none','t=time;d=dropped\nt1,d1')
    ]))
  arr_idx = ret_arr_idx[arr_typ]
  return arr_idx[0][arr_num][arr_idx[1]],arr_idx[2],','

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
  data_available = False # true after parse call
  for r in rx:
    r.set_radio_mode(Elkaradio.MODE_PRX)
    i += 1
    logger.debug('\nElkaradio number {0} is set to primary receive mode'\
                 .format(i))

def parse_logs():
  global ind,outd,ackd,data_available
  # Display displays set names, export sends to spreadsheet,
  # Plot plots with x,y,z as axes values
  # Return returns to Main
  p_options = ('\nHelp <help>'
               '\nDisplay available data sets <display>'
              '\nSave data file <save <./path/to/file.bar>>'
              '\nExport data to formatted file <export>'
              '\nPlot data <plot>'
              '\nParse log file <parse <logtype <./path/to/x.log>>>'
              '\nReturn to main menu <return>'
              '\nExit program <exit>')
  help_options = (
    '\nexit'
    '\n\tUsage:'
    '\n\t\tEnter <exit> from a particular submenu to exit the program.'
    '\n\tBehavior:'
    '\n\t\tExits program with system call. Leaves any active data unsaved.'

    '\nhelp'
    '\n\tUsage:'
    '\n\t\tEnter <help> from a particular submenu to display help menu.'
    '\n\tBehavior:'
    '\n\t\tDisplays help menu. Help menu contains usage information and'
    '\n\t\texpected behavior for each command.'

    '\ndisplay'
    '\n\tUsage:'
    '\n\t\tEnter <display> from the \'Parse\' submenu to display the usable'
    '\n\t\tdata sets.'
    '\n\tBehavior:'
    '\n\t\tDisplays data sets that were parsed during the current session.'
    '\n\t\tData sets are persistent across menu changes. There are three types'
    '\n\t\tof data sets: in, out, and ack.'
    '\n\t\tin data is the raw data sent by the controller to the internal'
    '\n\t\tmodel. It contains the raw versions of thrust, roll,'
    '\n\t\tpitch, and yaw.'
    '\n\t\tout data is the transformed data that is to be sent to the'
    '\n\t\treceive node. It contains the transformed versions of thrust,'
    '\n\t\troll, pitch, and yaw.'
    '\n\t\tack data is the specified return packet data from the receive'
    '\n\t\tnode. When operating with an elka vehicle, this packet contains'
    '\n\t\t6 bytes gyro data, 4 bytes euler angles, and 16 bytes commanded'
    '\n\t\tdata.'

    '\nplot'
    '\n\tUsage:'
    '\n\t\tEnter <plot> from the \'Parse\' submenu to enter a two-part plot'
    '\n\t\tprompt. In the first prompt, enter up to four valid lines to plot.'
    '\n\t\tIn the second prompt, specify plot details.'
    '\n\tBehavior:'
    '\n\t\tSpecify up to four linetype,linestyle tuples.'
    '\n\t\tLinestyles can also be specified with keyword arguments separated'
    '\n\t\t
    '''Specify lntyp0,lnsty0,...,pltsty up to four lntyp,lnsty tuples.
          Line styles can also be specified with keyword arguments.
          Use the following format:
          in thrust1 'rs-', out thrust2 '>c'; color=green, linestyle = '-' 
          Next, specify figure data if desired using keywords.
          No commas allowed.
          Use the following format:
          title = Dropped packets, xlabel = time (s)
    '''
    )

  lp = LogParser()
  dp = DataPlotter()

  sp = False

  # FIXME make sure that threading is not broken because while loop is now
  # outside of try clause
  while not sp:
    try:
        # prompt next step
        print '\nParse:\nWhat would you like to do?'
        print p_options

        r_cmd = raw_input('<')
        cmd = parse_raw_cmd(r_cmd)

        if cmd[0] == 'help':
          ''' Display options '''
          print help_options
        elif cmd[0] == 'exit':
          ''' Clean up and exit program '''
          #TODO clean up program before exiting
          sys.exit(0)
        elif cmd[0] == 'display' and len(cmd) == 1:
          ''' Display usable data sets '''
          print 'Input data: {}'.format([i for i in range(len(ind))])
          print 'Output data: {}'.format([i for i in range(len(outd))])
          print 'Ack data: {}'.format([i for i in range(len(ackd))])
        elif cmd[0] == 'plot':
          '''
          Specify lntyp0,lnsty0,...,pltsty up to four lntyp,lnsty tuples.
          Line styles can also be specified with keyword arguments.
          Use the following format:
          in thrust1 'rs-', out thrust2 '>c'; color=green, linestyle = '-' 
          Next, specify figure data if desired using keywords.
          No commas allowed.
          Use the following format:
          title = Dropped packets, xlabel = time (s) 
          '''
          if not data_available: raise InvalidCommand('No data available.')
          pcmd = raw_input('<Specify up to four lines and style\n<')
          fcmd = raw_input('<If desired: specify title, xlabel, ylabel, '
            'text, axes, and grid.\n<')
          lp.plot_data(**dict(zip(['fdata','arrs','style'],
              parse_plot(fcmd,pcmd,ind,outd,ackd))))
        elif cmd[0] == 'return' and len(cmd) == 1:
          ''' Return to main menu '''
          sp = True
        elif cmd[0] == 'save':
          '''
          Save log file in specified or default location.
          Default location is ./Logging/PrevLogs
          '''
          if len(cmd) > 2:
            lp.save_file(cmd[1], cmd[2])
          else:
            lp.save_file(cmd[1], None)
        elif cmd[0] == 'parse' and len(cmd) == 3:
          '''
          Parse specified log file.
          Must specify input, output, or ack as log type.
          Must then specify path to log.
          '''
          # parse logs
          if cmd[1] == 'in':
            ind.append(lp.parse_in(cmd[2]))
            print 'Parsed in data: {}'.format(ind[-1])
          elif cmd[1] == 'out':
            outd.append(lp.parse_out(cmd[2]))
            print 'Parsed out data: {}'.format(outd[-1])
          elif cmd[1] == 'ack':
            ackd.append(lp.parse_ack(cmd[2]))
            print 'Parsed ack data: {}'.format(ackd[-1])
          else:
            raise InvalidCommand('Could not parse {}'.format(cmd))
          data_available = True
        elif cmd[0] == 'export':
          '''
          Export entire log file in csv format.
          Specify: export <arr_type> <arr_num> <filename>
          '''
          '''
          arr,header,delimiter = retrieve_arr(cmd[1],int(cmd[2]))))
          print arr
          print type(arr)
          lp.export_arr(filename=cmd[3],arr=arr,
                  header=header,delimiter=delimiter)
          '''
          lp.export_arr(filename=cmd[3],
                  **dict(zip(['arr','header','delimiter'],
                  retrieve_arr(cmd[1],int(cmd[2])))))
        else:
          raise InvalidCommand('Invalid command for submenu Parse Logs.')
    except InvalidCommand as e:
      print "Invalid command:", e
      logger.exception(e)
    except Exception as e:
      print 'Exception:', e
      logger.exception(e)
################################################################################

################################ Main method ###################################
def main():
  global logger
  sp = False
  base = None
  options = ('\nHelp <help>\n'
               'Exit program <exit>\n'
               'Run ElkaControl with Elka <run elka>\n' 'Run ElkaControl with two ElkaRadios <run radios>\n'
              'Parse log files <parse>'
            )
  help_options = (
    '\nexit'
    '\n\tUsage:'
    '\n\t\tEnter <exit> from a particular submenu to exit the program.'
    '\n\tBehavior:'
    '\n\t\tExits program with system call. Leaves any active data unsaved.'

    '\nhelp'
    '\n\tUsage:'
    '\n\t\tEnter <help> from a particular submenu to display help menu.'
    '\n\tBehavior:'
    '\n\t\tDisplays help menu. Help menu contains usage information and'
    '\n\t\texpected behavior for each command.'

    '\n\nrun elka'
    '\n\tUsage:'
    '\n\t\tEnter <run elka> from the \'Main\' menu to run elka with a vehicle.'
    '\n\t\tTo stop running elka, press CTRL-C.'
    '\n\tBehavior:'
    '\n\t\tRuns elka as the basestation for a vehicle. Requires that the'
    '\n\t\tvehicle and the base station transceivers are both set to the same'
    '\n\t\tfrequency and the vehicle is set in receive mode.'

    '\n\nrun radios'
    '\n\tUsage:'
    '\n\t\tEnter <run radios> from the \'Main\' menu to run elka with radios.'
    '\n\t\tTo stop running elka, press CTRL-C.'
    '\n\tBehavior:'
    '\n\t\tRuns elka as the basestation for another elkaradio dongle.'
    '\n\t\tRequires that the vehicle and the base station transceivers are'
    '\n\t\tboth set to the same frequency. This is a mainly a debug mode.'

    '\n\nparse'
    '\n\tUsage:'
    '\n\t\tEnter <parse> from the \'Main\' menu to enter the \'Parse\' submenu.'
    '\n\tBehavior:'
    '\n\t\tEnters the \'Parse\' submenu. From there, you may parse and'
    '\n\t\tmanipulate recently captured as well as previously stored data.'
    )

  while not sp:
    try:
      print '\nMain:\nWhat would you like to do?'
      print options
      
      r_cmd = raw_input('< ')
      cmd = parse_raw_cmd(r_cmd)

      """ main option tree """
      if cmd[0] == 'exit':
        sp = True
      elif cmd[0] == 'help':
        print help_options
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
        raise InvalidCommand('Invalid command for menu Main.')

    except JoystickNotFound as e:
      print "Joystick not found: ", e
      logger.exception(e)
    except KeyboardInterrupt as e:
      print "Keyboard Interrupt: ", e
      logger.exception(e)
    except ElkaradioNotFound as e:
      print "Elkaradio not found: ", e
      logger.exception(e)
    except LinkException as e:
      print "Exception in comm link: ", e
      logger.exception(e)
    except JoystickThreadFinished as e:
      print 'Joystick thread has stopped: ', e
      logger.exception(e)
    except InvalidCommand as e:
      print "Invalid command:", e
      logger.exception(e)
    except Exception as e:
      print "Exception: ", e
      logger.exception(e)
    finally:
      logger.debug(traceback.format_exc())
      # should only show main thread as alive
      logger.debug(threading.enumerate()) 

if __name__ == '__main__':
    main()
