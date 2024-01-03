#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file = "/home/greenbean/GreenBean/PlotFiles/BotBox_Plotfile.csv"


def Plot_1x15_Bar_Graph( file ):

  Ah_D = []
  Ah_C = []

  f = open( file,"r+t" )
  Ah_D = f.readline() # A dummy read
  Ah_C = f.readline()
  f.close()

  Ah_C1, Ah_C2, Ah_C3, Ah_C4, \
         Ah_C5, Ah_C6, Ah_C7, Ah_C8, \
         Ah_C9, Ah_C10, Ah_C11, Ah_C12, \
         Ah_C13, Ah_C14, Ah_C15 = Ah_C.split( ',' )

  if Ah_C1 == str(''):
    Ah_C1 = int(00000)
  if Ah_C2 == str(''):
    Ah_C2 = int(00000)
  if Ah_C3 == str(''):
    Ah_C3 = int(00000)
  if Ah_C4 == str(''):
    Ah_C4 = int(00000)

  if Ah_C5 == str(''):
    Ah_C5 = int(00000)
  if Ah_C6 == str(''):
    Ah_C6 = int(00000)
  if Ah_C7 == str(''):
    Ah_C7 = int(00000)
  if Ah_C8 == str(''):
    Ah_C8 = int(00000)

  if Ah_C9 == str(''):
    Ah_C9 = int(00000)
  if Ah_C10 == str(''):
    Ah_C10 = int(00000)
  if Ah_C11 == str(''):
    Ah_C11 = int(00000)
  if Ah_C12 == str(''):
    Ah_C12 = int(00000)

  if Ah_C13 == str(''):
    Ah_C13 = int(00000)
  if Ah_C14 == str(''):
    Ah_C14 = int(00000)
  if Ah_C15 == str(''):
    Ah_C15 = int(00000)

  AmpereHours = np.array( [int(Ah_C1), int(Ah_C2), int(Ah_C3), int(Ah_C4), \
                           int(Ah_C5), int(Ah_C6), int(Ah_C7), int(Ah_C8), \
                           int(Ah_C9), int(Ah_C10), int(Ah_C11), int(Ah_C12), \
                           int(Ah_C13), int(Ah_C14), int(Ah_C15)] )

  Modules = ['Module 1', 'Module 2', 'Module 3', 'Module 4', \
             'Module 5', 'Module 6', 'Module 7', 'Module 8', \
             'Module 9', 'Module 10', 'Module 11', 'Module 12', \
             'Module 13', 'Module 14', 'Module 15']

  X = np.arange(15)
  df = pd.DataFrame( { 'Modules' : Modules, 'Final Charge Ampere Hours' : AmpereHours })

  ax = df.plot( kind = 'bar' )
  ax.set_xticklabels( df[ 'Modules' ], rotation=90 )

#  plt.title( "Green Bean Battery, LLC, 4-Channel Final Charge Profiler, Version 1.00.00" )
  plt.title( "Green Bean Battery, LLC.\nFinal Charge" )

  plt.xlabel( file )
  plt.ylabel( "FINAL CHARGE\nAMPERE HOURS" )
  plt.legend( loc=(0.8,1.0) )

  plt.show()

if __name__ == '__main__':
  Plot_1x15_Bar_Graph( file )
