b0VIM 7.4      tJVV�X e  eric                                    eric-Latitude-E6530                     ~eric/Documents/ElkaControlProject/ElkaControl/radio_link/__main__.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        utf-8 3210    #"! U                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 tp           s                            ]       t                     I       �                     c                           e       }                    [       �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ad          s       �  �  �  �  �  }  |  T  P  O    �  �  �  �  �  k  /  �  �  �  �  �  k  %    �  �  W    �  �  �  �  �  �  t  a  .  �
  �
  i
  B
  
  �	  �	  �	  [	  $	  �  �  �  b  .    �  �  �  �  �  �  �  �  �  z  K  J  �  �  �  �  h  .    �  �  �  �  �  �  }  D  (  #  	  �  �  �  �  {  W  D  ;  /      �  �  �  �  �  k  `  K  B  A  )     �  �  �  �  n  D                                              arrs.append([ind[k][:,0],ind[k][:,int(m[1])],m[3]])         if m[0] == 'in' and ind[k].any():         # append x, then y, then style         k = int(m[2])       for m in matches:     if matches:     arrs = [] # 2d list of objects [x,y,sty]     matches = re_data_arrs.findall(acmd)   def parse_arrs(acmd):               return style_arr       pass     except TypeError:           i += 1           d = dict()           style_arr.append(d)         if ';' in m[0] or m==matches[-1]:         d[m[1]] = m[2]       for m in matches:       d = dict()       i = 0     try:     style_arr = []     matches = re_ssty.findall(scmd)   def parse_sstyle(scmd):          return dict([(m[0],m[1].strip(',')) for m in matches])     if matches:     matches = re_fsty.findall(fcmd)   def parse_fstyle(fcmd):        arrs = None; style = None   global re_fsty, re_ssty, re_data_arrs, ind, outd, ackd def parse_plot(pcmd,scmd,fcmd):    return r.findall(r_cmd)   global r def parse_raw_cmd(r_cmd):    r'\s*(\w+)\s+(\d+)\s+(\d+)\s*\'?([\-a-z]+)?\'?,?') re_data_arrs = re.compile( re_ssty = re.compile(r'(\s*(\w+)\s*=\s*([^,;]+)\s*,?;?)') re_fsty = re.compile(r'(\S+)\s*=\s*([^,]+\s*)+') # use re.findall for these r = re.compile(r'(\S+)') # Global regexps for slight time efficiency ######################### Define helper functions ##############################  data_available = False # true after parse call dropd = [] gaind = [] ackd = [] outd = [] ind = [] ### set up parsed data arrays  clear_logs('mioa')      logger.debug('\nAck log cleared')     log_acks = logging.getLogger('ack')     open('./Logging/Logs/ack.log', 'r+').truncate()   if 'a' in k and isfile('./Logging/Logs/ack.log'):     logger.debug('\nOutput log cleared')     log_outputs = logging.getLogger('output')     open('./Logging/Logs/output.log', 'r+').truncate()   if 'o' in k and isfile('./Logging/Logs/output.log'):     logger.debug('\nInput log cleared')     log_inputs = logging.getLogger('input')     open('./Logging/Logs/input.log', 'r+').truncate()   if 'i' in k and isfile('./Logging/Logs/input.log'):     logger.debug('\nMain log cleared')     logger = logging.getLogger('main')     open('./Logging/Logs/main.log', 'r+').truncate()   if 'm' in k and isfile('./Logging/Logs/main.log'):   logging.config.fileConfig('./Logging/Logs/logging.conf', disable_existing_loggers=False)   global logger, log_inputs, log_outputs, log_acks def clear_logs(k): # call each time before logging to a file  log_acks = None log_outputs = None log_inputs = None logger = None #Establish loggers as module level globals ########################### Set up loggers ############################## run_elka = import_from_project(dETP,mELKATHREAD,'run_elka') LogParser = import_from_project(dLOGGING,mLOGPARSER,'LogParser')     dELKARADIO,mELKARADIOTRX,'_find_devices') _find_devices=import_from_project( Elkaradio = import_from_project(dELKARADIO,mELKARADIOTRX,'Elkaradio') from Utils.exceptions import * # Import project modules/classes  from elka_modules import * # Import project modules/classes global vars sys.path.append(os.path.join(os.getcwd(), 'Logging/Logs')) # and logging directory (stores current logs) to PYTHONPATH # Add parent directory (to access global module directories)  from os.path import isfile from IPython import embed # debugging         threading, re, string import os, sys, traceback, logging, logging.config, logging.handlers,\  """ Contains main function for Elka Control  Module: __main__.py Package: radio_link  Lab: Alfred Gessow Rotorcraft Center Project: Elkaradio Control  Author: Eric Solomon """ ad  W  �     [       �  �  �  �  l  R  E    �  �  p  o    �  �  }  P  :    �  �  �  �  �  �  q  Y  5  4    �  �  �  �  r  N  -  	  �
  �
  �
  �
  a
  =
  
  
  �	  �	  �	  ^	  <	  �  �  �  �  �  }  |  [  8        �  �  �  w  4  �  �  �  �  �  �  �  e  \  [  K    �  �  �  �  m  l  Q  	  �  �  �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 main_gui()   else:     main_console()   if sys.argv.__contains__('-c') or sys.argv.__contains__('--console'): if __name__ == '__main__':  ################################################################################   sys.exit(app.exec_())   window.show()   window = MyApp()   app = QApplication(sys.argv)   global logger,ind,outd,gaind,ackd,data_available def main_gui():      pass   def wrap_disp_properties():      pass     #TODO add stop signal   def wrap_stop_ec(self):                        self.gains_kpy.value()])                     self.gains_kir.value(),self.gains_kdr.value(),                     self.gains_kdp.value(),self.gains_kpr.value(),         init_gains=[self.gains_kpp.value(),self.gains_kip.value(),     run_elka_control(     clear_logs('ioa')     # TODO load GUI widgets   def wrap_run_ec(self):      # Connect Menu elements     # Connect Editor page elements     # Connect Plot page elements      lp = LogParser()      self.keyboard_input_button.setChecked(False)     self.joystick_input_button.setChecked(False)      self.properties_button.clicked.connect(self.wrap_disp_properties)     # properties button mechanics     self.stop_elka_button.clicked.connect(self.wrap_stop_ec)     # stop elka button mechanics     self.start_elka_button.clicked.connect(self.wrap_run_ec)     # start elka button mechanics      self.gains_kpy.setValue(200)     self.gains_kpy.setMaximum(1000)     self.gains_kdr.setValue(200)     self.gains_kdr.setMaximum(1000)     self.gains_kir.setValue(0)     self.gains_kir.setMaximum(1000)     self.gains_kpr.setValue(10)     self.gains_kpr.setMaximum(1000)     self.gains_kdp.setValue(200)     self.gains_kdp.setMaximum(1000)     self.gains_kip.setValue(0)     self.gains_kip.setMaximum(1000)     self.gains_kpp.setValue(10)     self.gains_kpp.setMaximum(1000)     # Connect Command page elements   def connectUI(self):            print "Unexpected error."       except Exception:         return QApplication.notify(self,obj,evt)       try:   def notify(self,obj,evt):      self.connectUI()     self.setupUi(self)     Ui_ElkaMainWindow.__init__(self)     QMainWindow.__init__(self)   def __init__(self): class MyApp(QMainWindow, Ui_ElkaMainWindow): from UI.elkamainwindow import Ui_ElkaMainWindow #TODO change this to dynamic import from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow,QDockWidget ################u############### Main gui method ###################################  ################################################################################       logger.debug(threading.enumerate())        # should only show main thread as alive       logger.debug(traceback.format_exc())     finally:       logger.exception(e)       print "Exception: ", e     except Exception as e:       logger.exception(e)       print "Invalid command:", e     except InvalidCommand as e: ad     �     ]       �  �  d  $  �  �  u  ,    �  �  q  n  ,  +    �  �  �  �  g  J    �  �  �  [  #  �
  �
  �
  �
  y
  x
  _
  -
  �	  �	  �	  �	  �	  d	  c	  J	  :	  	  �  �  �  �  w  l  "      �  �  �  `  E  &  �  �  w  T    �  �  ^  K  <  +  �  �  �  �  s  b      �  �  �  y  h      �  �  U    �  �           '\n\t\tmodel. It contains the raw versions of thrust, roll,'     '\n\t\tin data is the raw data sent by the controller to the internal'     '\n\t\tof data sets: in, out, gain, ack, and drop.'     '\n\t\tData sets are persistent across menu changes. There are five types'     '\n\t\tDisplays data sets that were parsed during the current session.'     '\n\tBehavior:'     '\n\t\tdata sets.'     '\n\t\tEnter <display> from the \'Parse\' submenu to display the usable'     '\n\tUsage:'     '\n\ndisplay'      '\n\t\texpected behavior for each command.'     '\n\t\tDisplays help menu. Help menu contains usage information and'     '\n\tBehavior:'     '\n\t\tEnter <help> from a particular submenu to display help menu.'     '\n\tUsage:'     '\n\nhelp'      '\n\t\tExits program with system call. Leaves any active data unsaved.'     '\n\tBehavior:'     '\n\t\tEnter <exit> from a particular submenu to exit the program.'     '\n\tUsage:'     '\n\nexit'   help_options = (               '\nExit program <exit>')               '\nReturn to main menu <return>'               '\nExport log file in csv format <export> <logtype> <lognum> <savefile.csv>'               '\nParse log file <parse> <logtype> <./path/to/x.log>'               '\nPlot data <plot>'               '\nExport data to formatted file <export>'               '\nSave data file <save> <./path/to/file.bar>'                '\nDisplay available data sets <display>'   p_options = ('\nHelp <help>'   # Return returns to Main   # Plot plots with x,y,z as axes values   # Display displays set names, export sends to spreadsheet,   global ind,outd,gaind,ackd,data_available def parse_logs():                   .format(i))     logger.debug('\nElkaradio number {0} is set to primary receive mode'\     i += 1     r.set_radio_mode(Elkaradio.MODE_PRX)   for r in rx:   data_available = False # true after parse call   i = 0   ''' Demonstrate ETP with two ElkaRadios '''   logger.debug('Setting up radios')   global logger def setup_radios(rx=[]):    run_elka(init_gains=init_gains)   logger.debug('Running Elka Control')     setup_radios(rx)   if rx:   global logger, log_inputs, log_outputs, log_acks def run_elka_control(rx=None,init_gains=None): # gains given in form kpp,kip,kdp,kpr,kir,kdr,kpy """ Run elka control """    return arr_idx[0][arr_num],arr_idx[1],','   arr_idx = ret_arr_idx[arr_typ]     ]))     (dropd,'t=time;d=drop\nt1,d1')     't1,g1,g2,g3,a1,a2,a3,e1,e2,c1,c2,c3,c4,c5'),     (ackd,'t=time;g=gyro;a=accel;e=euler;c=commanded\n'       'kpp,kip,kdp,kpr,kir,kdr,kpy'),       'kpr=Kp_roll;kir=Ki_roll;kdr=Kd_roll;kpy=Kp_yaw;\n'     (gaind,'t=time;kpp=Kp_pitch;kip=Ki_pitch;kdp=Kd_pitch;\n'          't1,th1,r1,p1,y1'),     (outd,'t=time;th=thrust;r=roll;p=pitch;y=yaw\n'          't1,th1,r1,p1,y1'),     (ind,'t=time;th=thrust;r=roll;p=pitch;y=yaw\n'     ],[     'in','out','gain','ack','drop',   ret_arr_idx = dict(zip([   global ind, outd, gaind, ackd, dropd def retrieve_arr(arr_typ,arr_num):    return parse_arrs(pcmd), parse_sstyle(scmd), parse_fstyle(fcmd)        return arrs             'Must specify between one and four valid lines.')     else: raise InvalidCommand('Incorrect plot lines specified. '           'type in, out, ack, or dropped')           raise InvalidCommand('Plot array must contain data and be of '         else:           arrs.append([dropd[k][:,0],dropd[k][:,int(m[1])],m[3]])         elif m[0] == 'drop' and dropd[k].any(): # FIXME IndexError: too many indices for array           arrs.append([ackd[k][:,0],ackd[k][:,int(m[1])],m[3]])         elif m[0] == 'ack' and ackd[k].any():           arrs.append([outd[k][:,0],outd[k][:,int(m[1])],m[3]])         elif m[0] == 'out' and outd[k].any(): ad     N     I       �  �  S  1  �  �  P    �  �  <  	    �  �  �  J     �  �  B  �
  �
  m
  Y
  
  �	  �	  �	  �	  n	  Y	  
	  �  �  \    �  �  v  )  �  �  e  B  �  �  �  �  �  j       �  �  S      
  �  �  t  `    �  |  ,  �  �  �  �  �  N  M                    '\n\t\tEnter <export> <arr_type> <arr_num> <savefile> to export a data set'     '\n\tUsage:'     '\n\nexport'      '\n\t\tparallelism among.'     '\n\t\tEmpty data sets, such as empty ack sets, are stored to maintain'     '\n\t\tOperations and plotting can then be performed with these data sets.'     '\n\t\toutline of the parsed data sets is displayed in the console.'     '\n\t\tsets. Logtypes may be: in/out/ack. After successful parsing, the'     '\n\t\tParse a recently or previously made log file into the usable data'     '\n\tBehavior:'     '\n\t\tparse a log file into the usable data sets.'     '\n\t\tEnter <parse> <logtype> <filepath> from the \'Parse\' submenu to'     '\n\tUsage:'     '\n\nparse'      '\n\t\tdefault save file is logtype-timestamp.log.'     '\n\t\tspecified, the default save directory is ./Logging/PrevLogs and the'     '\n\t\tSave a log file to be parsed now or later. If no savepath is'     '\n\tBehavior:'     '\n\t\tcurrent directory.'     '\n\t\tsubmenu to save a .log file created by elka. Use ./ to specify'     '\n\t\tEnter <save> <filepath> <savepath> from the \'Parse\''     '\n\tUsage:'     '\n\nsave'      '\n\t\ttitle=accel, xlabel = t[s]'     '\n\t\te.g. to title a plot \'accel\' with x axis label \'t[s]\', enter:'     '\n\t\tgrid may be on or off.'     '\n\t\taxis may be on, off, equal, scaled, tight, image, auto, or normal.'     '\n\t\ttitle, xlabel, ylabel, and text may be strings.'     '\n\t\ttitle, xlabel, ylabel, text, axis, and grid.'     '\n\t\tThen, specify plot details. The following details are available:'     '\n\t\tlabel = line 1, markersize = 15; label = line 2'     '\n\t\t2, enter:'     '\n\t\te.g. to add a label and a markersize to line 1 and a label to line'     '\n\t\tNext, specify line styles, such as label and markersize.'     '\n\t\tack 1 0 \'rs-\', in 3 1 \'g--\''     '\n\t\t variable of the second in set, enter:'     '\n\t\te.g. to plot the first variable of the first ack set and the third'     '\n\t\tNote: variable 0 is time, and this can be plotted vs time as well.'     '\n\t\tdrop [1]'     '\n\t\tack [1-13]'     '\n\t\tout [1-4]'     '\n\t\tin [1-4]'     '\n\t\tThe following linetypes are available:'     '\n\t\t<array type> <variable number> <array number>'     '\n\t\tSpecify up to four linetypes. Linetypes must be'     '\n\tBehavior:'     '\n\t\tIn the third prompt, specify lines to plot.'     '\n\t\thttp://matplotlib.org/1.3.1/api/axes_api.html#matplotlib.axes.Axes.plot'     '\n\t\tby commas. Line styles and keyword arguments can be found at'     '\n\t\tLine styles can also be specified with keyword arguments separated'     '\n\t\tassociate a line with a name.'     '\n\t\tline style to denote is label, as this will allow you to'     '\n\t\tIn the second prompt, specify line styles. The most important'     '\n\t\tprompt. In the first prompt, enter up to four valid lines to plot.'     '\n\t\tEnter <plot> from the \'Parse\' submenu to enter a three-part plot'     '\n\tUsage:'     '\n\nplot'      '\n\t\tpackets at that point in transmission.'     '\n\t\treceiving elka. It contains a timestamp and the number of dropped'     '\n\t\tdrop data is the data packets that could not be sent to the'     '\n\t\t13 16-bit variables of usable data.'     '\n\t\tnode. When operating with an elka vehicle, this data set contains'     '\n\t\tack data is the specified return packet data from the receive'     '\n\t\tkppitch, kipitch, kdpitch, kproll, kiroll, kdroll, and kpyaw.'     '\n\t\tgain data is the numerical gain set sent to the mcu. It contains'     '\n\t\troll, pitch, and yaw.'     '\n\t\treceive node. It contains the transformed versions of thrust,'     '\n\t\tout data is the transformed data that is to be sent to the'     '\n\t\tpitch, and yaw.' ad     �     c       �  �  �  S  M  L  9  8  +  *      �  �  �  �  �  f  e  Q  >    �  �  �  �  e  O    �  �  b    �  �  p  $  �
  �
  ]
  "
  �	  �	  �	  V	  0	  	  �  �  �  �  �  P  9    �  �  �  {  T  9    �  �  �  k  P  4  �  �  �  v  V  5    �  �  �  C  #    �  �  �  �  E  D  �  �  �  �  �  �  �  e  �  �  �  �  �           help_options = (             )               'Parse log files <parse>'                'Run ElkaControl with Elka <run elka>\n' 'Run ElkaControl with two ElkaRadios <run radios>\n'                'Exit program <exit>\n'   options = ('\nHelp <help>\n'   base = None   sp = False    global logger def main_console(): ################################ Main console method ###################################  ################################################################################       logger.exception(e)       print 'Exception:', e     except Exception as e:       logger.exception(e)       print "Invalid command:", e     except InvalidCommand as e:           raise InvalidCommand('Invalid command for submenu Parse Logs.')         else:                   retrieve_arr(cmd[1],int(cmd[2])))))                   **dict(zip(['arr','header','delimiter'],           lp.export_arr(filename=cmd[3],         elif cmd[0] == 'export':           data_available = True             raise InvalidCommand('Could not parse {}'.format(cmd))           else:                     ackd[-1],dropd[-1])             print 'Parsed ack data.\nacks: {0}\ndrops:{1}'.format(             dropd.append(d)             ackd.append(a)             a,d = lp.parse_ack(cmd[2])           elif cmd[1] == 'ack':                     outd[-1],gaind[-1])             print 'Parsed out data.\nouts: {0}\ngains:{1}'.format(             gaind.append(g)             outd.append(o)             o,g = lp.parse_out(cmd[2])           elif cmd[1] == 'out':             print 'Parsed in data: {}'.format(ind[-1])             if i.any(): ind.append(i)             i = lp.parse_in(cmd[2])           if cmd[1] == 'in':           # parse logs         elif cmd[0] == 'parse' and len(cmd) == 3:             lp.save_file(cmd[1], None)           else:             lp.save_file(cmd[1], cmd[2])           if len(cmd) > 2:         elif cmd[0] == 'save':           sp = True           ''' Return to main menu '''         elif cmd[0] == 'return' and len(cmd) == 1:               parse_plot(pcmd,scmd,fcmd))))           lp.plot_data(**dict(zip(['arrs','styles','fdata'],             'ylabel, text, axis, and grid.\n<')           fcmd = raw_input('<Specify plot title, xlabel, '           'attribute by a comma and each line by a semi-colon\n<')           scmd = raw_input('<Specify line styles separating each style '           pcmd = raw_input('<Specify up to four lines\n<')           if not data_available: raise InvalidCommand('No data available.')         elif cmd[0] == 'plot':           print 'Drop data: {}'.format([i for i in range(len(dropd))])           print 'Ack data: {}'.format([i for i in range(len(ackd))])           print 'Gain data: {}'.format([i for i in range(len(gaind))])           print 'Output data: {}'.format([i for i in range(len(outd))])           print 'Input data: {}'.format([i for i in range(len(ind))])           ''' Display usable data sets '''         elif cmd[0] == 'display' and len(cmd) == 1:           sys.exit(0)           #TODO clean up program before exiting           ''' Clean up and exit program '''         elif cmd[0] == 'exit':           print help_options           ''' Display options '''         elif cmd[0] == 'help':           continue         if not cmd:          cmd = parse_raw_cmd(r_cmd)         r_cmd = raw_input('<')          print p_options         print '\nParse:\nWhat would you like to do?'         # prompt next step     try:   while not sp:    sp = False    lp = LogParser()      )     '\n\t\tarr_type may be in/out/gain/ack/drop. arr_num indexes from 0.'     '\n\t\tExport a usable data set in csv format.'     '\n\tBehavior:'     '\n\t\tin csv format.' ad     �     e       �  �  �  �  :  9  *    �  �  s  C  B  /    �  ~  K      �  n  0  �  �  �  �  |  -  �
  �
  �
  V
  
  

  �	  �	  �	  �	  <	  �  �  �  �  �  �  �  �  e  D  C  $      �  �  �  �  i  O    �  �  �  �  B    �  �  �  y  Z  @  2    �  �  �  �  z  i  H  *    	  �  �  �  h  E      �  �  �  �  X  >    �  �  �                                     logger.exception(e)       print 'Joystick thread has stopped: ', e     except JoystickThreadFinished as e:       logger.exception(e)       print "Exception in comm link: ", e     except LinkException as e:       logger.exception(e)       print "Elkaradio not found: ", e     except ElkaradioNotFound as e:       logger.exception(e)       print "Keyboard Interrupt: ", e     except KeyboardInterrupt as e:       logger.exception(e)       print "Joystick not found: ", e     except JoystickNotFound as e:         raise InvalidCommand('Invalid command for menu Main.')       else:         parse_logs()       elif cmd[0] == 'parse':         run_elka_control(rx=rx)            i += 1             rx.append(Elkaradio(erads[i]))           if i != 0:           erads.append(e)         for e in _find_devices():         rx = [] # array of receive nodes         erads = []         i = 0         clear_logs('ioa')         # mainly for debugging       elif cmd[0] == 'run' and cmd[1] == 'radios':         run_elka_control(init_gains=gains)           pass         except ValueError:         # handle cases where user does not enter any gain values             'Enter gains separated by commas:\n< ').split(','))           gains = map(int,raw_input(         try:         gains = None         # If none provided in prompt, they are filled in by driver thread.         # Iinitialize gains to none in case none provided.         clear_logs('ioa')       elif cmd[0] == 'run' and cmd[1] == 'elka':         print help_options       elif cmd[0] == 'help':         sp = True       elif cmd[0] == 'exit':         continue       if not cmd:       """ main option tree """        cmd = parse_raw_cmd(r_cmd)       r_cmd = raw_input('< ')              print options       print '\nMain:\nWhat would you like to do?'     try:   while not sp:      )     '\n\t\tmanipulate recently captured as well as previously stored data.'     '\n\t\tEnters the \'Parse\' submenu. From there, you may parse and'     '\n\tBehavior:'     '\n\t\tEnter <parse> from the \'Main\' menu to enter the \'Parse\' submenu.'     '\n\tUsage:'     '\n\nparse'      '\n\t\tboth set to the same frequency. This is a mainly a debug mode.'     '\n\t\tRequires that the vehicle and the base station transceivers are'     '\n\t\tRuns elka as the basestation for another elkaradio dongle.'     '\n\tBehavior:'     '\n\t\tTo stop running elka, press CTRL-C.'     '\n\t\tEnter <run radios> from the \'Main\' menu to run elka with radios.'     '\n\tUsage:'     '\n\nrun radios'      '\n\t\tkdyaw. Default gains are [10 0 200 10 0 200 200].'     '\n\t\tGains specified in the format: kppitch kdpitch kproll kdroll kpyaw'     '\n\t\tfrequency and the vehicle is set in receive mode.'     '\n\t\tvehicle and the base station transceivers are both set to the same'     '\n\t\tRuns elka as the basestation for a vehicle. Requires that the'     '\n\tBehavior:'     '\n\t\tTo stop running elka, press CTRL-C.'     '\n\t\tblank to stick with the default gains.'     '\n\t\tA following prompt will allow you to enter custom gains. Leave this'     '\n\t\tEnter <run elka> from the \'Main\' menu to run elka with a vehicle.'     '\n\tUsage:'     '\n\nrun elka'      '\n\t\texpected behavior for each command.'     '\n\t\tDisplays help menu. Help menu contains usage information and'     '\n\tBehavior:'     '\n\t\tEnter <help> from a particular submenu to display help menu.'     '\n\tUsage:'     '\n\nhelp'      '\n\t\tExits program with system call. Leaves any active data unsaved.'     '\n\tBehavior:'     '\n\t\tEnter <exit> from a particular submenu to exit the program.'     '\n\tUsage:'     '\nexit' 