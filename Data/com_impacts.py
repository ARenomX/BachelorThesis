# -*- coding: utf-8 -*-
"""
Centre of Mass impacts

com_impacts.py
"""

import data_read as read
import graphing as plot
import numpy as np
from os import listdir
import pandas as pd
import matplotlib.pyplot as plt

def moving_average (data, n):
    new = np.copy(data)
    for i in range(0,n):
        new[i,1] = np.mean(data[0:i+n,1])
    for i in range(n,len(data-n)):
        new[i,1] = np.mean(data[i-n:i+n,1])
    return new


def double_acc (pos):
    namelist = listdir("PB_CoM_tests/"+pos)
    names=[i[:-4] for i in namelist]
    ret = []
    for name in names:
        file = pd.read_csv(r'PB_CoM_tests/{}/{}.csv'.format(pos,name),delimiter = ';',skiprows=6)
        res = file.values[:,1:4]
        acc1,acc2 = res[:,[0,1]],res[:,[0,2]]
        acc1[:,1] = acc1[:,1]*(1/0.00845)
        acc2[:,1] = acc2[:,1]*(1/0.0101)
        ret+=[(acc1,acc2)]
    return ret

def multiplot(datalist,a,b,titl):
    a,b = int(a),int(b)
    for i in datalist:
        fig = plt.figure(figsize=(12,8))
        m = np.argmax(i[1][:,1])
        time = i[0][m-a:m+b,0]-i[0][m-a,0]
        vals1 = moving_average(i[0][m-a:m+b],100)[:,1]
        vals2 = moving_average(i[1][m-a:m+b],100)[:,1]
        plt.plot(time,vals1,label='Foam')
        plt.plot(time,vals2,label='Metal')
        plt.xlabel('Time(s)',fontsize = 14)
        plt.ylabel('Acceleration (g)',fontsize = 14)
        plt.legend(fontsize=14)
        plt.show()
        
def plot_dif(datalist,a,b,titl):
    a,b = int(a),int(b)
    for i in datalist:
        fig = plt.figure(figsize=(15,10))
        m = np.argmax(i[1][:,1])
        time = i[0][m-a:m+b,0]-i[0][m-a,0]
        vals1 = moving_average(i[0][m-a:m+b],150)[:,1]
        vals2 = moving_average(i[1][m-a:m+b],150)[:,1]
        plt.plot(time,vals1-vals2)#,label='Foam - Metal')
        plt.xlabel('Time(s)',fontsize = 14)
        plt.ylabel('Acceleration (g)',fontsize = 14)
        #plt.legend(fontsize=14)
        plt.show()