"""
Function to translate double peak into single peak

double_2_single.py
"""

import data_read as read
import graphing as plot
import numpy as np


def model(time,peak,tau,att):
    return peak*np.exp(-time*att)*np.sin(time/tau)

def d2s (double,a=1,b=1,c=1000):
    s = 10
    while double[s,1] - 3 < double[s-10,1]:s+=1 
    s-=5
    peak = max(double[:,1])
    i,j,n = [np.argmax(double[:,1])]*3
    while double[i,1]>peak/2: i+=1
    while double[j,1]>peak/2: j-=1
    tau = (double[i,0]-double[j,0])
    n+=1000
    while double[n,1] != max(np.append(double[n-50:n+50,1],[1])): n+=1
    att = double[n,1]/peak
    func = np.copy(double)
    func[s:s+3000,1] = model(func[s:s+3000,0]-func[s-1,0],a*peak,b*tau,c*att)
    return func
    
def dif (a,b):
    peak = np.argmax(a[:,1])
    [i,j] = [peak]*2
    while a[i,0] >= a[peak,0]-0.01: i-=1
    while a[j,0] < a[peak,0]+0.01: j+=1
    return np.sum([np.abs(a[n,1] - b[n,1])**2 for n in range(i,j)]) + 2*(max(a[:,1])-max(b[:,1]))**3
                
def grad_step(doubles,singles,model,a,b,c,step):
    new = [[[np.sum([dif(singles[i], model(doubles[i],a+p*step,b+q*step,
                       c+r*500*step)) for i in range(len(doubles))]) for p
                            in range(-1,2)] for q in range(-1,2)] for r 
                                in range(-1,2)]
    return new

def mat_min(mat):
    mn = np.infty
    ind = (0,0,0)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if mat[i][j][k] < mn:
                    mn = mat[i][j][k]
                    ind = (k-1,j-1,i-1)
    return mn,ind

def grad_desc():
    doubles = [read.double_acc(i)[0] for i in range(1,7)]
    singles = [read.double_acc(i)[1] for i in range(1,7)]
    step = 0.5
    a=1.5
    b=2.0
    c=750
    while step>0.01:
        mat = grad_step(doubles,singles,d2s,a,b,c,step)
        mx,ind = mat_min(mat)
        if ind == (0,0,0):
            step = step/2
        else:
            (a,b,c) = (a+step*ind[0],b+step*ind[1],c+step*500*ind[2])
        print(a,b,c,step)
    return (a,b,c)
    
def d2s_a_tau (double,a,b,c):
    s = 5
    while double[s,1] - 3 < double[s-10,1]:s+=1 
    s-= 5
    peak = max(double[:,1])
    i,j,n = [np.argmax(double[:,1])]*3
    while double[i,1]>peak/2: i+=1
    while double[j,1]>peak/2: j-=1
    tau = (double[i,0]-double[j,0])
    n+=1000
    while n<len(double) and double[n,1] != max(np.append(double[n-50:n+50,1],[1])): n+=1
    if n>=len(double)-1:
        att = 0.001
    else:
        att = double[n,1]/peak
    func = np.copy(double)
    func[s:s+3000,1] = model(func[s:s+3000,0]-func[s-1,0],a*peak,b*tau,c*att)
    mx = max(func[s:s+3000,1])
    i,j = [np.argmax(func[s:s+3000,1])]*2
    while func[i,1]>mx/2: i+=1
    while func[j,1]>mx/2: j-=1
    tau_func = func[i,0]-func[j,0]
    return mx,tau_func,func