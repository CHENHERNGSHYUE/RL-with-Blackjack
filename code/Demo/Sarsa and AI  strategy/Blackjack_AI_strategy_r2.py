# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:34:58 2019

@author: Herng-Shyue, Chen
"""

from random import shuffle
import csv

class Blackjack(object): 
    
    def __init__(self):
         
        super(Blackjack, self).__init__()
       
        self.get_goal = 0 # for calculating winning rate
        self.get_goal_or_not = False # for deciding the way of record (win or lose)
        
        self.count = 0 #  for calculating the playing times in each round
        self.hide_card = None # dealer's unshown card
        
        self.bust = False  # if player bust
        self.win = False # if player win
        self.draw = False # if the game is draw
        self.double = False # if player make double action
        self.surrenders = False # if player make surrender action
        
        #--------------for the test of reinforcement learning------------------
        self.action_space = ['hit', 'stay', 'no play', 'double']
        self.n_actions = len(self.action_space)
        
        self.asset = 90 # original assets = 100-10 due to the play is operate directly after starting the new round
        self.cards = cards()

    def set_asset(self, asset_): # wager and control the assets
        self.asset -= asset_
        
    def deal_card(self, user): # inspired by Daniel P.
        card = self.cards.pop(0)
        if user == "dealer":
            self.dealer_hand.append(card)
        elif user == "player":
            self.player_hand.append(card)
        return card
    
    def update_score(self, user): # inspired by Daniel P.
        score = 0
        has_ace = False
        if user == "dealer":
            hand = self.dealer_hand
        elif user == "player":
            hand = self.player_hand
        for card in hand:
            value = card
            if value == 1:
                value = 11
                has_ace = True
            score += value
            if score > 21 and has_ace:
                score -= 10
                has_ace = False
        return score
    
    def _play(self): # start the new game
        
        self.set_asset(10) # wager
        
        if len(self.cards) < 11: # there are at least ten cards in the deck or renew a new deck with 52 cards
            self.cards = cards()
        shuffle(self.cards)
        
        self.playerScore = 0
        self.dealerScore = 0
        
        self.surrenders = False
        self.bust = False 
        self.win = False
        self.draw = False
        self.double = False
        
        #-------------inspired by Daniel P.---------------
        self.dealer_hand = []
        self.player_hand = []
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")

        self.playerScore = self.update_score("player")
    
    def hit(self): # hit the card if player's scores no bust
        self.deal_card("player") 
        self.playerScore = self.update_score("player")
        if self.playerScore > 21:
            self.bust = True
                  
    def stand(self): # stand the card
        self.dealerScore = self.update_score("dealer")
        while self.dealerScore < 17 and len(self.dealer_hand) < 5:
            self.deal_card("dealer")
            self.dealerScore = self.update_score("dealer")
        if self.dealerScore > 21:
            if self.double == True:
                self.set_asset(-40)
            else:
                self.set_asset(-20)
            self.win = True
        else:
            self.compare()
   
    def _double(self): # double action, player wagers double assets and just can hit one time
        self.set_asset(10)
        self.double = True
        self.deal_card("player")
        self.playerScore = self.update_score("player")
        if self.playerScore > 21:
            self.bust = True
        else:
            self.stand()
            
    def surrender(self): # surrender action, player calls back half of asset and starts next game directly
        self.surrenders = True
        self.set_asset(-10) # go to next round directly
        self.win = 'no play'
        self.dealerScore = self.update_score("dealer")
         
    def compare(self):  # compare dealer and player's scores if player no bust
        
        if self.playerScore > self.dealerScore:
            if self.double == True:
                self.set_asset(-40)
            else:
                self.set_asset(-20)
            self.win = True
        elif self.playerScore == self.dealerScore:
            if self.double == True:
                self.set_asset(-20)
            else:
                self.set_asset(-10)
            self.draw = True
        else:
            self.win = False
        
    def reset_all_game(self): # start the new round
        self.get_goal_or_not = False
        self.count = 0
        self.cards = cards()
        shuffle(self.cards)

        self.playerScore = 0
        self.dealerScore = 0
        
        self.bust = False 
        self.win = False
        self.draw = False
        self.double = False
        self.surrenders = False
        self.asset = 90
        
        #-------------inspired by Daniel P.---------------
        self.dealer_hand = []
        self.player_hand = []
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")

        self.playerScore = self.update_score("player")
        
    def step(self, action): # the action performed through Sarsa learning
        
        self.count += 1
        
        current_cards_state = []
        less_7 = []
        seven = []
        big_7 = []
        for card in self.cards:
            if card < 7:
                less_7.append(card)
            elif card == 7:
                seven.append(card)
            else:
                big_7.append(card)
        current_cards_state.append(len(less_7))
        current_cards_state.append(len(seven))
        current_cards_state.append(len(big_7))
        
        player_current_scores = self.player_hand[0]+self.player_hand[1]
        
        if action == 0:
            while self.playerScore < 19: # decide evaluation
                if len(self.player_hand) < 5:
                    self.hit()
                else:
                    break
            self.stand()           
        elif action == 1: 
            self.stand()
        elif action == 2:
            self.surrender()
        elif action == 3:
            self._double()           
        
        if self.asset >= 200:
            self.get_goal += 1
            self.get_goal_or_not = True
            reward = 1
            done = True
            s_ = 'terminal'
            with open('strategy.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['next', 'next', 'next', 'next', 'next'])
            
        elif self.asset < 5:
            reward = -1
            done = True
            s_ = 'terminal'
            with open('strategy.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['next', 'next', 'next', 'next', 'next'])
                
        #---------limitation of playing times----------------
        elif self.count == 20:
            if self.asset > 100:
                if self.win == True:
                    self.get_goal += 1
                    self.get_goal_or_not = True
                    reward = 1
                    done = True
                    s_ = 'terminal'
                    with open('strategy.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['next', 'next', 'next', 'next', 'next'])
                else:
                    reward = -1
                    done = True
                    s_ = 'terminal'
                    with open('strategy.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['next', 'next', 'next', 'next', 'next'])
            else:
                reward = -1
                done = True
                s_ = 'terminal'
                with open('strategy.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['next', 'next', 'next', 'next', 'next'])
        #--------------------------------------------------
              
        elif self.win == True:
            if self.double:
                reward = 2
            else:
                reward = 1
            done = False
            s_ = self.dealer_hand[0], player_current_scores, current_cards_state
            with open('strategy.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([self.dealer_hand[0], player_current_scores, 
                                 current_cards_state, action, self.win])
       
        else:
            if self.double:
                reward = -2
            else:
                reward = -1
            done = False
            s_ = self.dealer_hand[0], player_current_scores, current_cards_state
            with open('strategy.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([self.dealer_hand[0], player_current_scores, 
                                 current_cards_state, action, self.win])
#        else:
#            reward = 0
#            done = False
#            s_ = self.dealer_hand[0], player_current_scores, current_cards_state
            
          
        self._play()
        
        return s_, reward, done

def cards(): # renew the deck to 52 cards
    
    cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]*4
        
    return cards       