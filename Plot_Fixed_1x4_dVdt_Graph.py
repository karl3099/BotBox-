#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

file = "/home/carl/GreenBean/PlotFiles/BotBox_dVdtfile.csv"

def Plot_Fixed_1x4_dVdt_Graph( file ):

  X_Axis_4 = []
  Module_1 = []
  Module_2 = []
  Module_3 = []
  Module_4 = []

  Module =  [ Module_1, Module_2, Module_3, Module_4 ]

  Plot = plt.figure()
  axis1 = Plot.add_subplot( 1, 1, 1 )

  f = open( file,"r+t" )
  Ah_D = f.readline()
  dVdt = f.readlines()
  f.close()

  '''
  Module_Ah =  { 0: 00000, 1: 00000, 2: 00000, 3: 00000}

  mAh1, mAh2, mAh3, mAh4 = Ah_D.split ( ',' )

  Module_Ah[0] = mAh1
  Module_Ah[1] = mAh2
  Module_Ah[2] = mAh3
  Module_Ah[3] = mAh4
 
  n = 0
  Charge_High = int(Module_Ah[0])
  n += 1
  while n < 20:
    if int(Module_Ah[n]) >  Charge_High:
      Charge_High = int(Module_Ah[n])
    n += 1

  Ah_D1, Ah_D2, Ah_D3 = Ah_D.split( ',' )

  for Line in dVdt:
    if len( Line ) > 0:
      x, y1, y2, y3, y4 = Line.split( ',' )
      p = format(Charge_High / float(x), '0.16f')
      q = format(float(x) / Charge_High, '0.16f')
  '''

  for Line in dVdt:
    if len( Line ) > 0:
      x, y1, y2, y3, y4 = Line.split( ',' )

#      c = format((Charge_High * float(p)) * float(q), '0.2f')

      X_Axis_4.append( int(x) ) 
      Module[0].append( float(y1) )
      Module[1].append( float(y2) )
      Module[2].append( float(y3) )
      Module[3].append( float(y4) )

  axis1.clear()

  axis1.set_title( file )

  axis1.set_xlim( 0, int(x) )
  axis1.set_xlabel( "SAMPLES" )
  axis1.set_ylim( 0.00, 2.00 )
  axis1.set_ylabel( "Ch1-Ch4\n dVdt" )

  m1, = axis1.plot( X_Axis_4, Module[0], lw=1.0, color = 'red' )
  m2, = axis1.plot( X_Axis_4, Module[1], lw=1.0, color = 'green' )
  m3, = axis1.plot( X_Axis_4, Module[2], lw=1.0, color = 'orange' )
  m4, = axis1.plot( X_Axis_4, Module[3], lw=1.0, color = 'gray' )

  Plot.legend( ( m1, m2, m3, m4 ),
               ( 'Ch 1',
                 'Ch 2',
                 'Ch 3',
                 'Ch 4',
                 'Ch 5\n-------'), loc=(0.15, 0.7) )

  Plot.show()

if __name__ == '__main__':
  Plot_Fixed_1x4_dVdt_Graph( file )
