'''
preprocessing.py
Filtre by grid id the telco records from Milano.
Author : Charles Gaydon
Last edit : 20/11/2017
'''

## IMPORT
import pandas as pd 
import sys
import numpy as np

def geo_filter_a_MI(file, fileout):
  """
    Take a Milano file, name its columns, filter by square id the lines, 
    fill the NaN value with 0, and save.
  """
    d = pd.read_csv(file, sep = '\t',header=None)
    d.columns = ['Square','Time','Country','SMSin','SMSout','Callin','Callout','Internet']
    mask = d["Square"].apply(keep_a_square)
    d = d[mask]
    d = d.fillna(0)
    d.to_csv(path_or_buf = fileout, sep = '\t', index = False)
    print("Saved to : "+ fileout)
    return(d)

def geo_filter_a_MI2MI(file, fileout):
  """
    Take a Milano 2 Milano file, name its columns, filter by square id the lines, 
    fill the NaN value with 0, and save.
  """
    d = pd.read_csv(file, sep = '\t',header=None)
    d.columns = ['Id1','Id2','Time','Signal']
    mask = d['Id1'].apply(keep_a_square) and d['Id2'].appply(keep_a_square)
    d = d[mask]
    d.fillna(0)
    d.to_csv(path_or_buf = fileout, sep = '\t', index = False)
    print("Saved to : "+ fileout)
    return(d)

def keep_a_square(x,xmin=20,xmax=89,ymin=15,ymax=85):
  """
    Returns True if a square is within our chosen sub-grid.
  """
  j = x%100
  if j > xmax or j < xmin:
    return(False)
  i = (x-j)/100
  if i <ymin or i > ymax:
    return(False)
  return(True)

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage : python geo_filtre.py file_to_process")
    else : 
        file = sys.argv[1]
    fileout = file.split('.')[0]+"_processed"+'.csv'
    print("preprocessing file : "+file)
    d = geo_filter_a_MI(file,fileout)
    print("End of preprocessing")

