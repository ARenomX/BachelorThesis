"""
Interactive Graphing

interactive_graph.py
"""
import numpy as np
import matplotlib.pyplot as plt
import data_read as read


plt.switch_backend('Qt5Agg')
plt.install_repl_displayhook()
plt.ion()


roundstarts = []
    
def get_round_starts(data):
    def click(event):
        artist = event.artist
        plot = event.canvas
        plt.axvline(data[event.ind[0],0], color = 'red',linestyle='--')
        plot.draw()
        global roundstarts
        roundstarts += [event.ind[0]]
    fig = plt.figure(figsize=(12,8))
    line, = plt.plot(data[:,0],data[:,1], picker=5)
    plt.xlabel('Time (s)', fontsize = 14)
    plt.ylabel('Acceleration (g)', fontsize = 14)
    plt.title('Full Round: Click after each round start to split data. Close window when done.', fontsize = 18)
    cid = plt.gcf().canvas.mpl_connect("pick_event", click)
    plt.show(block=True)
    global roundstarts
    rs = np.copy(roundstarts)
    roundstarts = []
    return rs

def plot_two (data1,data2):
    fig = plt.figure(figsize=(12,8))
    plt.plot(data1[:,0],data1[:,1], label = 'Axis 1', picker=5)
    plt.plot(data2[:,0],data2[:,1], label = 'Axis 2', picker=5)
    plt.xlabel('Time (s)', fontsize = 14)
    plt.ylabel('Acceleration (g)', fontsize = 14)
    plt.legend()
    plt.show(block=True)
    
def plot_three (data1,data2,data3):
    fig = plt.figure(figsize=(12,8))
    plt.plot(data1[:,0],data1[:,1], label = 'Data 1', picker=5)
    plt.plot(data2[:,0],data2[:,1], label = 'Data 2', picker=5)
    plt.plot(data3[:,0],data3[:,1], label = 'Data 3', picker=5)
    plt.xlabel('Time (s)', fontsize = 14)
    plt.ylabel('Acceleration (g)', fontsize = 14)
    plt.show(block=True)
    
def plot_three_al (dat1,dat2,dat3):
    ref = read.nextpeak(dat1,0,3)
    targ = read.nextpeak(dat3,0,3)
    data4 = np.copy(dat3)
    data4[:,0] = data4[:,0] - (targ[2]-ref[2])
    data1 = read.moving_average(dat1,3)
    data2 = read.moving_average(dat2,3)
    data4 = read.moving_average(data4,3)
    fig = plt.figure(figsize=(12,8))
    plt.plot(data1[:,0],data1[:,1], label = 'Axis 1', picker=5)
    plt.plot(data2[:,0],data2[:,1], label = 'Axis 2', picker=5)
    plt.plot(data4[:,0],data4[:,1], label = 'Cabled Axis', picker=5)
    plt.xlabel('Time (s)', fontsize = 14)
    plt.ylabel('Acceleration (g)', fontsize = 14)
    plt.legend()
    plt.show(block=True)

def plot_round(data):
    fig = plt.figure(figsize=(12,8))
    line, = plt.plot(data[:,0],data[:,1], picker=5)
    plt.xlabel('Time (s)', fontsize = 14)
    plt.ylabel('Acceleration (g)', fontsize = 14)
    plt.show(block=True)
    
def double_plot(data,rounds,ilist,pm):
    newplot = plt.subplots(figsize=(20,8))
    plt.subplot(121)
    plt.ylabel('Acceleration (g)',fontsize=14)
    plt.xlabel('Tau (s)',fontsize=14)
    for i in range(len(rounds)):
        alist = rounds[i][0]
        taulist = rounds[i][1]
        labl = 'Round '+ str(i+1)
        plt.scatter(taulist,alist,label=labl)
    space = np.linspace(0.0001,0.03,299)
    plt.plot(space,wayne(space),label='WSTC')
    plt.xlim([0,0.02])
    plt.ylim([0,250])
    plt.legend()
    plt.subplot(122)
    line, = plt.plot(data[:,0],pm*data[:,1], picker=5)
    for i in ilist:
        plt.axvline(i, color = 'green',linestyle='--',ymax=0.5)
    plt.xlabel('Time (s)', fontsize = 14)
    plt.ylabel('Acceleration (g)', fontsize = 14)
    plt.show(block=True)
    
def a_tau_rounds(rounds):
    newplot,ax1 = plt.subplots(figsize=(12,8))
    ax1.set_ylabel('Acceleration (g)',fontsize=14)
    ax1.set_xlabel('Tau (s)',fontsize=14)
    for i in range(len(rounds)):
        alist = rounds[i][0]
        taulist = rounds[i][1]
        labl = 'Round '+ str(i+1)
        plt.scatter(taulist,alist,label=labl)
    space = np.linspace(0.0001,0.03,299)
    plt.plot(space,wayne(space),label = 'WSTC')
    plt.xlim([0,0.02])
    plt.ylim([0,250])
    plt.legend()
    plt.show(block=True)


def wayne(tau):
    return 250*(tau*1000)**(-0.86)+36