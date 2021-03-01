# -*- coding: utf-8 -*-
"""
2-axis wireless accelerometer analysis

2axis.py
"""

import interactive_graph as inter
from os import listdir

def read(name):
    file = pd.read_csv(r'{}.csv'.format(name),delimiter = ',',skiprows=1)
    res_int = file.values[:,:3]
    res = res_int.astype(float)
    res[:,1] = (res[:,1] - res[0,1])* 0.03
    res[:,2] = (res[:,2] - res[0,2])* 0.03
    res[:,0] = (res[:,0] - res[0,0]) * 0.000001
    res1 = res[:,[0,1]]
    res2 = res[:,[0,2]]
    return res1,res2


def ratio(serie):
    acc1,acc2 = serie
    rat_sum = []
    for i in range(len(acc1)):
        if acc2[i,1] != 0:
            rat_sum+=[acc1[i,1]/acc2[i,1]]
    return np.mean(rat_sum)

def read_cab(dirc):
    name = listdir(dirc)[0][:-4]
    file = pd.read_csv(r'{}/{}.csv'.format(dirc,name),delimiter = ';',skiprows=6)
    res = file.values[:,1:3]
    res[:,1] = res[:,1]*(1/0.0101)
    return res

def see(name):
    test = read('2axis_tests/'+name)
    inter.plot_two(test[0],test[1])