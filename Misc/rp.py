"""
Rayleigh Plesset Tests

rp.py
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint

###
acc_file_name = 'test_cuve_4'

radius_filename = 'rayon_verifRP11'
###


# define equations
def equation(y0, t):
    R, u = y0
    return u, (P_g-P_0-P(t)-2*sigma/R- 
4*miu*u/R+(2*sigma/R_0+P_0-P_g)*(R_0/R)**(3*k))/(R*rho)-3*u**2/(2*R)
    
    
p = open_acc(acc_file_name)

def P(t):
    i = 0
    while p[i:0]<t:i+=1
    return -0.83*9.81*0.31*p[i,1]

def open_acc(name):
    filename = name+'.xlsx'
    file = pd.read_excel(filename)
    return file.values[8:,:2]

def open_rad(name):
    filename = name+'.xlsx'
    file = pd.read_excel(filename)
    return file.values[:,:2]

# initial conditions
R_0 = 0.0001
u_0 = 0

# parameters
rho = 1000
sigma = 0.0728
miu = 8.9*10**(-4)
P_g = 2330
P_0 = 10000
k = 1.33

time = np.arange(0, p[-1,0], 0.000025)

p = open_acc(acc_file_name)

R_1 = odeint(equation, [R_0, u_0], time)


R = R_1[:,0]*10**6
mtimes = time*10**6

#plot results

fig, ax1 = plt.subplots()
ax1.set_xlabel("T/$\mu$s")
ax1.set_ylabel("R/$\mu$m", color = "red")
ax1.plot(mtimes, R, linewidth = 0.7, label = "Bubble Radius", color = 
"red")

ax1.legend()
ax2.legend(loc = "lower right")

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()