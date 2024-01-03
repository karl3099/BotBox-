#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

file = "/home/greenbean/GreenBean/PlotFiles/BotBox_dVdtfile.csv"

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

Module = [ Module_1, Module_2, Module_3, Module_4, Module_5, \
           Module_6, Module_7, Module_8, Module_9, Module_10, \
           Module_11, Module_12, Module_13, Module_14, Module_15 ]

def Plot_Fixed_1x20_dVdt_Graph( file ):

  #  Get the data from the plot file
  DISCHARGE_mAh = []
  CHARGE_mAh = []
  X_Axis_4 = []

  Ah_D = []

  Plot = plt.figure()
  axis1 = Plot.add_subplot( 4, 1, 1 )
  axis2 = Plot.add_subplot( 4, 1, 2 )
  axis3 = Plot.add_subplot( 4, 1, 3 )

  f = open( file,"r+t" )
  Ah_D = f.readline()
  dVdt = f.readlines()
  f.close()

  '''
  Module_Ah =  { 0: 00000, 1: 00000, 2: 00000, 3: 00000, 4: 00000, \
                 5: 00000, 6: 00000, 7: 00000, 8: 00000, 1: 00000, \
                10: 00000, 11: 00000, 12: 00000, 13: 00000, 14: 00000 }

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
  if Charge_High = 0:
    Charge_High = 1

  Ah_D1, Ah_D2, Ah_D3, Ah_D4, Ah_D5, Ah_D6, Ah_D7, Ah_D8, Ah_D9, Ah_D10, \
  Ah_D11, Ah_D12, Ah_D13, Ah_D14, Ah_D15 = Ah_D.split( ',' )

  for Line in dVdt:
    if len( Line ) > 0:
      x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15 = Line.split( ',' )
    if Charge_High = 0:
      Charge_High = 1

      p = format(Charge_High / float(x), '0.16f')
      q = format(float(x) / Charge_High, '0.16f')
  '''
  print(dVdt)
  for Line in dVdt:
    if len( Line ) > 0:

      x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15 = Line.split( ',' )

#      c = format((Charge_High * float(p)) * float(q), '0.2f')

      X_Axis_4.append( int(x) ) 
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

  axis1.set_xlim( 0, int(x) )
  axis1.set_xlabel( "SAMPLES" )
  axis1.set_ylim( 0.00, 1.00 )
  axis1.set_ylabel( "Ch1-Ch5\n dVdt" )

  m1, = axis1.plot( X_Axis_4, Module[0], lw=1.0, color = 'red' )
  m2, = axis1.plot( X_Axis_4, Module[1], lw=1.0, color = 'green' )
  m3, = axis1.plot( X_Axis_4, Module[2], lw=1.0, color = 'orange' )
  m4, = axis1.plot( X_Axis_4, Module[3], lw=1.0, color = 'blue' )
  m5, = axis1.plot( X_Axis_4, Module[4], lw=1.0, color = 'gray' )

  axis2.clear()
  axis2.set_xlim( 0, int(x) )
  axis2.set_xlabel( "SAMPLES" )
  axis2.set_ylim( 0.00, 1.00 )
  axis2.set_ylabel( "Ch6-Ch10\n dVdt" )

  m6, = axis2.plot( X_Axis_4, Module[5], lw=1.0, color = 'red' )
  m7, = axis2.plot( X_Axis_4, Module[6], lw=1.0, color = 'green' )
  m8, = axis2.plot( X_Axis_4, Module[7], lw=1.0, color = 'orange' )
  m9, = axis2.plot( X_Axis_4, Module[8], lw=1.0, color = 'blue' )
  m10, = axis2.plot( X_Axis_4, Module[9], lw=1.0, color = 'gray' )

  axis3.clear()
  axis3.set_xlim( 0, int(x) )
  axis3.set_xlabel( "SAMPLES" )
  axis3.set_ylim( 0.00, 1.00 )
  axis3.set_ylabel( "Ch11-Ch15\n dVdt" )

  m11, = axis3.plot( X_Axis_4, Module[10], lw=1.0, color = 'red' )
  m12, = axis3.plot( X_Axis_4, Module[11], lw=1.0, color = 'green' )
  m13, = axis3.plot( X_Axis_4, Module[12], lw=1.0, color = 'orange' )
  m14, = axis3.plot( X_Axis_4, Module[13], lw=1.0, color = 'blue' )
  m15, = axis3.plot( X_Axis_4, Module[14], lw=1.0, color = 'gray' )


  Plot.legend( ( m1, m2, m3, m4, m5, m6, m7, m8, m9, m10,
                 m11, m12, m13, m14, m15, m16, m17, m18, m19, m20 ),
               ( 'Ch 1',
                 'Ch 2',
                 'Ch 3',
                 'Ch 4',
                 'Ch 5\n-------',

                 'Ch 6',
                 'Ch 7',
                 'Ch 8',
                 'Ch 9',
                 'Ch 10\n-------',

                 'Ch 11',
                 'Ch 12',
                 'Ch 13',
                 'Ch 14',
                 'Ch 15' ), loc=(0.83,0.065) )

  Plot.show()

if __name__ == '__main__':
  Plot_Fixed_1x20_dVdt_Graph( file )
