"""
Author Charles
Last edited: 06/12/2017

This script acts on a folder of Mi 2 Mi files.
It keeps filter the squares and compute 
the sum of interactions along the day between
two squares, for each file (== day), and then 
saves the results.
Results are to be used with GraphX's pregel algo.
"""

import glob
import pandas as pd
import numpy as np

def MI2MI_for_pregel(f, fout):
    d = pd.read_csv(f, sep = '\t', names = ["Time", "Id1", "Id2", "Pow"])
    print(f + " - imported.")
    d.drop("Time",axis=1,inplace=True)
    d = d[d["Id1"].apply(keep_a_square) & d["Id2"].apply(keep_a_square)]
    print(f + " - filtered")
    d.set_index(["Id1", "Id2"],inplace=True)
    dPow = d.groupby(level = ["Id1", "Id2"]).sum()
    dPow.reset_index(["Id1", "Id2"],inplace=True)
    dPow.to_csv(path_or_buf = fout, header=None, sep = '\t', index = False)


folder_path = "data/decemberMi2Mi/"
files = glob.glob("./data/decemberMi2Mi/*.txt")

for f in files:
    MI2MI_for_pregel(f, f[:-4]+"-Pregel.txt")
