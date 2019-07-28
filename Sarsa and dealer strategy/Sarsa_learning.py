# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:55:07 2019

@author: chenmth
"""

import numpy as np
import pandas as pd

class Sarsa_table:
    
    def __init__(self, actions, learning_rate=0.5, reward_decay=0.9, e_greedy=0.99):
        self.actions = actions
        self.learning_rate = learning_rate 
        self.reward_decay = reward_decay
        self.e_greedy = e_greedy 
        
        self.s_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        
        self.result_table = pd.DataFrame

    def choose_action(self, observation):
        self.s_table.to_csv(r'D:\Computer Science\Semester 3\Project\code\Sarsa and dealer strategy\export_Sarsatable.csv', header=True)
        self.check_state_is_existed(observation) 
        
        if np.random.uniform() < self.e_greedy:
            state_action = self.s_table.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index)) 
            action = state_action.idxmax() 
        else:
            action = np.random.choice(self.actions)
        return action
   
    def learn(self, state, action, reward, state_, action_): # different with q learning
        
        self.check_state_is_existed(state_) 
         
        s_predict = self.s_table.loc[state, action]
         
        if state_ != 'terminal':
            s_target = reward + self.reward_decay * self.s_table.loc[state_, action_] #different with Q learning
        else:
            s_target = reward
        
        self.s_table.loc[state, action] += self.learning_rate * (s_target - s_predict) 
    
    def check_state_is_existed(self, state):
        
        if state not in self.s_table.index:
            self.s_table = self.s_table.append(
                    pd.Series(
                            [0]*len(self.actions), index = self.s_table.columns, name = state))