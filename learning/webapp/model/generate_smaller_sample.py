import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


# take 1% of each csv
def smallify_data(path="data/"):
    allFiles = glob.glob(os.getcwd() + "/" + path + "*.txt")
    for file_ in allFiles:
        df = pd.read_csv(file_, sep='\t', header=None).sample(frac=0.01, replace=True)
        df.to_csv(file_+"-sample.csv")
smallify_data()
