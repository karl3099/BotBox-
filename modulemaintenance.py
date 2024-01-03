import os
import io
import sys
import time
import timeit
import glob
import serial
import serial.tools.list_ports as port_list

from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk



ports = []
portslist = {}
PortList = {}

#global MAX_USB_PORTS
MAX_USB_PORTS = 0

#global baudrate
baudrate = 115200

TestModule = 1
x = 2
y = 2

#######################################################################
#######################################################################
#######################################################################

#---------------------------------------------------------------------#
def List_Comports( portlist ):
  global MAX_USB_PORTS

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
#    time.sleep( 0.1 )
    n += 1
#    print ( 'Module Address:', address )
    PortList[ int(address)-1 ] = comport.port # zero counts as a place holder

  List_Comports( PortList )

  return PortList
#---------------------------------------------------------------------#

#######################################################################
#######################################################################
#######################################################################

portlist = Initialize_Comports( baudrate )

#######################################################################
#######################################################################
#######################################################################

#---------------------------------------------------------------------#
def GetAddress( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'getaddress\n' )
  while port.out_waiting > 0:
    pass
  time.sleep( 0.05 )

  address = int( port.readline() )
  print ( 'Module Address:', address )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def EnterKey( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'enter\n' )
  while port.out_waiting > 0:
    pass
  time.sleep( 0.05 )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def BackKey( portlist, port ):
  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'mode\n' )

  while port.out_waiting > 0:
    pass
  time.sleep( 0.05 )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def IncKey( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'increment\n' )

  while port.out_waiting > 0:
    pass
  time.sleep( 0.05 )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def DecKey( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'decrement\n' )

  while port.out_waiting > 0:
    pass
  time.sleep( 0.05 )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def Seek_NiMH( portlist, port ):

  DecKey( portlist, port )
  time.sleep(0.105)

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'getnimhdisplay\n' )
  while port.out_waiting > 0:
    pass
  time.sleep(0.05)
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def Green_LED_On( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'greenledon\n' ) # Ensure charge LED == inactive
  while port.out_waiting > 0:
    pass
  time.sleep(0.05)
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def Green_LED_Off( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'greenledoff\n' ) # Ensure charge LED == inactive
  while port.out_waiting > 0:
    pass
  time.sleep(0.05)
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def Blue_LED_On( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'blueledon\n' ) # Ensure charge LED == inactive
  while port.out_waiting > 0:
    pass
  time.sleep(0.05)
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def Blue_LED_Off( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'blueledoff\n' ) # Ensure charge LED == inactive
  while port.out_waiting > 0:
    pass
  time.sleep(0.05)
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def Yellow_LED_On( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'yellowledon\n' ) # Ensure charge LED == inactive
  while port.out_waiting > 0:
    pass
  time.sleep(0.05)
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def Yellow_LED_Off( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'yellowledoff\n' ) # Ensure charge LED == inactive
  while port.out_waiting > 0:
    pass
  time.sleep(0.05)
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def Red_LED_On( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'redledon\n' ) # Ensure charge LED == inactive
  while port.out_waiting > 0:
    pass
  time.sleep(0.05)
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
def Red_LED_Off( portlist, port ):

  port = serial.Serial( portlist[port], baudrate, timeout = 0 )
  port.write( b'redledoff\n' ) # Ensure charge LED == inactive
  while port.out_waiting > 0:
    pass
  time.sleep(0.05)
#---------------------------------------------------------------------#

#######################################################################
#######################################################################
#######################################################################

#---------------------------------------------------------------------#
def SetModule( module ):
  global TestModule
  TestModule = module
#---------------------------------------------------------------------#

#######################################################################
#######################################################################
#######################################################################

#---------------------------------------------------------------------#
root = tk.Tk()
root.title( "Green Bean Battery   40 Channel Profiler" )
root.resizable( width=False, height=False )

mainframe = ttk.Frame( root, padding="5 5 5 5" )
mainframe.grid( column=0, row=0, sticky=( N, W, E, S ) )
mainframe.columnconfigure( 0, weight=1 )
mainframe.rowconfigure( 0, weight=1 )

button = ttk.LabelFrame( mainframe, text=' MAINTENENCE CENTER ')
button.grid( column=0, row=0, padx=5, pady=5, sticky=tk.W )

number = tk.StringVar()
module = ttk.Combobox( button, width=2, textvariable=number, state='readonly' )
module['value'] = ( 1, 2, 3, 4 )
module.grid( column=0, row=0 )
module.current( 0 ) # Modules 0 ---> 3
SetModule( module.get() )
root.mainloop
#---------------------------------------------------------------------#

#######################################################################
#######################################################################
#######################################################################

#---------------------------------------------------------------------#
class TestButtons():

#---------------------------------------------------------------------#
  def GetModule():
    root.update()

    SetModule( module.get() )

  moduleselect = ttk.Style()
  moduleselect.map("GetModule.TButton",
    foreground=[('!active', 'black'), ('active', 'black')],
    background=[('!active', 'lightgray'), ('active', 'yellow')] )

  moduleselect = ttk.Button( button, text="SELECT MODULE", style="GetModule.TButton", command=GetModule )
  moduleselect.grid( column=1, row=0, padx=2, pady=2, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def InitializeComports():
    root.update()

    Initialize_Comports( baudrate )

  initcomports = ttk.Style()
  initcomports.map("Init.TButton",
    foreground=[('disabled', 'BLACK'), ('active', 'BLACK')],
    background=[('!disabled', 'lightgrAY'), ('active', 'yellow')] )

  initcomports = ttk.Button( button, text="INITIALIZE COMPORTS", style="Init.TButton", command=InitializeComports )
  initcomports.grid( column=1, row=1, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def GetAddress():
    root.update()

    GetAddress( portlist, int(TestModule)-1 )

  getaddress = ttk.Style()
  getaddress.map("GetAddress.TButton",
    foreground=[('!active', 'black'), ('active', 'black')],
    background=[('!active', 'lightgray'), ('active', 'yellow')] )

  getaddress = ttk.Button( button, text="GET ADDRESS", style="GetAddress.TButton", command=GetAddress )
  getaddress.grid( column=1, row=2, padx=3, pady=2, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def EnterKey():
    root.update()

    EnterKey( portlist, int(TestModule)-1 )

  enterkey = ttk.Style()
  enterkey.map("Enter.TButton",
    foreground=[('disabled', 'green'), ('active', 'yellow')],
    background=[('!disabled', 'green'), ('active', 'yellow')] )

  enterkey = ttk.Button( button, text="START / ENTER", style="Enter.TButton", command=EnterKey )
  enterkey.grid( column=1, row=3, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def IncKey():
    root.update()

    IncKey( portlist, int(TestModule)-1 )

  increment = ttk.Style()
  increment.map("Inc.TButton",
    foreground=[('disabled', 'brown'), ('active', 'yellow')],
    background=[('!disabled', 'brown'), ('active', 'yellow')] )

  increment = ttk.Button( button, text="INCREMENT", style="Inc.TButton", command=IncKey )
  increment.grid( column=1, row=4, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def DecKey():
    root.update()

    DecKey( portlist, int(TestModule)-1 )

  decrement = ttk.Style()
  decrement.map("Dec.TButton",
    foreground=[('disabled', 'brown'), ('active', 'yellow')],
    background=[('!disabled', 'brown'), ('active', 'yellow')] )

  decrement = ttk.Button( button, text="DECCREMENT", style="Dec.TButton", command=DecKey )
  decrement.grid( column=1, row=5, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def EscapeKey():
    root.update()

    BackKey( portlist, int(TestModule)-1 )

  escape = ttk.Style()
  escape.map("Back.TButton",
    foreground=[('disabled', 'brown'), ('active', 'yellow')],
    background=[('!disabled', 'brown'), ('active', 'yellow')] )

  escape = ttk.Button( button, text="ESCAPE / MODE", style="Back.TButton", command=EscapeKey )
  escape.grid( column=1, row=6, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def SeekNiMH():
    root.update()

    Seek_NiMH( portlist, int(TestModule)-1 )

  seeknimh = ttk.Style()
  seeknimh.map("seeknimh.TButton",
    foreground=[('disabled', 'brown'), ('active', 'yellow')],
    background=[('!disabled', 'brown'), ('active', 'yellow')] )

  seeknimh = ttk.Button( button, text="SEEK NiMH", style="seeknimh.TButton", command=SeekNiMH )
  seeknimh.grid( column=1, row=7, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def GreenLED_On():
    root.update()

    Green_LED_On( portlist, int(TestModule)-1 )

  greenledon = ttk.Style()
  greenledon.map("GreenLEDOn.TButton",
    foreground=[('disabled', 'green'), ('active', 'black')],
    background=[('!disabled', 'green'), ('active', 'black')] )

  greenledon = ttk.Button( button, text="TURN GREEN LED ON", style="GreenLEDOn.TButton", command=GreenLED_On )
  greenledon.grid( column=2, row=0, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def GreenLED_Off():
    root.update()

    Green_LED_Off( portlist, int(TestModule)-1 )

  greenledoff = ttk.Style()
  greenledoff.map("GreenLEDOff.TButton",
    foreground=[('disabled', 'green'), ('active', 'black')],
    background=[('!disabled', 'green'), ('active', 'black')] )

  greenledoff = ttk.Button( button, text="TURN GREEN LED OFF", style="GreenLEDOff.TButton", command=GreenLED_Off )
  greenledoff.grid( column=2, row=1, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def BlueLED_On():
    root.update()

    Blue_LED_On( portlist, int(TestModule)-1 )

  blueledon = ttk.Style()
  blueledon.map("BlueLEDOn.TButton",
    foreground=[('disabled', 'blue'), ('active', 'black')],
    background=[('!disabled', 'blue'), ('active', 'black')] )

  blueledon = ttk.Button( button, text="TURN BLUE LED ON", style="BlueLEDOn.TButton", command=BlueLED_On )
  blueledon.grid( column=2, row=2, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def BlueLED_Off():
    root.update()

    Blue_LED_Off( portlist, int(TestModule)-1 )

  blueledoff = ttk.Style()
  blueledoff.map("BlueLEDOff.TButton",
    foreground=[('disabled', 'blue'), ('active', 'black')],
    background=[('!disabled', 'blue'), ('active', 'black')] )

  blueledoff = ttk.Button( button, text="TURN BLUE LED OFF", style="BlueLEDOff.TButton", command=BlueLED_Off )
  blueledoff.grid( column=2, row=3, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def YellowLED_On():
    root.update()

    Yellow_LED_On( portlist, int(TestModule)-1 )

  yellowledon = ttk.Style()
  yellowledon.map("YellowLEDOn.TButton",
    foreground=[('disabled', 'yellow'), ('active', 'black')],
    background=[('!disabled', 'yellow'), ('active', 'black')] )

  yellowledon = ttk.Button( button, text="TURN YELLOW LED ON", style="YellowLEDOn.TButton", command=YellowLED_On )
  yellowledon.grid( column=2, row=4, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def YellowLED_Off():
    root.update()

    Yellow_LED_Off( portlist, int(TestModule)-1 )

  yellowledoff = ttk.Style()
  yellowledoff.map("YellowLEDOff.TButton",
    foreground=[('disabled', 'yellow'), ('active', 'black')],
    background=[('!disabled', 'yellow'), ('active', 'black')] )

  yellowledoff = ttk.Button( button, text="TURN YELLOW LED OFF", style="YellowLEDOff.TButton", command=YellowLED_Off )
  yellowledoff.grid( column=2, row=5, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def RedLED_On():
    root.update()

    Red_LED_On( portlist, int(TestModule)-1 )

  redledon = ttk.Style()
  redledon.map("RedLEDOn.TButton",
    foreground=[('disabled', 'red'), ('active', 'black')],
    background=[('!disabled', 'red'), ('active', 'black')] )

  reledon = ttk.Button( button, text="TURN RED LED ON", style="RedLEDOn.TButton", command=RedLED_On )
  reledon.grid( column=2, row=6, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def RedLED_Off():
    root.update()

    Red_LED_Off( portlist, int(TestModule)-1 )

  redledoff = ttk.Style()
  redledoff.map("RedLEDOff.TButton",
    foreground=[('disabled', 'red'), ('active', 'black')],
    background=[('!disabled', 'red'), ('active', 'black')] )

  redledoff = ttk.Button( button, text="TURN RED LED OFF", style="RedLEDOff.TButton", command=RedLED_Off )
  redledoff.grid( column=2, row=7, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
  def CloseMaintenance():
    exit()

  closemaintenance = ttk.Style()
  closemaintenance.map("CloseMaintenance.TButton",
    foreground=[('disabled', 'yellow'), ('active', 'red')],
    background=[('!disabled', 'yellow'), ('active', 'red')] )

  closemaintenance = ttk.Button( button, text="CLOSE MAINTENaNCE", style="CloseMaintenance.TButton", command=CloseMaintenance )
  closemaintenance.grid( column=1, row=8, padx=x, pady=y, sticky=W+E )
#---------------------------------------------------------------------#

#######################################################################
#######################################################################
#######################################################################

def main():
  root.after( 100000000, TestButtons )
  root.update()

if __name__ == '__main__':
  main()
