"""
Bachelor Thesis Model Code
Main Code for running tests

main.py
"""

import full_definitions as model
import initial_conditions as init 
import graphing as plot


m,k,eta,A,F_0 = init.parameters()

e,ev,ea,sig,sigv = init.impact_SLSM(1,eta)
ev=1
(el,evl,eal,sigl,sigvl) = model.SLSM_kelvin_voigt(e,ev,ea,sig,sigv,0.00001,100000)

plot.stress(sigl)