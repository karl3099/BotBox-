#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file = "/home/greenbean/GreenBean/PlotFiles/BotBox_Loadfile.csv"

def Plot_1x20_IR_Bar_Graph( file ):

  Load_V = []

  f = open( file,"r+t" )
  Load_V = f.readline()
  f.close()

  Load_V1, Load_V2, Load_V3, Load_V4, Load_V5, \
  Load_V6, Load_V7, Load_V8, Load_V9, Load_V10, \
  Load_V11, Load_V12, Load_V13, Load_V14, Load_V15, \
  Load_V16, Load_V17, Load_V18, Load_V19, Load_V20 = Load_V.split( ',' )

  if Load_V1 == str(''):
    Load_V1 = float(0.000)
  if Load_V2 == str(''):
    Load_V2 = float(0.000)
  if Load_V3 == str(''):
    Load_V3 = float(0.000)
  if Load_V4 == str(''):
    Load_V4 = float(0.000)
  if Load_V5 == str(''):
    Load_V5 = float(0.000)

  if Load_V6 == str(''):
    Load_V6 = float(0.000)
  if Load_V7 == str(''):
    Load_V7 = float(0.000)
  if Load_V8 == str(''):
    Load_V8 = float(0.000)
  if Load_V9 == str(''):
    Load_V9 = float(0.000)
  if Load_V10 == str(''):
    Load_V10 = float(0.000)

  if Load_V11 == str(''):
    Load_V11 = float(0.000)
  if Load_V12 == str(''):
    Load_V12 = float(0.000)
  if Load_V13 == str(''):
    Load_V13 = float(0.000)
  if Load_V14 == str(''):
    Load_V14 = float(0.000)
  if Load_V15 == str(''):
    Load_V15 = float(0.000)

  if Load_V16 == str(''):
    Load_V16 = float(0.000)
  if Load_V17 == str(''):
    Load_V17 = float(0.000)
  if Load_V18 == str(''):
    Load_V18 = float(0.000)
  if Load_V19 == str(''):
    Load_V19 = float(0.000)
  if Load_V20 == str(''):
    Load_V20 = float(0.000)

  LoadVoltage = np.array( [ float(Load_V1), float(Load_V2), float(Load_V3), float(Load_V4), float(Load_V5),\
                           float(Load_V6), float(Load_V7), float(Load_V8), float(Load_V9), float(Load_V10),\
                           float(Load_V11), float(Load_V12), float(Load_V13), float(Load_V14), float(Load_V15),\
                           float(Load_V16), float(Load_V17), float(Load_V18), float(Load_V19), float(Load_V20) ] )

  Modules = [ 'Module 1', 'Module 2', 'Module 3', 'Module 4', 'Module 5', \
              'Module 6', 'Module 7', 'Module 8', 'Module 9', 'Module 10', \
              'Module 11', 'Module 12', 'Module 13', 'Module 14', 'Module 15', \
              'Module 16', 'Module 17', 'Module 18', 'Module 19', 'Module 20' ]

  X = np.arange(4)
  df = pd.DataFrame( { 'Modules' : Modules, 'Module Load Test' : LoadVoltage })

  ax = df.plot( kind = 'bar' )
  ax.set_xticklabels( df[ 'Modules' ], rotation=90 )

#  plt.title( "Green Bean Battery, LLC, 4-Channel Final Charge Profiler, Version 1.00.00" )
  plt.title( "Green Bean Battery, LLC.\n Module Load Voltage" )

  plt.xlabel( file )
  plt.ylabel( "Load Voltage" )
  plt.legend( loc=(0.8, 1.0) )

  plt.show()

if __name__ == '__main__':
  Plot_1x20_IR_Bar_Graph( file )
