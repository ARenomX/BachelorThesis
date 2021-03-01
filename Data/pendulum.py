
"""
Pendulum analysis

pendulum.py
"""


import data_read as read
import graphing as plot
import numpy as np
from os import listdir
import pandas as pd
import matplotlib.pyplot as plt

def double_acc (dirc):
    namelist = listdir(dirc)
    names=[i[:-4] for i in namelist]
    ret = []
    for name in names:
        file = pd.read_csv(r'{}/{}.csv'.format(dirc,name),delimiter = ';',skiprows=6)
        res = file.values[:,1:4]
        acc1,acc2 = res[:,[0,1]],res[:,[0,2]]
        if dirc in ['green_static_down','green_prop_test']:
            acc1[:,1] = acc1[:,1]*-(1/0.00845)
            acc2[:,1] = acc2[:,1]*-(1/0.00516)
        else:
            acc1[:,1] = acc1[:,1]*(1/0.00845)
            acc2[:,1] = acc2[:,1]*(1/0.00516)
        ret += [(acc1,acc2)]
    return ret

def prop_time(acc1,acc2):
    i,j=50,50
    while i<len(acc1) and acc1[i,1]!=max(np.append(acc1[i-10:i+10,1],[5])):i+=1
    while j<len(acc2) and acc2[j,1]!=max(np.append(acc2[j-10:j+10,1],[5])):j+=1
#    fig=plt.figure(figsize=(12,8))
#    plt.plot(acc1[i-200:i+400,0],acc1[i-200:i+400,1])
#    plt.plot(acc2[j-200:j+400,0],acc2[j-200:j+400,1])
#    plt.axvline(acc1[i,0])
#    plt.axvline(acc2[j,0])
#    plt.show()
    return acc1[i,0]-acc2[j,0],i,j

def scatter(a,b,labels=['x-axis','y-axis'],mean=0,theory=True):
    newplot,ax1 = plt.subplots(figsize=(12,8))
    plt.xlabel(labels[0],fontsize=14)
    plt.ylabel(labels[1],fontsize=14)
    plt.ylim([0,0.008])
    plt.scatter(a,b,label = 'Data')
    if mean != 0:
        theoretical = 0.00196
        plt.axhline(mean,linestyle='--', label = 'Average = '+str(np.round(mean*1000,2))+ ' ms')
        if theory:
            print('-')
            plt.axhline(theoretical,color='orange',linestyle='--', label = 'Theoretical Value = '+str(np.round(theoretical*1000,3))+ ' ms')
        plt.legend()
    plt.show()


def full(data_list,rev=1):
    gap_list = []
    acc_list = []
    dif_list = []
    for acc1,acc2 in data_list:
        acc1 = read.moving_average(acc1,5)
        acc2 = read.moving_average(acc2,5)
        dif,q,w = prop_time(acc1,acc2)
        gap = read.double_peak(acc1)[0]
        dif_list+=[dif*rev]
        acc = max(acc2[:,1])
        acc_list+=[acc]
        gap_list+=[gap]
    scatter(acc_list,dif_list,['Max Acceleration','Propagation time'],np.mean(dif_list),True) 
    scatter(acc_list,gap_list,['Max Acceleration','Double peak gap time'],np.mean(gap_list),theory = False)
    return gap_list,acc_list,dif_list

def check(data_list):
    for acc1,acc2 in data_list:
        acc1 = read.moving_average(acc1,5)
        acc2 = read.moving_average(acc2,5)
        plt.figure(figsize=(12,8))
        dif,i,j = prop_time(acc1,acc2)
        plt.plot(acc1[i-100:i+300,0],acc1[i-100:i+300,1],'b')
        plt.axvline(acc1[i,0],c='b')
        plt.plot(acc2[i-100:i+300,0],acc2[i-100:i+300,1],'r')
        plt.axvline(acc2[j,0],c='r')
        plt.show()
    
def compare_at(data_lists):
    newplot,ax1 = plt.subplots(figsize=(12,8))
    plt.xlabel('Acceleration (g)',fontsize=14)
    plt.ylabel('Propagation time (s)',fontsize=14)
    plt.ylim([0,0.004])
    labels=['Forward','Backward']
    revs=[1,-1]
    cols = ['r','b']
    theory = 0.00196
    for i in range(len(data_lists)):
        dl = data_lists[i]
        acc_list = []
        dif_list = []
        for acc1,acc2 in dl:
            acc1 = read.moving_average(acc1,4)
            acc2 = read.moving_average(acc2,4)
            dif,q,w = prop_time(acc1,acc2)
            dif_list+=[dif*revs[i]]
            if revs[i] == 1:
                acc = max(acc2[:,1])
            else:
                acc = max(acc1[:,1])
            acc_list+=[acc]   
        plt.scatter(acc_list,dif_list,label=labels[i] , color = cols[i])
        plt.axhline(np.mean(dif_list),label=labels[i]+' average = ' + str(np.round(np.mean(dif_list) * 1000,3)) + ' ms',color = cols[i])
    plt.axhline(theory,color='orange',linestyle='--', label = 'Theoretical Value = '+str(np.round(theory*1000,3))+ ' ms')
    plt.legend()
    plt.show()
        