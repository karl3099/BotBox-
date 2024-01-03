#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

file = "/home/greenbean/GreenBean/PlotFiles/BotBox_Plotfile.csv"

def Plot_1x20_Line_Graph( file ):

  #  Get the data from the plot file
  DISCHARGE_mAh = []
  CHARGE_mAh = []

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
  Module_16 = []
  Module_17 = []
  Module_18 = []
  Module_19 = []
  Module_20 = []

  Module =  { 0:00000, 1:00000, 2:00000, 3:00000, 4:00000, \
              5:00000, 6:00000, 7:00000, 8:00000, 9:00000, \
              10:00000, 11:00000, 12:00000, 13:00000, 14:00000, \
              15:00000, 16:00000, 17:00000, 18:00000, 19:00000 }

  f = open( file, "r+t" )
  DISCHARGE_mAh = f.readline()
  CHARGE_mAh = f.readline()
  data = f.readlines()
  f.close()

  m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, \
      m12, m13, m14, m15, m16, m17, m18, m19, m20 = DISCHARGE_mAh.split( ',' )

  Module[0] = int(m1)
  Module[1] = int(m2)
  Module[2] = int(m3)
  Module[3] = int(m4)
  Module[4] = int(m5)
  Module[5] = int(m6)
  Module[6] = int(m7)
  Module[7] = int(m8)
  Module[8] = int(m9)
  Module[9] = int(m10)
  Module[10] = int(m11)
  Module[11] = int(m12)
  Module[12] = int(m13)
  Module[13] = int(m14)
  Module[14] = int(m15)
  Module[15] = int(m16)
  Module[16] = int(m17)
  Module[17] = int(m18)
  Module[18] = int(m19)
  Module[19] = int(m20)

  Charge_High = 00000
  n = 0
  while n < 20:
    if int(Module[n]) > Charge_High:
      Charge_High = int(Module[n])
    n += 1
  Charge_High = Charge_High * 5

#------------------------------------------------------------#

  #  Find the 'X' axis multiplier
  for Line in data:
      if len( Line ) > 0:
          #  Here, we are only concerned with finding
          #  the last (highest) value of 'X'
          X_Max, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, \
             y11, y12, y13, y14, y15, y16, y17, y18, y19, y20 = Line.split( ',' )

#------------------------------------------------------------#

  p = format( 1 / int(X_Max), '0.16f')

#  Plot the module volltage
  for Line in data:
     if len( Line ) > 0:
       x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, \
          y11, y12, y13, y14, y15, y16, y17, y18, y19, y20,  = Line.split( ',' )

#       p = format( int(x) / int(X_Max), '0.16f')
#       X_Axis.append( float(Charge_High) * float(p) ) 

       X_Axis.append( float(Charge_High) * (float( int(x) * float(p))) ) 

       Module_1.append( float(y1) )
       Module_2.append( float(y2) )
       Module_3.append( float(y3) )
       Module_4.append( float(y4) )
       Module_5.append( float(y5) )
       Module_6.append( float(y6) )
       Module_7.append( float(y7) )
       Module_8.append( float(y8) )
       Module_9.append( float(y9) )
       Module_10.append( float(y10) )
       Module_11.append( float(y11) )
       Module_12.append( float(y12) )
       Module_13.append( float(y13) )
       Module_14.append( float(y14) )
       Module_15.append( float(y15) )
       Module_16.append( float(y16) )
       Module_17.append( float(y17) )
       Module_18.append( float(y18) )
       Module_19.append( float(y19) )
       Module_20.append( float(y20) )

  Plot, axis = plt.subplots()
  axis.clear()
  axis.set_title(file)
  axis.set_xlim( 0, Charge_High )
  axis.set_xlabel( "\nAMPERE HOURS" )
  axis.set_ylim( 6.01, 8.75 )
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

  line16, = axis.plot(X_Axis, Module_16, lw=1.0, color='red', label='Module 16')
  line17, = axis.plot(X_Axis, Module_17, lw=1.0, color='green', label='Module 17')
  line18, = axis.plot(X_Axis, Module_18, lw=1.0, color='orange', label='Module 18')
  line19, = axis.plot(X_Axis, Module_19, lw=1.0, color='blue', label='Module 19')
  line20, = axis.plot(X_Axis, Module_20, lw=1.0, color='gray', label='Module 20')

  leg = axis.legend(loc=(1.005, 0.05), fancybox=True, shadow=True)
  leg.get_frame().set_alpha(0.9)

  """
     We will set up a dict, mapping the legend line to the plot line,
     then the line picker == instantated
  """

  lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, \
           line11, line12, line13, line14, line15, line16, line17, line18, line19, line20 ]
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
  Plot_1x20_Line_Graph( file )
