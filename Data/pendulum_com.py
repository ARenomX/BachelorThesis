
"""
Pendulum analysis

pendulum_com.py
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
        res = file.values[:,1:5]
        acc1,acc2,acc3 = res[:,[0,1]],res[:,[0,2]],res[:,[0,3]]
        acc1[:,1] = acc1[:,1]*-(1/0.00845)
        acc2[:,1] = acc2[:,1]*-(1/0.00516)
        acc3[:,1] = acc3[:,1]*-(2/0.01010)
        ret += [(acc1,acc2,acc3)]
    return ret

def smooth(data_list,n):
    new_data_list = []
    for i in data_list:
        new_data_list+=[moving_average(i,n)]
    return new_data_list

def moving_average (data, n):
    new = np.copy(data)
    for i in range(0,n):
        new[i,1] = np.mean(data[0:i+n,1])
    for i in range(n,len(data-n)):
        new[i,1] = np.mean(data[i-n:i+n,1])
    return new


def triplot(a,b,c,lab = ['Back','Front','Centre of Mass']):
    plt.figure(figsize=(12,8))
    m=np.argmax(b[:,1])
    s = m-100
    e = m+300
    plt.plot(a[s:e,0],a[s:e,1],label=lab[0])
    plt.plot(b[s:e,0],b[s:e,1],label=lab[1])
    plt.plot(c[s:e,0],c[s:e,1],label=lab[2])
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.show()
    
def biplot(a,b,lab = ['Back','Front']):
    plt.figure(figsize=(12,8))
    m=np.argmax(b[:,1])
    s = m-100
    e = m+300
    plt.plot(a[s:e,0],a[s:e,1],label=lab[0])
    plt.plot(b[s:e,0],b[s:e,1],label=lab[1])
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.show()
    
def adj_com(a,b,c):
    a1 = np.copy(a)#moving_average(a,10)
    b1 = np.copy(b)#moving_average(b,10)
    c1 = moving_average(c,3)
    a2,b2 = np.copy(a1),np.copy(b1)
    a2[:,1],b2[:,1] = a1[:,1]-c1[:,1],b1[:,1]-c1[:,1]
    return a2,b2