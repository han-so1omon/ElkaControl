"""
Author: Eric Solomon
Project: Elkaradio Control 
Lab: Alfred Gessow Rotorcraft Center
Package: radio_link 
Module: __main__.py

Contains main function for Elka Control
"""

import os, sys, traceback, logging, logging.config, logging.handlers,\
       threading, re, string

from IPython import embed # debugging

#add logging module to path
sys.path.append(os.path.join(os.getcwd(), 'Logging/Logs'))

from os.path import isfile
from Elkaradio.elkaradioTRX import Elkaradio
from Elkaradio.elkaradioTRX import _find_devices 
from Utils.exceptions import *
from Logging.logParser import LogParser
from ETP.elkaThread import run_elka

########################### Set up loggers ##############################
#Establish loggers as module level globals
logger = None
log_inputs = None
log_outputs = None
log_acks = None

# call each time before logging to a file
def clear_logs(k):
  global logger, log_inputs, log_outputs, log_acks
  logging.config.fileConfig('./Logging/Logs/logging.conf', disable_existing_loggers=False)
  if 'm' in k and isfile('./Logging/Logs/main.log'):
    open('./Logging/Logs/main.log', 'r+').truncate()
    logger = logging.getLogger('main')
  if 'i' in k and isfile('./Logging/Logs/input.log'):
    #open('./Logging/Logs/inputs.log', 'w').close()
    open('./Logging/Logs/input.log', 'r+').truncate()
    log_inputs = logging.getLogger('input')
  if 'o' in k and isfile('./Logging/Logs/output.log'):
    #open('./Logging/Logs/outputs.log', 'w').close()
    open('./Logging/Logs/output.log', 'r+').truncate()
    log_outputs = logging.getLogger('output')
  if 'a' in k and isfile('./Logging/Logs/ack.log'):
    open('./Logging/Logs/ack.log', 'r+').truncate()
    log_acks = logging.getLogger('ack')

clear_logs('mioa')
logger.debug('\nLog files cleared')

#TODO headers

### set up parsed data arrays
ind = []
outd = []
ackd = []
gaind = []
dropd = []
data_available = False # true after parse call

######################### Define helper functions ##############################
# Global regexps for slight time efficiency
r = re.compile(r'(\S+)')
# use re.findall for these
#sty = re.compile(r'(\S+)\s*=\s*(\S+)')
re_sty = re.compile(r'(\S+)\s*=\s*([^,]+\s*)+')
re_data_arrs = re.compile(r'\s*(\w+)\s+(\d+)\s+(\d+)\s+\'(\S+)\',?')

def parse_raw_cmd(r_cmd):
  global r
  return r.findall(r_cmd)

def parse_plot(fcmd,cmd):
  global re_sty, re_data_arrs, ind, outd, ackd
  arrs = None; style = None
    
  def parse_style(scmd):
    matches = re_sty.findall(scmd)
    if matches:
      return dict([(m[0],m[1].strip(',')) for m in matches])

  def parse_arrs(acmd):
    matches = re_data_arrs.findall(acmd)
    arrs = []
    if matches:
      for m in matches:
        k = int(m[2])
        # append x, then y, then style
        if m[0] == 'in' and ind[k].any():
          arrs.append(ind[k][:,0])
          arrs.append(ind[k][:,int(m[1])])
        elif m[0] == 'out' and outd[k].any():
          arrs.append(outd[k][:,0])
          arrs.append(outd[k][:,int(m[1])])
        elif m[0] == 'ack' and ackd[k].any():
          arrs.append(ackd[k][:,0])
          arrs.append(ackd[k][:,int(m[1])])
        elif m[0] == 'drop' and dropd[k].any(): # FIXME IndexError: too many indices for array
          arrs.append(dropd[k][:,0])
          arrs.append(dropd[k][:,int(m[1])])
        else:
          raise InvalidCommand('Plot must contain data and be of type in, out, ack, or dropped')
        arrs.append(m[3]) # append line style
    else: raise InvalidCommand('Incorrect plot lines specified. '
            'Must specify between one and four valid lines.')
    return arrs
  
  return parse_style(fcmd), parse_arrs(cmd), parse_style(cmd)

def retrieve_arr(arr_typ,arr_num):
  global ind, outd, gaind, ackd, dropd
  ret_arr_idx = dict(zip([
    'in','out','gain','ack','drop',
    ],[
    (ind,'t=time;th=thrust;r=roll;p=pitch;y=yaw\n'
         't1,th1,r1,p1,y1'),
    (outd,'t=time;th=thrust;r=roll;p=pitch;y=yaw\n'
         't1,th1,r1,p1,y1'),
    (gaind,'t=time;kpp=Kp_pitch;kip=Ki_pitch;kdp=Kd_pitch;\n'
      'kpr=Kp_roll;kir=Ki_roll;kdr=Kd_roll;kpy=Kp_yaw;\n'
      'kpp,kip,kdp,kpr,kir,kdr,kpy'),
    (ackd,'t=time;g=gyro;a=accel;e=euler;c=commanded\n'
    't1,g1,g2,g3,a1,a2,a3,e1,e2,c1,c2,c3,c4,c5'),
    (dropd,'t=time;d=drop\nt1,d1')
    ]))
  arr_idx = ret_arr_idx[arr_typ]
  return arr_idx[0][arr_num],arr_idx[1],','

""" Run elka control """
# gains given in form kpp,kdp,kpr,kdr,kpy,kdy
def run_elka_control(rx=None,init_gains=None):
  global logger, log_inputs, log_outputs, log_acks
  if rx:
    setup_radios(rx)
  logger.debug('Running Elka Control')
  run_elka(init_gains=init_gains)

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
  global ind,outd,gaind,ackd,data_available
  # Display displays set names, export sends to spreadsheet,
  # Plot plots with x,y,z as axes values
  # Return returns to Main
  p_options = ('\nHelp <help>'
               '\nDisplay available data sets <display>'
              '\nSave data file <save> <./path/to/file.bar>'
              '\nExport data to formatted file <export>'
              '\nPlot data <plot>'
              '\nParse log file <parse> <logtype> <./path/to/x.log>'
              '\nExport log file in csv format <export> <logtype> <lognum> <savefile.csv>'
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
    '\n\t\tData sets are persistent across menu changes. There are five types'
    '\n\t\tof data sets: in, out, gain, ack, and dropped.'
    '\n\t\tin data is the raw data sent by the controller to the internal'
    '\n\t\tmodel. It contains the raw versions of thrust, roll,'
    '\n\t\tpitch, and yaw.'
    '\n\t\tout data is the transformed data that is to be sent to the'
    '\n\t\treceive node. It contains the transformed versions of thrust,'
    '\n\t\troll, pitch, and yaw.'
    '\n\t\tgain data is the numerical gain sent to the mcu. It contains'
    '\n\t\tkppitch, kipitch, kdpitch, kproll, kiroll, kdroll, and kpyaw.'
    '\n\t\tack data is the specified return packet data from the receive'
    '\n\t\tnode. When operating with an elka vehicle, this data set contains'
    '\n\t\t13 16-bit variables of usable data.'
    '\n\t\tdropped data is the data packets that could not be sent to the'
    '\n\t\treceiving elka. It contains a timestamp and the number of dropped'
    '\n\t\tpackets so at that point in transmission.'

    '\nplot'
    '\n\tUsage:'
    '\n\t\tEnter <plot> from the \'Parse\' submenu to enter a two-part plot'
    '\n\t\tprompt. In the first prompt, enter up to four valid lines to plot.'
    '\n\t\tIn the second prompt, specify plot details.'
    '\n\tBehavior:'
    '\n\t\tSpecify up to four linetype,linestyle tuples. Linetypes must be'
    '\n\t\t<array type> <variable number> <array number>'
    '\n\t\tThe following linetypes are available:'
    '\n\t\tin [1-4]'
    '\n\t\tout [1-4]'
    '\n\t\tack [1-13]'
    '\n\t\tLinestyles can also be specified with keyword arguments separated'
    '\n\t\tby commas.'
    '\n\t\tlinestyles and keyword arguments can be found at'
    '\n\t\thttp://matplotlib.org/1.3.1/api/axes_api.html#matplotlib.axes.Axes.plot'
    '\n\t\te.g. ack 1 0 \'rs-\', in 3 1 \'g--\';linewidth=1.0'
    '\n\t\tThen, specify plot details. The following details are available:'
    '\n\t\ttitle, xlabel, ylabel, text, axes, and grid.'

    '\nsave'
    '\n\tUsage:'
    '\n\t\tEnter <save> <filepath> <savepath> from the \'Parse\''
    '\n\t\tsubmenu to save a .log file created by elka. Use ./ to specify'
    '\n\t\tcurrent directory.'
    '\n\tBehavior:'
    '\n\t\tSave a log file to be parsed now or later. If no savepath is'
    '\n\t\tspecified, the default save directory is ./Logging/PrevLogs and the'
    '\n\t\tdefault save file is logtype-timestamp.log.'

    '\nparse'
    '\n\tUsage:'
    '\n\t\tEnter <parse> <logtype> <filepath> from the \'Parse\' submenu to'
    '\n\t\tparse a log file into the usable data sets.'
    '\n\tBehavior:'
    '\n\t\tParse a recently or previously made log file into the usable data'
    '\n\t\tsets. Logtypes may be: in/out/ack. After successful parsing, the'
    '\n\t\toutline of the parsed data sets are displayed in the console.'
    '\n\t\tOperations and plotting can then be performed with these data sets.'
    '\n\t\tEmpty data sets, such as empty ack sets, are stored to maintain'
    '\n\t\tparallelism among.'

    '\nexport'
    '\n\tUsage:'
    '\n\t\tEnter <export> <arr_type> <arr_num> <savefile> to export a data set'
    '\n\t\tin csv format.'
    '\n\tBehavior:'
    '\n\t\tExport a usable data set in csv format.'
    '\n\t\tarr_type may be in/out/gain/ack/drop. arr_num indexes from 0.'
    )

  lp = LogParser()

  sp = False

  while not sp:
    try:
        # prompt next step
        print '\nParse:\nWhat would you like to do?'
        print p_options

        r_cmd = raw_input('<')
        cmd = parse_raw_cmd(r_cmd)

        if not cmd:
          continue
        elif cmd[0] == 'help':
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
          print 'Gain data: {}'.format([i for i in range(len(gaind))])
          print 'Ack data: {}'.format([i for i in range(len(ackd))])
          print 'Drop data: {}'.format([i for i in range(len(dropd))])
        elif cmd[0] == 'plot':
          if not data_available: raise InvalidCommand('No data available.')
          pcmd = raw_input('<Specify up to four lines and style\n<')
          fcmd = raw_input('<If desired: specify title, xlabel, ylabel, '
            'text, axes, and grid.\n<')
          lp.plot_data(**dict(zip(['fdata','arrs','style'],
              parse_plot(fcmd,pcmd))))
        elif cmd[0] == 'return' and len(cmd) == 1:
          ''' Return to main menu '''
          sp = True
        elif cmd[0] == 'save':
          if len(cmd) > 2:
            lp.save_file(cmd[1], cmd[2])
          else:
            lp.save_file(cmd[1], None)
        elif cmd[0] == 'parse' and len(cmd) == 3:
          # parse logs
          if cmd[1] == 'in':
            i = lp.parse_in(cmd[2])
            if i.any(): ind.append(i)
            print 'Parsed in data: {}'.format(ind[-1])
          elif cmd[1] == 'out':
            o,g = lp.parse_out(cmd[2])
            outd.append(o)
            gaind.append(g)
            print 'Parsed out data.\nouts: {0}\ngains:{1}'.format(
                    outd[-1],gaind[-1])
          elif cmd[1] == 'ack':
            a,d = lp.parse_ack(cmd[2])
            ackd.append(a)
            dropd.append(d)
            print 'Parsed ack data.\nacks: {0}\ndrops:{1}'.format(
                    ackd[-1],dropd[-1])
          else:
            raise InvalidCommand('Could not parse {}'.format(cmd))
          data_available = True
        elif cmd[0] == 'export':
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
    '\n\t\tA following prompt will allow you to enter custom gains. Leave this'
    '\n\t\tblank to stick with the default gains.'
    '\n\t\tTo stop running elka, press CTRL-C.'
    '\n\tBehavior:'
    '\n\t\tRuns elka as the basestation for a vehicle. Requires that the'
    '\n\t\tvehicle and the base station transceivers are both set to the same'
    '\n\t\tfrequency and the vehicle is set in receive mode.'
    '\n\t\tGains specified in the format: kppitch kdpitch kproll kdroll kpyaw'
    '\n\t\tkdyaw. Default gains are [10 200 10 200 200 0].'

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
        clear_logs('ioa')
        gains = map(int,parse_raw_cmd(raw_input(
          'Enter gains:\n< ')))
        run_elka_control(init_gains=gains)
      elif cmd[0] == 'run' and cmd[1] == 'radios':
        # mainly for debugging
        clear_logs('ioa')
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
