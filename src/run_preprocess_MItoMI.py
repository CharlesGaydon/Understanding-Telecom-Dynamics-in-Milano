# preprocess a MItoMI file

from preprocess_tools import *
import sys

if __name__ == "__main__":
    verbose = False
    if len(sys.argv)<2:
        print("Usage : python run_preprocess_MItoMI.py file_to_process [output_file verbose]")
    elif len(sys.argv) == 2 :
        input_file = sys.argv[1]
        output_file = input_file[:-4]+"-processed.txt"
    elif len(sys.argv) == 3: 
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else :    
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        verbose = True
    geo_filter_a_MI2MI(input_file,output_file,verbose=verbose)

