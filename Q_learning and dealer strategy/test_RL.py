# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:12:28 2019

@author: chenmth
"""

from Blackjack_dealer_strategy import Blackjack
from Q_learning import QLtable
import time as t

def update():
    for episode in range(2):
        
        print("----------------Game{}----------------".format(episode+1))
        observation = env.reset_all_game()
        
        while True:
            
            action = rl.choose_action(str(observation))
            
            observation_, reward, done = env.step(action)
            
            #t.sleep(10)
            
            rl.learn(str(observation), action, reward, str(observation_))
            
            observation = observation_
            
            if done:
                break
            
    print("End test") #just run 100 times
    env.destroy()

if __name__ == "__main__":
    env = Blackjack()
    rl = QLtable(actions=list(range(env.n_actions)))
    
    env.after(200, update) #after(delay_ms, callback=None, *args)
    env.mainloop()
    