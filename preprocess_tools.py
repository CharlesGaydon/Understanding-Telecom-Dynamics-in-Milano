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
import datetime

def geo_filter_a_MI(file, fileout):
    """
    Take a Milano file, name its columns, filter by square id the lines, 
    fill the NaN value with 0, add a Charge information based on a threeshold, and save.

    output : 
    ['Square','Time','Country','SMSin','SMSout','Callin','Callout',
    'Internet',"Month","Day","Hour","WDay", "Charge"]
    """
    d = pd.read_csv(file, sep = '\t',header=None)
    th_score = [0.3, 15]
    d.columns = ['Square','Time','Country','SMSin','SMSout','Callin','Callout','Internet']

    # mask = d["Square"].apply(keep_a_square)
    # d = d[mask]
    d = d.fillna(0)
    t = pd.DataFrame(data=d['Time'].apply(unix_to_ints))
    d['Month'] = t["Time"].apply(lambda x : x[0])
    d['Day'] = t["Time"].apply(lambda x : x[1])
    d['Hour'] = t["Time"].apply(lambda x : x[2])
    d['WDay'] = t["Time"].apply(lambda x : x[3])
    d["Charge"] = d[["SMSin","SMSout","Callin","Callout","Internet"]].apply(lambda x:above_threeshold(score(x),th_score),axis=1)
    d.to_csv(path_or_buf = fileout, sep = '\t', index = False, header=True)
    print("Saved to : "+ fileout)
    return(d)

def geo_filter_a_MI2MI(file, fileout):
    """
    Take a Milano 2 Milano file, name its columns, filter by square id the lines, 
    fill the NaN value with 0, and save.
    ['Id1','Id2','Time','Signal',
    "Month","Day","Hour","WDay"]
    """
    d = pd.read_csv(file, sep = '\t',header=None)
    d.columns = ['Id1','Id2','Time','Signal']
    mask = d['Id1'].apply(keep_a_square) and d['Id2'].appply(keep_a_square)
    d = d[mask]
    d.fillna(0)
    t = pd.DataFrame(data=d['Time'].apply(unix_to_ints))
    d['Month'] = t["Time"].apply(lambda x : x[0])
    d['Day'] = t["Time"].apply(lambda x : x[1])
    d['Hour'] = t["Time"].apply(lambda x : x[2])
    d['WDay'] = t["Time"].apply(lambda x : x[3])
    d = get_Y_from_MI_data(d,th_score= [0.5, 18]) # TODO : change !
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

def unix_to_ints(unix_code):
    tstamp = datetime.datetime.utcfromtimestamp(unix_code/1000)
    mdH = tstamp.strftime('%m-%d-%H').split('-')
    mdH.append(tstamp.weekday())
    return(list(map(int,mdH)))

"""
input:
MI: a pd.DataFrame with header ->
    Square Time SMSin SMSout Callin Callout Internet [transformed time...]
th_score: [th_SMS_and_Calls, th_Internet]

output:
Y : Id time Class
Class is in {0,1,2}

"""
def get_Y_from_MI_data(MI, th_score= [0.5, 18]):
    MI["Score"] = MI[["SMSin", "SMSout", "Callin", "Callout","Internet"]].apply(lambda x : score(x),axis=1)
    print(MI["Score"].head())
    return(MI)

def score(data):
    Sin = data[0]
    Sout = data[1]
    Cin = data[2]
    Cout = data[3]
    Itnt = data[4]
    sco = [Sin+Sout+Cin+Cout,Itnt]
    return(sco)

def above_threeshold(score, th_score):
    SC = score[0]>=th_score[0]
    IT = score[1]>=th_score[1]
    return(int(SC) + int(IT))

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage : python geo_filtre.py file_to_process")
    else : 
        file = sys.argv[1]
    fileout = file.split('.')[0]+"_processed"+'.csv'
    print("preprocessing file : "+file)
    d = geo_filter_a_MI(file,fileout)
    print("End of preprocessing")

