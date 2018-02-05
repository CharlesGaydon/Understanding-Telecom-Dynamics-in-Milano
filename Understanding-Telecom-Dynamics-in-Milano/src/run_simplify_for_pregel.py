import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from preprocess_tools import *
import os
import sys

if __name__ == "__main__":
    verbose = True
    if len(sys.argv)<2:
        print("Usage : python run_preprocess_MItoMI.py file_to_process [output_file verbose]")
        input_file = "data/MItoMI-2013-12-01.txt"
        print("we use " + input_file)
        output_file = input_file[:4]+"-4Pregel.txt"
    elif len(sys.argv) == 2 :
        input_file = sys.argv[1]
        output_file = input_file[:-4]+"-4Pregel.txt"
    elif len(sys.argv) >= 3: 
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    
    df = simplify_Mi_to_Mi_for_pregel(input_file,output_file,verbose=verbose)


