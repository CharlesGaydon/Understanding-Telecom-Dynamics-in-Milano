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
import os

def geo_filter_a_MI(file, fileout,keep_only = (60,55)):
    """
    Take a Milano file, name its columns, filter by square id the lines, 
    fill the NaN value with 0, add a Charge information based on a threeshold, and save.

    output : 
    ['Square','Time','Country','SMSin','SMSout','Callin','Callout',
    'Internet',"Month","Day","Hour","WDay", "Charge"]
    """
    d = pd.read_csv(file, sep = '\t',header=None)
    th_score = [1000, 300] # change this ! 
    d.columns = ['Square','Time','Country','SMSin','SMSout','Callin','Callout','Internet']

    mask = d["Square"].apply(lambda x : keep_a_square(x,keep_only = keep_only))
    # mask = d["Square"].apply(keep_a_square)
    d = d[mask]
    d = d.fillna(0)

    ### for LSTM usage
    d = simplify_for_learning(d)
    # FOR TESTING ONLY :
    d = amplify_for_Learning(d)
    # print("final shape : " + str(d.shape))

    # Info about time
    t = pd.DataFrame(data=d['Time'].apply(unix_to_ints))
    d['Month'] = t["Time"].apply(lambda x : x[0])
    d['Day'] = t["Time"].apply(lambda x : x[1])
    d['Hour'] = t["Time"].apply(lambda x : x[2])
    d['WDay'] = t["Time"].apply(lambda x : x[3])
    #d["Charge"] = d[["SMSin","SMSout","Callin","Callout","Internet"]].apply(lambda x:above_threeshold(score(x),th_score),axis=1)
    d["Charge"] = d[["SMSin","SMSout","Callin","Callout","Internet"]].apply(lambda x : 1,axis=1)
    d.to_csv(path_or_buf = fileout, sep = '\t', index = False, header=True)
    print("Saved to : "+ fileout)

    return(d)

def simplify_for_learning(d):

    d.drop(["Country"],axis=1,inplace=True)
    d.set_index(["Square","Time"],inplace=True)
    d = d.groupby(level = ["Square","Time"]).sum()
    d.reset_index(["Square","Time"],inplace=True)
    return(d)

"""
    Fill the missing timestamps by 0 values ;
    Assume a UNIQUE Square selected, and that country-wise data were summed ! 
"""
def amplify_for_Learning(d):
    d["Time"] = d["Time"]/600000
    timesteps = int((d.iloc[d.shape[0]-1]["Time"] - d.iloc[0]["Time"]))+1
    my_range = d.iloc[0]["Time"] + np.arange(timesteps)
    d = d.set_index(["Time"])
    d = d.reindex(my_range)
    d.reset_index("Time", inplace = True)
    d["Time"] = d["Time"]*600000
    d[["SMSin","SMSout","Callin","Callout","Internet"]] =d[["SMSin","SMSout","Callin","Callout","Internet"]].fillna(value = 0.0)
    d["Square"] = d["Square"].fillna(method = "ffill")
    return(d)

def geo_filter_a_MI2MI(file, fileout=None, verbose=False):
    """
    Take a Milano 2 Milano file, name its columns, filter by square id the lines, 
    fill the NaN value with 0, and save.
    ['Id1','Id2','Time','Signal',
    "Month","Day","Hour","WDay"]
    """
    d = pd.read_csv(file, sep = '\t',header=None)
    if verbose:
        print("Read : " +file)

    d.columns = ['Time','Id1','Id2','Signal']
    mask = np.logical_and(d['Id1'].apply(keep_a_square),d['Id2'].apply(keep_a_square))
    
    if verbose:
        print("Kept standard squares.")
    d = d[mask]
    d.fillna(0)
    t = pd.DataFrame(data=d['Time'].apply(unix_to_ints))
    if verbose:
        print("Time conversion.")
    d['Month'] = t["Time"].apply(lambda x : x[0])
    d['Day'] = t["Time"].apply(lambda x : x[1])
    d['Hour'] = t["Time"].apply(lambda x : x[2])
    d['WDay'] = t["Time"].apply(lambda x : x[3])
    dPow = d.groupby(level = ["Id1", "Id2", "WDay","Hour"]).sum()
    dPow.reset_index(["Id1", "Id2"],inplace=True)
    if fileout:
        d.to_csv(path_or_buf = fileout, sep = '\t', index = False)
        print("Saved to : "+ fileout)
    return(d)


def simplify_Mi_to_Mi_for_pregel(file, fileout, verbose = False):
    d = pd.read_csv(file, sep = '\t',header=None)
    if verbose:
        print("Read : " +file)

    d.columns = ['Time','Id1','Id2','Signal']
    mask = np.logical_and(d['Id1'].apply(keep_a_square),d['Id2'].apply(keep_a_square))
    d = d.drop(["Time"],axis=1)
    if verbose:
        print("Kept standard squares.")
    d = d[mask]
    d.fillna(0)
    dPow = d.set_index(["Id1", "Id2"])
    dPow = d.groupby(["Id1", "Id2"]).sum()
    dPow.reset_index(["Id1", "Id2"],inplace=True)

    if not fileout:
        fileout = file[:4]+"-4Pregel.txt"
    d.to_csv(path_or_buf = fileout, sep = '\t', index = False)
    print("Saved to : "+ fileout)

    return(d)
def vectorize_per_day(file,fileout=None):
    d = pd.read_csv(file, sep = '\t',header=None)
    print("Read : "+file)
    d.columns = ['Square','Time','Country','SMSin','SMSout','Callin','Callout','Internet']
    mask = d["Square"].apply(lambda x : keep_a_square(x))
    d = d[mask]
    d.fillna(0,inplace=True)
    t = pd.DataFrame(data=d['Time'].apply(unix_to_ints))
    d['Period'] = t["Time"].apply(lambda x : int(x[2]/4))
    print("Time formatted.")

    d.drop(["Country","Time"],axis=1,inplace=True)


    d = d.groupby(["Square","Period"],axis=1).sum()
    print("Grouped by Square and Period.")
    d["Phone"] = d["SMSin"]+d["SMSout"]+d["Callin"]+d["Callout"]

    Phone = d["Phone"]
    Internet = d["Internet"]
    dphone = Phone.pivot(index = "Square",columns = "Periode",values="Phone")
    print("Pivot of Phone data.")
    dinternet = Internet.pivot(index = "Square",columns="Periode",values="Phone")
    print("Pivot of Internet data.")

    if not fileout:
        fileout_phone = file[:-4]+"-phone-vct.txt"
        fileout_internet = file[:-4]+"-internet-vct.txt"
    else :
        fileout_phone = fileout[:-4]+"-phone-vct.txt"
        fileout_internet = fileout[:-4]+"-internet-vct.txt"

    dphone.to_csv(path_or_buf = fileout_phone, sep = '\t', index = False)
    dinternet.to_csv(path_or_buf = fileout_internet, sep = '\t', index = False)
    print("Saved to : "+ fileout_phone + " and "+fileout_internet)
    
    return(1)
def keep_a_square(x,xmin=20,xmax=89,ymin=15,ymax=85, keep_only = False):
    """
    Returns True if a square is within our chosen sub-grid.
    """
    j = x%100
    if keep_only:
        if j == keep_only[0]:
            if (x-j)/100 == keep_only[1]:
                return(True)
        return(False)

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
    return(int(SC or IT))

def get_label(df,transform,name_columns,percentage = .05):  
    dftemp = df.copy()
    dftemp['seuil'] = transform(*[df[name] for name in name_columns])
    n = len(dftemp)
    take = int(n*percentage)
    seuil = np.min(dftemp.nlargest(take,'seuil').seuil)
    dftemp['y'] = (dftemp.seuil>seuil).astype(int)
    dftemp.drop('seuil',axis=1)
    return(dftemp)

def extract_a_square(square_to_extract = 5560,ori_path = "../data/MI_data/",next_path = "../data/MI_squares/"):

    # EXTRACT ALL
    square_str = str(square_to_extract)
    square_to_extract = (square_to_extract//100,square_to_extract%100)

    print("Extracting square at position "+str(square_to_extract))
    next_path = next_path+square_str
    original_dir = os.listdir(ori_path)
    next_dir = os.listdir(next_path)
    os.system("mkdir -p "+next_path+"/")
    for index,file_ori in enumerate(original_dir):
        print("["+str(index+1)+"/"+str(len(original_dir))+"]")
        file_target = next_path + "/"+square_str+"_"+file_ori
        if square_str+"_"+file_ori not in next_dir:
            geo_filter_a_MI(ori_path+file_ori,file_target,keep_only = square_to_extract)

    # AGGREGATE
    d = pd.DataFrame()
    next_dir = os.listdir(next_path)
    if square_str+"_all.csv" not in next_dir:
        for file in next_dir:
            if file != square_str+"_all.csv":
                sub = pd.read_csv(next_path+"/"+file,sep="\t")
                print(sub.shape)
                d = pd.concat([d,sub])
    else:
        print(square_str+"_all.csv does already exist in dir : "+next_path)
    
    d.to_csv(next_path+'/'+square_str+"_all.csv", index = False,sep="\t")

    return(1)

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage : python preprocess_tools.py square_to_extract")
    else : 
        square_to_extract = int(sys.argv[1])
    assert (square_to_extract>=0 and square_to_extract<=10000)
    extract_a_square(square_to_extract = square_to_extract)

