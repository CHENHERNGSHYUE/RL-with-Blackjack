# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:55:07 2019

@author: Herng-Shyue, Chen
"""

import numpy as np
import pandas as pd

class Sarsa_table: # inspired by Morvan Z.
    
    def __init__(self, actions, learning_rate=0.5, reward_decay=0.999, e_greedy=0.8): # define parameter
        
        self.actions = actions
        self.learning_rate = learning_rate # for learning
        self.reward_decay = reward_decay # decaying rate for learning
        self.e_greedy = e_greedy # for choosing action
        
        self.s_table = pd.DataFrame(columns=self.actions, dtype=np.float64) # create Sarsa table

    def choose_action(self, observation):
        
        self.check_state_is_existed(observation) # check if state has existed or add to the Sarsa table
        
        if np.random.uniform() < self.e_greedy: # for explore more state or exploit the past information
            state_action = self.s_table.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index)) # avoid select specific action when two Q-values are always the same
            action = state_action.idxmax() 
        else:
            action = np.random.choice(self.actions) # greedy -> select random action
        return action
   
    def learn(self, state, action, reward, state_, action_): # different with q learning
        
        self.check_state_is_existed(state_) 
         
        s_predict = self.s_table.loc[state, action]
         
        if state_ != 'terminal':
            s_target = reward + self.reward_decay * self.s_table.loc[state_, action_] # for calculating loss
        else:
            s_target = reward
        
        self.s_table.loc[state, action] += self.learning_rate * (s_target - s_predict) 
    
    def check_state_is_existed(self, state): # examine and add new states into Sarsa table
        
        if state not in self.s_table.index:
            self.s_table = self.s_table.append(
                    pd.Series(
                            [0]*len(self.actions), index = self.s_table.columns, name = state))