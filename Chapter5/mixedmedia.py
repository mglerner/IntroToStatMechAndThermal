#!/usr/bin/env python
from __future__ import division
import numpy as np
import pylab as pl
from random import choice,shuffle
from numpy.random import random #import only one function from somewhere
from numpy.random import randint
from numpy import exp, array, linspace, log, arange
import scipy
from time import sleep
from copy import deepcopy

def unmixed(x,GA0=1.0,GB0=2.0):
    return (1-x)*GA0 + x*GB0

R = 8.31
def deltaS_mixing(x):
    return -R*(x*log(x) + (1-x)*log(1-x))

def idealmixed(x,T,GA0=1.0,GB0=2.0):
    return unmixed(x,GA0,GB0) - T*deltaS_mixing(x)

def deltaU_mixing(x):
    umax = 2.0
    return (.25 - (x-0.5)**2)*umax/.25

def nonidealmixed(x,T):
    return idealmixed(x,T) + deltaU_mixing(x)

def showfirst():
    pl.clf()
    x = linspace(0,1,1000)
    Ts = linspace(0,1,11)
    legloc = 'lower right'
    pl.subplot(121)
    pl.plot(x,unmixed(x),label="unmixed")
    pl.title("Ideal Mixture")
    pl.xlabel("fraction B")
    pl.ylabel("G")
    for T in Ts:
        pl.plot(x,idealmixed(x,T),label="T=%3.1f"%T)
    pl.legend(loc=legloc)

    pl.subplot(122)
    pl.plot(x,unmixed(x),label="unmixed")
    pl.title("Non-ideal Mixture")
    pl.xlabel("fraction B")
    pl.ylabel("G")
    for T in Ts:
        pl.plot(x,nonidealmixed(x,T),label="T=%3.1f"%T)
    pl.legend(loc=legloc)
    return

def fig5_30():
    pl.clf()
    x = linspace(0,1,1000)
    pl.subplot(221)
    T = 0.3
    pl.plot(x,idealmixed(x,T,GA0=1.0,GB0=2.0),'b-')
    pl.plot(x,idealmixed(x,T,GA0=0.8,GB0=2.0),'r--')
    pl.subplot(222)
    T = 0.2
    pl.plot(x,idealmixed(x,T,GA0=1.0,GB0=2.0),'b-')
    pl.plot(x,idealmixed(x,T,GA0=0.6,GB0=2.2),'r--')
    
### NOW for problem 5.67 part d ###

def A(t, tA, hA,):
    """
    
    Arguments:
     - `t`: temperature
     - `tA`: boiling point of substance A
     - `hA`: Delta H^0_A/R
    """
    return exp(hA*((1/t) - (1/tA)))

def B(t, tB, hB,):
    """
    
    Arguments:
     - `t`: temperature
     - `tB`: boiling point of substance B
     - `hB`: Delta H^0_B/R
    """
    return exp(hB*((1/t) - (1/tB)))

def xg(t, tA, tB, hA, hB):
    return (A(t, tA, hA) - 1)/(A(t, tA, hA) - B(t, tB, hB))

def xl(t, tA, tB, hA, hB):
    return xg(t, tA, tB, hA, hB)*B(t, tB, hB)

def plot_phase_diagram(tA, tB, hA, hB):
    pl.clf()
    t = arange(tA, tB, 0.01)
    pl.plot(xg(t,tA,tB,hA,hB),t,'r-',xl(t,tA,tB,hA,hB),t,'b-')

R = 8.315
def fig5_31():
    tA, hA = 77.4, 5570/R
    tB, hB = 90.2, 6820/R
    plot_phase_diagram(tA, tB, hA, hB)

def fig5_32_():
    tA, hA = 1370, 50000/R
    tB, hB = 1820, 115000/R
    plot_phase_diagram(tA, tB, hA, hB)

def fig5_32(HA, HB):
    tA, hA = 1370, HA/R
    tB, hB = 1820, HB/R
    plot_phase_diagram(tA, tB, hA, hB)


