#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file = "/home/carl/GreenBean/PlotFiles/BotBox_Chargefile.csv"

def Plot_1x4_Bar_Graph( file ):

  Ah_C = []

  f = open( file,"r+t" )
  Ah_C = f.readline()
  f.close()

  Ah_C1, Ah_C2, Ah_C3, Ah_C4 = Ah_C.split( ',' )

  if Ah_C1 == str(''):
    Ah_C1 = int(00000)
  if Ah_C2 == str(''):
    Ah_C2 = int(00000)
  if Ah_C3 == str(''):
    Ah_C3 = int(00000)
  if Ah_C4 == str(''):
    Ah_C4 = int(00000)

  AmpereHours = np.array( [int(Ah_C1), int(Ah_C2), int(Ah_C3), int(Ah_C4)] )

  Modules = ['Module 1', 'Module 2', 'Module 3', 'Module 4']

  X = np.arange(4)
  df = pd.DataFrame( { 'Modules' : Modules, 'Final Charge Ampere Hours' : AmpereHours })

  ax = df.plot( kind = 'bar' )
  ax.set_xticklabels( df[ 'Modules' ], rotation=45 )

#  plt.title( "Green Bean Battery, LLC, 4-Channel Final Charge Profiler, Version 1.00.00" )
  plt.title( "Green Bean Battery, LLC.\nFinal Charge" )

  plt.xlabel( file )
  plt.ylabel( "FINAL CHARGE\nAMPERE HOURS" )
  plt.legend( loc=(0.8, 1.0) )

  plt.show()

if __name__ == '__main__':
  Plot_1x4_Bar_Graph( file )
