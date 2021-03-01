"""
Data calibration
Take calibrated and uncalibratd data input, and find calibration

calibration.py
"""

import data_read as read
import graphing as plt
import numpy as np

constants  = [1/10.1,-1/5.16]


def constant (calibrated,uncalibrated,constants):
    (i,j) = calibrated.shape
    total = np.zeros((i,j+1))
    total[:,:j] = calibrated
    total[:,j] = uncalibrated
    plt.plot(total)
    adjusted = np.copy(calibrated)
    for n in range(j):
        adjusted[:,n] = adjusted[:,n]*constants[n]
    difsum=[0]*j
    for q in range(i):
        for p in range(j):
            difsum[p]+= adjusted[q,p]/uncalibrated[q]
    newcalib = sum(difsum)/(j*q)
    newcalibrated = newcalib*uncalibrated
    total = np.zeros((i,j+1))
    total[:,:j] = adjusted
    total[:,j] = newcalibrated
    plt.plot(total)
    return newcalib,total

newconstants = [1/10.1,-1/5.16,-1/8.45]

def test(calibrated, constants):
    (i,j) = calibrated.shape
    adjusted = np.copy(calibrated)
    for n in range(j):
        adjusted[:,n] = adjusted[:,n]*constants[n]
    plt.plot(adjusted)
    return adjusted

def time_archive(reference,uncalibrated):
    i,j=0,0
    while reference[i,1]<15: i+=1
    while uncalibrated[j,1]<15: j+=1
    shift = uncalibrated[j,0] - reference[i,0]
    calibrated = np.zeros(np.shape(uncalibrated))
    calibrated[:,0] = uncalibrated[:,0] - (shift) #  - 0.014
    calibrated[:,1] = uncalibrated[:,1]
    ref = j
    i,j = len(reference)-1,len(calibrated)-1
    while reference[i,1]<15: i-=1
    while calibrated[j,1]<15: j-=1
    delta = calibrated[j,0] - reference[i,0]
    increment = 1-(delta/(calibrated[j,0]-calibrated[ref,0]))
    calibrated[ref:,0] = calibrated[:,0]*increment
    return reference, calibrated, shift, increment

def time_old(reference,uncalibrated):
    r,c = reference,uncalibrated
    i,j=0,0
    while r[i,1] != max(np.append(r[i-50:i+50,1],[15])): i+=1
    while c[j,1] != max(np.append(c[j-50:j+50,1],[15])): j+=1
    shift = uncalibrated[j,0] - reference[i,0]
    calibrated = np.zeros(np.shape(uncalibrated))
    calibrated[:,0] = uncalibrated[:,0] - (shift) #  - 0.014
    calibrated[:,1] = uncalibrated[:,1]
    ref = j
    i,j = len(reference)-51,len(calibrated)-51
    while r[i,1] != max(np.append(r[i-50:i+50,1],[15])): i-=1
    while c[j,1] != max(np.append(c[j-50:j+50,1],[15])): j-=1
    delta = calibrated[j,0] - reference[i,0]
    increment = 1-(delta/(calibrated[j,0]-calibrated[ref,0]))
    calibrated[0:,0] = calibrated[:,0]*increment
    return reference, calibrated, shift, increment

def time(reference,uncalibrated):
    r,c = reference,uncalibrated
    i,j=0,0
    while r[i,1] != max(np.append(r[i-50:i+50,1],[15])): i+=1
    while c[j,1] != max(np.append(c[j-50:j+50,1],[15])): j+=1
    ii,jj = len(r)-51,len(c)-51
    while r[ii,1] != max(np.append(r[ii-50:ii+50,1],[15])): ii-=1
    while c[jj,1] != max(np.append(c[jj-50:jj+50,1],[15])): jj-=1
    r_range,c_range = r[ii,0]-r[i,0],c[jj,0]-c[j,0]
    increment = r_range/c_range
    uncalibrated[:,0] = uncalibrated[:,0]*increment
    c = uncalibrated
    i,j=0,0
    while r[i,1] != max(np.append(r[i-50:i+50,1],[15])): i+=1
    while c[j,1] != max(np.append(c[j-50:j+50,1],[15])): j+=1
    shift = uncalibrated[j,0] - reference[i,0]
    calibrated = np.zeros(np.shape(uncalibrated))
    calibrated[:,0] = uncalibrated[:,0] - (shift)
    calibrated[:,1] = uncalibrated[:,1]
    return reference, calibrated, shift, increment


def force_position(f,p):
    i,j=0,15
    while f[i,1] != max(np.append(f[i-30:i+30,1],[5])): i+=1
    while p[j,1] != min(np.append(p[j-15:j+15,1],[-0.0015])): j+=1
    t,T = f[i,0],p[j,0]
    T_final = p[-1,0]
    newforce = np.copy(read.cut(f,t,t+(T_final-T)))
    newforce[:,0] = newforce[:,0] - newforce[0,0]
    newpos = np.copy(read.cut(p,T,T_final))
    newpos[:,0] = newpos[:,0] - newpos[0,0]
    print(t,T)
    return newforce,newpos

def phyling_test(cable_name,phy_name):
    cab = read.cabled(cable_name)
    phy = read.wireless(phy_name)
    cab,phy_cal,shift,incr = time(cab,phy)
    return incr
