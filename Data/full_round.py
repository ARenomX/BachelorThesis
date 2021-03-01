"""
Analysis of full round

full_round.py
"""

import data_read as read
import graphing as plot
import numpy as np
import time

def full_read(name,thresh = 10):
    file = read.phy_round(name)
    impact_list=[]
    i=0
    while i<len(file)+100:
        (a,tau,b,c) = read.nextpeak(file,i)
        if a > thresh:
            (a1,tau1,b1,c1) = read.nextpeak(file,c+100)
            if b1-b <= 0.02 and a1 > (2/3)*a:
                impact_list+=[(max(a1,a),tau+tau1,b,c,True)]
            else:    
                impact_list+=[(a,tau,b,c,False)]
        i=c+500
    return impact_list[:-1]

def manual_read(name,thresh = 5):
    file = read.phy_round(name)
    impact_list=[]
    i=0
    while i<len(file)+100:
        (a,tau,b,c) = read.nextpeak(file,i)
        if a > thresh and 0.02 > tau > 0.0008:
            (a1,tau1,b1,c1) = read.nextpeak(file,c+100)
            if b1-b <= 0.04 and a1 > (2/3)*a:
                if a1 > 1.5*a:
                    impact_list+=[(a,tau,b,c,False)]
                    impact_list+=[(a1,tau1,b1,c1,False)]
                else:
                    a = max(a1,a)
                    impact_list+=[(a,tau+tau1,b,c,True)]
            else:    
                impact_list+=[(a,tau,b,c,False)]
            
        i=c+500
    return impact_list[:-1]

def round_read(r,thresh=10):
    file = r
    impact_list=[]
    i=0
    while i<len(file)+100:
        (a,tau,b,c) = read.nextpeak(file,i)
        if a > thresh and 0.02 > tau > 0.0008:
            (a1,tau1,b1,c1) = read.nextpeak(file,c+100)
            if b1-b <= 0.04 and a1 > (2/3)*a:
                if a1 > 1.5*a:
                    impact_list+=[(a,tau,b,c,False)]
                    impact_list+=[(a1,tau1,b1,c1,False)]
                else:
                    a = max(a1,a)
                    impact_list+=[(a,tau+tau1,b,c,True)]
#                plot.peak(file,c)
#                print(a,True)
            else:    
                impact_list+=[(a,tau,b,c,False)]
#                plot.peak(file,c)
#                print(a,False)
            
        i=c+500
    return impact_list[:-1]

def concus_risk (alist,taulist):
    check = False
    number = 0
    for i in range(len(alist)):
        if alist[i] > 250*(taulist[i]*1000)**(-0.86)+36:
            check = True
            number+=1
    return (check,number)
            
def round_a_tau(name,athresh=10,num_rounds=4,pm=1):
    a = read.phy_round(name,pm)
    round_list = read.split_rounds(a,num_rounds)
    round_data = []
    alist_tot = []
    for r in round_list:
        ll = round_read(r,athresh)
        alist=[i[0] for i in ll]
        taulist = [i[1] for i in ll]
        round_data+=[(alist,taulist)]
        alist_tot = np.append(alist_tot,alist)
    plot.a_tau_rounds(round_data)
    print('Number of Rounds: ' + str(len(round_list)))
    btot=0
    for i in range(len(round_list)):
        print()
        print('In Round ' + str(i+1) + ': ')
        a,b = concus_risk(round_data[i][0],round_data[i][1])
        btot+=b
        if a:
            if b==1:
                print('    Risk of Concussion: High, 1 dangerous impact.')
            else:
                print('    Risk of Concussion: High, ' + str(b) + ' dangerous impacts.')
        else:
            print('    Risk of Concussion: Low, 0 dangerous impacts')
        print('    Number of Impacts: ' + str(len(round_data[i][0])))
        print('    Average Impact Acceleration: ' + 
              str(np.round(np.mean(round_data[i][0]),3)))
            
    print('In Total:')
    if btot==0:
        print('    Risk of Concussion: Low, 0 dangerous impacts')
    else:
        print('    Risk of Concussion: High, ' + str(btot) + ' dangerous impacts.')
    print('    Number of Impacts: ' + str(len(alist_tot)))
    print('    Average Impact Acceleration: ' + 
              str(np.round(np.mean(alist_tot),3)))

def main():
    name = input('Enter Filename: ')
    rn = int(input('Enter number of rounds: '))
    a = read.phy_round(name)
    print()
    print('Full Dataset:')
    plot.plot_time(a,['Time (s)', 'Acceleration (g)'])
    i = np.argmax(a[:,1])
    time.sleep(1)
    print('Example peak: ')
    plot.peak(a,i)
    time.sleep(1)
    pos = input('Is the plot the right way up? (y/n)')
    pm = -1 if pos == 'n' else 1
    print('Calculating...')
    rd = round_a_tau(name, 7.5, rn, pm)