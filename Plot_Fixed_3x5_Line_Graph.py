#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

file = "/home/greenbean/GreenBean/BotBox_Dischargefile.csv"

def Plot_Fixed_3x5_Line_Graph( file ):

  Ah_D = []
  X_Axis = []

  Plot = plt.figure()
  axis1 = Plot.add_subplot( 4, 1, 1 )
  axis2 = Plot.add_subplot( 4, 1, 2 )
  axis3 = Plot.add_subplot( 4, 1, 3 )

  f = open( file,"r+t" )
  Ah_D = f.readline()
  Volts = f.readlines()
  f.close()

#----------------------------------------------------------------------------------
# Find the plot line with the highest mAh in the profile.
# This will be used to scale the 'X' axis of the graph.

  Module_Ah =  { 0: 00000, 1: 00000, 2: 00000, 3: 00000, 4: 00000, \
                 5: 00000, 6: 00000, 7: 00000, 8: 00000, 9: 00000, \
                10: 00000, 11: 00000, 12: 00000, 13: 00000, 14: 00000, \

  mAh1, mAh2, mAh3, mAh4, mAh5, mAh6, mAh7, mAh8, mAh9, mAh10, mAh11, mAh12, \
        mAh13, mAh14, mAh15 = Ah_D.split ( ',' )

  Module_Ah[0] = mAh1
  Module_Ah[1] = mAh2
  Module_Ah[2] = mAh3
  Module_Ah[3] = mAh4
  Module_Ah[4] = mAh5
  Module_Ah[5] = mAh6
  Module_Ah[6] = mAh7
  Module_Ah[7] = mAh8
  Module_Ah[8] = mAh9
  Module_Ah[9] = mAh10
  Module_Ah[10] = mAh11
  Module_Ah[11] = mAh12
  Module_Ah[12] = mAh13
  Module_Ah[13] = mAh14
  Module_Ah[14] = mAh15
 
  n = 0
  Charge_High = int(Module_Ah[0])
  n += 1
  while n < 20:
    if int(Module_Ah[n]) >  Charge_High:
      Charge_High = int(Module_Ah[n])
    n += 1

  if Charge_High == 0:
    Charge_High = 1
  else: Charge_High = Charge_High * 2

#----------------------------------------------------------------------------------

  Ah_D1, Ah_D2, Ah_D3, Ah_D4, Ah_D5, Ah_D6, Ah_D7, Ah_D8, Ah_D9, Ah_D10, \
  Ah_D11, Ah_D12, Ah_D13, Ah_D14, Ah_D15 = Ah_D.split( ',' )

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

  Module =  [ Module_1, Module_2, Module_3, Module_4, Module_5, \
              Module_6, Module_7, Module_8, Module_9, Module_10, \
              Module_11, Module_12, Module_13, Module_14, Module_15 ]

#----------------------------------------------------------------------------------
# Here, we are just looking for the last value of 'X'.

  for Line in Volts:
    if len( Line ) > 0:
      x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15 = Line.split( ',' )

      if x == 0:
        x = 1
      p = format(Charge_High / float(x), '0.16f')

#  print('P =', p, '\tq =', q, '\tc =', c)

#----------------------------------------------------------------------------------

  for Line in Volts:
    if len( Line ) > 0:
      x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15 = Line.split( ',' )

      q = format(float(x) / Charge_High, '0.16f')
      c = format((Charge_High * float(p)) * float(q), '0.2f')
      X_Axis_4.append( float(c) ) 

      Module[0].append( float(y1) )
      Module[1].append( float(y2) )
      Module[2].append( float(y3) )
      Module[3].append( float(y4) )
      Module[4].append( float(y5) )
      Module[5].append( float(y6) )
      Module[6].append( float(y7) )
      Module[7].append( float(y8) )
      Module[8].append( float(y9) )
      Module[9].append( float(y10) )
      Module[10].append( float(y11) )
      Module[11].append( float(y12) )
      Module[12].append( float(y13) )
      Module[13].append( float(y14) )
      Module[14].append( float(y15) )

  axis1.clear()

  axis1.set_title( file )
  axis1.set_xlim( 0, Charge_High )
  axis1.set_xlabel( "MILIAMPERE HOURS" )
  axis1.set_ylim( 8.001, 12.00 )
  axis1.set_ylabel( "Ch1-Ch5\n VOLTS" )
  axis1.grid(True, linewidth=1.0, color='#aaaaaa', linestyle='-')

  m1, = axis1.plot( X_Axis_4, Module[0], lw=1.0, color='red', label='Module 1' )
  m2, = axis1.plot( X_Axis_4, Module[1], lw=1.0, color='green', label='Module 2' )
  m3, = axis1.plot( X_Axis_4, Module[2], lw=1.0, color='orange', label='Module 3' )
  m4, = axis1.plot( X_Axis_4, Module[3], lw=1.0, color='blue', label='Module 4' )
  m5, = axis1.plot( X_Axis_4, Module[4], lw=1.0, color='gray', label='Module 5' )

  axis2.clear()
  axis2.set_xlim( 0, Charge_High )
  axis2.set_xlabel( "MILIAMPERE HOURS" )
  axis2.set_ylim( 8.001, 12.00 )
  axis2.set_ylabel( "Ch6-Ch10\n VOLTS" )
  axis2.grid(True, linewidth=1.0, color='#aaaaaa', linestyle='-')

  m6, = axis2.plot( X_Axis_4, Module[5], lw=1.0, color = 'red' )
  m7, = axis2.plot( X_Axis_4, Module[6], lw=1.0, color = 'green' )
  m8, = axis2.plot( X_Axis_4, Module[7], lw=1.0, color = 'orange' )
  m9, = axis2.plot( X_Axis_4, Module[8], lw=1.0, color = 'blue' )
  m10, = axis2.plot( X_Axis_4, Module[9], lw=1.0, color = 'gray' )

  axis3.clear()
  axis3.set_xlim( 0, Charge_High )
  axis3.set_xlabel( "MILIAMPERE HOURS" )
  axis3.set_ylim( 8.001, 12.00 )
  axis3.set_ylabel( "Ch11-Ch15\n VOLTS" )
  axis3.grid(True, linewidth=1.0, color='#aaaaaa', linestyle='-')

  m11, = axis3.plot( X_Axis_4, Module[10], lw=1.0, color = 'red' )
  m12, = axis3.plot( X_Axis_4, Module[11], lw=1.0, color = 'green' )
  m13, = axis3.plot( X_Axis_4, Module[12], lw=1.0, color = 'orange' )
  m14, = axis3.plot( X_Axis_4, Module[13], lw=1.0, color = 'blue' )
  m15, = axis3.plot( X_Axis_4, Module[14], lw=1.0, color = 'gray' )

  Plot.legend( ( m1, m2, m3, m4, m5 ),
               ( 'Ch 1: ' + str(int(Ah_D1)*2) + ' mAh',
                 'Ch 2: ' + str(int(Ah_D2)*2) + ' mAh',
                 'Ch 3: ' + str(int(Ah_D3)*2) + ' mAh',
                 'Ch 4: ' + str(int(Ah_D4)*2) + ' mAh',
                 'Ch 5: ' + str(int(Ah_D5)*2) + ' mAh' ), loc=(0.83,0.72) )

  Plot.legend( ( m6, m7, m8, m9, m10 ),
               ( 'Ch 6: ' + str(int(Ah_D6)*2) + ' mAh',
                 'Ch 7: ' + str(int(Ah_D7)*2) + ' mAh',
                 'Ch 8: ' + str(int(Ah_D8)*2) + ' mAh',
                 'Ch 9: ' + str(int(Ah_D9)*2) + ' mAh',
                 'Ch 10: ' + str(int(Ah_D10)*2) + ' mAh' ), loc=(0.83,0.52) )

  Plot.legend( ( m11, m12, m13, m14, m15 ),
               ( 'Ch 11: ' + str(int(Ah_D11)*2) + ' mAh',
                 'Ch 12: ' + str(int(Ah_D12)*2) + ' mAh',
                 'Ch 13: ' + str(int(Ah_D13)*2) + ' mAh',
                 'Ch 14: ' + str(int(Ah_D14)*2) + ' mAh',
                 'Ch 15: ' + str(int(Ah_D15)*2) + ' mAh' ), loc=(0.83,0.32) )

  Plot.show()

if __name__ == '__main__':
  Plot_Fixed_3x5_Line_Graph( file )
