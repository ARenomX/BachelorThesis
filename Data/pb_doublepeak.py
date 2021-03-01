"""
Shockwave Video Analysis

shockwave_videos.py
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
    return new[:-n]

def read_positions(filename):
    file = pd.read_excel(r'PB_doublepeak/{}.xlsx'.format(filename))
    x1 = file.values[:,[0,1]]
    x2 = file.values[:,[0,2]]
    x1[:,1]=-(x1[:,1]-x1[0,1])
    x2[:,1]=-(x2[:,1]-x2[0,1])
    return (x1,x2)

def read_acc (name):
    file = pd.read_csv(r'{}.csv'.format(name),delimiter = ';',skiprows=6)
    res = file.values[:,1:3]
    acc = res[:,[0,1]]
    acc[:,1] = acc[:,1]*(9.81/0.01001)
    return acc

def smooth(data_list,n):
    new_data_list = []
    for i in data_list:
        new_data_list+=[moving_average(i,n)]
    return new_data_list

def deriv(data,dt=0.0001):
    new=np.copy(data)
    new[0,1],new[-1,1] = 0,0
    for i in range(1,len(new)):
        new[i,1] = (data[i,1]-data[i-1,1])*(1/dt)
    return new

def deriv_list(data_list):
    new=[]
    for i in data_list:
        new+=[moving_average(deriv(i),4)]
    return new

def v_comp(filename):
    raw = read_positions(filename)
    net = smooth(raw,10)
    vel = deriv_list(net)
    fig = plt.figure(figsize=(12,8))
    for i in range(len(vel)):
        lab = 'Position '+str(i+1)
        plt.plot(vel[i][:,0],vel[i][:,1], label = lab)
    plt.xlabel('Time (s)',fontsize=14)
    plt.ylabel('Velocity (m/s)', fontsize=14)
    plt.legend()
    plt.show()
    
def x_comp(filename):
    raw = read_positions(filename)
    net = smooth(raw,10)
    fig = plt.figure(figsize=(12,8))
    for i in range(len(net)):
        lab = 'Position '+str(i+1)
        plt.plot(net[i][:,0],net[i][:,1], label = lab)
    plt.xlabel('Time (s)',fontsize=14)
    plt.ylabel('Displacement (m)', fontsize=14)
    plt.legend()
    plt.show()
    
def a_comp(filename):
    raw = read_positions(filename)
    net = smooth(raw,2)
    vel = deriv_list(net)
    net_vel = smooth(vel,2)
    acc = deriv_list(net_vel)
    fig = plt.figure(figsize=(12,8))
    for i in [0]:
        lab = 'Rear (Camera)'
        plt.plot(acc[i][:,0],acc[i][:,1], label = lab)
    acc1 = read_acc('PB_doublepeak/impact2/Analog - 15-02-2021 15-03-33.1694')
    start = 19460
    length = 250
    lims=[start,start+length]
    time1 = acc1[lims[0]:lims[1],0]-acc1[lims[0]-3300,0]
#    time1 = acc1[shift1:shift2,0]
    plt.plot(time1,acc1[lims[0]:lims[1],1],label = 'Rear (sensor)')
    #plt.plot(time2,acc2[lims[0]:lims[1],1],label = 'pos 1 (sensor)')
    plt.xlabel('Time (s)',fontsize=14)
    plt.ylabel('Acceleration $(ms^{-2})$', fontsize=14)
    plt.legend()
    plt.show()