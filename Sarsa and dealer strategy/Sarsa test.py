# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:57:00 2019

@author: chenmth
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:12:28 2019

@author: chenmth
"""

from Blackjack_dealer_strategy_2 import Blackjack
from Sarsa_learning import Sarsa_table
import csv

def update():
    for episode in range(10):
        
        print("----------------Game{}----------------".format(episode+1))
        observation = env.reset_all_game()
        
        action = rl.choose_action(str(observation)) # Sarsa method
        
        while True:
            
            observation_, reward, done = env.step(action)
            
            action_ = rl.choose_action(str(observation_)) # Sarsa method
            
            rl.learn(str(observation), action, reward, str(observation_), action_) # Sarsa method
            
            observation = observation_
            
            action = action_ # Sarsa method
            
            if done:
                winning_rate = env.get_goal/(episode+1)
                if env.get_goal_or_not:
                    with open('S_table_test_result.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([episode+1, env.count, 'win', winning_rate])
                else:
                     with open('S_table_test_result.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([episode+1, env.count, 'fail', winning_rate])
                break

if __name__ == "__main__":
    with open('S_table_test_result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Round', 'Playing times', 'Result', 'Accumulating_winning_rate'])
    env = Blackjack()
    rl = Sarsa_table(actions=list(range(env.n_actions)))
    update()
    