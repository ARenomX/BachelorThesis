"""
Dentist Paste analysis

shockwave_tests.py
"""

import data_read as read
import graphing as plot
import numpy as np
from os import listdir
import pandas as pd
import matplotlib.pyplot as plt

def double_acc (pos):
    namelist = listdir("dentist_paste/dentist_paste_"+pos)
    names=[i[:-4] for i in namelist]
    ret = []
    for name in names:
        file = pd.read_csv(r'dentist_paste/dentist_paste_{}/{}.csv'.format(pos,name),delimiter = ';',skiprows=6)
        res = file.values[:,1:4]
        acc1,acc2 = res[:,[0,1]],res[:,[0,2]]
        if pos in ['reverse','reverse_l','reverse_h']:
            acc1[:,1] = -acc1[:,1]*(1/0.00845)
            acc2[:,1] = -acc2[:,1]*(1/0.00516)
        else:
            acc1[:,1] = acc1[:,1]*(1/0.00845)
            acc2[:,1] = acc2[:,1]*(1/0.00516)
        ret += [(acc1,acc2)]
    return ret

def prop_time(acc1,acc2):
    t1,t2,ignore = read.nextpeak(acc1,0,-1),read.nextpeak(acc2,0,-1),False
    if np.abs(t1[2]-t2[2]) < 0.002:# or np.abs(t1[2]-t2[2]) > 0.006:
        ignore = True
    if max(t1[0]/t2[0],t2[0]/t1[0])>10:
        ignore = True
#        print(t1[2],t2[2])
#        plot.plot_2time(acc1,acc2,cut=True)
#        plot.plot_2time(acc1,acc2,cut=False)
    return np.abs(t1[2]-t2[2]),max(t1[0],t2[0]), max(t1[0]/t2[0],t2[0]/t1[0]),ignore

def full(data_list):
    dif_list = []
    acc_list = []
    for acc1,acc2 in data_list:
        dif,acc = prop_time(acc1,acc2)
        dif_list+=[dif]
        acc_list+=[acc]
    plot.scatter(acc_list,dif_list,['Max Acceleration','Propagation time'])
    return dif_list,acc_list
    
def compare (data_lists):
    labels = ['High','Middle','Low','Reverse']
    fig = plt.figure(figsize = (12,8))
    tot_dif_list=[]
    tot_att_list=[]
    tot_acc_list=[]
    for i in range(len(data_lists)):
        data_list=data_lists[i]
        dif_list = []
        acc_list = []
        att_list = []
        for acc1,acc2 in data_list:
            dif,acc,att,ign = prop_time(acc1,acc2)
            if not ign:
                dif_list+=[dif]
                tot_dif_list+=[dif]
                acc_list+=[acc]
                att_list+=[att]
        tot_att_list+=[att_list]
        tot_acc_list+=[acc_list]
        plt.scatter(acc_list,dif_list,label = labels[i])
    plt.xlabel('Max Acceleration (g)',fontsize=14)
    plt.ylabel('Propagation Time (s)',fontsize=14)
    plt.ylim((0,0.006))
    mean = np.mean(tot_dif_list)
    avrg = 'Average = ' + str(np.round(mean*1000,3)) + ' ms'
    #plt.axhline(0.00251,linestyle='--',label='Theoretical Value = 2.511 ms',c='orange')
    #plt.axhline(mean,linestyle='--',label=avrg,c='blue')
    plt.legend(fontsize=14)
    plt.show()
    newfig = plt.figure(figsize = (12,8))
    for i in range(len(tot_att_list)):
        plt.scatter(tot_acc_list[i],tot_att_list[i],label=labels[i])
        #coeff = np.polyfit(tot_acc_list[i],tot_att_list[i],1)
        #fn = np.poly1d(coeff)
        #plt.plot(tot_acc_list[i],fn(tot_acc_list[i]))
    plt.xlabel('Max Acceleration (g)',fontsize=14)
    plt.ylabel('Attenuation ratio',fontsize=14)
    plt.xlim(left=0)
    plt.ylim((0,8))
    plt.legend(fontsize=14)
    plt.show()
    
    return mean
    

def energy_calc(acc,plot=False):
    a,b,c,d = read.nextpeak(acc,0,-1)
    i,j = d,d
    while acc[i,1]>0.5: i-=1
    while acc[j,1]>0.5: j+=1
    energy=0
    if plot:
        newplot=plt.figure(figsize=(12,8))
        plt.plot(acc[i-50:j+100,0],acc[i-50:j+100,1],label = 'Acceleration')
        plt.fill_between(acc[i-5:j+1,0],acc[i-5:j+1,1],color='pink',label = 'Change in velocity')
        plt.xlabel('Time (s)',fontsize=14)
        plt.ylabel('Accelration (g)',fontsize=14)
        plt.legend()
    for n in range (i-5,j+1):
        energy += 0.0001 * acc[n,1]
    return energy,a

def energy_comp(data_lists):
    tot_acc_list = []
    tot_rat_list = []
    labels = ['High','Middle','Low','Reverse','Rev High','Rev Low']
    fig = plt.figure(figsize = (12,8))
    for i in range(len(data_lists)):
        acc_list = []
        ene_list = []
        for ac1,ac2 in data_lists[i]:
            acc1, acc2, switch = order(ac1,ac2)
            #print(switch)
            e1,a = energy_calc(acc1)
            e2,b = energy_calc(acc2)
            acc_list += [a]
            ene_list += [(e2/e1)**2]
        plt.scatter(acc_list,ene_list,label = labels[i])
#        tot_acc_list += [acc_list]
#        tot_rat_list += [ene_list]
    plt.xlabel('Max Acceleration (g)',fontsize=14)
    plt.ylabel('Energy Loss Ratio',fontsize=14)
    plt.axhline(1,linestyle='--',c='red')
    plt.xlim(left=0)
    plt.ylim((0,2))
    plt.legend(fontsize=14)
    plt.show()

    
def profile(acc):
    amax = max(acc[:,1])
    maxpos = np.argmax(acc[:,1])
    maxtime = acc[maxpos,0]
    startpos = maxpos
    while acc[startpos,1] > 0.5: startpos -= 1
    starttime = acc[startpos,0]
    endpos = maxpos
    while acc[endpos,1] > 0.5: endpos += 1
    endtime = acc[endpos,0]
    return amax, startpos, maxpos, endpos, starttime, maxtime, endtime

def check(acc,series,number):
    figure = plt.figure(figsize=(12,8))
    a,sp,mp,ep,st,mt,et = profile(acc)
    new = read.cut(acc,st-0.01,et+0.02)
    plt.plot(new[:,0],new[:,1])
    plt.axvline(st,linestyle='--',c='green')
    plt.axvline(mt,linestyle='--',c='orange')
    plt.axvline(et,linestyle='--',c='red')
    plt.axhline(a,linestyle='--',c='blue')
    plt.title(series +' '+str(number))
    plt.show()
    
def check_all(data_lists):
    errors = []
    labels = ['high','mid','low','reverse']
    for i in range(len(data_lists)):
        for ii in range(len(data_lists[i])):
            for iii in range(2):
                check(data_lists[i][ii][iii],labels[i],ii + 0.5*iii)
                ch = input('Correct? (y/n) ')
                if ch == 'n':
                    print('error acknowledged')
                    errors+=[(i,ii,iii)]
    return errors

def order(acc1,acc2):
    if np.argmax(acc1[:,1]) > np.argmax(acc2[:,1]):
        return np.copy(acc2), np.copy(acc1), True
    else:
        return np.copy(acc1), np.copy(acc2), False
            