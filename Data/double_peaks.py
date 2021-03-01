"""
Analysis of double peaks

double_peaks.py
"""

import data_read as rd
import double_2_single as d2s
import graphing as plot
import numpy as np


alist=[]
tlist=[]
ilist=[]
dlist=[]
rlist=[]


for i in range(1,21):
    x,v,a,ar,t,imp = rd.impact(i)
    alist+=[ar]
    tlist+=[t]
    ilist+=[imp]
    dif,rat = rd.double_peak(ar)
    dlist+=[dif]
    rlist+=[rat]
    
    
    
plot.scatter(ilist,dlist,['Impact Speed $(ms^{-1})$','Time between Peaks (s)'])
plot.scatter(ilist,rlist,['Impact Speed', 'Ratio of peaks'])
plot.scatter(tlist,dlist,['Impact Time (ms)','Time between Peaks (s)'])
plot.scatter(tlist,rlist,['Impact Time', 'Ratio of peaks'])