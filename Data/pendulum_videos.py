"""
Pendulum Video Analysis

pendulum_videos.py
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
    for i in range(n,len(data)-n):
        new[i,1] = np.mean(data[i-n:i+n,1])
    for i in range(len(data)-n,len(data)):
        new[i,1] = np.mean(data[i-n:-1,1])
    return new

def read_positions(filename):
    file = pd.read_excel(r'Pendulum_Filmed/{}.xlsx'.format(filename))
    x1 = file.values[:,[0,1]]
    x2 = file.values[:,[0,2]]
    x3 = file.values[:,[0,3]]
    x4 = file.values[:,[0,4]]
    x1[:,1]=x1[:,1]-x1[0,1]
    x2[:,1]=x2[:,1]-x2[0,1]
    x3[:,1]=x3[:,1]-x3[0,1]
    x4[:,1]=x4[:,1]-x4[0,1]
    return (x1,x2,x3,x4)

def double_acc (folder):
    name = listdir('Pendulum_Filmed/'+folder)[0][:-4]
    file = pd.read_csv(r'Pendulum_Filmed/{}/{}.csv'.format(folder,name),delimiter = ';',skiprows=6)
    res = file.values[:,1:4]
    acc1,acc2 = res[:,[0,1]],res[:,[0,2]]
    acc1[:,1] = acc1[:,1]*(-9.81/0.00845)
    acc2[:,1] = acc2[:,1]*(-9.81/0.00516)
    return acc1,acc2

def smooth(data_list,n):
    new_data_list = []
    for i in data_list:
        new_data_list+=[moving_average(i,n)[:-n]]
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
    vel = smooth(vel,5)
    fig = plt.figure(figsize=(12,8))
    for i in range(len(vel)):
        lab = 'Position '+str(i+1)
        plt.plot(vel[i][:,0],vel[i][:,1], label = lab)
    plt.xlabel('Time (s)',fontsize=14)
    plt.ylabel('Velocity $(ms^{-1})$', fontsize=14)
    plt.legend()
    plt.show()
    
def x_comp(filename):
    raw = read_positions(filename)
    net = smooth(raw,10)
    fig = plt.figure(figsize=(12,8))
    for i in range(len(net)):
        lab = 'Position '+str(i+1)
        plt.plot(net[i][:,0],net[i][:,1], label = lab)
#    com = get_com(net)
#    plt.plot(com[:,0],com[:,1], label = 'Centre of Mass')
    plt.xlabel('Time (s)',fontsize=14)
    plt.ylabel('Displacement (m)', fontsize=14)
    plt.legend()
    plt.show()
    
def a_comp(filename):
    raw = read_positions(filename)
    net = smooth(raw,2)
    vel = deriv_list(net)
    net_vel = smooth(vel,2)
    ac = deriv_list(net_vel)
    fig = plt.figure(figsize=(12,8))
    acc = smooth(ac,2)
    cut=100
    cuts = 40
    for i in [2]:#range(len(acc)):
        lab = 'Pos '+str(i+1) + ' (Camera)'
        plt.plot(acc[i][cuts:-cut,0],acc[i][cuts:-cut,1], label = lab)
    shift = 0#0.0005
    acc1,acc2 = double_acc('impact1')
    acc1 = moving_average(read.cut(acc1,acc[0][cuts,0],acc[0][-cut,0]),1)
    acc2 = moving_average(read.cut(acc2,acc[0][cuts,0],acc[0][-cut,0]),1)
    acc1[:,0] = acc1[:,0]+shift
    acc2[:,0] = acc2[:,0]+shift
    #plt.plot(acc2[:,0],acc2[:,1],label = 'pos 1 (sensor)')
    plt.plot(acc1[:,0],acc1[:,1],label = 'pos 3 (sensor)')
    plt.xlabel('Time (s)',fontsize=14)
    plt.ylabel('Acceleration $(ms^{-2})$', fontsize=14)
    plt.legend()
    plt.show()
    
def get_com(data):
    com = np.copy(data[0])
    for i in range(len(com)):
        com[i,1] = np.mean([j[i,1] for j in data])
    return com

def acc_wo_com(filename):
    raw = read_positions(filename)
    net = smooth(raw,5)
    vel = deriv_list(net)
    net_vel = smooth(vel,5)
    ac = deriv_list(net_vel)
    fig = plt.figure(figsize=(12,8))
    acc = smooth(ac,5)
    com = get_com(acc)
    cut=100
    cuts = 40
    for i in range(len(acc)):
        lab = 'Pos '+str(i+1) + ' (Camera)'
        plt.plot(acc[i][cuts:-cut,0],acc[i][cuts:-cut,1]-com[cuts:-cut,1], label = lab) #com[cuts:-cut,1]
    #plt.plot(com[cuts:-cut,0],com[cuts:-cut,1])
    shift = 0#0.0005
    acc1,acc2 = double_acc('impact2')
    acc1 = moving_average(read.cut(acc1,acc[0][cuts,0],acc[0][-cut,0]),2)
    acc2 = moving_average(read.cut(acc2,acc[0][cuts,0],acc[0][-cut,0]),2)
    acc1[:,0] = acc1[:,0]+shift
    acc2[:,0] = acc2[:,0]+shift
    #plt.plot(acc2[:,0],acc2[:,1],label = 'pos 1 (sensor)')
    #plt.plot(acc1[:,0],acc1[:,1],label = 'pos 3 (sensor)')
    plt.xlabel('Time (s)',fontsize=14)
    plt.ylabel('Acceleration $(ms^{-2})$', fontsize=14)
    plt.legend()
    plt.show()
