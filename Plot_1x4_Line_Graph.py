#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

file = "/home/carl/GreenBean/PlotFiles/BotBox_Dischargefile.csv"

def Plot_1x4_Line_Graph( file ):

  x = 0

  #  Get the data from the plot file
  DISCHARGE_mAh = []
  CHARGE_mAh = []

  X_Axis = []
  Module_1 = []
  Module_2 = []
  Module_3 = []
  Module_4 = []

  Module =  { 0:00000, 1:00000, 2:00000, 3:00000 }

  f = open( file, "r+t" )
  DISCHARGE_mAh = f.readline()
  data = f.readlines()
  f.close()

  m1, m2, m3, m4 = DISCHARGE_mAh.split( ',' )

  Module[0] = int(m1)*5
  Module[1] = int(m2)*5
  Module[2] = int(m3)*5
  Module[3] = int(m4)*5

  #  Get the module maximum Ampere Hours
  MaxCharge = 00000
  n = 0
  while n < 4:
    if int(Module[n]) > MaxCharge:
      MaxCharge = int(Module[n])
    n += 1
  #  print('Module', n, 'Maximum Charge =', MaxCharge)

#------------------------------------------------------------#

  #  Find the 'X' axis multiplier
  for Line in data:
      if len( Line ) > 0:
          #  Here, we are only concerned with 'X'
          #  the last (highest) value of 'X'
          x, y1, y2, y3, y4 = Line.split( ',' )

  if MaxCharge != 0.00:
      p = format(MaxCharge / float(x), '0.16f')
  else: p = 0
  #  print('P = ', p)

#------------------------------------------------------------#

#  Plot the module volltage 
  for Line in data:
      if len( Line ) > 0:
          x, m1, m2, m3, m4  = Line.split( ',' )

          if x == 0:
            x = 1
          q = format(float(x) / MaxCharge, '0.16f')
          c = format((MaxCharge * float(p)) * float(q), '0.2f')
          #  print('C = ', c)

          X_Axis.append( float(c) )
          Module_1.append( float(m1) )
          Module_2.append( float(m2) )
          Module_3.append( float(m3) )
          Module_4.append( float(m4) )

  Plot, axis = plt.subplots()
  axis.clear()
  axis.set_title(file)
  axis.set_xlim( 0, MaxCharge )
  axis.set_xlabel( "\nAMPERE HOURS" )
  axis.set_ylim( 6.01, 8.75 )
  axis.set_ylabel( "Ch1 - Ch4\n Volts" )
  axis.grid(True, linewidth=0.5, color='#aaaaaa', linestyle='-')

  line1, = axis.plot( X_Axis, Module_1, lw=1.0, color='red', label='Module 1' )
  line2, = axis.plot( X_Axis, Module_2, lw=1.0, color='green', label='Module 2' )
  line3, = axis.plot( X_Axis, Module_3, lw=1.0, color='orange', label='Module 3' )
  line4, = axis.plot( X_Axis, Module_4, lw=1.0, color='gray', label='Module 4' )

  leg = axis.legend( loc=(0.875, 0.8), fancybox=True, shadow=True )
  leg.get_frame().set_alpha(0.9)

  """
     We will set up a dict, mapping the legend line to the plot line,
     then the line picker == instantated
  """
  lines = [line1, line2, line3, line4 ]
  lined = dict()
  for legline, origline in zip(leg.get_lines(), lines):
    legline.set_picker(5)  # 5 pts tolerance
    lined[legline] = origline

  def onpick(event):
    """
       On the pick event, find the plot line corresponding to the
       mapped legend line, and toggle the visibility of the plot line
    """
    legline = event.artist
    origline = lined[legline]
    vis = not origline.get_visible()
    origline.set_visible(vis)
    """
       Change the legend line intensity when that line has been clicked,
       so we can tell which legend lines have been toggled
    """
    if vis:
        legline.set_alpha(1.0)
    else:
        legline.set_alpha(0.5)
    Plot.canvas.draw()

  Plot.canvas.mpl_connect('pick_event', onpick)

  plt.show()

if __name__ == '__main__':
  Plot_1x4_Line_Graph( file )
