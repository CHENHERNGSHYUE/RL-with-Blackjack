# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 11:26:35 2019

@author: chenmth
"""

import numpy as np
import pandas as pd

class QLtable:
    
    def __init__(self, actions, learning_rate=0.05, reward_decay=0.999, e_greedy=0.9):
        self.actions = actions
        self.learning_rate = learning_rate # alpha
        self.reward_decay = reward_decay # gamma
        self.e_greedy = e_greedy # epsilon
        
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        
    def choose_action(self, observation):
        self.q_table.to_csv(r'D:\Computer Science\Semester 3\Project\code\Q_learning and AI  strategy\table.csv', header=True)
        self.check_state_is_existed(observation) #check state is existed or not
        
        if np.random.uniform() < self.e_greedy:#uniform is the same as random for float number, while randit is for int number
            state_action = self.q_table.loc[observation, :] #iloc is for index (x,y) instead of name
            state_action = state_action.reindex(np.random.permutation(state_action.index)) # re-arrange the index to avoid the same value
            action = state_action.idxmax() 
        else:
            action = np.random.choice(self.actions)
        return action
   
    def learn(self, state, action, reward, state_):
        
        self.check_state_is_existed(state_) #check the next state is existed or not
         
        q_predict = self.q_table.loc[state, action]
         
        if state_ != 'terminal':
            q_target = reward + self.reward_decay * self.q_table.loc[state_, :].max()
        else:
            q_target = reward
        
        self.q_table.loc[state, action] += self.learning_rate * (q_target - q_predict) # update
    
    def check_state_is_existed(self, state):
        
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                    pd.Series(
                            [0]*len(self.actions), index = self.q_table.columns, name = state))