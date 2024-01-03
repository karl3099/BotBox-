#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

file = "/home/greenbean/Desktop/PlotFiles/BotBox_Dischargefile.csv"

def Plot_1x15_Line_Graph( file ):

  #  Get the data from the plot file
  DISCHARGE_mAh = []

  f = open( file, "r+t" )
  DISCHARGE_mAh = f.readline()
#  print('Maximum Charge = ', DISCHARGE_mAh)
  data = f.readlines()
  f.close()

#------------------------------------------------------------#
#  Find the module with the highest charge 

  Module =  { 0:00000, 1:00000, 2:00000, 3:00000, 4:00000, \
              5:00000, 6:00000, 7:00000, 8:00000, 9:00000, \
              10:00000, 11:00000, 12:00000, 13:00000, 14:00000 }

  m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, \
      m12, m13, m14, m15 = DISCHARGE_mAh.split( ',' )

  Module[0] = int(m1)*2
  Module[1] = int(m1)*2
  Module[2] = int(m1)*2
  Module[3] = int(m1)*2
  Module[4] = int(m1)*2
  Module[5] = int(m1)*2
  Module[6] = int(m1)*2
  Module[7] = int(m1)*2
  Module[8] = int(m1)*2
  Module[9] = int(m1)*2
  Module[10] = int(m1)*2
  Module[11] = int(m1)*2
  Module[12] = int(m1)*2
  Module[13] = int(m1)*2
  Module[14] = int(m1)*2

  #  Get the module maximum Ampere Hours
  MaxCharge = 00000
  n = 0
  while n < 20:
    if int(Module[n]) > MaxCharge:
      MaxCharge = int(Module[n])
    n += 1
  #  print('Module', n, 'Maximum Charge =', MaxCharge)

  #  Find the 'X' axis multiplier
  for Line in data:
      if len( Line ) > 0:
          #  Here, we are only concerned with finding
          #  the last (highest) value of 'X'
          x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, \
             y11, y12, y13, y14, y15 = Line.split( ',' )

  if MaxCharge != 0.00:
      p = format(MaxCharge / float(x), '0.16f')
  else: p = 0

#  MaxCharge = MaxCharge * 2
  #  print('P = ', p)

# ******************************************************************************** #
#------------------------------------------------------------#
#  Plot the module volltage

  X_Axis = []
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

  for Line in data:
      if len( Line ) > 0:
          x, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, \
             m11, m12, m13, m14, m15 = Line.split( ',' )

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
      Module_5.append( float(m5) )
      Module_6.append( float(m6) )
      Module_7.append( float(m7) )
      Module_8.append( float(m8) )
      Module_9.append( float(m9) )
      Module_10.append( float(m10) )
      Module_11.append( float(m11) )
      Module_12.append( float(m12) )
      Module_13.append( float(m13) )
      Module_14.append( float(m14) )
      Module_15.append( float(m15) )

  Plot, axis = plt.subplots()
  axis.clear()
  axis.set_title(file)
  axis.set_xlim( 0, MaxCharge )
  axis.set_xlabel( "\nAMPERE HOURS" )
  axis.set_ylim( 8.01, 9.75 )
  axis.set_ylabel( "Ch1-Ch20\n Volts" )
  axis.grid(True, linewidth=0.5, color='#aaaaaa', linestyle='-')

  line1, = axis.plot(X_Axis, Module_1, lw=1.0, color='red', label='Module 1')
  line2, = axis.plot(X_Axis, Module_2, lw=1.0, color='green', label='Module 2')
  line3, = axis.plot(X_Axis, Module_3, lw=1.0, color='orange', label='Module 3')
  line4, = axis.plot(X_Axis, Module_4, lw=1.0, color='blue', label='Module 4')
  line5, = axis.plot(X_Axis, Module_5, lw=1.0, color='gray', label='Module 5')

  line6, = axis.plot(X_Axis, Module_6, lw=1.0, color='red', label='Module 6')
  line7, = axis.plot(X_Axis, Module_7, lw=1.0, color='green', label='Module 7')
  line8, = axis.plot(X_Axis, Module_8, lw=1.0, color='orange', label='Module 8')
  line9, = axis.plot(X_Axis, Module_9, lw=1.0, color='blue', label='Module 9')
  line10, = axis.plot(X_Axis, Module_10, lw=1.0, color='gray', label='Module 10')

  line11, = axis.plot(X_Axis, Module_11, lw=1.0, color='red', label='Module 11')
  line12, = axis.plot(X_Axis, Module_12, lw=1.0, color='green', label='Module 12')
  line13, = axis.plot(X_Axis, Module_13, lw=1.0, color='orange', label='Module 13')
  line14, = axis.plot(X_Axis, Module_14, lw=1.0, color='blue', label='Module 14')
  line15, = axis.plot(X_Axis, Module_15, lw=1.0, color='gray', label='Module 15')

  leg = axis.legend(loc=(1.005, 0.05), fancybox=True, shadow=True)
  leg.get_frame().set_alpha(0.9)

  """
     We will set up a dict, mapping the legend line to the plot line,
     then the line picker == instantated
  """

  lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, \
           line11, line12, line13, line14, line15 ]
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
  Plot_1x15_Line_Graph( file )
