#!/usr/bin/env python
from __future__ import division
import numpy as np
import pylab
from matplotlib import pyplot as plt
from numpy.random import random #import only one function from somewhere
from numpy.random import randint
import scipy
from time import sleep

size = 100 # lattice length
T = 2.5 # in units of epsilon/k

plot_extra = True

def initialize():
    """
    Initialize a random array where our spins are all up or down.
    """
    myarray = random([size,size]) # initializes with random numbers from 0 to 1.
    myarray[myarray<0.5] = -1
    myarray[myarray>=0.5] = 1
    colorsquare(myarray)
    pylab.show()
    return myarray


def deltaU(i,j):
    """
    Compute delta U of flipping a given dipole at i,j
    Note periodic boundary conditions.
    """
    from numpy import mod
    above = s[mod(i+1,size),j]
    below = s[mod(i-1,size),j]
    right = s[i,mod(j+1,size)]
    left =  s[i,mod(j-1,size)]
    if 0:
        mydu = 2*s[i,j]*(above+below+left+right)
        if i == size - 1: above = s[0,j]
        else:             above = s[i+1,j]

        if i == 0:        below = s[-1,j] # s[size,j]
        else:             below = s[i-1,j]

        if j == size - 1: right = s[i,0]
        else:             right = s[i,j+1]

        if j == 0:        left = s[i,-1]
        else:             left = s[i,j-1]
        du = 2*s[i,j]*(above+below+left+right)
        #assert(du==mydu)
        #print du,mydu

    return 2*s[i,j]*(above+below+left+right)

# Some magic to set up plotting
pylab.ion() # You need this

fig = pylab.figure()
ax =  fig.add_subplot(111)
import matplotlib.cm as cm

colorcounter = 0
energies = [0]
def colorsquare(s,showevery=None):
    global colorcounter,energies
    delay = 0.0
    if showevery is None:
        if size <= 10:
            showevery = 1
            delay = 5
        elif size <= 100:
            showevery = int(size*size/2)
        else:
            showevery = size*size
    if divmod(colorcounter,showevery)[1] == 0:
        fig.clear()
        if plot_extra:
            plt.subplot(2,2,1)
        pylab.imshow(s,interpolation='nearest',cmap=cm.Greys_r)
        if plot_extra:
            plt.subplot(2,2,2)
            if len(energies) > 100:
                plt.hist(energies,30)
            plt.subplot(2,1,2)
            plt.plot(energies)
        fig.canvas.draw()
        #sleep(delay)
        pylab.draw()
    colorcounter = colorcounter + 1

s = initialize()

numtrials = 100*size**2
print "numtrials",numtrials
showevery = int(numtrials/100)
#showevery = 1
for trial in xrange(numtrials):
    i = randint(size) # choose random row
    j = randint(size) # and random column
    ediff = deltaU(i,j)
    if ediff <= 0: # flipping reduces the energy
        s[i,j] = -s[i,j]
        colorsquare(s,showevery=showevery)
        energies.append(energies[-1] + ediff)
    else:
        if random() < np.exp(-ediff/T):
            s[i,j] = -s[i,j]
            colorsquare(s,showevery=showevery)
            energies.append(energies[-1] + ediff)
        else:
            energies.append(energies[-1])
        
raw_input()  # you need this.

