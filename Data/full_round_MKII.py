"""
Analysis of full round with interactivity

full_round.py
"""

import data_read as read
import numpy as np
import interactive_graph as inter
from os import listdir

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
        else:
            (a1,tau1,b1,c1) = read.nextpeak(file,c+100)
            if c1-c <= 400 and a1 > thresh:
                impact_list+=[(a1,tau1,b1,c1,False)]
        i=c+400
    return impact_list

def concus_risk (alist,taulist):
    check = False
    number = 0
    for i in range(len(alist)):
        if alist[i] > 250*(taulist[i]*1000)**(-0.86)+36:
            check = True
            number+=1
    return (check,number)
            
def round_a_tau(name,rs,athresh=10,pm=1):
    a = read.phy_round(name,pm)
    round_list = split_rounds_rs(a,rs)
    round_data = []
    alist_tot = []
    ilist = []
    for r in round_list:
        ll = round_read(r,athresh)
        for i in ll:
            ilist += [i[2]]
        if len(ll) == 0:
            alist = [0]
            taulist=[0]
        else:
            alist=[i[0] for i in ll]
            taulist = [i[1] for i in ll]
        round_data+=[(alist,taulist)]
        alist_tot = np.append(alist_tot,alist)
        
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
                print('    Risk of Concussion: High, ' + str(b) +
                      ' dangerous impacts.')
        else:
            print('    Risk of Concussion: Low, 0 dangerous impacts')
        print('    Number of Impacts: ' + str(len(round_data[i][0])))
        print('    Average Impact Acceleration: ' + 
              str(np.round(np.mean(round_data[i][0]),3)))
            
    print('In Total:')
    if btot==0:
        print('    Risk of Concussion: Low, 0 dangerous impacts')
    else:
        print('    Risk of Concussion: High, ' + str(btot) + 
              ' dangerous impacts.')
    print('    Number of Impacts: ' + str(len(alist_tot)))
    print('    Average Impact Acceleration: ' + 
              str(np.round(np.mean(alist_tot),3)))
    inter.a_tau_rounds(round_data)
    return round_data,ilist
    
def split_rounds_rs(data,rs):
    n = len(rs)
    rounds=[]
    re = []
    for i in range(1,n):
        j = rs[i]
        while data[j,0]-data[j-1,0]<3: j-=1
        re+=[j]
    re+=[len(data)]
    for i in range(n):
        rounds += [data[rs[i]:re[i]]]
    return rounds

def main():
    namelist = listdir('Phyling_rounds/')
    names = [i[:-4] for i in namelist]
    q = 0
    while True:
        name = input('Enter Filename: ')
        if name in names:
            break
        else:
            print('This file does not exist.')
            q+=1
        if q>= 2:
            a = input('Do you want a list of available files? (y/n) ')
            if a == 'y':
                print(names)
            
    a = read.phy_round(name)
    global show
    def s():
        inter.plot_round(a)
    rs = inter.get_round_starts(a)
    while True:
        print('Is the plot the right way up? (y/n) you can press s to show the plot again. ')
        pos = input()
        if pos == 's':
            s()
        else:
            pm = -1 if pos == 'n' else 1
            break
    print('Calculating...')
    rd,ilist = round_a_tau(name, rs, 3, pm)
    global a_t
    def show():
        inter.double_plot(a,rd,[],pm)#ilist)
    print("Type 'show()' to see the graphs again.")
    print("Type 'main()' to analyse another file.")
    
    
main()