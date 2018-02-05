# preprocess a MItoMI file

from preprocess_tools import *
import sys

if __name__ == "__main__":
    verbose = False
    if len(sys.argv)<2:
        print("Usage : python run_vectorizer.py file_to_process [output_file]")
    elif len(sys.argv) == 2 :
        input_file = sys.argv[1]
        vectorize_per_day(input_file)
    elif len(sys.argv) == 3: 
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        vectorize_per_day(input_file,fileout=output_file)

