"""
Analysis of rigid impacts

rigid_impacts.py
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
    namelist = listdir("rigid_drops/"+pos)
    names=[i[:-4] for i in namelist]
    ret = []
    for name in names:
        file = pd.read_csv(r'rigid_drops/{}/{}.csv'.format(pos,name),delimiter = ';',skiprows=6)
        res = file.values[:,[1,2]]
        ret += [res[:,[0,1]]]
    return ret

def multiplot(datalist,a,b,titl):
    a,b = int(a),int(b)
    fig = plt.figure(figsize=(12,8))
    for i in datalist:
        m = np.argmax(i[:,1])
        time = i[m-a:m+b,0]-i[m-a,0]
        vals = moving_average(i[m-a:m+b],8)[:,1]
        plt.plot(time,vals)
    plt.xlabel('Time(s)',fontsize = 14)
    plt.ylabel('Acceleration (g)',fontsize = 14)
    plt.title(titl,fontsize = 16)
    plt.show()