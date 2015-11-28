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
from os.path import isfile

# Add parent directory (to access global module directories)
# and logging directory (stores current logs) to PYTHONPATH
sys.path.append(os.path.join(os.getcwd(), 'Logging/Logs'))
# Import project modules/classes global vars
from elka_modules import *

# Import project modules/classes
from Utils.exceptions import *
Elkaradio = import_from_project(dELKARADIO,mELKARADIOTRX,'Elkaradio')
_find_devices=import_from_project(
    dELKARADIO,mELKARADIOTRX,'_find_devices')
LogParser = import_from_project(dLOGGING,mLOGPARSER,'LogParser')
run_elka = import_from_project(dETP,mELKATHREAD,'run_elka')
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
    logger.debug('\nMain log cleared')
  if 'i' in k and isfile('./Logging/Logs/input.log'):
    open('./Logging/Logs/input.log', 'r+').truncate()
    log_inputs = logging.getLogger('input')
    logger.debug('\nInput log cleared')
  if 'o' in k and isfile('./Logging/Logs/output.log'):
    open('./Logging/Logs/output.log', 'r+').truncate()
    log_outputs = logging.getLogger('output')
    logger.debug('\nOutput log cleared')
  if 'a' in k and isfile('./Logging/Logs/ack.log'):
    open('./Logging/Logs/ack.log', 'r+').truncate()
    log_acks = logging.getLogger('ack')
    logger.debug('\nAck log cleared')

clear_logs('mioa')

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
re_fsty = re.compile(r'(\S+)\s*=\s*([^,]+\s*)+')
re_ssty = re.compile(r'(\s*(\w+)\s*=\s*([^,;]+)\s*,?;?)')
re_data_arrs = re.compile(
  r'\s*(\w+)\s+(\d+)\s+(\d+)\s*\'?([\-a-z]+)?\'?,?')

def parse_raw_cmd(r_cmd):
  global r
  return r.findall(r_cmd)

def parse_plot(pcmd,scmd,fcmd):
  global re_fsty, re_ssty, re_data_arrs, ind, outd, ackd
  arrs = None; style = None
    
  def parse_fstyle(fcmd):
    matches = re_fsty.findall(fcmd)
    if matches:
      return dict([(m[0],m[1].strip(',')) for m in matches])
  
  def parse_sstyle(scmd):
    matches = re_ssty.findall(scmd)
    style_arr = []
    try:
      i = 0
      d = dict()
      for m in matches:
        d[m[1]] = m[2]
        if ';' in m[0] or m==matches[-1]:
          style_arr.append(d)
          d = dict()
          i += 1
    except TypeError:
      pass
    return style_arr
        

  def parse_arrs(acmd):
    matches = re_data_arrs.findall(acmd)
    arrs = [] # 2d list of objects [x,y,sty]
    if matches:
      for m in matches:
        k = int(m[2])
        # append x, then y, then style
        if m[0] == 'in' and ind[k].any():
          arrs.append([ind[k][:,0],ind[k][:,int(m[1])],m[3]])
        elif m[0] == 'out' and outd[k].any():
          arrs.append([outd[k][:,0],outd[k][:,int(m[1])],m[3]])
        elif m[0] == 'ack' and ackd[k].any():
          arrs.append([ackd[k][:,0],ackd[k][:,int(m[1])],m[3]])
        elif m[0] == 'drop' and dropd[k].any(): # FIXME IndexError: too many indices for array
          arrs.append([dropd[k][:,0],dropd[k][:,int(m[1])],m[3]])
        else:
          raise InvalidCommand('Plot array must contain data and be of '
          'type in, out, ack, or dropped')
    else: raise InvalidCommand('Incorrect plot lines specified. '
            'Must specify between one and four valid lines.')
    return arrs
  
  return parse_arrs(pcmd), parse_sstyle(scmd), parse_fstyle(fcmd)

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
# gains given in form kpp,kip,kdp,kpr,kir,kdr,kpy
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
    '\n\nexit'
    '\n\tUsage:'
    '\n\t\tEnter <exit> from a particular submenu to exit the program.'
    '\n\tBehavior:'
    '\n\t\tExits program with system call. Leaves any active data unsaved.'

    '\n\nhelp'
    '\n\tUsage:'
    '\n\t\tEnter <help> from a particular submenu to display help menu.'
    '\n\tBehavior:'
    '\n\t\tDisplays help menu. Help menu contains usage information and'
    '\n\t\texpected behavior for each command.'

    '\n\ndisplay'
    '\n\tUsage:'
    '\n\t\tEnter <display> from the \'Parse\' submenu to display the usable'
    '\n\t\tdata sets.'
    '\n\tBehavior:'
    '\n\t\tDisplays data sets that were parsed during the current session.'
    '\n\t\tData sets are persistent across menu changes. There are five types'
    '\n\t\tof data sets: in, out, gain, ack, and drop.'
    '\n\t\tin data is the raw data sent by the controller to the internal'
    '\n\t\tmodel. It contains the raw versions of thrust, roll,'
    '\n\t\tpitch, and yaw.'
    '\n\t\tout data is the transformed data that is to be sent to the'
    '\n\t\treceive node. It contains the transformed versions of thrust,'
    '\n\t\troll, pitch, and yaw.'
    '\n\t\tgain data is the numerical gain set sent to the mcu. It contains'
    '\n\t\tkppitch, kipitch, kdpitch, kproll, kiroll, kdroll, and kpyaw.'
    '\n\t\tack data is the specified return packet data from the receive'
    '\n\t\tnode. When operating with an elka vehicle, this data set contains'
    '\n\t\t13 16-bit variables of usable data.'
    '\n\t\tdrop data is the data packets that could not be sent to the'
    '\n\t\treceiving elka. It contains a timestamp and the number of dropped'
    '\n\t\tpackets at that point in transmission.'

    '\n\nplot'
    '\n\tUsage:'
    '\n\t\tEnter <plot> from the \'Parse\' submenu to enter a three-part plot'
    '\n\t\tprompt. In the first prompt, enter up to four valid lines to plot.'
    '\n\t\tIn the second prompt, specify line styles. The most important'
    '\n\t\tline style to denote is label, as this will allow you to'
    '\n\t\tassociate a line with a name.'
    '\n\t\tLine styles can also be specified with keyword arguments separated'
    '\n\t\tby commas. Line styles and keyword arguments can be found at'
    '\n\t\thttp://matplotlib.org/1.3.1/api/axes_api.html#matplotlib.axes.Axes.plot'
    '\n\t\tIn the third prompt, specify lines to plot.'
    '\n\tBehavior:'
    '\n\t\tSpecify up to four linetypes. Linetypes must be'
    '\n\t\t<array type> <variable number> <array number>'
    '\n\t\tThe following linetypes are available:'
    '\n\t\tin [1-4]'
    '\n\t\tout [1-4]'
    '\n\t\tack [1-13]'
    '\n\t\tdrop [1]'
    '\n\t\tNote: variable 0 is time, and this can be plotted vs time as well.'
    '\n\t\te.g. to plot the first variable of the first ack set and the third'
    '\n\t\t variable of the second in set, enter:'
    '\n\t\tack 1 0 \'rs-\', in 3 1 \'g--\''
    '\n\t\tNext, specify line styles, such as label and markersize.'
    '\n\t\te.g. to add a label and a markersize to line 1 and a label to line'
    '\n\t\t2, enter:'
    '\n\t\tlabel = line 1, markersize = 15; label = line 2'
    '\n\t\tThen, specify plot details. The following details are available:'
    '\n\t\ttitle, xlabel, ylabel, text, axis, and grid.'
    '\n\t\ttitle, xlabel, ylabel, and text may be strings.'
    '\n\t\taxis may be on, off, equal, scaled, tight, image, auto, or normal.'
    '\n\t\tgrid may be on or off.'
    '\n\t\te.g. to title a plot \'accel\' with x axis label \'t[s]\', enter:'
    '\n\t\ttitle=accel, xlabel = t[s]'

    '\n\nsave'
    '\n\tUsage:'
    '\n\t\tEnter <save> <filepath> <savepath> from the \'Parse\''
    '\n\t\tsubmenu to save a .log file created by elka. Use ./ to specify'
    '\n\t\tcurrent directory.'
    '\n\tBehavior:'
    '\n\t\tSave a log file to be parsed now or later. If no savepath is'
    '\n\t\tspecified, the default save directory is ./Logging/PrevLogs and the'
    '\n\t\tdefault save file is logtype-timestamp.log.'

    '\n\nparse'
    '\n\tUsage:'
    '\n\t\tEnter <parse> <logtype> <filepath> from the \'Parse\' submenu to'
    '\n\t\tparse a log file into the usable data sets.'
    '\n\tBehavior:'
    '\n\t\tParse a recently or previously made log file into the usable data'
    '\n\t\tsets. Logtypes may be: in/out/ack. After successful parsing, the'
    '\n\t\toutline of the parsed data sets is displayed in the console.'
    '\n\t\tOperations and plotting can then be performed with these data sets.'
    '\n\t\tEmpty data sets, such as empty ack sets, are stored to maintain'
    '\n\t\tparallelism among.'

    '\n\nexport'
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
          pcmd = raw_input('<Specify up to four lines\n<')
          scmd = raw_input('<Specify line styles separating each style '
          'attribute by a comma and each line by a semi-colon\n<')
          fcmd = raw_input('<Specify plot title, xlabel, '
            'ylabel, text, axis, and grid.\n<')
          lp.plot_data(**dict(zip(['arrs','styles','fdata'],
              parse_plot(pcmd,scmd,fcmd))))
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

################################ Main console method ###################################
def main_console():
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

    '\n\nhelp'
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
    '\n\t\tkdyaw. Default gains are [10 0 200 10 0 200 200].'

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
      if not cmd:
        continue
      elif cmd[0] == 'exit':
        sp = True
      elif cmd[0] == 'help':
        print help_options
      elif cmd[0] == 'run' and cmd[1] == 'elka':
        clear_logs('ioa')
        # Iinitialize gains to none in case none provided.
        # If none provided in prompt, they are filled in by driver thread.
        gains = None
        try:
          gains = map(int,raw_input(
            'Enter gains separated by commas:\n< ').split(','))
        # handle cases where user does not enter any gain values
        except ValueError:
          pass
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
################################################################################

################u############### Main gui method ###################################
from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow,QDockWidget,\
                            QMessageBox,QFileDialog
#TODO change this to dynamic import
from UI.elkamainwindow import Ui_ElkaMainWindow
class MyApp(QMainWindow, Ui_ElkaMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    Ui_ElkaMainWindow.__init__(self)
    self.setupUi(self)
    self.connectUI()

  def notify(self,obj,evt):
      try:
        return QApplication.notify(self,obj,evt)
      except Exception:
          print "Unexpected error."

  def connectUI(self):
    # Connect Command page elements
    self.gains_kpp.setMaximum(1000)
    self.gains_kpp.setValue(10)
    self.gains_kip.setMaximum(1000)
    self.gains_kip.setValue(0)
    self.gains_kdp.setMaximum(1000)
    self.gains_kdp.setValue(200)
    self.gains_kpr.setMaximum(1000)
    self.gains_kpr.setValue(10)
    self.gains_kir.setMaximum(1000)
    self.gains_kir.setValue(0)
    self.gains_kdr.setMaximum(1000)
    self.gains_kdr.setValue(200)
    self.gains_kpy.setMaximum(1000)
    self.gains_kpy.setValue(200)

    # start elka button mechanics
    self.start_elka_button.clicked.connect(self.wrap_run_ec)
    # stop elka button mechanics
    self.stop_elka_button.clicked.connect(self.wrap_stop_ec)
    # properties button mechanics
    self.properties_button.clicked.connect(self.wrap_disp_properties)
    # parse log button mechanics
    self.parse_log_button.clicked.connect(self.wrap_parse_log)
    # save log button mechanics
    self.save_log_button.clicked.connect(self.wrap_save_log)
    # export data button mechanics
    self.export_data_button.clicked.connect(self.wrap_export_data)
    # plot data button mechanics
    self.plot_data_button.clicked.connect(self.wrap_plot_data)

    self.joystick_input_button.setChecked(False)
    self.keyboard_input_button.setChecked(False)

    lp = LogParser()

    # Connect Plot page elements
    # Connect Editor page elements
    # Connect Menu elements

  def wrap_run_ec(self):
    # TODO load GUI widgets
    clear_logs('ioa')
    run_elka_control(
        init_gains=[self.gains_kpp.value(),self.gains_kip.value(),
                    self.gains_kdp.value(),self.gains_kpr.value(),
                    self.gains_kir.value(),self.gains_kdr.value(),
                    self.gains_kpy.value()])
  
  def wrap_stop_ec(self):
    #TODO add stop signal
    pass

  #TODO connect to properties menu option. Add app properties
  def wrap_disp_properties(self):
    props_string='hello'
    properties = QMessageBox.information(self,'Properties',props_string,
                    QMessageBox.Yes,QMessageBox.Yes)

  def wrap_parse_log(self):
    file=QFileDialog.getOpenFileName(self,'Select Log File','.','(*.log)')
    if file:
      pass


  def wrap_save_log(self):
    pass

  def wrap_export_data(self):
    pass

  def wrap_plot_data(self):
    pass


def main_gui():
  global logger,ind,outd,gaind,ackd,data_available
  app = QApplication(sys.argv)
  window = MyApp()
  window.show()
  sys.exit(app.exec_())
################################################################################

if __name__ == '__main__':
  if sys.argv.__contains__('-c') or sys.argv.__contains__('--console'):
    main_console()
  else:
    main_gui()
