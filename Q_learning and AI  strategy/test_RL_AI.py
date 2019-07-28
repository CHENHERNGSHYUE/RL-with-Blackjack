# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 11:27:46 2019

@author: chenmth
"""

from Blackjack_AI_strategy import Blackjack
from Q_learning_AI import QLtable
import csv

def update():
    for episode in range(10000):
        
        print("----------------Game{}----------------".format(episode+1))
        observation = env.reset_all_game()
        
        while True:
            
            action = rl.choose_action(str(observation))
            
            observation_, reward, done = env.step(action)
            
            rl.learn(str(observation), action, reward, str(observation_))
            
            observation = observation_
            
            if done:
                winning_rate = env.get_goal/(episode+1)
                print(env.get_goal_or_not)
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
