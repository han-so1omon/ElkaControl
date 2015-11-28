# Contains paths to python modules used in ElkaControl project
# import with:
# from importlib import import_module
# class=getattr(__import__(PACKAGE+'.'+MODULE,fromlist=['class']),'class')

import sys,os
from importlib import import_module
sys.path.append(os.getcwd())

# Define import methods
# Does not support from mod import *
# TODO add support for from mod import *
def import_from_project(pkg,mod,cls=None):
  # for importing class or method
  if cls is None:
    return import_module(pkg+'.'+mod)
    # TODO update this to 0 for python 3.3 upgrade
    return __import__(pkg+'.'+mod,globals(),locals(),[],-1)
  elif cls is not '*':
    return getattr(__import__(pkg+'.'+mod,fromlist=[cls]),cls)
  '''
  else:
    m=import_module(pkg+'.'+mod).__dict__
    print m
    globals().update(m)
    locals().update(m)
  '''

# Define packages

# Debug contains: basicParse,collectThreads,elkaThread,exceptionType,
# experiment,get_set,inputDisplay,in_to_out,joystick_calls,joystick_debug,
# main_method,pack_unpack,queuePtr,radio_match,saveFile,send_data,serialConfig,
# serialIdent,serialList,set_global,USBscan
dDEBUG='Debug'
# Elkaradio contains: elkaradioTRX,elkatalk,joy_read
dELKARADIO='Elkaradio'
# ETP contains: dataPacket,elkaDriver,elkaThread,exceptionThread
dETP='ETP'
# Inputs contains: gui,joy_read
dINPUTS='Inputs'
# Logging contains: logParser,plotData,testCtrl
dLOGGING='Logging'
# Tests contains: globals,inputs,outputs,testCommands,testCtrl,testJoystick
dTESTS='Tests'
# Utils contains: exceptions,exThread
dUTILS='Utils'

# Define modules
mBASICPARSE='basicParse'
mCOLLECTTHREADS='collectThreads'
mDATAPACKET='dataPacket'
mELKADRIVER='elkaDriver'
mELKARADIOTRX='elkaradioTRX'
mELKATALK='elkatalk'
mELKATHREAD='elkaThread'
mEXCEPTIONS='exceptions'
mEXCEPTIONTHREAD='exceptionThread'
mEXCEPTIONTYPE='exceptionType'
mEXPERIMENT='experiment'
mEXTHREAD='exThread'
mGETSET='get_set'
mGLOBALS='globals'
mGUI='gui'
mINPUTDISPLAY='inputDisplay'
mINPUTS='inputs'
mINTOOUT='in_to_out'
mJOYSTICKCALLS='joystick_calls'
mJOYSTICKDEBUG='joystick_debug'
mJOYREAD='joy_read'
mLOGPARSER='logParser'
mMAINMETHOD='main_method'
mOUTPUTS='outputs'
mPACKUNPACK='pack_unpack'
mPLOTDATA='plotData'
mQUEUEPTR='queuePtr'
mRADIOMATCH='radio_match'
mSAVEFILE='saveFile'
mSENDDATA='send_data'
mSERIALCONFIG='serialConfig'
mSERIALIDENT='serialIdent'
mSERIALLIST='serialList'
mSETGLOBAL='set_global'
mTESTCOMMANDS='testCommands'
mTESTCTRL='testCtrl'
mTESTJOYSTICK='testJoystick'
mUSBSCAN='USBscan'
