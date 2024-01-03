#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file = "/home/carl/GreenBean/PlotFiles/BotBox_Loadfile.csv"

def Plot_1x4_IR_Bar_Graph( file ):

  Load_V = []

  f = open( file,"r+t" )
  Load_V = f.readline()
  f.close()

  Load_V1, Load_V2, Load_V3, Load_V4 = Load_V.split( ',' )

  if Load_V1 == str(''):
    Load_V1 = float(0.000)
  if Load_V2 == str(''):
    Load_V2 = float(0.000)
  if Load_V3 == str(''):
    Load_V3 = float(0.000)
  if Load_V4 == str(''):
    Load_V4 = float(0.000)

  LoadVoltage = np.array( [float(Load_V1), float(Load_V2), float(Load_V3), float(Load_V4)] )

  Modules = ['Module 1', 'Module 2', 'Module 3', 'Module 4']

  X = np.arange(4)
  df = pd.DataFrame( { 'Modules' : Modules, 'Module Load Test' : LoadVoltage })

  ax = df.plot( kind = 'bar' )
  ax.set_xticklabels( df[ 'Modules' ], rotation=90 )

#  plt.title( "Green Bean Battery, LLC, 4-Channel Final Charge Profiler, Version 1.00.00" )
  plt.title( "Green Bean Battery, LLC.\nModule Load Voltage" )

  plt.xlabel( file )
  plt.ylabel( "Load Voltage" )
  plt.legend( loc=(0.8, 1.0) )

  plt.show()

if __name__ == '__main__':
  Plot_1x4_IR_Bar_Graph( file )
