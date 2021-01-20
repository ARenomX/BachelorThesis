"""
Bachelor Thesis Model Code
Functions for visual representation of models

graphing.py
"""
import matplotlib.pyplot as plt
import data_read as read
import numpy as np

def multi (el, evl, sigl, sigvl):
    newplot = plt.figure(figsize=(12,8))
    plt.xlabel('Time')
    plt.subplot(221)
    plt.title('stress')
    plt.plot(sigl)
    plt.subplot(222)
    plt.title('strain')
    plt.plot(el)
    plt.subplot(223)
    plt.title('speed')
    plt.plot(evl)
    plt.subplot(224)
    plt.title('stress speed')
    plt.plot(sigvl)
    plt.show()
    
def stress (sig):
    newplot = plt.figure(figsize=(9,6))
    plt.xlabel('Time')
    plt.ylabel('Stress')
    plt.title('Plot of stress over time')
    plt.plot(sig)
    plt.show()
    
def stress_data (sig,data):
    newplot = plt.figure(figsize=(9,6))
    plt.xlabel('Time')
    plt.ylabel('Stress')
    plt.title('Plot of stress over time')
    plt.plot(sig, label = 'Model')
    plt.scatter(data, label = 'Data')
    plt.show()
    
def plot(data):
    newplot = plt.figure(figsize=(12,8))
    plt.plot(data)
    plt.legend(['line1','line2','line3'])
    plt.show()
    
def plot_force(ff, force):
    newplot = plt.figure(figsize=(12,8))
    plt.plot(ff,force)
    plt.show()
    
    
def plot_time(data):
    newplot = plt.figure(figsize=(12,8))
    plt.plot(data[:,0],data[:,1])
    plt.legend(['line1','line2','line3'])
    plt.show()
    
def plot_2time(data1,data2,names=['Wired','Wireless'],cut=False):
    if cut:
        m = np.argmax(data1[:,1])
        plot_cut(data1,data2,data1[m,0]-0.03,data1[m,0]+0.05,names)
    else:
        newplot = plt.figure(figsize=(12,8))
        plt.plot(data1[:,0],data1[:,1])
        plt.plot(data2[:,0],data2[:,1])
        plt.legend(names)
        plt.show()
    
def plot_cut(data1,data2,start,end,names=['Wired','Wireless']):
    d1 = read.cut(data1,start,end)
    d2 = read.cut(data2,start,end)
    plot_2time(d1,d2,names)
    
def plot_cut_1(data1,start,end):
    d1 = read.cut(data1,start,end)
    plot_time(d1)
    
def split_ax(v,a):
    newplot,ax1 = plt.subplots(figsize=(12,8))
    ax1.set_xlabel('time (s)')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.plot(a[:,0],a[:,1],color='tab:blue')
    ax2 = ax1.twinx()
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax2.plot(v[:,0],v[:,1],color='tab:red')
    newplot.tight_layout()
    
def split_cut(v,a,start,end):
    v1=read.cut(v,start,end)
    a1=read.cut(a,start,end)
    split_ax(v1,a1)
    
def colourmap (x,y,z,zname = ''):
    cm = plt.cm.get_cmap('plasma')
    newplot,ax = plt.subplots(figsize=(12,8))
    sc = plt.scatter(x,y,c=z, cmap=cm)
    ax.set_xlabel('Impact Time (ms)')
    ax.set_ylabel('Impact Velocity (m/s)')
    cbar = plt.colorbar(sc)
    cbar.set_label(zname)
    plt.show()
    
def trip_plot(a,b,c):
    m = np.argmax(a[:,1])
    start = a[m,0]-0.02
    end = a[m,0] + 0.1
    d1 = read.cut(a,start,end)
    d2 = read.cut(b,start,end)
    d3 = read.cut(c,start,end)
    newplot = plt.figure(figsize=(12,8))
    plt.plot(d1[:,0],d1[:,1])
    plt.plot(d2[:,0],d2[:,1])
    plt.plot(d3[:,0],d3[:,1])
    plt.legend(['Rear','Side','Model'])
    plt.show()
    
def peak(file,index,double=False,sim = None):
    if not double:
        plot_cut_1(file,file[index,0]-0.02,file[index,0]+0.1)
    else:
        plot_cut(file,sim,file[index,0]-0.02,file[index,0]+0.1)
        
def a_tau(alist,taulist):
    newplot,ax1 = plt.subplots(figsize=(12,8))
    ax1.set_ylabel('Acceleration (g)')
    ax1.set_xlabel('Tau (s)')
    plt.scatter(taulist,alist)
    space = np.linspace(0.0001,0.03,299)
    plt.plot(space,wayne(space))
    plt.xlim([0,0.02])
    plt.ylim([0,250])
    plt.show()
    
def a_tau_rounds(rounds):
    newplot,ax1 = plt.subplots(figsize=(12,8))
    ax1.set_ylabel('Acceleration (g)')
    ax1.set_xlabel('Tau (s)')
    for i in range(len(rounds)):
        alist = rounds[i][0]
        taulist = rounds[i][1]
        labl = 'Round '+ str(i+1)
        plt.scatter(taulist,alist,label=labl)
    space = np.linspace(0.0001,0.03,299)
    plt.plot(space,wayne(space))
    plt.xlim([0,0.02])
    plt.ylim([0,250])
    plt.legend()
    plt.show()
    
def wayne(tau):
    return 250*(tau*1000)**(-0.86)+36