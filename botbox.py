#!/usr/bin/python3.10

"""

/****************************************************************************/
/****************************************************************************/
/****************************************************************************/
/******************************* BotBox 1.00 ********************************/
/****************************************************************************/
/****************************************************************************/
/****************************************************************************/


Version = 12.25.2023KA

This program was written by Carl W Livingston. BRAVO-KARL

/****************************************************************************/
/******************************** WARNING ***********************************/
/****************************************************************************/

No license it granted or implied in this document!
 This source code == the exclusive property of Greenbean Battery LLC.

Copyright Notice!
  Greenbean Battery and retains all rights to this program code.

  No part of this program may be reproduced, in part or in whole, in any form
  or by any means, without written permission from Greenbean Battery LLC.

  The object code shall not be decompiled, dis-assembled, or otherwise
  decoded for any reason.

  No part of this program may be used, in part or in whole, for any product
  other then that for which it was written.

  Performing any of the above restrictions may be in violation of federal
  and/or state copyright law!

/****************************************************************************/
/****************************YOU HAVE BEEN WARNED !!! ***********************/
/****************************************************************************/
"""

"""
  October 16:
      Make it so ALL channels stop at the same time, whenever the
      first channel becomes "DONE".

  October 18:
       Remove the first channel "DONE" modification.

  October 22:
       Restructured file naming so that file names are only
       assigned at the beginning for this program file.

  October 22:
       Renamed "Slacker_Profile.tmp" to "BotBox_Profile.tmp"
       Renamed "Slacker_Profile.csv" to "BotBox_Profile.csv"

  November 06:
       Added an "off-line" line plotting function for discharge profiling.

  November 08:
       Added an "off-line" bar chart function for the final charge Ampere hours.

"""

#
#*********************** BotBox Starts Here **************************
#
# lsusb 2>/dev/null | sed 's/.*\(ID .*\)/\1/'
# dmesg | grep ttyUSB | grep -v grep | grep -o ttyUSB[0-50]
# dmesg | grep -o ttyUSB[0-50]
#
#

import os
import io
import sys
import time
import timeit
import glob
import serial
import serial.tools.list_ports as port_list
import threading
import inspect
import gc

#import re
#import string

from datetime import date
from datetime import datetime

from tkinter import *
from tkinter import ttk
import tkinter as tk

import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import style
import pandas as pd

from Plot_1x4_IR_Bar_Graph import Plot_1x4_IR_Bar_Graph
from Plot_1x20_IR_Bar_Graph import Plot_1x20_IR_Bar_Graph

#######################################################################
######################### Variable Initialization #####################
#######################################################################
version = "02.01.2020"

global MAX_USB_PORTS
MAX_USB_PORTS = 0

global baudrate
baudrate = 115200

global SampleCount
SampleCount = 0

global MaxSampleCount
MaxSampleCount = 500

global SampleTime
SampleTime = 5.00

global PassCount
PassCount = 0

global PassTarget
PassTarget = 0

global GraphEnable
GraphEnable = False

global KeyStatus
KeyStatus = "Value"

global mode
mode = "IDLE"

global ProfileStatus
ProfileStatus = 'IDLE'

global RunStatus
RunStatus = "Value"

global Profile_Time
Profile_Time = 0.00

global Delta_V
Delta_V = 0.00

global Delta_I
Delta_I = 0.00

global IR
IR = 0.00

ports = []
portslist = {}
PortList = {}
SampleStatus = {}
DoneStatus = {}

'''
global TEMP_FILE
global CSV_FILE
global CHG_FILE
global DVDT_FILE
global IR_FILE
global LOAD_FILE
global CFG_FILE
'''

'''
TEMP_FILE = "/home/greenbean/GreenBean/PlotFiles/BotBox_Profile.tmp"
DSC_FILE = "/home/greenbean/GreenBean/PlotFiles/BotBox_Dischargefile.csv"
CHG_FILE = "/home/greenbean/GreenBean/PlotFiles/BotBox_Chargefile.csv"
CFG_FILE = "/home/greenbean/GreenBean/BotBox.cfg"
'''
LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"

#######################################################################
#######################################################################
#######################################################################

#Sample = []
#Module_1 = []
#Module_2 = []
#Module_3 = []
#Module_4 = []

X_Axis_4 = []
Module_1 = []
Module_2 = []
Module_3 = []
Module_4 = []
Module_5 = []
Module_6 = []
Module_7 = []
Module_8 = []
Module_9 = []
Module_10 = []
Module_11 = []
Module_12 = []
Module_13 = []
Module_14 = []
Module_15 = []
Module_16 = []
Module_17 = []
Module_18 = []
Module_19 = []
Module_20 = []

#######################################################################
#######################################################################
#######################################################################

PortList = { 0:99, 1:99, 2:99, 3:99,
             4:99, 5:99, 6:99, 7:99,
             8:99, 9:99, 10:99, 11:99,
            12:99, 13:99, 14:99, 15:99,
            16:99, 17:99, 18:99, 19:99,
            20:99, 21:99, 22:99, 23:99,
            24:99, 25:99, 26:99, 27:99,
            28:99, 29:99, 30:99, 31:99,
            32:99, 33:99, 34:99, 35:99,
            36:99, 37:99, 38:99, 39:99 }

#---------------------------------------------------------------------#

SampleStatus = { 0:"Value", 1:"Value", 2:"Value", 3:"Value",
                 4:"Value", 5:"Value", 6:"Value", 7:"Value",
                 8:"Value", 9:"Value", 10:"Value", 11:"Value",
                12:"Value", 13:"Value", 14:"Value", 15:"Value",
                16:"Value", 17:"Value", 18:"Value", 19:"Value",
                20:"Value", 21:"Value", 22:"Value", 23:"Value",
                24:"Value", 25:"Value", 26:"Value", 27:"Value",
                28:"Value", 29:"Value", 30:"Value", 31:"Value",
                32:"Value", 33:"Value", 34:"Value", 35:"Value",
                36:"Value", 37:"Value", 38:"Value", 39:"Value" }

SampleStatusLast = { 0:"Value", 1:"Value", 2:"Value", 3:"Value",
                     4:"Value", 5:"Value", 6:"Value", 7:"Value",
                     8:"Value", 9:"Value", 10:"Value", 11:"Value",
                    12:"Value", 13:"Value", 14:"Value", 15:"Value",
                    16:"Value", 17:"Value", 18:"Value", 19:"Value",
                    20:"Value", 21:"Value", 22:"Value", 23:"Value",
                    24:"Value", 25:"Value", 26:"Value", 27:"Value",
                    28:"Value", 29:"Value", 30:"Value", 31:"Value",
                    32:"Value", 33:"Value", 34:"Value", 35:"Value",
                    36:"Value", 37:"Value", 38:"Value", 39:"Value" }

ProfileDischargeStatus = { 0:"Value", 1:"Value", 2:"Value", 3:"Value",
                           4:"Value", 5:"Value", 6:"Value", 7:"Value",
                           8:"Value", 9:"Value", 10:"Value", 11:"Value",
                          12:"Value", 13:"Value", 14:"Value", 15:"Value",
                          16:"Value", 17:"Value", 18:"Value", 19:"Value",
                          20:"Value", 21:"Value", 22:"Value", 23:"Value",
                          24:"Value", 25:"Value", 26:"Value", 27:"Value",
                          28:"Value", 29:"Value", 30:"Value", 31:"Value",
                          32:"Value", 33:"Value", 34:"Value", 35:"Value",
                          36:"Value", 37:"Value", 38:"Value", 39:"Value" }

DoneStatus = { 0:"Value", 1:"Value", 2:"Value", 3:"Value",
               4:"Value", 5:"Value", 6:"Value", 7:"Value",
               8:"Value", 9:"Value", 10:"Value", 11:"Value",
              12:"Value", 13:"Value", 14:"Value", 15:"Value",
              16:"Value", 17:"Value", 18:"Value", 19:"Value",
              20:"Value", 21:"Value", 22:"Value", 23:"Value",
              24:"Value", 25:"Value", 26:"Value", 27:"Value",
              28:"Value", 29:"Value", 30:"Value", 31:"Value",
              32:"Value", 33:"Value", 34:"Value", 35:"Value",
              36:"Value", 37:"Value", 38:"Value", 39:"Value" }

Error_200_List = { 0:"Value", 1:"Value", 2:"Value", 3:"Value",
                 4:"Value", 5:"Value", 6:"Value", 7:"Value",
                 8:"Value", 9:"Value", 10:"Value", 11:"Value",
                12:"Value", 13:"Value", 14:"Value", 15:"Value",
                16:"Value", 17:"Value", 18:"Value", 19:"Value",
                20:"Value", 21:"Value", 22:"Value", 23:"Value",
                24:"Value", 25:"Value", 26:"Value", 27:"Value",
                28:"Value", 29:"Value", 30:"Value", 31:"Value",
                32:"Value", 33:"Value", 34:"Value", 35:"Value",
                36:"Value", 37:"Value", 38:"Value", 39:"Value" }

#---------------------------------------------------------------------#

ModuleVoltage = { 0:0.00, 1:0.00, 2:0.00, 3:0.00,
                  4:0.00, 5:0.00, 6:0.00, 7:0.00,
                  8:0.00, 9:0.00, 10:0.00, 11:0.00,
                 12:0.00, 13:0.00, 14:0.00, 15:0.00,
                 16:0.00, 17:0.00, 18:0.00, 19:0.00,
                 20:0.00, 21:0.00, 22:0.00, 23:0.00,
                 24:0.00, 25:0.00, 26:0.00, 27:0.00,
                 28:0.00, 29:0.00, 30:0.00, 31:0.00,
                 32:0.00, 33:0.00, 34:0.00, 35:0.00,
                 36:0.00, 37:0.00, 38:0.00, 39:0.00 }

LastVoltage = { 0:0.00, 1:0.00, 2:0.00, 3:0.00,
                4:0.00, 5:0.00, 6:0.00, 7:0.00,
                8:0.00, 9:0.00, 10:0.00, 11:0.00,
               12:0.00, 13:0.00, 14:0.00, 15:0.00,
               16:0.00, 17:0.00, 18:0.00, 19:0.00,
               20:0.00, 21:0.00, 22:0.00, 23:0.00,
               24:0.00, 25:0.00, 26:0.00, 27:0.00,
               28:0.00, 29:0.00, 30:0.00, 31:0.00,
               32:0.00, 33:0.00, 34:0.00, 35:0.00,
               36:0.00, 37:0.00, 38:0.00, 39:0.00 }

Module_dVdt = { 0:0.00, 1:0.00, 2:0.00, 3:0.00,
                4:0.00, 5:0.00, 6:0.00, 7:0.00,
                8:0.00, 9:0.00, 10:0.00, 11:0.00,
               12:0.00, 13:0.00, 14:0.00, 15:0.00,
               16:0.00, 17:0.00, 18:0.00, 19:0.00,
               20:0.00, 21:0.00, 22:0.00, 23:0.00,
               24:0.00, 25:0.00, 26:0.00, 27:0.00,
               28:0.00, 29:0.00, 30:0.00, 31:0.00,
               32:0.00, 33:0.00, 34:0.00, 35:0.00,
               36:0.00, 37:0.00, 38:0.00, 39:0.00 }

#---------------------------------------------------------------------#

ChargeAmpereHours = {
                  0:b'00000', 1:b'00000', 2:b'00000', 3:b'00000',
                  4:b'00000', 5:b'00000', 6:b'00000', 7:b'00000',
                  8:b'00000', 9:b'00000', 10:b'00000', 11:b'00000',
                 12:b'00000', 13:b'00000', 14:b'00000', 15:b'00000',
                 16:b'00000', 17:b'00000', 18:b'00000', 19:b'00000',
                 20:b'00000', 21:b'00000', 22:b'00000', 23:b'00000',
                 24:b'00000', 25:b'00000', 26:b'00000', 27:b'00000',
                 28:b'00000', 29:b'00000', 30:b'00000', 31:b'00000',
                 32:b'00000', 33:b'00000', 34:b'00000', 35:b'00000',
                 36:b'00000', 37:b'00000', 38:b'00000', 39:b'00000' }

ChargeLastAmpereHours = {
                      0:b'00000', 1:b'00000', 2:b'00000', 3:b'00000',
                      4:b'00000', 5:b'00000', 6:b'00000', 7:b'00000',
                      8:b'00000', 9:b'00000', 10:b'00000', 11:b'00000',
                     12:b'00000', 13:b'00000', 14:b'00000', 15:b'00000',
                     16:b'00000', 17:b'00000', 18:b'00000', 19:b'00000',
                     20:b'00000', 21:b'00000', 22:b'00000', 23:b'00000',
                     24:b'00000', 25:b'00000', 26:b'00000', 27:b'00000',
                     28:b'00000', 29:b'00000', 30:b'00000', 31:b'00000',
                     32:b'00000', 33:b'00000', 34:b'00000', 35:b'00000',
                     36:b'00000', 37:b'00000', 38:b'00000', 39:b'00000' }

#---------------------------------------------------------------------#

DischargeAmpereHours = {
                     0:b'00000', 1:b'00000', 2:b'00000', 3:b'00000',
                     4:b'00000', 5:b'00000', 6:b'00000', 7:b'00000',
                     8:b'00000', 9:b'00000', 10:b'00000', 11:b'00000',
                    12:b'00000', 13:b'00000', 14:b'00000', 15:b'00000',
                    16:b'00000', 17:b'00000', 18:b'00000', 19:b'00000',
                    20:b'00000', 21:b'00000', 22:b'00000', 23:b'00000',
                    24:b'00000', 25:b'00000', 26:b'00000', 27:b'00000',
                    28:b'00000', 29:b'00000', 30:b'00000', 31:b'00000',
                    32:b'00000', 33:b'00000', 34:b'00000', 35:b'00000',
                    36:b'00000', 37:b'00000', 38:b'00000', 39:b'00000' }

DischargeLastAmpereHours = {
                         0:b'00000', 1:b'00000', 2:b'00000', 3:b'00000',
                         4:b'00000', 5:b'00000', 6:b'00000', 7:b'00000',
                         8:b'00000', 9:b'00000', 10:b'00000', 11:b'00000',
                        12:b'00000', 13:b'00000', 14:b'00000', 15:b'00000',
                        16:b'00000', 17:b'00000', 18:b'00000', 19:b'00000',
                        20:b'00000', 21:b'00000', 22:b'00000', 23:b'00000',
                        24:b'00000', 25:b'00000', 26:b'00000', 27:b'00000',
                        28:b'00000', 29:b'00000', 30:b'00000', 31:b'00000',
                        32:b'00000', 33:b'00000', 34:b'00000', 35:b'00000',
                        36:b'00000', 37:b'00000', 38:b'00000', 39:b'00000' }

#---------------------------------------------------------------------#

IR_Five_A_Load_Voltage = { 0:0.00, 1:0.00, 2:0.00, 3:0.00,
                           4:0.00, 5:0.00, 6:0.00, 7:0.00,
                           8:0.00, 9:0.00, 10:0.00, 11:0.00,
                          12:0.00, 13:0.00, 14:0.00, 15:0.00,
                          16:0.00, 17:0.00, 18:0.00, 19:0.00 }

IR_One_A_Load_Voltage = { 0:0.00, 1:0.00, 2:0.00, 3:0.00,
                          4:0.00, 5:0.00, 6:0.00, 7:0.00,
                          8:0.00, 9:0.00, 10:0.00, 11:0.00,
                         12:0.00, 13:0.00, 14:0.00, 15:0.00,
                         16:0.00, 17:0.00, 18:0.00, 19:0.00 }


Five_A_Load_Voltage = { 0:0.00, 1:0.00, 2:0.00, 3:0.00,
                        4:0.00, 5:0.00, 6:0.00, 7:0.00,
                        8:0.00, 9:0.00, 10:0.00, 11:0.00,
                       12:0.00, 13:0.00, 14:0.00, 15:0.00,
                       16:0.00, 17:0.00, 18:0.00, 19:0.00 }

One_A_Load_Voltage = { 0:0.00, 1:0.00, 2:0.00, 3:0.00,
                       4:0.00, 5:0.00, 6:0.00, 7:0.00,
                       8:0.00, 9:0.00, 10:0.00, 11:0.00,
                      12:0.00, 13:0.00, 14:0.00, 15:0.00,
                      16:0.00, 17:0.00, 18:0.00, 19:0.00 }

Full_Load_Status = { 0:"Value", 1:"Value", 2:"Value", 3:"Value",
                     4:"Value", 5:"Value", 6:"Value", 7:"Value",
                     8:"Value", 9:"Value", 10:"Value", 11:"Value",
                    12:"Value", 13:"Value", 14:"Value", 15:"Value",
                    16:"Value", 17:"Value", 18:"Value", 19:"Value" }

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################
'''
def Get_CFG(file):
  global TEMP_FILE
  global CHG_FILE
  global DSC_FILE
  global DVDT_FILE
  global LOAD_FILE

  global SampleTime
  global MaxSampleCount

  cfg = open( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/BotBox.cfg","r+t" )
  SampleTime = cfg.readline()
  MaxSampleCount = int(cfg.readline())
  baudrate = int(cfg.readline())
  TEMP_FILE = cfg.readline()
  DSC_FILE = cfg.readline()
  CHG_FILE = cfg.readline()
  DVDT_FILE = cfg.readline()
  LOAD_FILE = cfg.readline()

  cfg.close()

  return baudrate
'''
#######################################################################
#######################################################################
#######################################################################

def Get_CFG( file ):

    global TEMP_FILE
    global DSC_FILE
    global CHG_FILE
    global DVDT_FILE
    global LOAD_FILE

    global SampleTime
    global MaxSampleCount
#    global baudrate
    global ChargemAhCutoff

    #  Open the configuration file
    cfg = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/BotBox.cfg"
    with open( cfg, "r+t" ) as f:
        pass

        S = f.readline()  # Read in the Test Start Trigger Voltage
        text, Time = S.split( ' = ' )
        SampleTime = int(Time)
        print( text + ' =', SampleTime )

        S = f.readline()  # Read in the Module load 'On" time
        text, SampleCount = S.split( ' = ' )
        MaxSampleCount = int(SampleCount)
        print( text + ' =', MaxSampleCount )

        S = f.readline()  # Read in the ADC Maximum Voltage
        text, baud = S.split( ' = ' )
        baudrate = int(baud)
        print( text + ' =', baudrate )

        S = f.readline()  # Read in the ADC Maximum Current
        text, ChargeCutoff = S.split( ' = ' )
        ChargemAhCutoff = int(ChargeCutoff)
        print(text + ' =', ChargemAhCutoff )

        S = f.readline()  # Read in the Unloaded Voltage Allias Voltage
        text, TEMP = S.split( ' = ' )
        TEMP_FILE = str(TEMP)
        print( text + ' =', TEMP_FILE )

        S = f.readline()  # Read in the Unloaded Voltage Fail Voltage
        text, DSC = S.split( ' = ' )
        DSC_FILE = str(DSC)
        print( '\n' + text + ' =', DSC_FILE )

        S = f.readline()  # Read in the Unloaded Voltage Fail Voltage
        text, CHG = S.split( ' = ' )
        CHG_FILE = str(CHG)
        print( text + ' =', CHG_FILE )

        S = f.readline()  # Read in the Loaded Voltage Fail Voltage
        text, DVDT = S.split( ' = ' )
        DVDT_FILE = str(DVDT)
        print( text + ' =', DVDT_FILE )

        S = f.readline()  # Read in the Loaded Voltage Fail Voltage
        text, LOAD = S.split( ' = ' )
        LOAD_FILE = str(LOAD)
        print( text + ' =', LOAD_FILE )

    f.close()

    return baudrate

#######################################################################
########################### PySerial  Class ###########################
#######################################################################

def Open_Comports( portlist ):
  global MAX_USB_PORTS

  p = 0
  while p <= MAX_USB_PORTS:
    port = serial.Serial( portlist[p], baudrate, timeout = 0.05 )
    port.open()
    p = p + 1

#---------------------------------------------------------------------#

def Close_Comports( portlist ):
  global MAX_USB_PORTS

  p = 0
  while p <= MAX_USB_PORTS:
    port = serial.Serial( portlist[p], baudrate, timeout = 0.05 )
    port.close()
    p = p + 1

#---------------------------------------------------------------------#

def List_Comports( portlist ):
  global MAX_USB_PORTS

#  root.update()
  print()
  print( '----------------------------------------------------------' )

  n = 0
  while n < MAX_USB_PORTS:
    # Address range 0 <= addres <= 39
    if portlist[n] == 99:
      print( '\n\nNo USB comport at address:', n+1 )
      print( 'Module:', n+1, '== mapped to USB port: ---\n\n' )
    else: print( 'Module', n+1, 'Address', n+1, '== mapped to USB port:', portlist[ n ] )
    n += 1
  print( '----------------------------------------------------------\n' )

#---------------------------------------------------------------------#

def Initialize_Comports( baudrate ): # List of available open comports
  """ Maps the Slacker physical address to its respective USB serial port """
  global MAX_USB_PORTS

  comports = []
  address = "Value"

  # Creat list of all available USB comports
  portslist = glob.glob( '/dev/ttyUSB*' )

  n = 0
  for p in portslist:
    comports.append( p )
    n += 1
  MAX_USB_PORTS = n

  print()
  print( 'The total number of available USB comports =', n )

  if n == 0:
    print( 'No USB comports were found' )
  else:
    print( '\nMapping USB comports to respective NiMH modules' )
    print( 'One moment please...' )

  """
      For a given initialized USB comport, read the physical address
      (rack/slot) of the attached Slacker module.
      Address range: 0 <= addres <= 39
  """
  n = 0
  while n < MAX_USB_PORTS:
    comport = serial.Serial( comports[n], baudrate, timeout = 0.05 )
    comport.write( b'getaddress\n' )
    while comport.out_waiting > 0:
      pass
    time.sleep( 0.05 )
    address = comport.readline()
    time.sleep( 0.1 )
    n += 1
    print ( 'Module Address:', address )
    PortList[ int(address)-1 ] = comport.port # zero counts as a place holder

  List_Comports( PortList )

  q = 0
  print('\n')
  for p in PortList:
    NiMH_Status = "\0"
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'getnimhdisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )
    else: break
    q += 1

  return PortList
#######################################################################
#######################################################################
#######################################################################

#######################################################################
######################### Log Current errors ##########################
#######################################################################
def Log_Exception( currentlinenumber, error, module ):
  global PassCount
  global TargetCount
  global mode
  global SampleCount

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
        logfile.write( '  LINE: ' + str(currentlinenumber) )
        logfile.write( '   MODULE: {}'.format(int(module+1)) )
        logfile.write( '   ' + str( error ) )
        logfile.write( '   PASS: ' + str(PassCount) + ' of ' + str(PassTarget) )
        logfile.write( '   MODE: ' + mode )
        logfile.write( '   SAMPLE: ' + str(SampleCount) )
        logfile.write( '   TIME: ' + datetime.today().strftime("%H:%M HOURS") + '\n')
#######################################################################
#######################################################################
#######################################################################

#######################################################################
################# Get The Module Internal Resistance ##################
#######################################################################
def Get_IR( MAX_USB_PORTS, baudrate ):

  global Delta_V
  global Delta_I
  global IR

  Status = b"Value"
  COMMS_TimeoutCounter = 10 

  print()
  print()
  print( '***********     Starting IR Test     ***********' )
  print( 'One moment...' )

  temp = 0.00
  Delta_I = 4.00

  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'getnimhdisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1

  time.sleep( 3.0 )

  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'enter\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1

  time.sleep( 0.1 )

  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'getmanualdischargedisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1

  time.sleep( 2.0 ) # Wait until the seek operation == finished

# ---------------------------------------------------------------------

#-- Need to pre-scan each module to over come the Slacker pre-fetch --#
  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'start\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1

  time.sleep( 5.0 )

  print('\nCollecting Module IR Data')
  print( 'MODULE  STATUS     V AT 1A     V AT 5A        IR' )

# ----------- Check the module voltage at a 1 Ampere load -----------
  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 1.0 )
      while Status != bytes(b'DSC'):
        port.write( b'getstatus\n' )
        while port.out_waiting > 0:
          pass
        time.sleep(0.6)
        Status = port.read(5)

#        print( 'MODULE', q+1, 'STATUS =', Status ) # Use this for a "Tattle-Tail."

        if Status == bytes(b'DSC'):
          break

        if Status == b'': # Looking for a "NULL" character
          Status = b'TYPE'

        try:
          bytes(Status)
        except TypeError:
          Status = b'TYPE'

        if COMMS_TimeoutCounter == 0:
          COMMS_TimeoutCounter -= 1
        else:
          Status = 'DONE'
          break

      port.write( b'redledon\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )

      port.write( b'getV\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 1.0 )
      temp = port.read(5) # Dummy POER Read

      port.write( b'getV\n' ) # Fetch the current module voltage
      while port.out_waiting > 0:
        pass
      time.sleep( 1.0 )
      temp = port.read(5)

      try:
        float(temp)
      except ValueError or TypeError:
        temp = 0.00
      finally:
        IR_One_A_Load_Voltage[q] = float(temp)

      port.write( b'redledoff\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'redledoff\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'redledoff\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      q += 1

# ----------- Check the module voltage at a 5 Ampere load -----------
  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 1.0 )

      while Status != bytes(b'DSC'):
        port.write( b'getstatus\n' )
        while port.out_waiting > 0:
          pass
        time.sleep(0.6)
        Status = port.read(5)

#        print( 'MODULE', q+1, 'STATUS =', Status ) # Use this for a "Tattle-Tail."

        if Status == bytes(b'DSC'):
          break

        if Status == b'': # Looking for a "NULL" character
          Status = b'TYPE'

        try:
          bytes(Status)
        except TypeError:
          Status = b'TYPE'

        if COMMS_TimeoutCounter == 0:
          COMMS_TimeoutCounter -= 1
        else:
          Status = 'DONE'
          break

      port.write( b'hicurrenton\n' ) # Turn on the high current load
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1)

      port.write( b'getV\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 1.0 )
      temp = port.read(5) # Dummy POER Read

      port.write( b'getV\n' ) # Fetch the current module voltage
      while port.out_waiting > 0:
        pass
      time.sleep( 1.0 )
      temp = port.read(5)

      port.write( b'hicurrentoff\n' ) # Turn off the high current load
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'hicurrentoff\n' ) # Turn off the high current load
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'hicurrentoff\n' ) # Turn off the high current load
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'stop\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1)

      try:
        float(temp)
      except ValueError or TypeError:
        temp = 0.00
      finally:
        IR_Five_A_Load_Voltage[q] = float(temp)

      if IR_Five_A_Load_Voltage[q] > 6.80:
        Full_Load_Status[q] = "PASS"
      else: Full_Load_Status[q] = "FAIL"

      IR = abs( ( IR_One_A_Load_Voltage[q] - IR_Five_A_Load_Voltage[q] ) / Delta_I )

      print( ' ', q+1,
             '    ', Full_Load_Status[q],
             '     {0:.2f}'.format(IR_One_A_Load_Voltage[q]), 'V',
             '     {0:.2f}'.format(IR_Five_A_Load_Voltage[q]), 'V',
             '     {0:.1f}'.format(IR*1000), 'mOhms' )
      q += 1
      time.sleep( 0.5 )

  print( '\n***********     IR Test Complete...     ***********\n\n' )
#######################################################################
#######################################################################
#######################################################################

#######################################################################
##################### Get The Module Load Voltage #####################
#######################################################################
def Get_Load_Voltage( MAX_USB_PORTS, baudrate ):

  global Delta_V
  global Delta_I
  global IR

  temp = 0.00
  Delta_I = 4.00
  Status = b"Value"
  COMMS_TimeoutCounter = 10 

  print( '***********     Starting FINAL LOAD Test     ***********' )
  print( 'One moment...' )

  print('\nCollecting Module LOAD Data')
  print( 'MODULE  STATUS     V AT 1A     V AT 5A     DELTA V' )

  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'getnimhdisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1

  time.sleep( 2.0 )

  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'enter\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1

  time.sleep( 0.1 )

  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'getmanualdischargedisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1

  time.sleep( 2.0 ) # Wait until the seek operation == finished

# ---------------------------------------------------------------------

#-- Need to pre-scan each module to over come the Slacker pre-fetch --#
  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'start\n' ) # Start discharge mode
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1

  time.sleep( 5.0 ) # 5 seconds, minimum

# ----------- Check the module voltage at a 1 Ampere load -----------
  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.5 )
      while Status != bytes(b'DSC'):
        port.write( b'getstatus\n' )
        while port.out_waiting > 0:
          pass
        time.sleep(0.6)
        Status = port.read(5)

#        print( 'MODULE', q+1, 'STATUS =', Status ) # Use this for a "Tattle-Tail."

        if Status == bytes(b'DSC'):
          break

        if Status == b'': # Looking for a "NULL" character
          Status = b'TYPE'

        try:
          bytes(Status)
        except TypeError:
          Status = b'TYPE'

        if COMMS_TimeoutCounter == 0:
          COMMS_TimeoutCounter -= 1
        else:
          Status = 'DONE'
          break

      port.write( b'redledon\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )

      port.write( b'getV\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 1.0 )
      temp = port.read(5) # Dummy POER Read

      port.write( b'getV\n' ) # Fetch the current module voltage
      while port.out_waiting > 0:
        pass
      time.sleep( 1.0 )
      temp = port.read(5)

      try:
        float(temp)
      except ValueError or TypeError:
        temp = 0.00
      finally:
        One_A_Load_Voltage[q] = float(temp)

      port.write( b'redledoff\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'redledoff\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'redledoff\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      q += 1

      # Delay the "High Current" enable so the interval between
      # interval between enabled channels closely matches the
      # interval between disabling the "High Current" loads
      time.sleep( 1.0 )

  time.sleep( 5.0 ) # 5 Ampere Dwell time - 5 seconds, minimum

  LOAD_File = open( LOAD_FILE,"w" )

  FirstPass = True

# ----------- Check the module voltage at a 5 Ampere load -----------
  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 1.0 )


      while Status != bytes(b'DSC'):
        port.write( b'getstatus\n' )
        while port.out_waiting > 0:
          pass
        time.sleep(0.6)
        Status = port.read(5)

#        print( 'MODULE', q+1, 'STATUS =', Status ) # Use this for a "Tattle-Tail."

        if Status == bytes(b'DSC'):
          break

        if Status == b'': # Looking for a "NULL" character
          Status = b'TYPE'

        try:
          bytes(Status)
        except TypeError:
          Status = b'TYPE'

        if COMMS_TimeoutCounter == 0:
          COMMS_TimeoutCounter -= 1
        else:
          Status = 'DONE'
          break

      port.write( b'hicurrenton\n' ) # Turn on the high current load
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1)

      port.write( b'getV\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 1.0 )
      temp = port.read(5) # Dummy POER Read

      port.write( b'getV\n' ) # Fetch the current module voltage
      while port.out_waiting > 0:
        pass
      time.sleep( 1.0 )
      temp = port.read(5)

      port.write( b'hicurrentoff\n' ) # Turn off the high current load
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'hicurrentoff\n' ) # Turn off the high current load
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'hicurrentoff\n' ) # Turn off the high current load
      while port.out_waiting > 0:
        pass
      time.sleep( 0.2 )

      port.write( b'stop\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )

      try:
        float(temp)
      except ValueError or TypeError:
        temp = 0.00
      finally:
        Five_A_Load_Voltage[q] = float(temp)

      if FirstPass == True:
        FirstPass = False
      else: LOAD_File.write( ',' )

      LOAD_File.write( str(Five_A_Load_Voltage[q]) )

      if Five_A_Load_Voltage[q] > 7.00:
        Full_Load_Status[q] = "PASS"
      else: Full_Load_Status[q] = "FAIL"

      Delta_V = One_A_Load_Voltage[q] - Five_A_Load_Voltage[q]

      print( ' ', q+1,
             '    ', Full_Load_Status[q],
             '     {0:.2f}'.format(One_A_Load_Voltage[q]), 'V',
             '     {0:.2f}'.format(Five_A_Load_Voltage[q]), 'V',
             '     {0:.2f}'.format( abs(Delta_V) ), 'V' )
      q += 1
      time.sleep( 0.5 )

  LOAD_File.close()

# ---------Find the Max/Min voltage under the 5 Ampere load ---------
  q = 0
  Min_V = 9.00
  Max_V = 5.00

  while q < MAX_USB_PORTS:

    if Five_A_Load_Voltage[q] < Min_V:
      Min_V = Five_A_Load_Voltage[q]

    if Five_A_Load_Voltage[q] > Max_V:
      Max_V = Five_A_Load_Voltage[q]
    q += 1

  print()
  print('MIN V = ' + '{0:.2f}'.format( Min_V ), 'V' )
  print('MAX V = ' + '{0:.2f}'.format( Max_V ), 'V\n' )    

  print('( MAX V - MIN V ) = ' + '{0:.2f}'.format( Max_V - Min_V ), 'Volts\n' )    


  print( '**************************************************************' )
  print( '**************************************************************' )
  print( '**************************************************************' )
  print( '***********                                        ***********' )
  print( '***********        FINAL LOAD Test Complete        ***********' )
  print( '***********                                        ***********' )
  print( '**************************************************************' )
  print( '**************************************************************' )
  print( '**************************************************************' )


#######################################################################
#######################################################################
#######################################################################

#######################################################################
############################ Run Load Test ############################
#######################################################################

def Run_LoadTest():

  global KeyStatus
  #global MAX_USB_PORTS

  print()
  print()
  print( '***********     Starting IR Test     ***********' )
  print( 'One moment...' )

  Get_IR( MAX_USB_PORTS, baudrate )
  print( '***********     IR Test Complete...     ***********\n\n' )

  print( '***********     Starting FINAL LOAD Test     ***********' )
  print( 'One moment...' )

  Get_Load_Voltage( MAX_USB_PORTS, baudrate )

  q = 0
  for p in PortList:
    if q < MAX_USB_PORTS:
      port = serial.Serial( PortList[p], baudrate, timeout = 0.05 )
      port.write( b'getnimhdisplay\n' )
      while port.out_waiting > 0:
        pass
#      time.sleep( 0.05 )
    else: break
    q += 1


  print( '**************************************************************' )
  print( '**************************************************************' )
  print( '**************************************************************' )
  print( '***********                                        ***********' )
  print( '***********        FINAL LOAD Test Complete        ***********' )
  print( '***********                                        ***********' )
  print( '**************************************************************' )
  print( '**************************************************************' )
  print( '**************************************************************' )
#######################################################################
#######################################################################
#######################################################################

#######################################################################
######################## Stop Current Module ##########################
#######################################################################
def ModuleStop( port, module ):
  global KeyStatus
  global SampleStatus
  global DoneStatus

  # Turn off the current charger channel when that module == "DONE".
  if DoneStatus[module] != 'DONE':
    DoneStatus[module] = 'DONE'
    # Data Pre-fetch == currently executing....
    if KeyStatus != 'STOP':
      time.sleep(5.0) # Wait for quad charger beeper to stop

      if mode == 'DISCHARGE':
        try:
          port.write( b' \n' ) # Test for "write" attribute
          while port.out_waiting > 0:
            pass
          time.sleep(0.05)
        except Exception as Error: # Check for errors
          pass  # port.write fault. Log the fault
          Error = "ERROR 101:   >>> USB COMMAND WRITE ERROR <<<"
          CurrentLineNumber = inspect.currentframe().f_lineno
          SampleStatus[module] = 'DONE'
          Log_Exception( CurrentLineNumber+1, Error, module )
        else:
          port.write( b'hicurrentoff\n' ) # Turn off hign current load
          while port.out_waiting > 0:
            pass
          time.sleep(0.05)

      if mode == 'CHARGE':
        try:
          port.write( b' \n' ) # Turn off charge LED
          while port.out_waiting > 0:
            pass
          time.sleep(0.05)
        except Exception as Error:
          pass  # port.write fault. Log the fault
          Error = "ERROR 201:   >>> USB COMMAND WRITE ERROR <<<"
          SampleStatus[module] = 'DONE'
          CurrentLineNumber = inspect.currentframe().f_lineno
          Log_Exception( CurrentLineNumber+1, Error, module )
        else:
          port.write( b'blueledoff\n' ) # Turn off charge LED
          while port.out_waiting > 0:
            pass
          time.sleep(0.05)

      try:
        port.write( b' \n' )
        while port.out_waiting > 0:
          pass
        time.sleep(0.05)
      except Exception as Error:
          pass  # port.write fault. Log the fault
          Error = "ERROR 001:   >>> USB COMMAND WRITE ERROR <<<"
          SampleStatus[module] = 'DONE'
          CurrentLineNumber = inspect.currentframe().f_lineno
          Log_Exception( CurrentLineNumber+1, Error, module )
      else:
        port.write( b'stop\n' )
        while port.out_waiting > 0:
          pass
        time.sleep(0.05)
#######################################################################
#######################################################################
#######################################################################

#######################################################################
####################### Sample A Single Channel #######################
#######################################################################
def GetSample( port, baudrate, module, mode ):

  global ProfileStatus
  Status = b"Value"
  COMMS_TimeoutCounter = 10
  temp = b'Value'
  temp1 = 0.00
  temp2 = 0.00
  temp3 = 00000
  temp4 = 00000

#---------------------------------------------------------------------#

  with serial.Serial( port, baudrate, timeout = 0 ) as com:

    if mode == 'CHARGE':
      if DoneStatus[module] != 'DONE':
        try:
          com.write( b' \n' )
          while com.out_waiting > 0:
            pass
          time.sleep(0.05)
        except Exception as Error:
            pass  # port.write fault. Log the fault
        else:
          com.write( b'blueledon\n' )
          while com.out_waiting > 0:
            pass
          time.sleep(0.05)

        #----- Begin Status Check...
        while Status != bytes(b'CHG'):
          # "getstatus" does NOT use Slacker "Get Last - Accquire Next" method
          try:
            com.write( b' \n' )
            while com.out_waiting > 0:
              pass
            time.sleep(0.05)
          except Exception as Error:
              pass  # port.write fault. Log the fault
          else:
            com.write( b'getstatus\n' )
            while com.out_waiting > 0:
              pass
            time.sleep(0.05)

          try:
            Status = com.read(5)
          except Exception as error: # Check for all errors
            pass
            Status = b''

#        print( 'MODULE', module+1, 'STATUS =', Status ) # Use this for a "Tattle-Tail."

          if Status == bytes(b'CHG'):
            break
          elif Status == b'END' or Status == b'FULL' or Status == b'CAPA':
            Status = 'DONE'
            break
          else: Status = b''

          COMMS_TimeoutCounter -= 1
          if COMMS_TimeoutCounter == 0:
            Status = 'STATUS FAULT'
            break
        #----- End Status Check...

        if Status == 'STATUS FAULT':
          ChargeAmpereHours[module] = b'00200'
          Status = 'DONE'
          Error = "ERROR 200:   >>> CHARGE SAMPLE STATUS <<<"
          Error_200_List[module] = True
          CurrentLineNumber = inspect.currentframe().f_lineno
          Log_Exception( CurrentLineNumber+1, Error, module )
        else:
          Error_200_List[module] = False
          # "getA" uses Slacker "Get Last - Accquire Next" method
          #######################################################
          #######################################################
          x = 0
          while x < 3:
              try:
                  com.write( b' \n' )
                  while com.out_waiting > 0:
                      pass
                  time.sleep(0.05)
              except Exception as Error:
                  pass  # port.write fault. Log the fault
                  ChargeAmpereHours[module] = ChargeLastAmpereHours[module]
                  x += 1
                  continue  # Continue the while loop
              else:
                  com.write( b'getA\n\n' )
                  while com.out_waiting > 0:
                      pass
                  time.sleep(0.05)

                  try:
                      ChargeAmpereHours[module] = com.read(5)
                  except Exception as Error: # Check for all errors
                      ChargeAmpereHours[module] = ChargeLastAmpereHours[module]
                  break
          #######################################################
          #######################################################

          # Looking for a "SPACE" character or a "NULL" character
          if ChargeAmpereHours[module] == b'' or ChargeAmpereHours[module] == b'\x00':
            ChargeAmpereHours[module] = ChargeLastAmpereHours[module]

          temp3 = int(ChargeAmpereHours[module])
          ChargeLastAmpereHours[module] = ChargeAmpereHours[module]

          if ProfileStatus == '1st' or ProfileStatus == '2nd':
            temp4 = ChargemAhCutoff
          else: temp4 = ChargemAhCutoff

          if temp3 >= temp4:
            Status = 'DONE'

#---------------------------------------------------------------------#

    if mode == 'DISCHARGE':
      if DoneStatus[module] != 'DONE':
        try:
          com.write( b' \n' )
          while com.out_waiting > 0:
            pass
          time.sleep(0.05)
        except Exception as Error:
            pass  # port.write fault. Log the fault
        else:
          com.write( b'hicurrenton\n' )
          while com.out_waiting > 0:
            pass
          time.sleep(0.05)

        #----- Begin Status Check...
        while Status != bytes(b'DSC'):
          # "getstatus" does NOT use Slacker "Get Last - Accquire Next" method
          try:
            com.write( b' \n' )
            while com.out_waiting > 0:
              pass
            time.sleep(0.05)
          except Exception as Error:
              pass  # port.write fault. Log the fault
          else:
            com.write( b'getstatus\n' )
            while com.out_waiting > 0:
              pass
            time.sleep(0.05)

          try:
            Status = com.read(5)
          except Exception as Error: # Check for all errors
            pass
            Status = b''

#        print( 'MODULE', module+1, 'STATUS =', Status ) # Use this for a "Tattle-Tail."

          if Status == bytes(b'DSC'):
            break
          elif Status == b'CAPA':
            Status = 'DONE'
            break
          elif Status == b'END' or Status == b'EMPTY' or Status == b'DRY':
            ModuleVoltage[module] = b' 5.99'
            LastVoltage[module] = b' 5.99'
            Status = 'DONE'
            break
          else: Status = b''

          COMMS_TimeoutCounter -= 1
          if COMMS_TimeoutCounter == 0:
            Status = 'STATUS FAULT'
            break
        #----- End Status Check...

        if Status == 'STATUS FAULT':
          ModuleVoltage[module] = b'0.00'
          LastVoltage[module] = b'0.00'
          DischargeAmpereHours[module] = b'00020' # 20 * 5 = 100
          Status = 'DONE'
          Error = "ERROR 100:   >>> DISCHARGE SAMPLE STATUS <<<"
          CurrentLineNumber = inspect.currentframe().f_lineno
          Log_Exception( CurrentLineNumber+1, Error, module )
        else:
          Error_200_List[module] = False  # Remove after testing
          if Error_200_List[module] == True:  # Check for an ERROR_200
            DischargeAmpereHours[module] = b'00020' # 20 * 5 = 100

          #######################################################
          #######################################################
          # Get the last Module mAh
          # "getA" uses Slacker "Get Last - Accquire Next" method
          x = 0
          while x < 3:
              try:
                  com.write( b' \n' )
                  while com.out_waiting > 0:
                      pass
                  time.sleep(0.05)
              except Exception as Error:
                  pass  # port.write fault. Log the fault
                  DischargeAmpereHours[module] = DischargeLastAmpereHours[module]
                  x += 1
                  continue  # Continue the while loop
              else:
                  com.write( b'getA\n\n' ) # Accquire the last module Ampere Hours
                  while com.out_waiting > 0: # Slacker automatically gets next
                      pass
                  time.sleep(0.05) # Wait for Slacker to process the command

                  try:
                      DischargeAmpereHours[module] = com.read(5)
                  except Exception as error: # Check for all errors
                      pass
                      DischargeAmpereHours[module] = DischargeLastAmpereHours[module]
                  break
          #######################################################
          #######################################################

          # Looking for a "SPACE" character or a "NULL" character
          if DischargeAmpereHours[module] == b'' or DischargeAmpereHours[module] == b'\x00':
            DischargeAmpereHours[module] = DischargeLastAmpereHours[module]
        time.sleep(0.5) # Wait for Slacker to process the last command

        # Now get the module last voltage
        if Status != 'DONE':
          #######################################################
          #######################################################
          x = 0
          while x < 3:
              try:
                  com.write( b' \n' )
                  while com.out_waiting > 0:
                      pass
                  time.sleep(0.05)
              except Exception as Error:
                  pass  # port.write fault. Log the fault
                  ModuleVoltage[module] = LastVoltage[module]
                  x += 1
                  continue  # Continue the while loop
              else:
                  # "getV" uses Slacker "Get Last - Accquire Next" method
                  com.write( b'getV\n' ) # Accquire the last module Ampere Hours
                  while com.out_waiting > 0: # Slacker automatically gets next
                      pass
                  time.sleep(0.05) # Wait for Slacker to process the command

                  try:
                      ModuleVoltage[module] = com.read(5)
                  except Exception as Error:
                      pass
                      ModuleVoltage[module] = LastVoltage[module]
                  break
          #######################################################
          #######################################################


          # Looking for a "SPACE" character or a "NULL" character
          if ModuleVoltage[module] == b'' or ModuleVoltage[module] == b'\x00':
            ModuleVoltage[module] = LastVoltage[module]

          if ProfileStatus == '1st' or ProfileStatus == '2nd':
            temp2 = float(5.50)
          else: temp2 = float(6.00)

#---------------------------------------------------------------------#
          # If the module voltage == <= to the target voltage,
          # set the last voltage reading to 5.99 volts.
          temp1 = float(ModuleVoltage[module])

          if temp1 <= temp2:
            ModuleVoltage[module] = b' 5.99'
            Status = 'DONE'
#---------------------------------------------------------------------#

          if float(ModuleVoltage[module]) > 9.00:
            ModuleVoltage[module] = LastVoltage[module]

          LastVoltage[module] = ModuleVoltage[module]  
          DischargeLastAmpereHours[module] = DischargeAmpereHours[module]

#          print( 'MODULE', module+1, 'VOLTAGE =', format(float(ModuleVoltage[module]),'>0.2f') ) # Use this for a "Tattle-Tail."

    if Status == 'DONE':
      ModuleStop( com, module )

#---------------------------------------------------------------------#

    return Status

#######################################################################
#######################################################################
#######################################################################

#######################################################################
######################### Sample Every Module #########################
#######################################################################

def SampleData( portlist, baudrate, mode, samplecount ):
  global MAX_USB_PORTS
  global SampleStatus
  global AmpereHours
  global GraphEnable
  global KeyStatus
  global ProfileStatus

  module = 0
  temp1 = 0.00
  temp2 = 0.00

  if (mode == 'DISCHARGE') and (GraphEnable == True):
#    TEMP_File = open( TEMP_FILE,"a+t" )
    TEMP_File = open( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Profile.tmp","a+t" )
    TEMP_File.write( str( samplecount ) )

  print( 'Sample: ', samplecount, '\n' )

  while module < MAX_USB_PORTS:

# ************************************************************************* #
    Module_Sample_Time = 0.00
    Module_Start_Time = float(time.time())

    if DoneStatus[module] == 'DONE':
      while int(Module_Sample_Time) < int(1.00):
        root.update() # Update the GUI status
        Module_Current_Time = format(float(time.time()),'>5.2f')
        Module_Sample_Time = format( int(float(Module_Current_Time) - float(Module_Start_Time)),'>d')
    else:
      SampleStatusLast[module] = SampleStatus[module]

      # /////////////////////////////////////////////////////////////////// #
      SampleStatus[module] = GetSample( portlist[module], baudrate, module, mode )
      # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #

      while int(Module_Sample_Time) < int(1.00):
        root.update() # Update the GUI status
        Module_Current_Time = format(float(time.time()),'>5.2f')
        Module_Sample_Time = format( int(float(Module_Current_Time) - float(Module_Start_Time)),'>d')
#    print( 'MODULE SAMPLE TIME =', format(float(Module_Sample_Time),'>0.2f') )

# ************************************************************************* #

#    TEMP_File = open( TEMP_FILE,"a+b" )
    TEMP_File = open( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Profile.tmp","a+b" )
    if (mode == 'DISCHARGE') and (GraphEnable == True):
      TEMP_File.write( b',' )

      try:
        TEMP_File.write( bytes(ModuleVoltage[module]) )
      except: # Check for all errors
        pass
        TEMP_File.write( b' 0.00' )
        ModuleVoltage[module] = b' 0.00'
        SampleStatus[module] = 'DONE'
        ModuleStop( portlist[module], module )

    if mode == 'CHARGE':
      print( '   MODULE', module+1, 'STATUS:  ', format(str(SampleStatus[module]), '>s'), \
             '\t' + format(int(ChargeAmpereHours[module]),'>5d') + ' mAh')

    if mode == 'DISCHARGE':
      if ProfileStatus == '1st' or ProfileStatus == '2nd':
        print( '   MODULE', module+1, 'STATUS:  ', format(str(SampleStatus[module]), '>s'), \
               '\t' + format(float(ModuleVoltage[module]),'>0.2f') + ' VOLTS', \
               '\t' + format(int(DischargeAmpereHours[module])*5,'>5d') + ' mAh')
      else:
        print( '   MODULE', module+1, 'STATUS:  ', format(str(SampleStatus[module]), '>s'), \
               '\t' + format(float(ModuleVoltage[module]),'>0.2f') + ' VOLTS', \
               '\t' + format(int(DischargeAmpereHours[module])*5,'>5d') + ' mAh')
#               '\t' + format(float(Module_dVdt[module]), '>0.2f') + ' dVdt')

    root.update() # Update the GUI status
    if KeyStatus == 'STOP':
      break

    module += 1

  if (mode == 'DISCHARGE') and (GraphEnable == True):
    TEMP_File.write( b'\n' )
#    DVDT_File.write( '\n' )

  return SampleStatus

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#############################  End Cycle  #############################
#######################################################################

def EndCycle( portlist ):
  # There are only two ways to get here:
  #   1. The end of the current profile.
  #   2. The 'STOP' button in the GUI was pushed.

  global MAX_USB_PORTS
  global RunStatus
  global SampleStatus
  global KeyStatus

  if KeyStatus == 'STOP': # Was the current profile aborted
    RunStatus = 'STOP'

  module = 0
  for p in portlist:
    if module < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0.05 )
      if DoneStatus[ module ] != 'DONE':
        SampleStatus[ module ] = 'STOP'

        if mode == 'DISCHARGE':
          try:
            port.write( b' \n' ) # Test for "write" attribute
            while port.out_waiting > 0:
              pass
            time.sleep(0.05)
          except Exception as Error: # Check for errors
            pass  # port.write fault. Log the fault
            Error = "ERROR 101:   >>> USB COMMAND WRITE ERROR <<<"
            CurrentLineNumber = inspect.currentframe().f_lineno
            Log_Exception( CurrentLineNumber+1, Error, module )
          else:
            port.write( b'hicurrentoff\n' ) # Turn off hign current load
            while port.out_waiting > 0:
              pass
            time.sleep(0.05)

        if mode == 'CHARGE':
          try:
            port.write( b' \n' ) # Turn off charge LED
            while port.out_waiting > 0:
              pass
            time.sleep(0.05)
          except Exception as Error:
            pass  # port.write fault. Log the fault
            Error = "ERROR 201:   >>> USB COMMAND WRITE ERROR <<<"
            CurrentLineNumber = inspect.currentframe().f_lineno
            Log_Exception( CurrentLineNumber+1, Error, module )
          else:
            port.write( b'blueledoff\n' ) # Turn off charge LED
            while port.out_waiting > 0:
              pass
            time.sleep(0.05)
    
        try:
          port.write( b' \n' )
          while port.out_waiting > 0:
            pass
          time.sleep(0.05)
        except Exception as Error:
            pass  # port.write fault. Log the fault
            Error = "ERROR 001:   >>> USB COMMAND WRITE ERROR <<<"
            CurrentLineNumber = inspect.currentframe().f_lineno
            Log_Exception( CurrentLineNumber+1, Error, module )
        else:
          port.write( b'stop\n' )
          while port.out_waiting > 0:
            pass
        time.sleep(0.05)

      module += 1
    else: break

#######################################################################
#######################################################################
#######################################################################

#######################################################################
############################# Cycle Start #############################
#######################################################################

def BeginCycle( portlist, mode ):
#----------------- Initialize all system variables -------------------#
  global MAX_USB_PORTS
  global MaxSampleCount
  global SampleStatus
  global DoneStatus
  global RunStatus
  global KeyStatus
  global Profile_Time
  global PassCount
  global PassTarget
  global GraphEnable
  global ProfileStatus

  s = 0 # Sentenel status
  temp = '\0'
  KeyStatus = 'RUN'
  RunStatus = 'RUN'
  SampleCount = 0
  Start_Time = 0
  Stop_Time = 0
  Last_Time = 0
  Current_Time = 0
  Sample_Time =0
  FP1 = "Value"
  FP2 = "Value"

  root.update() # Update the GUI status
#  gc.collect(2)  # Clear the "Freed" list at the end of servicing threshold 2

  if (mode == 'DISCHARGE') and (GraphEnable == True):
#    TEMP_File = open( TEMP_FILE,"w+b" )
    TEMP_File = open( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Profile.tmp","w+b" )
#    DVDT_File = open( DVDT_FILE,"w" )

  q = 0
  while q <= MAX_USB_PORTS:
    if mode == 'DISCHARGE':
      ModuleVoltage[q] = 8.50
      LastVoltage[q] = 8.50
      DischargeAmpereHours[q] = 00000
      DischargeLastAmpereHours[q] = b'00100'

    if mode == 'CHARGE':
      ChargeAmpereHours[q] = 00000
      ChargeLastAmpereHours[q] = b'00200'

    SampleStatus[q] = 'RUN'
    SampleStatusLast[q] = 'STOP'    
    DoneStatus[q] = 'RUN'
    q += 1

  Metrics.Display_Status()
  Metrics.Display_SampleCount(SampleCount)
#---------------------------------------------------------------------#

#----------- Start the requested operation for each module------------#
  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      with serial.Serial( portlist[p], baudrate, timeout = 0 ) as port:

        try:
          port.write( b' \n' )
          while port.out_waiting > 0:
            pass
          time.sleep(0.05)
        except Exception as Error:
            pass  # port.write fault. Log the fault
        else:
          port.write( b'start\n' )
          while port.out_waiting > 0:
            pass
            time.sleep(0.05)

      q += 1
    else: break

  # Update the GUI STATUS/DATA display area.
  Metrics.Display_Status()

  time.sleep( 5 ) # Wait for the chargers to start

#-- Need to pre-scan each module to over come the Slacker pre-fetch --#
  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      with serial.Serial( portlist[p], baudrate, timeout = 0.5 ) as port:
        port.write( b'getV\n' )
        while port.out_waiting > 0:
          pass
        time.sleep( 0.05 )
        temp = port.read(5)

#        time.sleep( 1.00 )

        port.write( b'getV\n' )
        while port.out_waiting > 0:
          pass
        time.sleep( 0.05 )
        temp = port.read(5)
      q += 1
    else: break

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      with serial.Serial( portlist[p], baudrate, timeout = 0.5 ) as port:
        port.write( b'getA\n' )
        while port.out_waiting > 0:
          pass
        time.sleep( 0.05 )
        temp = port.read(5)

#        time.sleep( 1.00 )

        port.write( b'getA\n' )
        while port.out_waiting > 0:
          pass
        time.sleep( 0.05 )      
        temp = port.read(5)
      q += 1
    else: break
  time.sleep( 1.00 )

#*********************************************************************#
#***** This == the beginning of the actual sample & control loop *****#
#*********************************************************************#

  Sample_Time = 0
  Start_Time = float(time.time())
  while RunStatus == 'RUN':

#---------------- Starting of sample interval control ----------------#
    if (mode == 'DISCHARGE'):
      if FP1 == True:
        FP1 = False
      else:
        Sample_Time = 0
        Start_Time = float(time.time())
#---------------------------------------------------------------------#

    if RunStatus == 'RUN':
      SentenelStatus_Label = ttk.Label( button, text="SAMPLE" )
      SentenelStatus_Label.grid( column=1, row=4 ) #, sticky=tk.N )
    root.update() # Update the GUI BUTTON status

    # Gather data samples for each module, building the battery profile
    SampleData( portlist, baudrate, mode, SampleCount )

    SentenelStatus_Label = ttk.Label( button, text=" DWELL " )
    SentenelStatus_Label.grid( column=1, row=4 ) #, sticky=tk.N )

    SampleCount += 1

    # Check for ALL modules "DONE" during "CHARGE" or "DISCHARGE" cycles.
    q = 0
    RunStatus = 'STOP'
    while q < MAX_USB_PORTS:
      if SampleStatus[q] != 'DONE':
        RunStatus = 'RUN' # The current module == noot "DONE"
      q += 1

    if RunStatus == 'STOP':
      EndCycle( portlist )

    # Update the GUI STATUS/DATA display area.
    Metrics.Display_Status()

    #*********************************************************************#
    #****************** sample interval and STOP control *****************#
    #*********************************************************************#

    if RunStatus != 'STOP' or KeyStatus != 'STOP':

      # For "CHARGE" mode, SampleCount == demensionless
      if mode == 'CHARGE':
        if ProfileStatus == '1st' or ProfileStatus == '2nd':
          if SampleCount >= 300: # Maximum charge capacity = 10,000mAh
            RunStatus = 'STOP'
        else:
          if SampleCount >= 300: # Maximum charge capacity = 5,000mAh
            RunStatus = 'STOP'

      if mode == 'DISCHARGE':
        if SampleCount >= MaxSampleCount: # Maximum time = 90 minutes
          RunStatus = 'STOP'
        else:
          while int(Sample_Time) < int(SampleTime):
            Current_Time = format(float(time.time()),'>5.2f')
            Sample_Time = format( int(float(Current_Time) - float(Start_Time)),'>d')

            root.update() # Update the GUI BUTTON status
            if KeyStatus == 'STOP':
              Sample_Time = float(SampleTime) + 1
              RunStatus = 'STOP'
              break
          print( '\nLOOP SAMPLE TIME =', int(Sample_Time), '\n' )

    #---------------------------------------------------------------------#

    # See if there == an external "STOP" command from the GUI.
    root.update() # Update the GUI status
    if RunStatus == 'STOP' or KeyStatus == 'STOP':
      EndCycle( portlist )
    Metrics.Display_SampleCount(SampleCount)

    print( '\n\n\n' )

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0.05 )

      if mode == 'CHARGE':
        port.write( b'blueledoff\n' ) # Ensure charge LED == active   
        while port.out_waiting > 0:
          pass
        time.sleep( 0.05 ) 

      if mode == 'DISCHARGE':
        port.write( b'hicurrentoff\n' ) # Ensure high current load == active
        while port.out_waiting > 0:
          pass
        time.sleep( 0.05 )
        ProfileDischargeStatus[q] = SampleStatus[q]  # Preserve the module discharge status
        Metrics.Update_R_Errors()
      q += 1
    else: break


#*********************************************************************#
#************* This == the end of the actual sample loop *************#
#*********************************************************************#

  # Wait here until all chargers have funished cycling down
  # This time may need to be as long as 5 second long when in "AUTO" mode.
  time.sleep( 5.0 )

#*********************************************************************#
#********************** Create a valid CSV File **********************#
#*********************************************************************#

  if (mode == 'CHARGE'):

#    CHG_File = open( CHG_FILE,"w+b" )
    CHG_File = open( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Chargefile.csv","w+b" )


    n = 0
    while n < MAX_USB_PORTS:
      SampleStatus[n] = ProfileDischargeStatus[n]  # Recover the module discharge statu
      n += 1

    n = 0
    FirstPass = True
    while n < MAX_USB_PORTS:
      if FirstPass == True:
        FirstPass = False
      else: CHG_File.write( b', ' )

      if int(ChargeAmpereHours[n]) != int('00200') and int(ChargeAmpereHours[n]) < int('4000'): #SUGJESTION '4000'
        ChargeAmpereHours[n] = b'00000'
        SampleStatus[n] = 'X'  # Module Failure
      elif int(ChargeAmpereHours[n]) == int('00200'):
        SampleStatus[n] = 'R'  # CQ3 Status Loss

      try:
        CHG_File.write( bytes(ChargeAmpereHours[n]) )
      except Exception as error:
        pass
        CHG_File.write( b'00200' )

      n += 1
    CHG_File.close()

  if (mode == 'DISCHARGE') and (GraphEnable == True):

#    DSC_File = open( DSC_FILE,"w+b" )
    DSC_File = open( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Dischargefile.csv","w+b" )

    n = 0
    FirstPass = True
    while n < MAX_USB_PORTS:

      if FirstPass == True:
        FirstPass = False
      else: DSC_File.write( b', ' )

      if SampleStatus[n] != 'R' and SampleStatus != 'X':
        #  # 5 x 20 = 100; [ DischargeAmpereHours[n] != 100 ]
        if bytes(DischargeAmpereHours[n]) == b'00020':
          SampleStatus[n] = 'R'  # "100" error ---> CQ3 Status Loss
        #  [ 2,999 < DischargeAmpereHours[n] and DischargeAmpereHours[n] != 100 ]
        elif bytes(DischargeAmpereHours[n]) < b'00600' and bytes(DischargeAmpereHours[n]) != b'00020':
          SampleStatus[n] = 'X'  # Less that 3,000mAh, but not a "100" error  ---> Module Failure
        #  [ 2,999 < DischargeAmpereHours[n] < 4,000 ]
        elif bytes(DischargeAmpereHours[n]) >= b'00600' and bytes(DischargeAmpereHours[n]) < b'00800':
          SampleStatus[n] = '3'  # Register Ah as 3Ah
        #  [ 3,999 < DischargeAmpereHours[n] < 5,000 ]
        elif bytes(DischargeAmpereHours[n]) >= b'00800' and bytes(DischargeAmpereHours[n]) < b'01000':
          SampleStatus[n] = '4'  # Register Ah as 4Ah
        #  [ 4,999 < DischargeAmpereHours[n] < 6,000 ]
        elif bytes(DischargeAmpereHours[n]) >= b'01000' and bytes(DischargeAmpereHours[n]) < b'01200':
          SampleStatus[n] = '5'  # Register Ah as 5Ah
        #  [ 5,999 < DischargeAmpereHours[n] < 7,000 ]
        elif bytes(DischargeAmpereHours[n]) >= b'01200' and bytes(DischargeAmpereHours[n]) < b'01400':
          SampleStatus[n] = '6'  # Register Ah as 6Ah
        #  [ 6,999 < DischargeAmpereHours[n] < 8,000 ]
        elif bytes(DischargeAmpereHours[n]) >= b'01400' and bytes(DischargeAmpereHours[n]) < b'01600':
          SampleStatus[n] = 'R'  # Register Ah as 7Ah  #KA = R
        #  [ 7,999 < DischargeAmpereHours[n] < 9,000 ]
        elif bytes(DischargeAmpereHours[n]) >= b'01600' and bytes(DischargeAmpereHours[n]) < b'1800':
          SampleStatus[n] = 'R'  # Register Ah as 8Ah  #KA = R
        #  5 x 1,800 = 9,000mAh; [ DischargeAmpereHours[n] > 9,000 ]
        if bytes(DischargeAmpereHours[n]) > b'01800':
          SampleStatus[n] = 'R'  # Register Ah as 9Ah. #KA = R

        ProfileDischargeStatus[n] = SampleStatus[n]


      try:
        DSC_File.write( bytes(DischargeAmpereHours[n]) )
      except Exception as error:
        pass
        DSC_File.write( b'00020' )

      n += 1
    DSC_File.write( b'\n' )

    # DUMMY READ
    temp = TEMP_File.readline()

    # Send the CSV data to the CSV file
    temp = TEMP_File.readlines()
    DSC_File.writelines(temp)

    TEMP_File.close()
    DSC_File.close()
#    DVDT_File.close()

  Metrics.Display_Status()

#*********************************************************************#
#***************** A Valid CSV File Has Been Created *****************#  
#*********************************************************************#

#######################################################################
#######################################################################
#######################################################################

def Sync_Quad_Chargers( portlist ):
  global MAX_USB_PORTS
  root.update()

  DecKey( portlist )
  time.sleep(0.5)

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )

      try:
        port.write( b'getnimhdisplay\n' )
      except: # Check for any error
        time.sleep(0.05)
        port.write( b'getnimhdisplay\n' )

      while port.out_waiting > 0:
        pass
      time.sleep(0.05)

      q += 1
    else: break

  time.sleep(1.00)
#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

def Seek_Charge_Auto( portlist ):
  global MAX_USB_PORTS
  global KeyStatus

  root.update()

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )
      port.write( b'getnimhdisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1
    else: break

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )
      port.write( b'enter\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )
      q += 1
    else: break

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )
      port.write( b'getmanualchargedisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1
    else: break

  time.sleep( 1.0 ) # Wait until the seek operation == finished

#  KeyStatus = 'STOP' # Release the GUI buttons

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

def Run_Charge_Auto( portlist, mode ):
  global KeyStatus

  print()
  print( '**********************************************************' )
  print()
  print( '>>>>>>>>>>>>>>>>>> RUNNING CHARGE AUTO <<<<<<<<<<<<<<<<<<<' )
  print()
  print( '**********************************************************' )
  print()
  print()

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    # logfile.write( '\nDATE: ' + datetime.today().strftime("%D   \n") )
    logfile.write( '>>>>>>>>>>>>>>>>>> RUNNING CHARGE AUTO <<<<<<<<<<<<<<<<<<<\n' )

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Charge_Label = ttk.Label( ChargeList_Frame, text='  ' + TimeString )
  Module_Charge_Label.grid( column=9, row=1, sticky=tk.W )

  Seek_Charge_Auto( portlist )

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

  BeginCycle( portlist, mode )

  time.sleep( 5.0 )

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )
      port.write( b'getnimhdisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )
      q += 1
    else: break


  print()
  print( '**********************************************************\n' )
  print()
  print( '>>>>>>>>>>>>>>>>> CHARGE AUTO FINISHED <<<<<<<<<<<<<<<<<<<\n' )
  print()
  print( '**********************************************************\n' )  
  print( '\n\n' )

  KeyStatus = 'STOP' # Release the GUI buttons

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Charge_Label = ttk.Label( ChargeList_Frame, text='  ' + TimeString )
  Module_Charge_Label.grid( column=9, row=3, sticky=tk.W )

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

def Seek_Discharge_Auto( portlist ):
  global MAX_USB_PORTS
  global KeyStatus

  root.update()

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )
      port.write( b'getnimhdisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1
    else: break

  time.sleep( 5.0 )

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )
      port.write( b'enter\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )
      q += 1
    else: break

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )
      port.write( b'getmanualdischargedisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.1 )
      q += 1
    else: break

  time.sleep( 1.0 )

#  KeyStatus = 'STOP' # Release the GUI buttons

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

def Run_Discharge_Auto( portlist, mode ):
  global KeyStatus

  print()
  print( '**********************************************************' )
  print()
  print( '***************** RUNNING DISCHARGE AUTO *****************' )
  print()
  print( '**********************************************************' )
  print()
  print()

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    # logfile.write( '\nDATE: ' + datetime.today().strftime("%D   \n") )
    logfile.write( '>>>>>>>>>>>>>>>> RUNNING DISCHARGE AUTO <<<<<<<<<<<<<<<<<<\n' )

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Discharge_Label = ttk.Label( DischargeList_Frame, text='  ' + TimeString )
  Module_Discharge_Label.grid( column=10, row=1, sticky=tk.W )

  Seek_Discharge_Auto( portlist )

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

  BeginCycle( portlist, mode )

  time.sleep( 5.0 )

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )
      port.write( b'hicurrentoff\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )

      port.write( b'hicurrentoff\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )
      q += 1
    else: break

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0 )
      port.write( b'getnimhdisplay\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )
      q += 1
    else: break

  print()
  print( '**********************************************************' )
  print()
  print( '>>>>>>>>>>>>>>>> DISCHARGE AUTO FINISHED <<<<<<<<<<<<<<<<<' )
  print()
  print( '**********************************************************' )
  print( '\n\n' )

  KeyStatus = 'STOP' # Release the GUI buttons

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Discharge_Label = ttk.Label( DischargeList_Frame, text='  ' + TimeString )
  Module_Discharge_Label.grid( column=10, row=3, sticky=tk.W )

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

'''
  ******************** DISCHARGE / CHARGE CYCLE ***********************
'''
def Run_Discharge_Charge_Cycle( portlist ):
  global mode
  global PassCount
  global PassTarget
  global GraphEnable
  global GraphEnable
  global ProfileStatus

  PassTarget = 1

  print()
  print( '**********************************************************' )
  print( '*                                                        *' )
  print( '*                        STARTING                        *' )  
  print( '*                DISCHARGE > > > > CHARGE                *' )
  print( '*                     WITH  PROFILE                      *' )
  print( '*                                                        *' )
  print( '**********************************************************' )
  print()
  print()

  Metrics.Create_Cycle_Time_List()
  Metrics.Create_Charge_Time_List()
  Metrics.Create_Discharge_Time_List()

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Cycle_Label = ttk.Label( CycleList_Frame, text='  ' + TimeString )
  Module_Cycle_Label.grid( column=8, row=1, sticky=tk.W )

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    logfile.write( '\n\n\n\nDATE: ' + datetime.today().strftime("%D\n") )
    logfile.write( 'START TIME: ' + datetime.today().strftime("%H:%M HOURS\n") )
    logfile.write( '>>>>>>>>>>>>>>>>>>>>>>>>> DISCHARGE > > > > CHARGE <<<<<<<<<<<<<<<<<<<<<<<<<<<\n' )

#----------------------------------------------------------
  PassCount = 1
  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

  GraphEnable = True
#  print( 'Opening:  ' + DSC_FILE )
  mode = 'DISCHARGE'
  ProfileStatus = 'DSC_CHG'
  Metrics.Display_Operating_Mode()

  Run_Discharge_Auto( portlist, mode )

#  print( 'Closing:  ' + DSC_FILE )

#---------------------------------------------------------- 

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

#  print( 'Opening:  ' + CHG_FILE )
  mode = 'CHARGE'
  GraphEnable = False
  ProfileStatus = 'DSC_CHG'
  Metrics.Display_Operating_Mode()

  Run_Charge_Auto( portlist, mode )

  mode = 'FINISHED'
  ProfileStatus = 'IDLE'
  GraphEnable = False
  Metrics.Display_Operating_Mode()
#  print( 'Closing:  ' + CHG_FILE )

#----------------------------------------------------------

  Get_IR( MAX_USB_PORTS, baudrate )
  Get_Load_Voltage( MAX_USB_PORTS, baudrate )

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Cycle_Label = ttk.Label( CycleList_Frame, text='  ' + TimeString )
  Module_Cycle_Label.grid( column=8, row=3, sticky=tk.W )

  KeyStatus = 'STOP' # Release the GUI buttons

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    logfile.write( '>>>>>>>>>>>>>>>>>>>>>>>>>>> RECONDITIONING COMPLETE <<<<<<<<<<<<<<<<<<<<<<<<<<\n' )
    logfile.write( 'STOP TIME: ' + datetime.today().strftime("%H:%M HOURS\n") )

  print( '\n\n\n' )

#---------------------------------------------------------- 

  print( '*****************************************************************************' )
  print( '*****************************************************************************' )
  print( '**                                                                         **' )
  print( '**                                                                         **' )
  print( '**           ******  ******   *****  ******* ** **      *******            **' )
  print( '**           ******* ******* ******* ******* ** **      *******            **' )
  print( '**           **   ** **   ** **   ** **         **      **                 **' )
  print( '**           ******* ******* **   ** *****   ** **      *****              **' )
  print( '**           ******  ******  **   ** *****   ** **      *****              **' )
  print( '**           **      ** **   **   ** **      ** **      **                 **' )
  print( '**           **      **  **  ******* **      ** ******* *******            **' )
  print( '**           **      **   **  *****  **      ** ******* *******            **' )
  print( '**                                                                         **' )
  print( '**                                                                         **' )
  print( '**    *****   *****  ***    *** ******* **      ******* ******** *******   **' )
  print( '**   ******* ******* ****  **** ******* **      ******* ******** *******   **' )
  print( '**   **   ** **   ** ** **** ** **   ** **      **         **    **        **' )
  print( '**   **      **   ** **  **  ** ******* **      *****      **    *****     **' )
  print( '**   **      **   ** **      ** ******  **      *****      **    *****     **' )
  print( '**   **   ** **   ** **      ** **      **      **         **    **        **' )
  print( '**   ******* ******* **      ** **      ******* ******     **    *******   **' )
  print( '**    *****   *****  **      ** **      ******* *******    **    *******   **' )
  print( '**                                                                         **' )
  print( '**                                                                         **' )
  print( '*****************************************************************************' )
  print( '*****************************************************************************' )

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

'''
  ******************** ONE PASS RECONDITIONING ***********************
'''
def Start_One_Cycle_Reconditioning( portlist ):
  global mode
  global PassCount
  global PassTarget
  global GraphEnable
  global ProfileStatus

  print()
  print( '----------------------------------------------------------' )
  print( '>>>>>>>>>>>>>>> SINGLE PASS RECONDITIONING <<<<<<<<<<<<<<<' )
  print( '----------------------------------------------------------' )
  print()
  print( '>>>>>>>>>>>>>>>>>>>>> STARTING PASS <<<<<<<<<<<<<<<<<<<<<<' )
  print()

  Metrics.Create_Cycle_Time_List()
  Metrics.Create_Charge_Time_List()
  Metrics.Create_Discharge_Time_List()

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Cycle_Label = ttk.Label( CycleList_Frame, text='  ' + TimeString )
  Module_Cycle_Label.grid( column=8, row=1, sticky=tk.W )

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    logfile.write( '\n\n\n\nDATE: ' + datetime.today().strftime("%D   \n") )
    logfile.write( 'START TIME: ' + datetime.today().strftime("%H:%M HOURS\n") )
    logfile.write( '>>>>>>>>>>>>>>>>>>>>>>>>>> SINGLE PASS RECONDITIONING <<<<<<<<<<<<<<<<<<<<<<<<\n' )
    logfile.write( '\n>>>>>>>>>>>>>>>>>> STARTING PASS ONE <<<<<<<<<<<<<<<<<<<<<\n' )

#----------------------------------------------------------

  PassTarget = 1
  PassCount = 1
  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

  mode = 'DISCHARGE' # First Pass - graph disabled
  GraphEnable = False
  ProfileStatus = '1st'
  Metrics.Display_Operating_Mode()

  # Clear the Error_200_List
  q = 0
  while q <= MAX_USB_PORTS:
    Error_200_List[q] = False
    q += 1

  Run_Discharge_Auto( portlist, mode )

  mode = 'IDLE'
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()

  time.sleep( 5.0 )

#---------------------------------------------------------- 

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

  mode = 'CHARGE'
  GraphEnable = False
  ProfileStatus = '1st'
  Metrics.Display_Operating_Mode()

  # Clear the Error_200_List
  q = 0
  while q <= MAX_USB_PORTS:
    Error_200_List[q] = False
    q += 1

  Run_Charge_Auto( portlist, mode )

  mode = 'IDLE'
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()

  time.sleep( 5.0 )

#---------------------------------------------------------- 

  print()
  print( '----------------------------------------------------------' )
  print( '>>>>>>>>>>>>>>> SINGLE PASS RECONDITIONING <<<<<<<<<<<<<<<' )
  print( '----------------------------------------------------------' )
  print()
  print( '>>>>>>>>>>>>>>>>>> STARTING FINAL PASS <<<<<<<<<<<<<<<<<<<' )
  print( '\n\n\n' )

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    # logfile.write( '\nDATE: ' + datetime.today().strftime("%D   \n") )
    logfile.write( '\n>>>>>>>>>>>>>>>>> STARTING FINAL PASS <<<<<<<<<<<<<<<<<<\n' )  

  Metrics.Create_Charge_Time_List()
  Metrics.Create_Discharge_Time_List()

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

#  print( 'Opening:  ' + DSC_FILE )
  mode = 'DISCHARGE' # Final Pass - graph ensabled
  GraphEnable = True
  ProfileStatus = 'PROFILE'
  Metrics.Display_Operating_Mode()

  Run_Discharge_Auto( portlist, mode )

  mode = 'IDLE'
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()
#  print( 'Closing:  ' + DSC_FILE )

  time.sleep( 5.0 )

#---------------------------------------------------------- 

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

#  print( 'Opening:  ' + CHG_FILE )
  mode = 'CHARGE'
  GraphEnable = False
  ProfileStatus = 'PROFILE'
  Metrics.Display_Operating_Mode()

  Run_Charge_Auto( portlist, mode )

  mode = 'FINISHED'
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()
#  print( 'Closing:  ' + CHG_FILE )

  time.sleep( 5.0 )

#---------------------------------------------------------- 

  Get_IR( MAX_USB_PORTS, baudrate )
  Get_Load_Voltage( MAX_USB_PORTS, baudrate )

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Cycle_Label = ttk.Label( CycleList_Frame, text='  ' + TimeString )
  Module_Cycle_Label.grid( column=8, row=3, sticky=tk.W )

  KeyStatus = 'STOP' # Release the GUI buttons

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    logfile.write( '>>>>>>>>>>>>>>>>>>>>>>>>>>> RECONDITIONING COMPLETE <<<<<<<<<<<<<<<<<<<<<<<<<<\n' )
    logfile.write( 'STOP TIME: ' + datetime.today().strftime("%H:%M HOURS\n") )

  print( '\n\n\n' )

  print( '*****************************************************************************' )
  print( '*****************************************************************************' )
  print( '**                                                                         **' )
  print( '**                                                                         **' )
  print( '**           ******  ******   *****  ******* ** **      *******            **' )
  print( '**           ******* ******* ******* ******* ** **      *******            **' )
  print( '**           **   ** **   ** **   ** **         **      **                 **' )
  print( '**           ******* ******* **   ** *****   ** **      *****              **' )
  print( '**           ******  ******  **   ** *****   ** **      *****              **' )
  print( '**           **      ** **   **   ** **      ** **      **                 **' )
  print( '**           **      **  **  ******* **      ** ******* *******            **' )
  print( '**           **      **   **  *****  **      ** ******* *******            **' )
  print( '**                                                                         **' )
  print( '**                                                                         **' )
  print( '**    *****   *****  ***    *** ******* **      ******* ******** *******   **' )
  print( '**   ******* ******* ****  **** ******* **      ******* ******** *******   **' )
  print( '**   **   ** **   ** ** **** ** **   ** **      **         **    **        **' )
  print( '**   **      **   ** **  **  ** ******* **      *****      **    *****     **' )
  print( '**   **      **   ** **      ** ******  **      *****      **    *****     **' )
  print( '**   **   ** **   ** **      ** **      **      **         **    **        **' )
  print( '**   ******* ******* **      ** **      ******* ******     **    *******   **' )
  print( '**    *****   *****  **      ** **      ******* *******    **    *******   **' )
  print( '**                                                                         **' )
  print( '**                                                                         **' )
  print( '*****************************************************************************' )
  print( '*****************************************************************************' )

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

  '''
  ******************** TWO PASS RECONDITIONING ***********************
  '''
def Start_Two_Cycle_Reconditioning( portlist ):
  global mode
  global PassCount
  global PassTarget
  global GraphEnable
  global ProfileStatus

  print()
  print( '----------------------------------------------------------' )
  print( '>>>>>>>>>>>>>>>> TWO PASS RECONDITIONING <<<<<<<<<<<<<<<<<' )
  print( '----------------------------------------------------------' )
  print()
  print( '>>>>>>>>>>>>>>>>>>> STARTING PASS ONE <<<<<<<<<<<<<<<<<<<<' )
  print()

  Metrics.Create_Cycle_Time_List()
  Metrics.Create_Charge_Time_List()
  Metrics.Create_Discharge_Time_List()

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Cycle_Label = ttk.Label( CycleList_Frame, text='  ' + TimeString )
  Module_Cycle_Label.grid( column=8, row=1, sticky=tk.W )

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    logfile.write( '\n\n\n\nDATE: ' + datetime.today().strftime("%D   \n") )
    logfile.write( 'START TIME: ' + datetime.today().strftime("%H:%M HOURS\n") )
    logfile.write( '>>>>>>>>>>>>>>>>>>>>>>>>>> TWO PASS RECONDITIONING <<<<<<<<<<<<<<<<<<<<<<<<<<<\n' )
    logfile.write( '\n>>>>>>>>>>>>>>>>>>> STARTING PASS ONE <<<<<<<<<<<<<<<<<<<<\n' )

#----------------------------------------------------------

  PassTarget = 2
  PassCount = 1
  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

  mode = 'DISCHARGE' # First Pass - graph disabled
  GraphEnable = False
  ProfileStatus = '1st'
  Metrics.Display_Operating_Mode()

  # Clear the Error_200_List
  q = 0
  while q <= MAX_USB_PORTS:
    Error_200_List[q] = False
    q += 1

  Run_Discharge_Auto( portlist, mode )

  mode = 'IDLE' # First Pass - graph disabled
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()

  time.sleep( 5.0 )

#---------------------------------------------------------- 

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

  mode = 'CHARGE'
  GraphEnable = False
  ProfileStatus = '1st'
  Metrics.Display_Operating_Mode()

  # Clear the Error_200_List
  q = 0
  while q <= MAX_USB_PORTS:
    Error_200_List[q] = False
    q += 1

  Run_Charge_Auto( portlist, mode )

  mode = 'IDLE'
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()

  time.sleep( 5.0 )

  print( '\n\n\n' )

#----------------------------------------------------------

  print()
  print( '----------------------------------------------------------' )
  print( '>>>>>>>>>>>>>>>> TWO PASS RECONDITIONING <<<<<<<<<<<<<<<<<' )
  print( '----------------------------------------------------------' )
  print()
  print( '>>>>>>>>>>>>>>>>>>> STARTING PASS TWO <<<<<<<<<<<<<<<<<<<<' )
  print()

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    # logfile.write( '\nDATE: ' + datetime.today().strftime("%D   \n") )
    logfile.write( '\n>>>>>>>>>>>>>>>>>>> STARTING PASS TWO <<<<<<<<<<<<<<<<<<<<\n' )

  PassCount = 2

  Metrics.Create_Charge_Time_List()
  Metrics.Create_Discharge_Time_List()

#----------------------------------------------------------

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

  mode = 'DISCHARGE'# Second Pass - graph disabled
  GraphEnable = False
  ProfileStatus = '2nd'
  Metrics.Display_Operating_Mode()

  # Clear the Error_200_List
  q = 0
  while q <= MAX_USB_PORTS:
    Error_200_List[q] = False
    q += 1

  Run_Discharge_Auto( portlist, mode )

  mode = 'IDLE'# Second Pass - graph disabled
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()

#---------------------------------------------------------- 

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

  mode = 'CHARGE'
  GraphEnable = False
  ProfileStatus = '2nd'
  Metrics.Display_Operating_Mode()

  # Clear the Error_200_List
  q = 0
  while q <= MAX_USB_PORTS:
    Error_200_List[q] = False
    q += 1

  Run_Charge_Auto( portlist, mode )

  mode = 'IDLE'
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()

  time.sleep( 5.0 )

  print( '\n\n\n' )

#----------------------------------------------------------

  print()
  print( '----------------------------------------------------------' )
  print( '>>>>>>>>>>>>>>>> TWO PASS RECONDITIONING <<<<<<<<<<<<<<<<<' )
  print( '----------------------------------------------------------' )
  print()
  print( '>>>>>>>>>>>>>>>>>> STARTING FINAL PASS <<<<<<<<<<<<<<<<<<<' )
  print()

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    #logfile.write( '\nDATE: ' + datetime.today().strftime("%D   \n") )
    logfile.write( '\n>>>>>>>>>>>>>>>>>>> STARTING FINAL PASS <<<<<<<<<<<<<<<<<<\n' )


  PassTarget = 2
  PassCount = 2

  Metrics.Create_Charge_Time_List()
  Metrics.Create_Discharge_Time_List()

#----------------------------------------------------------

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

#  print( 'Opening:  ' + DSC_FILE )
  mode = 'DISCHARGE' # Final Pass - graph enabled
  GraphEnable = True
  ProfileStatus = 'PROFILE'
  Metrics.Display_Operating_Mode()

  Run_Discharge_Auto( portlist, mode )

  mode = 'IDLE' # Final Pass - graph enabled
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()
#  print( 'Closing:  ' + DSC_FILE )

  time.sleep( 5.0 )

#---------------------------------------------------------- 

  SampleCount = 0
  Metrics.Display_SampleCount(SampleCount)

#  print( 'Opening:  ' + CHG_FILE )
  mode = 'CHARGE'
  GraphEnable = False
  ProfileStatus = 'PROFILE'
  Metrics.Display_Operating_Mode()

  Run_Charge_Auto( portlist, mode )

  mode = 'FINISHED'
  GraphEnable = False
  ProfileStatus = 'IDLE'
  Metrics.Display_Operating_Mode()
#  print( 'Closing:  ' + CHG_FILE )

  time.sleep( 5.0 )

#----------------------------------------------------------

  Get_IR( MAX_USB_PORTS, baudrate )
  Get_Load_Voltage( MAX_USB_PORTS, baudrate )

  TimeString = datetime.today().strftime("%D : %H%M")
  Module_Cycle_Label = ttk.Label( CycleList_Frame, text='  ' + TimeString )
  Module_Cycle_Label.grid( column=8, row=3, sticky=tk.W )

  KeyStatus = 'STOP' # Release the GUI buttons

  now = date.today()
  DateStamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
  #  LOG_FILE = "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/LOG_FILES/logfile.txt"
  with open( LOG_FILE, 'a+t' ) as logfile:
    logfile.write( '>>>>>>>>>>>>>>>>>>>>>>>>>>> RECONDITIONING COMPLETE <<<<<<<<<<<<<<<<<<<<<<<<<<\n' )
    logfile.write( 'STOP TIME: ' + datetime.today().strftime("%H:%M HOURS\n") )

  print( '\n\n\n' )

  print( '*****************************************************************************' )
  print( '*****************************************************************************' )
  print( '**                                                                         **' )
  print( '**                                                                         **' )
  print( '**           ******  ******   *****  ******* ** **      *******            **' )
  print( '**           ******* ******* ******* ******* ** **      *******            **' )
  print( '**           **   ** **   ** **   ** **         **      **                 **' )
  print( '**           ******* ******* **   ** *****   ** **      *****              **' )
  print( '**           ******  ******  **   ** *****   ** **      *****              **' )
  print( '**           **      ** **   **   ** **      ** **      **                 **' )
  print( '**           **      **  **  ******* **      ** ******* *******            **' )
  print( '**           **      **   **  *****  **      ** ******* *******            **' )
  print( '**                                                                         **' )
  print( '**                                                                         **' )
  print( '**    *****   *****  ***    *** ******* **      ******* ******** *******   **' )
  print( '**   ******* ******* ****  **** ******* **      ******* ******** *******   **' )
  print( '**   **   ** **   ** ** **** ** **   ** **      **         **    **        **' )
  print( '**   **      **   ** **  **  ** ******* **      *****      **    *****     **' )
  print( '**   **      **   ** **      ** ******  **      *****      **    *****     **' )
  print( '**   **   ** **   ** **      ** **      **      **         **    **        **' )
  print( '**   ******* ******* **      ** **      ******* ******     **    *******   **' )
  print( '**    *****   *****  **      ** **      ******* *******    **    *******   **' )
  print( '**                                                                         **' )
  print( '**                                                                         **' )
  print( '*****************************************************************************' )
  print( '*****************************************************************************' )

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

def EnterKey( portlist ):
  global MAX_USB_PORTS

  root.update()

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0.05 )
      port.write( b'enter\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 ) # Start all chargers
    else: break
    q += 1

#---------------------------------------------------------------------#

def BackKey( portlist ):
  global MAX_USB_PORTS

  root.update()

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0.05 )

      port.write( b'blueledoff\n' ) # Ensure CHARGE LED == inactive
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )

      port.write( b'redledoff\n' ) # Ensure DISCHARGE LED == inactive
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )

      port.write( b'greenledoff\n' ) # Ensure READY LED == inactive
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )

      port.write( b'mode\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )
    else: break
    q += 1

#---------------------------------------------------------------------#

def IncKey( portlist ):
  global MAX_USB_PORTS

  root.update()

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0.05 )

      port.write( b'increment\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )
    else: break
    q += 1

#---------------------------------------------------------------------#

def DecKey( portlist ):
  global MAX_USB_PORTS

  root.update()

  q = 0
  for p in portlist:
    if q < MAX_USB_PORTS:
      port = serial.Serial( portlist[p], baudrate, timeout = 0.05 )
      port.write( b'decrement\n' )
      while port.out_waiting > 0:
        pass
      time.sleep( 0.05 )
    else: break
    q += 1

#---------------------------------------------------------------------#

def StartCycle( portlist ):
  root.update()

  BeginCycle( portlist )

#---------------------------------------------------------------------#

def StopCycle( portlist ):
  root.update()

  EndCycle( portlist )

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

root = tk.Tk()
root.title( "Green Bean Battery, LLC.\t 40 Channel 5xI Multi-Function Profiler\t\t Version " + version )
root.resizable( width=False, height=False )

mainframe = ttk.Frame( root, padding="5 5 5 5" )
mainframe.grid( column=0, row=0, sticky=( N, W, E, S ) )
mainframe.columnconfigure( 0, weight=1 )
mainframe.rowconfigure( 0, weight=1 )
mainframe.mainloop

#.....................................................................#

button = ttk.LabelFrame( mainframe, text=' COMMAND CENTER ')
button.grid( column=0, row=0, padx=5, pady=5, sticky=tk.W )

ModuleList_Frame = ttk.LabelFrame( mainframe, text=' MODULE STATUS ' )
ModuleList_Frame.grid( column=6, row=0, padx=0, pady=0, sticky=tk.N  )

StatusList_Frame = ttk.LabelFrame( ModuleList_Frame, text=' STATUS ' )
StatusList_Frame.grid( column=6, row=0, padx=0, pady=0, sticky=tk.N  )

CycleList_Frame = ttk.LabelFrame( ModuleList_Frame, text=' CYCLE ' )
CycleList_Frame.grid( column=8, row=0, padx=0, pady=0, sticky=tk.N  )

ChargeList_Frame = ttk.LabelFrame( ModuleList_Frame, text=' CHARGE ' )
ChargeList_Frame.grid( column=9, row=0, padx=0, pady=0, sticky=tk.N  )

DischargeList_Frame = ttk.LabelFrame( ModuleList_Frame, text=' DISCHARGE ' )
DischargeList_Frame.grid( column=10, row=0, padx=0, pady=0, sticky=tk.N  )

dVdT_List_Frame = ttk.LabelFrame( ModuleList_Frame, text=' dV/dt ' )
dVdT_List_Frame.grid( column=12, row=0, padx=0, pady=0, sticky=tk.N )

OperatingList_Frame = ttk.LabelFrame( button, text=' SYSTEM STATUS ' )
OperatingList_Frame.grid( column=0, row=4, padx=0, pady=0, sticky=tk.W )
#.....................................................................#

baudrate = Get_CFG( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/BotBox.cfg" )

portlist = Initialize_Comports( baudrate )

#-------------- Turn off the blue LED and 4 Ampere load --------------#
q = 0
for p in portlist:
  if q < MAX_USB_PORTS:
    port = serial.Serial( portlist[p], baudrate, timeout = 0 ) #.005 )

    port.write( b'blueledoff\n' ) # Ensure charge LED == NOT active   
    while port.out_waiting > 0:
      pass
    time.sleep( 0.05 )

    port.write( b'blueledoff\n' ) # Ensure charge LED == NOT active
    while port.out_waiting > 0:
      pass
    time.sleep( 0.05 )

    port.write( b'hicurrentoff\n' ) # Ensure high current load == NOT active
    while port.out_waiting > 0:
      pass
    time.sleep(0.05)

    port.write( b'hicurrentoff\n' ) # Ensure high current load NOT active
    while port.out_waiting > 0:
      pass
    time.sleep(0.05)
  else: break
  q += 1
#.....................................................................#

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

class Metrics():
  global mode

  x = 3
  y = 1

  def __init__(self):
    self.ModuleVoltage = ModuleVoltage
    self.DischargeAmpereHours = DischargeAmpereHours
    self.ChargeAmpereHours = ChargeAmpereHours
    self.SampleStatus = SampleStatus

    self.StatusList_Frame = StatusList_Frame
    self.CycleList_Frame = CycleList_Frame
    self.OperatingList_Frame = OperatingList_Frame
    self.ChargeList_Frame = ChargeList_Frame
    self.DischargeList_Frame = DischargeList_Frame
    self.dVdT_List_Frame = dVdT_List_Frame

    Sentenel_Status_Label = ttk.Label( button, text="-", foreground=yellow, background='blue' )
    Sentenel_Status_Label.grid( column=1, row=4 ) #, sticky=tk.E )

  def sentenel(s):

    if s == 0:
      Sentenel_Status_Label = ttk.Label( button, text="-" )
      Sentenel_Status_Label.grid( column=1, row=4 ) #, sticky=tk.N )
#      ModuleStatus_Label.grid( padx=0, pady=0 )
    if s == 1:
      Sentenel_Status_Label = ttk.Label( button, text="\\" )
      Sentenel_Status_Label.grid( column=1, row=4 ) #, sticky=tk.E )
#      ModuleStatus_Label.grid( padx=0, pady=0 )
    if s == 2:
      Sentenel_Status_Label = ttk.Label( button, text="|" )
      Sentenel_Status_Label.grid( column=1, row=4 ) #, sticky=tk.S )
#      ModuleStatus_Label.grid( padx=0, pady=0 )
    if s == 3:
      Sentenel_Status_Label = ttk.Label( button, text="/" )
      Sentenel_Status_Label.grid( column=1, row=4 ) #, sticky=tk.W )
#      ModuleStatus_Label.grid( padx=0, pady=0 )
    if s == 3:
      s = 0
    else:
      s += 1
      root.update()
    return s

#---------------------------------------------------------------------#

  def Create_Status_List():
    pass

    q = 0
    n = 0
    while n < MAX_USB_PORTS:
      Module_Status_Label = ttk.Label( StatusList_Frame, text="MODULE " + str(n+1) )
      Module_Status_Label.grid( column=6, row=q, sticky=tk.W+E )
      Module_Status_Label.grid( padx=0, pady=0 )

      Module_Status_Label = ttk.Label( StatusList_Frame, text=" STOP ", background='yellow' )
      Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
      Module_Status_Label.grid( padx=0, pady=0 )
      q += 1
      n +=1

  def Update_R_Errors():
    pass
    global ProfileStatus

    q = 0
    n = 0
    while n < MAX_USB_PORTS:
      #  # 5 x 20 = 100; [ DischargeAmpereHours[n] != 100 ]
      if bytes(DischargeAmpereHours[n]) == b'00020':
        SampleStatus[n] = 'R'  # "100" error ---> CQ3 Status Loss
      #  [ 2,999 < DischargeAmpereHours[n] and DischargeAmpereHours[n] != 100 ]
      elif bytes(DischargeAmpereHours[n]) < b'00600' and bytes(DischargeAmpereHours[n]) != b'00020':
        SampleStatus[n] = 'X'  # Less that 3,000mAh, but not a "100" error  ---> Module Failure
      n += 1
      q += 1
    Metrics.Display_Status()

  def Display_Status():
    pass
    global ProfileStatus

    q = 0
    n = 0
    while n < MAX_USB_PORTS:
#      if SampleStatus[n] != SampleStatusLast[n] or ProfileStatus == 'PROFILE':
        if SampleStatus[n] == 'DONE':
          Module_Status_Label = ttk.Label( StatusList_Frame, text=' DONE', background='lightgreen' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == 'RUN':
          Module_Status_Label = ttk.Label( StatusList_Frame, text='  RUN ', background='cyan')
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == 'STOP':
          Module_Status_Label = ttk.Label( StatusList_Frame, text=' STOP', background='violet' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == 'X':
          Module_Status_Label = ttk.Label( StatusList_Frame, text='    X', background='red' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == 'R':
          Module_Status_Label = ttk.Label( StatusList_Frame, text='    R', background='yellow' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == '3':
          Module_Status_Label = ttk.Label( StatusList_Frame, text=' 3  Ah', background='lightgreen' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == '4':
          Module_Status_Label = ttk.Label( StatusList_Frame, text=' 4  Ah', background='lightgreen' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == '5':
          Module_Status_Label = ttk.Label( StatusList_Frame, text=' 5  Ah', background='lightgreen' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == '6':
          Module_Status_Label = ttk.Label( StatusList_Frame, text=' 6  Ah', background='lightgreen' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == '7':
          Module_Status_Label = ttk.Label( StatusList_Frame, text=' 7  Ah', background='lightgreen' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == '8':
          Module_Status_Label = ttk.Label( StatusList_Frame, text=' 8  Ah', background='lightgreen' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )
        elif SampleStatus[n] == '9':
          Module_Status_Label = ttk.Label( StatusList_Frame, text=' 9  Ah', background='lightgreen' )
          Module_Status_Label.grid( column=7, row=q, sticky=tk.W+E )         
#        SampleStatusLast[n] = SampleStatus[n]
        n += 1
        q += 1
#---------------------------------------------------------------------#

  def Create_Cycle_Time_List():
    pass

    TimeString = datetime.today().strftime("%D : %H%M")
    Module_Cycle_Label = ttk.Label( CycleList_Frame, text='START TIME:      ' )
    Module_Cycle_Label.grid( column=8, row=0, sticky=tk.W+E )
    Module_Cycle_Label = ttk.Label( CycleList_Frame, text='                            ' )
    Module_Cycle_Label.grid( column=8, row=1, sticky=tk.W+E )

    TimeString = datetime.today().strftime("%D : %H%M")
    Module_Cycle_Label = ttk.Label( CycleList_Frame, text='STOP TIME:       ' )
    Module_Cycle_Label.grid( column=8, row=2, sticky=tk.W+E )
    Module_Cycle_Label = ttk.Label( CycleList_Frame, text='                            ' )
    Module_Cycle_Label.grid( column=8, row=3, sticky=tk.W+E )

#---------------------------------------------------------------------#

  def Create_Charge_Time_List():
    pass

    TimeString = datetime.today().strftime("%D : %H%M")
    Module_Charge_Label = ttk.Label( ChargeList_Frame, text='START TIME:      ' )
    Module_Charge_Label.grid( column=9, row=0, sticky=tk.W )
    Module_Charge_Label = ttk.Label( ChargeList_Frame, text='                            ' )
    Module_Charge_Label.grid( column=9, row=1, sticky=tk.W )

    TimeString = datetime.today().strftime("%D : %H%M")
    Module_Charge_Label = ttk.Label( ChargeList_Frame, text='STOP TIME:       ' )
    Module_Charge_Label.grid( column=9, row=2, sticky=tk.W )
    Module_Charge_Label = ttk.Label( ChargeList_Frame, text='                            ' )
    Module_Charge_Label.grid( column=9, row=3, sticky=tk.W )

#---------------------------------------------------------------------#

  def Create_Discharge_Time_List():
    pass

    TimeString = datetime.today().strftime("%D : %H%M")
    Module_Discharge_Label = ttk.Label( DischargeList_Frame, text='START TIME:      ' )
    Module_Discharge_Label.grid( column=10, row=0, sticky=tk.W )
    Module_Discharge_Label = ttk.Label( DischargeList_Frame, text='                            ' )
    Module_Discharge_Label.grid( column=10, row=1, sticky=tk.W )

    TimeString = datetime.today().strftime("%D : %H%M")
    Module_Discharge_Label = ttk.Label( DischargeList_Frame, text='STOP TIME:       ' )
    Module_Discharge_Label.grid( column=10, row=2, sticky=tk.W )
    Module_Discharge_Label = ttk.Label( DischargeList_Frame, text='                            ' )
    Module_Discharge_Label.grid( column=10, row=3, sticky=tk.W )

#---------------------------------------------------------------------#

  def Create_dVdt_List():
    pass

    q = 0
    n = 0
    while n < MAX_USB_PORTS:
      dVdT_Label = ttk.Label( dVdT_List_Frame, text=str( '       0.00' ), background='lightgray' )
      dVdT_Label.grid( column=12, row=q, sticky=tk.E )
      dVdT_Label.grid( padx=0, pady=0 )
      q += 1
      n += 1

  def Display_dVdT():
    pass

    dVdT = 0.00
    n = 0
    q = 0
    while n < MAX_USB_PORTS:

      dVdT_Label = ttk.Label( dVdT_List_Frame, text='             ', background='lightgray' )
      dVdT_Label.grid( column=12, row=q, sticky=tk.E )

      if float(Module_dVdt[n]) <= float(0.20):
        dVdT_Label = ttk.Label( dVdT_List_Frame, text=str(Module_dVdt[n]), background='lightgreen' )
      else:
        dVdT_Label = ttk.Label( dVdT_List_Frame, text=str(Module_dVdt[n]), background='yellow' )
      dVdT_Label.grid( column=12, row=q, sticky=tk.E )
      dVdT_Label.grid( padx=0, pady=0 )
      q += 1
      n += 1

#---------------------------------------------------------------------#

  def Create_Operating_List(SampleCount):
    pass

    global PassCount
    global PassTarget

    System_Mode_Label = ttk.Label( OperatingList_Frame, text='                               ', background='cyan' )
    System_Mode_Label.grid( column=0, row=3, sticky=tk.W )
    System_Mode_Label.grid( padx=0, pady=0 )

    System_Mode_Label = ttk.Label( OperatingList_Frame, text='IDLE ', background='cyan' )
    System_Mode_Label.grid( column=0, row=3, sticky=tk.W )
    System_Mode_Label.grid( padx=0, pady=0 )

    System_Mode_Label = ttk.Label( OperatingList_Frame, text='                                ', background='cyan' )
    System_Mode_Label.grid( column=0, row=4, sticky=tk.W )
    System_Mode_Label.grid( padx=0, pady=0 )

    System_Mode_Label = ttk.Label( OperatingList_Frame, text='IDLE: ' + str(mode), background='cyan' )
    System_Mode_Label.grid( column=0, row=4, sticky=tk.W )
    System_Mode_Label.grid( padx=0, pady=0 )

    System_Mode_Label = ttk.Label( OperatingList_Frame, text='                                ', background='cyan' )
    System_Mode_Label.grid( column=0, row=5, sticky=tk.W )
    System_Mode_Label.grid( padx=0, pady=0 )

    System_Mode_Label = ttk.Label( OperatingList_Frame, text='SAMPLE: ' + str(SampleCount), background='cyan' )
    System_Mode_Label.grid( column=0, row=5, sticky=tk.W )
    System_Mode_Label.grid( padx=0, pady=0 )

#---------------------------------------------------------------------#

  def Display_Operating_Mode():
    pass

    global mode
    global PassCount
    global ProfileStatus
    global PassTarget

    System_Status_Label = ttk.Label( OperatingList_Frame, text='                                ', background='cyan' )
    System_Status_Label.grid( column=0, row=3, sticky=tk.W )
    System_Status_Label.grid( padx=0, pady=0 )

    if ProfileStatus == '1st':
      System_Status_Label = ttk.Label( OperatingList_Frame, text='NiMH CYCLE 1 of ' + str(PassTarget), background='cyan' )
    if ProfileStatus == '2nd':
      System_Status_Label = ttk.Label( OperatingList_Frame, text='NiMH CYCLE 2 of ' + str(PassTarget), background='cyan' )
    if ProfileStatus == 'PROFILE':
      System_Status_Label = ttk.Label( OperatingList_Frame, text='PROFILE CYCLE', background='cyan')
    if ProfileStatus == 'DISCHARGE':
     System_Status_Label = ttk.Label( OperatingList_Frame, text='DISCHARGE', background='cyan')
    if ProfileStatus == 'DIS_AUTO':
     System_Status_Label = ttk.Label( OperatingList_Frame, text='DISCHARGE AUTO', background='cyan')
    if ProfileStatus == 'CHARGE':
     System_Status_Label = ttk.Label( OperatingList_Frame, text='CHARGE', background='cyan')
    if ProfileStatus == 'CHG_AUTO':
     System_Status_Label = ttk.Label( OperatingList_Frame, text='CHARGE AUTO', background='cyan')
    if ProfileStatus == 'DSC_CHG':
     System_Status_Label = ttk.Label( OperatingList_Frame, text='DSC ---> CHG', background='cyan')
    if ProfileStatus == 'IR_TEST':
     System_Status_Label = ttk.Label( OperatingList_Frame, text='IR_TEST', background='cyan')
    if ProfileStatus == 'IDLE':
     System_Status_Label = ttk.Label( OperatingList_Frame, text='IDLE', background='cyan')

    System_Status_Label.grid( column=0, row=3, sticky=tk.W )
    System_Status_Label.grid( padx=0, pady=0 )

    System_Mode_Label = ttk.Label( OperatingList_Frame, text='                              ', background='cyan' )
    System_Mode_Label.grid( column=0, row=4, sticky=tk.W )
    System_Mode_Label.grid( padx=0, pady=0 )

    if mode == 'IDLE':
      System_Mode_Label = ttk.Label( OperatingList_Frame, text='IDLE' + '                   ', foreground='black', background='cyan' )
    if mode == 'CHARGE':
      System_Mode_Label = ttk.Label( OperatingList_Frame, text='CHARGE' + '                  ', foreground='yellow', background='blue' )
    if mode == 'DISCHARGE':
      System_Mode_Label = ttk.Label( OperatingList_Frame, text='DISCHARGE' + '             ', foreground='white', background='red')
    if mode == 'IR_TEST':
      System_Mode_Label = ttk.Label( OperatingList_Frame, text='IR_TEST', background='cyan')

    if mode == 'FINISHED':
      System_Mode_Label = ttk.Label( OperatingList_Frame, text='                                ', background='green' )
      System_Mode_Label.grid( column=0, row=4, sticky=tk.W )
      System_Mode_Label = ttk.Label( OperatingList_Frame, text='FINISHED', foreground='white', background='green' )

    System_Mode_Label.grid( column=0, row=4, sticky=tk.W )
    System_Mode_Label.grid( padx=0, pady=0 )

  def Display_SampleCount(SampleCount):
    System_Sample_Label = ttk.Label( OperatingList_Frame, text='SAMPLE ' + str(SampleCount) + '      ', background='cyan' )
    System_Sample_Label.grid( column=0, row=5, sticky=tk.W )
    System_Sample_Label.grid( padx=0, pady=0 )

#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################

x = 2
y = 2

class GUI_Handler():
  global KeyStatus
  global MAX_USB_PORTS
  global GraphEnable

#---------------------------------------------------------------------#

  def EnterKey():
    global KeyStatus

    if KeyStatus == 'RUN':
      return
    root.update()

    EnterKey( portlist )

  enterkey = ttk.Style()
  enterkey.map("Enter.TButton",
    foreground=[('disabled', 'green'), ('active', 'yellow')],
    background=[('!disabled', 'green'), ('active', 'yellow')] )

  enterkey = ttk.Button( button, text="\n START\n(ENTER)\n", style="Enter.TButton", command=EnterKey )
  enterkey.grid( column=0, row=1, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def StopKey():
    global KeyStatus

    root.update()

    KeyStatus = 'STOP'
    BackKey( portlist )

  stop = ttk.Style()
  stop.map("Stop.TButton",
    foreground=[('disabled', 'red'), ('active', 'yellow')],
    background=[('!disabled', 'red'), ('active', 'yellow')] )

  stop = ttk.Button( button, text="\nCYCLE\n STOP\n", style="Stop.TButton", command=StopKey )
  stop.grid( column=0, row=2, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def EscapeKey():
    global KeyStatus

    root.update()

    KeyStatus = 'STOP'
    BackKey( portlist )

  escape = ttk.Style()
  escape.map("Back.TButton",
    foreground=[('disabled', 'brown'), ('active', 'yellow')],
    background=[('!disabled', 'brown'), ('active', 'yellow')] )

  escape = ttk.Button( button, text="\nESCAPE\n(MODE)\n", style="Back.TButton", command=EscapeKey )
  escape.grid( column=1, row=3, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def IncKey():
    global KeyStatus

    if KeyStatus == 'RUN':
      return
    root.update()

    IncKey( portlist )

  increment = ttk.Style()
  increment.map("Inc.TButton",
    foreground=[('disabled', 'brown'), ('active', 'yellow')],
    background=[('!disabled', 'brown'), ('active', 'yellow')] )

  increment = ttk.Button( button, text="\n   DISPLAY\nINCREMENT\n", style="Inc.TButton", command=IncKey )
  increment.grid( column=1, row=1, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def DecKey():
    global KeyStatus

    if KeyStatus == 'RUN':
      return
    root.update()

    DecKey( portlist )

  decrement = ttk.Style()
  decrement.map("Dec.TButton",
    foreground=[('disabled', 'brown'), ('active', 'yellow')],
    background=[('!disabled', 'brown'), ('active', 'yellow')] )

  decrement = ttk.Button( button, text="\n    DISPLAY\nDECCREMENT\n", style="Dec.TButton", command=DecKey )
  decrement.grid( column=1, row=2, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def CloseBotBox():
      global KeyStatus

      if KeyStatus == 'RUN':
        return
      quit()

  closebotbox = ttk.Style()
  closebotbox.map("Close.TButton",
    foreground=[('disabled', 'yellow'), ('active', 'red')],
    background=[('!disabled', 'yellow'), ('active', 'red')] )

  closebotbox = ttk.Button( button, text="\nCLOSE\nBotBox\n", style="Close.TButton", command=CloseBotBox )
  closebotbox.grid( column=0, row=3, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def InitializeComports():
    global KeyStatus

    if KeyStatus == 'RUN':
      return
    root.update()

    Initialize_Comports( baudrate )

  initcomports = ttk.Style()
  initcomports.map("Init.TButton",
    foreground=[('disabled', 'lightgreen'), ('active', 'yellow')],
    background=[('!disabled', 'lightgreen'), ('active', 'yellow')] )

  initcomports = ttk.Button( button, text="\n       INITIALIZE      \n      COMPORTS\n", style="Init.TButton", command=InitializeComports )
  initcomports.grid( column=5, row=1, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def SyncQuadChargers():
    global KeyStatus

    if KeyStatus == 'RUN':
      return
    root.update()

    Sync_Quad_Chargers( portlist )

  syncquadchargers = ttk.Style()
  syncquadchargers.map("SyncChargers.TButton",
    foreground=[('disabled', 'lightgreen'), ('active', 'yellow')],
    background=[('!disabled', 'lightgreen'), ('active', 'yellow')] )

  syncquadchargers = ttk.Button( button, text="\n          SYNC\nQUAD CHARGERS\n", style="SyncChargers.TButton", command=SyncQuadChargers )
  syncquadchargers.grid( column=5, row=2, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def StartOnePass():
    global KeyStatus

    if KeyStatus == 'RUN':
      return
    KeyStatus = 'RUN'
    root.update()

    Start_One_Cycle_Reconditioning( portlist )

  startonepass = ttk.Style()
  startonepass.map("OneCycle.TButton",
    foreground=[('disabled', 'yellow'), ('active', 'red')],
    background=[('!disabled', 'yellow'), ('active', 'red')] )

  startonepass = ttk.Button( button, text="\n  ONE PASS\n NiMH CYCLE\n",
                             style="OneCycle.TButton", command=StartOnePass )
  startonepass.grid( column=2, row=1, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def StartTwoPass():
    global KeyStatus

    if KeyStatus == 'RUN':
      return
    KeyStatus = 'RUN'
    root.update()

    Start_Two_Cycle_Reconditioning( portlist )

  starttwopass = ttk.Style()
  starttwopass.map("TwoCycle.TButton",
    foreground=[('disabled', 'yellow'), ('active', 'red')],
    background=[('!disabled', 'yellow'), ('active', 'red')] )

  starttwopass = ttk.Button( button, text="\n      TWO PASS\n     NiMH CYCLE    \n",
                             style="TwoCycle.TButton", command=StartTwoPass )
  starttwopass.grid( column=2, row=2, padx=x, pady=y, sticky=W+E )

# --------------------------------------------------------------------#

  def RunChargeAuto():
    global mode
    global KeyStatus
    global GraphEnable
    global ProfileStatus

    if KeyStatus == 'RUN':
      return
    KeyStatus = 'RUN'

    Metrics.Create_Cycle_Time_List()
    Metrics.Create_Charge_Time_List()
    Metrics.Create_Discharge_Time_List()

    root.update()

    GraphEnable = False
    print( 'Opening:  ' + CHG_FILE )
    mode = 'CHARGE'
    ProfileStatus = 'CHG_AUTO'
    Metrics.Display_Operating_Mode()

    Run_Charge_Auto( portlist, mode )

    GraphEnable = False
    print( 'Closing:  ' + CHG_FILE )
    mode = 'FINISHED'
    ProfileStatus = 'IDLE'
    Metrics.Display_Operating_Mode()

  runchargeauto = ttk.Style()
  runchargeauto .map("RunChargeAuto.TButton",
    foreground=[('disabled', 'orange'), ('active', 'yellow')],
    background=[('!disabled', 'orange'), ('active', 'yellow')] )

  runchargeauto = ttk.Button( button, text="\n            RUN\n    CHARGE AUTO    \n", style="RunChargeAuto.TButton", command=RunChargeAuto )
  runchargeauto.grid( column=3, row=1, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def RunDischargeAuto():
    global mode
    global KeyStatus
    global GraphEnable
    global ProfileStatus

    if KeyStatus == 'RUN':
      return
    KeyStatus = 'RUN'

    Metrics.Create_Cycle_Time_List()
    Metrics.Create_Charge_Time_List()
    Metrics.Create_Discharge_Time_List()

    root.update()

    GraphEnable = True
    print( 'Opening:  ' + DSC_FILE )
    mode = 'DISCHARGE'
    ProfileStatus = 'DIS_AUTO'
    Metrics.Display_Operating_Mode()
    Run_Discharge_Auto( portlist, mode )

    GraphEnable = False
    print( 'Closing:  ' + DSC_FILE )
    mode = 'FINISHED'
    ProfileStatus = 'IDLE'
    Metrics.Display_Operating_Mode()

  rundischargeauto = ttk.Style()
  rundischargeauto.map("RunDischargeAuto.TButton",
    foreground=[('disabled', 'orange'), ('active', 'yellow')],
    background=[('!disabled', 'orange'), ('active', 'yellow')] )

  rundischargeauto = ttk.Button( button, text="\n            RUN\n DISCHARGE AUTO \n", style="RunDischargeAuto.TButton", command=RunDischargeAuto )
  rundischargeauto.grid( column=3, row=2, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def RunDischargeChargeCycle():
    global KeyStatus

    if KeyStatus == 'RUN':
      return
    KeyStatus = 'RUN'
    root.update()

    Run_Discharge_Charge_Cycle( portlist )

  rundischargechargecycle = ttk.Style()
  rundischargechargecycle.map("RunDischargeChargeCycle.TButton",
    foreground=[('disabled', 'orange'), ('active', 'yellow')],
    background=[('!disabled', 'orange'), ('active', 'yellow')] )

  rundischargechargecycle = ttk.Button( button, text="\n        RUN\n DIS ---> CHG\n", style="RunDischargeChargeCycle.TButton", command=RunDischargeChargeCycle )
  rundischargechargecycle.grid( column=4, row=1, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#
  
  def Run_Load_Test():

    global KeyStatus
    global MAX_USB_PORTS
    global baudrate

    if KeyStatus == 'RUN':
      return
    root.update()

    Get_IR( MAX_USB_PORTS, baudrate )
  #  Get_Load_Voltage( MAX_USB_PORTS, baudrate )

  LoadTest = ttk.Style()
  LoadTest.map("LoadTest.TButton",
    foreground=[('disabled', 'orange'), ('active', 'yellow')],
    background=[('!disabled', 'orange'), ('active', 'yellow')] )

  LoadTest = ttk.Button( button, text="\n     RUN\nLOAD TEST\n", style="LoadTest.TButton", command=Run_Load_Test )
  LoadTest.grid( column=4, row=2, padx=x, pady=y, sticky=W+E )
  '''
#---------------------------------------------------------------------#'''

  def Plot_4X5_Profile():

    global KeyStatus
    global MAX_USB_PORTS

    if KeyStatus == 'RUN':
      return
    root.update()

    if MAX_USB_PORTS < 5:
      from Plot_1x4_Line_Graph import Plot_1x4_Line_Graph
      Plot_1x4_Line_Graph( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Dischargefile.csv" )
    else:
      from Plot_Fixed_4x5_Line_Graph import Plot_Fixed_4x5_Line_Graph
      Plot_Fixed_4x5_Line_Graph( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Dischargefile.csv" )
      
  plotdischarge = ttk.Style()
  plotdischarge.map("discharge.TButton",
    foreground=[('disabled', 'blue'), ('active', 'yellow')],
    background=[('!disabled', 'blue'), ('active', 'yellow')] )

  plotdischarge = ttk.Button( button, text="\n          Plot 4x5\n       LINE GRAPH      \n", style="discharge.TButton", command=Plot_4X5_Profile )
  plotdischarge.grid( column=2, row=4, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#

  def Plot_1X20_Profile():

    global KeyStatus
    global MAX_USB_PORTS

    if KeyStatus == 'RUN':
      return
    root.update()
    
    if MAX_USB_PORTS < 5:
      from Plot_1x4_Line_Graph import Plot_1x4_Line_Graph
      Plot_1x4_Line_Graph( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Dischargefile.csv" )
    else:
      from Plot_1x20_Line_Graph import Plot_1x20_Line_Graph
      Plot_1x20_Line_Graph( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Dischargefile.csv" )
      
  plot_1x20_Profile = ttk.Style()
  plot_1x20_Profile.map("Plot_1X20_Profile.TButton",
    foreground=[('disabled', 'blue'), ('active', 'yellow')],
    background=[('!disabled', 'blue'), ('active', 'yellow')] )

  plot_1x20_Profile = ttk.Button( button, text="\n Plot 1x20\nLINE GRAPH\n", style="Plot_1X20_Profile.TButton", command=Plot_1X20_Profile )
  plot_1x20_Profile.grid( column=4, row=4, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#
  ''
  def Plot_IR_Bar_Graph():
    global KeyStatus
    global MAX_USB_PORTS

    if KeyStatus == 'RUN':
      return
    root.update()

    if MAX_USB_PORTS < 5:
      from Plot_1x4_IR_Bar_Graph import Plot_1x4_IR_Bar_Graph
      Plot_1x4_IR_Bar_Graph( LOAD_FILE )
    else:
      from Plot_1x20_IR_Bar_Graph import Plot_1x20_IR_Bar_Graph
      Plot_1x20_IR_Bar_Graph( LOAD_FILE )
      
  plot_IR_Bar_Graph = ttk.Style()
  plot_IR_Bar_Graph.map("Plot_IR_Bar_Graph.TButton",
    foreground=[('disabled', 'blue'), ('active', 'yellow')],
    background=[('!disabled', 'blue'), ('active', 'yellow')] )

  plot_IR_Bar_Graph = ttk.Button( button, text="\n         Plot \nIR BAR GRAPH\n", style="Plot_IR_Bar_Graph.TButton", command=Plot_IR_Bar_Graph )
  plot_IR_Bar_Graph.grid( column=5, row=4, padx=x, pady=y, sticky=W+E )
  ''
#---------------------------------------------------------------------#

  def PlotBar():

    global KeyStatus
    global MAX_USB_PORTS

    if KeyStatus == 'RUN':
      return
    root.update()

    if MAX_USB_PORTS < 5:
      from Plot_1x4_Bar_Graph import Plot_1x4_Bar_Graph
      Plot_1x4_Bar_Graph( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Chargefile.csv" )
    else:
      from Plot_1x20_Bar_Graph import Plot_1x20_Bar_Graph
      Plot_1x20_Bar_Graph( "/home/greenbean/Documents/GUI/BotBox_Script/BotBox_5xI_02_01_2020/GreenBean/PlotFiles/BotBox_Chargefile.csv" )

  plotbar = ttk.Style()
  plotbar.map("Bar.TButton",
    foreground=[('disabled', 'blue'), ('active', 'yellow')],
    background=[('!disabled', 'blue'), ('active', 'yellow')] )

  plotbar = ttk.Button( button, text="\nPLOT CHARGE\n  BAR GRAPH\n", style="Bar.TButton", command=PlotBar )
  plotbar.grid( column=3, row=4, padx=x, pady=y, sticky=W+E )

#---------------------------------------------------------------------#
  '''
  def PlotdVdt():
      from Plot_Fixed_4x5_dVdt_Graph import Plot_Fixed_4x5_dVdt_Graph
      from Plot_Fixed_1x4_dVdt_Graph import Plot_Fixed_1x4_dVdt_Graph
      global KeyStatus

      if KeyStatus == 'RUN':
        return
      root.update()

      if MAX_USB_PORTS < 5:
        Plot_Fixed_1x4_dVdt_Graph( DVDT_FILE )
      else: Plot_Fixed_4x5_dVdt_Graph( DVDT_FILE )

  plotdvdt = ttk.Style()
  plotdvdt.map("dvdt.TButton",
    foreground=[('disabled', 'blue'), ('active', 'yellow')],
    background=[('!disabled', 'blue'), ('active', 'yellow')] )

  plotdvdt = ttk.Button( button, text="\n PLOT dV/dt\n LINE GRAPH\n", style="dvdt.TButton", command=PlotdVdt )
  plotdvdt.grid( column=5, row=4, padx=x, pady=y, sticky=W+E )
  '''
#---------------------------------------------------------------------#

#######################################################################
#######################################################################
#######################################################################

#---------------------------------------------------------------------#

Metrics.Create_Status_List()
Metrics.Create_Cycle_Time_List()
Metrics.Create_Charge_Time_List()
Metrics.Create_Discharge_Time_List()
Metrics.Create_Operating_List(00000)
mode = 'IDLE'
GraphEnable = False
ProfileStatus = 'IDLE'
Metrics.Display_Operating_Mode()

#---------------------------------------------------------------------#

#######################################################################
#######################################################################
#######################################################################

def main():
  root.after( 100000000, GUI_Handler )
  root.update()
  gc.enable()  # Enable gargage collection

if __name__ == '__main__':
  main()

#######################################################################
#######################################################################
#######################################################################
