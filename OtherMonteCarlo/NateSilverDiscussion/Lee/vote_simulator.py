#!/usr/bin/env python
'''
Created on Nov 2, 2012

Author: Lee Clemmer
'''

from random import random
import math
import polling_data
import ec_votes

def state_prob(name,poll_D,poll_R,moe,iterations):
    '''
    This function takes a state name, its D & R polls, margin of error, and number of iterations.
    It then randomly picks a value within the MOE range for each D & R poll, picks an actual vote value based
    on the MOE and given poll value, and determines a winner.  It does this 'iteration' number of times.
    Finally what's returned is the percent value that either D or R won the vote.
    '''
    winner_R = 0
    winner_D = 0
    winner_O = 0
    winner_Tie = 0
    
    # First check if spread is within MOE; if not, no simulations needed (saving time)
    if math.fabs(poll_D - poll_R) <= (2 * moe):
        for i in range(iterations):
            # Define MOE for each party
            RMOE = random() * moe * 2 - moe
            DMOE = random() * moe * 2 - moe
            OMOE = random() * moe * 2 - moe
            
            # Calculate vote percentage based on MOE
            R_votes = poll_R + RMOE
            D_votes = poll_D + DMOE
            O_votes = 100 - poll_R - poll_D + OMOE
            
            # Determine Winner
            winner = max(R_votes,D_votes,O_votes)
            if R_votes == winner:
                winner_R += 1
            elif D_votes == winner:
                winner_D += 1
            elif O_votes == winner:
                winner_O += 1
            else:
                winner_Tie += 1
    else:
        if poll_D > poll_R:
            winner_D += 1
        elif poll_R > poll_D:
            winner_R += 1
        iterations = 1.0
    
    print '%s,%s,%s'%(name,winner_D / (iterations * 1.0),winner_R / (iterations * 1.0))
    
    return (name,winner_D / (iterations * 1.0),winner_R / (iterations * 1.0))

def state_avg(state_polls,falloff):
    '''
    This function takes a list of all polls for a given state and calculates the average for D and R.
    Falloff determines how many polls to use, going back from the most recent.
    Returns a list with average D poll, average R poll, and average margin of error.
    '''
    total_D = 0
    total_R = 0
    total_MOE = 0
    
    for i in range(falloff):
        try:
            total_D += state_polls[i][1]
            total_R += state_polls[i][2]
            total_MOE += state_polls[i][3]
        except:
            break

    mean_D = falloff > len(state_polls) and total_D/len(state_polls) or total_D/falloff
    mean_R = falloff > len(state_polls) and total_R/len(state_polls) or total_R/falloff
    mean_MOE = falloff > len(state_polls) and total_MOE/len(state_polls) or total_MOE/falloff
    
    return [mean_D,mean_R,mean_MOE]

def competitive_states(state_probs):
    return [state for state in state_probs if state[1] != 0.0 and state[2] != 0.0]

def non_competitive_states(state_probs):
    return [state for state in state_probs if state[1] == 0 or state[2] == 0]

def vote(D_base,R_base,comp_states):
    '''
    This function simulates one election being held.  It takes the guaranteed D and R votes
    and then determines the winner of each state randomly using the passed probabilities 
    in comp_states. Finally it returns a list containing:
    [D_states_won (string of state abbreviations),R_states_won,D_EC_votes,R_EC_votes,winner]
    '''
    D_votes = 0
    R_votes = 0
    
    D_states_won = ''
    R_states_won = ''
    
    winner = ''
    
    for state in comp_states:
        x = random()
        if x <= state[1]:
            D_votes += ec_votes.Electoral_College[state[0]][1]
            D_states_won += ec_votes.Electoral_College[state[0]][0] + '-'
        elif x > (1 - state[2]):
            R_votes += ec_votes.Electoral_College[state[0]][1]
            R_states_won += ec_votes.Electoral_College[state[0]][0] + '-'
    
    D_votes += D_base
    R_votes += R_base
    
    if D_votes > R_votes:
        winner = 'D'
    elif R_votes > D_votes:
        winner = 'R'
    else:
        winner = 'Tie'        
    
    return [D_states_won,R_states_won,D_votes,R_votes,winner]
    
if __name__ == '__main__':
    # Setting: how many times to run simulation
    iterations = 1000000
    
    # Setting: how many polls to look back, i.e. "look at the last X number of polls"
    falloff = 10
    
    # This list will hold the states and the D & R poll averages
    state_avgs = []
    
    # Calculate poll averages for states using data in polling_data
    for state in polling_data.States:
        state_avgs.append([state] + state_avg(polling_data.States[state],falloff))
    
    # Sort the state averages list alphabetically
    state_avgs.sort()
    
    print state_avgs
    
    # Calculate the probabilities for D & R for each state using the state poll averages
    state_probs = []
    for state_avg in state_avgs:
        state_probs.append(state_prob(state_avg[0],state_avg[1],state_avg[2],state_avg[3],iterations))
    
    D_votes = 0
    R_votes = 0
    
    # Determine EC votes for non-competitive states (100% certain to fall one way or the other)
    for state in non_competitive_states(state_probs):
        if state[1] == 1:
            D_votes += ec_votes.Electoral_College[state[0]][1]
        elif state[2] == 1:
            R_votes += ec_votes.Electoral_College[state[0]][1]
    
    print 'Base Dem votes: %s'%(D_votes)
    print 'Base Rep votes: %s'%(R_votes)
    print 'Hold on... still loading...'
    
    # Determine EC votes for competitive
    
    ''' 
    Outcomes is a dictionary in format
    outcomes = {'D':{'CO-IA-M2-MI-MN-NV-NH-OH-PA-WI-':[290,4],
                      'AZ-CO-IA-M2-MI-MN-NV-OH-PA-VA-WI-':[310,1]},
                'R':{'AZ-FL-N2-NC-VA-':[248,4]}}
    '''
    outcomes = {'D':{},
                'R':{}}
    
    D_wins = 0
    R_wins = 0
    Ties = 0
    
    for i in range(iterations):
        outcome = vote(D_votes,R_votes,competitive_states(state_probs))
        if outcome[4] == 'D': D_wins += 1
        elif outcome[4] == 'R': R_wins += 1
        elif outcome[4] == 'Tie': Ties += 1
        
        if outcome[0] in outcomes['D']:
            # The outcome has happened before, so increment counter
            outcomes['D'][outcome[0]][1] += 1
        elif outcome[0] not in outcomes['D']:
            # This is a new outcome, so add it to outcome and initialize at 1
            outcomes['D'][outcome[0]] = [outcome[2],1]
            
        if outcome[1] in outcomes['R']:
            # The outcome has happened before, so increment counter
            outcomes['R'][outcome[1]][1] += 1
        elif outcome[1] not in outcomes['R']:
            # This is a new outcome, so add it to outcome and initialize at 1
            outcomes['R'][outcome[1]] = [outcome[3],1]
    print outcomes    
    print 'D wins: %s, %s%%'%(D_wins,D_wins/(iterations*1.0)*100)
    print 'R wins: %s, %s%%'%(R_wins,R_wins/(iterations*1.0)*100)
    print 'Ties: %s, %s%%'%(Ties,Ties/(iterations*1.0)*100)
