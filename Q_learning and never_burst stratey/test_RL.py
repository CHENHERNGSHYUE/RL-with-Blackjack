# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:12:28 2019

@author: chenmth
"""

from Blackjack_never_burst__strategy import Blackjack
from Q_learning import QLtable
import csv

def update():
    for episode in range(10):
        
        print("----------------Game{}----------------".format(episode+1))
        observation = env.reset_all_game()
        
        while True:
            
            action = rl.choose_action(str(observation))
            
            observation_, reward, done = env.step(action)
            
            rl.learn(str(observation), action, reward, str(observation_))
            
            observation = observation_
            
            if done:
                winning_rate = env.get_goal/(episode+1)
                if env.get_goal_or_not:
                    with open('Q_table_test_result.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([episode+1, env.count, 'win', winning_rate])
                else:
                     with open('Q_table_test_result.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([episode+1, env.count, 'fail', winning_rate])
                break
            
if __name__ == "__main__":
    with open('Q_table_test_result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Round', 'Playing times', 'Result', 'Accumulating_winning_rate'])
    env = Blackjack()
    rl = QLtable(actions=list(range(env.n_actions)))
    update()
    