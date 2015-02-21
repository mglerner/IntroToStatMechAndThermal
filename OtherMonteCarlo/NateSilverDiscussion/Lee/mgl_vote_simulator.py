#!/usr/bin/env python

"""
My strategy: we'll let the nation vote N times. Each time, each state
picks an answer according to a normal distribution with the
appropriate stdev. This is actually little strange to do, since the
polls give DEM, REP, MOE. So, we'll pick DEM numbers and REP numbers
independently, then pick a winner.

This is different from calculating individual state probabilities and
then summing them.

MOE = stdev * 2
"""

from __future__ import division

import numpy as np
from numpy import array,random,zeros,hstack
from numpy.random import normal
import matplotlib.pyplot as plt
from collections import Counter
import polling_data, ec_votes

# For efficiency, let's fix some orders

STATE_NAMES = array(polling_data.States.keys())
SHORT_STATE_NAMES = array([ec_votes.Electoral_College[state][0] for state in STATE_NAMES])
EC_VOTES = array([ec_votes.Electoral_College[state][1] for state in STATE_NAMES])

def get_drm_probs(falloff,reverse=False):
    #dem_p,rep_p,moe = state_avg(polling_data.States[state],falloff)
    result = [polling_data.state_avg(polling_data.States[state],falloff,reverse) for state in STATE_NAMES]
    return array(result)


def nation_vote_once(D,R,STD):
    """
    
    Arguments:
     - `D`: Dem percentage in poll, array, one element per state
     - `R`: Rep percentage in poll, array, one element per state
     - `STD`: Poll standard deviation (not MOE), array, one element per state
    """
    dem = normal(loc=D,scale=STD)
    rep = normal(loc=R,scale=STD)
    ec_dem = EC_VOTES[dem>rep]
    return dem,rep,ec_dem.sum()

def nation_vote(trials,falloff=10,reverse=False):
    DRM_PROBS = get_drm_probs(falloff,reverse)
    D = DRM_PROBS[:,0]
    R = DRM_PROBS[:,1]
    MOE = DRM_PROBS[:,2]
    STD = MOE/2
    
    results = array([nation_vote_once(D,R,STD) for i in range(trials)])

    dem = results[:,0]
    rep = results[:,1]
    ec_dem = results[:,2]

    dem_win_pct = sum(ec_dem > 270) / len(ec_dem)
    print dem_win_pct
    bin_edges = range(538)
    frequencies,bin_edges = np.histogram(ec_dem,bins=bin_edges)

    colors = 'r'*270 + 'b'*(538-270)
    plt.clf()
    # For a histogram, the heights would just be frequencies. We'll
    # scale it by trials to get percentages
    plt.bar(bin_edges[:-1],frequencies/trials,width=bin_edges[1]-bin_edges[0],color=colors)
    plt.title("Obama win percent: %s%% with %s trials"%(100*dem_win_pct,trials))
    plt.xlabel('Obama electoral vote count')
    plt.ylabel('Probability of this outcome')

    # Now we want to determine the paths to victory. That means
    # figuring out which states are competitive and counting up the
    # others.

    # Competitive states are states where the spread is greater than the MOE.
    competitive = abs(D - R) < 2*MOE
    print "Competitive states",SHORT_STATE_NAMES[competitive]
    dem_win_paths = ['-'.join(SHORT_STATE_NAMES[(d > r)*competitive]) for (d,r) in zip(dem,rep)]
    rep_win_paths = ['-'.join(SHORT_STATE_NAMES[(d < r)*competitive]) for (d,r) in zip(dem,rep)]

    dc = Counter(dem_win_paths)
    rc = Counter(rep_win_paths)
    print "Most common Dem win paths"
    for (win_path,count) in dc.most_common(10):
        print win_path
    print "Most common Rep win paths"
    for (win_path,count) in rc.most_common(10):
        print win_path
    

