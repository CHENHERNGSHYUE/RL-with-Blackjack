# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:57:00 2019

@author: Herng-Shyue, Chen
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:12:28 2019

@author: chenmth
"""

from Blackjack_never_bust_strategy_2 import Blackjack
from Sarsa_learning_r2 import Sarsa_table
import csv
import time
import matplotlib.pyplot as plt

def update(): # inspired by Morvan
    for episode in range(1000): # set the testing rounds
        
        print("----------------Round {}----------------".format(episode+1)) # monitor the testing process
        observation = env.reset_all_game() # start the new round
        
        action = rl.choose_action(str(observation)) # select the action first
        
        while True: # loop (playing times) within each round
            
            observation_, reward, done = env.step(action) # make action and feedback the results
            
            action_ = rl.choose_action(str(observation_)) # choose next action according to the next state
            
            rl.learn(str(observation), action, reward, str(observation_), action_) # Sarsa learning method
            
            observation = observation_ # update state
            
            action = action_ # update action (on-policy)
            if done: # achieve the goal or faliure, then done would be true
                
                winning_rate = env.get_goal/(episode+1) # calculate the current winning rate
                
                #------------------------------make record----------------------------------
                if env.get_goal_or_not:
                    with open('S_table_test_result.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([episode+1, 'win', winning_rate])
                else:
                     with open('S_table_test_result.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([episode+1, 'fail', winning_rate])
                break

if __name__ == "__main__":
    with open('S_table_test_result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Round', 'Result', 'Accumulating_winning_rate'])

    start = time.time() # calculate total testing time
    env = Blackjack()
    rl = Sarsa_table(actions=list(range(env.n_actions)))
    update()
    end = time.time()
    
    rl.s_table.to_csv(r'export_Sarsatable.csv', header=True)
    
    print('The total time is {} seconds'.format(end-start))
    
    #------------------------------create diagram-------------------------------
    y_win = []
    with open('S_table_test_result.csv', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            y_win.append(round(float(row['Accumulating_winning_rate']),5))
    plt.plot(y_win)
    plt.ylabel('Winning Rate')
    plt.xlabel('Round')
    plt.ylim(0,1.2)
    plt.show()