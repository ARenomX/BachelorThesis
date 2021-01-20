"""
Bachelor Thesis Model Code
Full Definitions of Models
 - Kelvin-Voigt
 - Standard Linear Solid Model - Maxwell Representation
 - Standard Linear Solid Model - Kelvin-Voigt Representation
 
full_definitions.py
"""

import iterative_definitions as iter_def


def kelvin_voigt(e_init,ev_init,ea_init,sig_init,dt,N):
    #Defines the full loop of kelvin voigt model, performing iteratve step N times, with step dt.
    (e,ev,ea,sig) = (e_init,ev_init,ea_init,sig_init)
    (elist,evlist,ealist,siglist) = ([e],[ev],[ea],[sig])
    for i in range(N):
        (enew,evnew,eanew,signew) = iter_def.kv(e,ev,ea,sig,dt)
        elist.append(enew)
        evlist.append(evnew)
        ealist.append(eanew)
        siglist.append(signew)
        (e,ev,ea,sig) = (enew,evnew,eanew,signew)
    return elist,evlist,ealist,siglist


def SLSM_maxwell(e_init,ev_init,ea_init,sig_init,sigv_init,dt,N):
    #Defines the full loop of SLSM-maxwell model, performing iteeratve step N times, with step dt.
    (e,ev,ea,sig,sigv) = (e_init,ev_init,ea_init,sig_init,sigv_init)
    (elist,evlist,ealist,siglist,sigvlist) = ([e],[ev],[ea],[sig],[sigv])
    for i in range(N):
        (enew,evnew,eanew,signew,sigvnew) = iter_def.SLSM_max(e,ev,ea,sig,sigv,dt)
        elist.append(enew)
        evlist.append(evnew)
        ealist.append(eanew)
        siglist.append(signew)
        sigvlist.append(sigvnew)
        (e,ev,ea,sig,sigv) = (enew,evnew,eanew,signew,sigvnew)
    return elist,evlist,ealist,siglist,sigvlist


def SLSM_kelvin_voigt(e_init,ev_init,ea_init,sig_init,sigv_init,dt,N):
    #Defines the full loop of SLSM-kelvin-voigt model, performing iteratve step N times, with step dt.
    (e,ev,ea,sig,sigv) = (e_init,ev_init,ea_init,sig_init,sigv_init)
    (elist,evlist,ealist,siglist,sigvlist) = ([e],[ev],[ea],[sig],[sigv])
    for i in range(N):
        (enew,evnew,eanew,signew,sigvnew) = iter_def.SLSM_kv(e,ev,ea,sig,sigv,dt)
        elist.append(enew)
        evlist.append(evnew)
        ealist.append(eanew)
        siglist.append(signew)
        sigvlist.append(sigvnew)
        (e,ev,ea,sig,sigv) = (enew,evnew,eanew,signew,sigvnew)
    i=15
    sigvlist[0:i] = [sigvlist[i]]*i
    return elist,evlist,ealist,siglist,sigvlist