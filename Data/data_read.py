"""
Functions for reading Excel Files

data_read.py
"""

import pandas as pd
import calibration as calib
import graphing as plot
from os import listdir
import numpy as np
import csv

def open_xl(name):
    filename = name+'.xlsx'
    file = pd.read_excel(filename)
    return file.values


def cabled (name):
    file = pd.read_csv(r'{}.csv'.format(name),delimiter = ';',skiprows=6)
    res = file.values[:,1:3]
    res[:,1] = res[:,1]*(1/0.00845)
    res[:,0] = res[:,0]
    return res

def read_2(path):
    file = pd.read_csv(r'{}.csv'.format(name),delimiter = ';',skiprows=6)
    res = file.values[:,1:4]
    acc1,acc2 = res[:,[0,1]],res[:,[0,2]]
    acc1[:,1] = acc1[:,1]*(1/0.00845)
    acc2[:,1] = acc2[:,1]*(1/0.0101)
    return acc1,acc2

def wireless (name):
    file = pd.read_csv(r'{}.csv'.format(name),delimiter = ',',skiprows=1)
    res_int = file.values[:,:2]
    res = res_int.astype(float)
    res[:,1] = (res[:,1] - res[0,1])* 0.03
    res[:,0] = (res[:,0] - res[0,0]) * 0.000001
    return res

def accelero (number):
    name = listdir("Filmed PB_Impacts/20210114_"+str(number))[0][:-4]
    return cabled("Filmed PB_Impacts/20210114_"+str(number)+'/' + name)
    
def double_acc (number):
    name = listdir("Double_acc_impacts/20210118_"+str(number))[0][:-4]
    file = pd.read_csv(r'Double_acc_impacts/20210118_{}/{}.csv'.format(str(number),name),delimiter = ';',skiprows=6)
    res = file.values[:,1:4]
    acc1,acc2 = res[:,[0,1]],res[:,[0,2]]
    acc1[:,1] = acc1[:,1]*(1/0.00845)
    acc2[:,1] = acc2[:,1]*(1/0.0101)
    return acc1,acc2
    

def cut(file,start,end):
    i,j=0,0
    while file[i,0] <= start:
        i+=1
    while j<len(file) and file[j,0] <= end:
        j+=1
    return np.copy(file[i:j,:])

def fullread(cabledname,wirelessname):
    a = cabled(cabledname)
    b = wireless(wirelessname)
    a1,b1,shift,incr = calib.time(a,b)
    print(shift,incr)
    return a1, b1

def write_impact(number):
    name = 'Filmed PB_Impacts/impact_'+str(number)+'.csv'
    with open(name,'x') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Time (s)','Position','Velocity','Acceleration','Impact Time (ms)','Impact Velocity (mm/0.0002s)'])
        
def impact(number):
    acc_real = accelero(number)
    filename = 'Filmed PB_Impacts/impact_'+str(number)
    file = pd.read_csv(r'{}.csv'.format(filename),delimiter = ',',skiprows=0)
    vals = file.values[:,:4]
    vals = vals.astype(float)
    vals[:,0] = [np.round(0.1*vals[i,0],5) for i in range(len(vals))]
    pos = vals[:,:2]
    vel = vals[:,[0,2]]
    vel[:,1] = vel[:,1]*0.01
    acc = vals[:,[0,3]]
    acc[:,1] = acc[:,1]*0.01
    pos[:,1],vel[:,1],acc[:,1] = -pos[:,1],-vel[:,1],-acc[:,1]
    t0 = vals[0,0]
    tn = vals[-1,0]
    time = file.values[0,4]
    imp_vel = file.values[0,5]
    return pos,vel,acc,cut(acc_real,t0-0.0002,tn),time,imp_vel

def tau(data):
    m = max(data[:,1])
    n = np.argmax(data[:,1])
    i,j= n,n
    while i<len(data)-1 and max(data[i:i+10,1])>m/2:
        i+=1
    while j>10 and  max(data[j-10:j,1])>m/2:
        j-=1
    return np.round(data[i,0]-data[j,0],5)

def moving_average (data, n):
    new = np.copy(data)
    for i in range(0,n):
        new[i,1] = np.mean(data[0:i+n,1])
    for i in range(n,len(data-n)):
        new[i,1] = np.mean(data[i-n:i+n,1])
    return new


def phy_round(name,pm=1):
    file = pd.read_csv(r'Phyling_rounds/{}.csv'.format(name),delimiter = ',',skiprows=1)
    res_int = file.values[:,:2]
    res = res_int.astype(float)
    res[:,1] = pm*(res[:,1] - res[0,1])* 0.03
    res[:,0] = (res[:,0] - res[0,0]) * 0.000001
    return moving_average(res,5)

def nextpeak(file, start, thresh=5):
    i = start
    if thresh == -1:
        i = np.argmax(file[:,1])
    else:
        while i<len(file)-1 and file[i,1] != max(np.append(file[i-50:i+50,1],[thresh])):i+=1
    if i >= len(file)-2:
        return 0,0,0,np.infty
    else:
        return file[i,1],tau(file[max(i-700,0):i+700]),file[i,0],i
    
def split_rounds(file,numb_rounds):
    difs = [(file[i+1,0]-file[i,0],i) for i in range(len(file)-1)]
    q = np.copy([i[0] for i in difs])
    q.sort()
    thresh = q[-numb_rounds]-1
    dif_thresh = [i for i in difs if i[0] > thresh]
    if dif_thresh[-1][1]+5000 < len(file):
        check=True
        thresh = q[-(numb_rounds-1)]-1
        dif_thresh = [i for i in difs if i[0] > thresh]
    else:
        check = False
    rounds = []
    start = 0
    for i in dif_thresh:
        rounds+=[file[start:i[1]]]
        start = i[1]+1
    if check:
        rounds += [file[start:]]
    return rounds

def force(name):
    file = pd.read_csv(r'{}.csv'.format(name),delimiter = ';',skiprows=6)
    ret = file.values[:,[1,2]]
    ret[:,1] = (0.94414 - 4.06581*ret[:,1])*9.81
    return ret

def position(name):
    file = pd.read_excel(r'{}.xlsx'.format(name))
    ret = file.values[:,[0,1]]
    return ret
    
def double_peak(file):
    i=0
    while i<len(file)-1 and file[i,1] != max(np.append(file[i-20:i+20,1],[5])):i+=1
    j=i+5
    while j<len(file)-1 and file[j,1] != max(np.append(file[j-20:j+20,1],[5])):j+=1
    #print(i,j,file[i,0],file[j,0])
    time_dif = file[j,0]-file[i,0]
    ratio = file[i,1]/file[j,1]
    return np.round(time_dif,4),np.round(ratio,4)

def moving_average (data, n):
    new = np.copy(data)
    for i in range(0,n):
        new[i,1] = np.mean(data[0:i+n,1])
    for i in range(n,len(data-n)):
        new[i,1] = np.mean(data[i-n:i+n,1])
    return new