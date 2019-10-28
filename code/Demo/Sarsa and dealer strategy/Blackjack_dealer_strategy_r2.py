# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:00:25 2019

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
        
        self.bet10 = False # if bet 10
        self.bust = False  # if player bust
        self.dealer_bust = False # if dealer bust
        self.win = False # if player win 
        self.draw = False # if the game is draw
        
        #--------------for the test of reinforcement learning------------------
        self.action_space = ['no play', 'bet 10', 'bet 20']
        self.n_actions = len(self.action_space)
        
        self.asset = 100
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
    
    #-------------------------- action----------------------------------
    
    def deal_card_none(self): 
        self.dealer_hand = []
        self.player_hand = []
        shuffle(self.cards)
        self.win = 'no play'
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")
        
    def deal_card_ten(self):
        self.bet10 = True
        self.dealer_hand = []
        self.player_hand = []
        self.set_asset(10)
        shuffle(self.cards)
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")
        
        while self.update_score("player") < 17:
            if len(self.player_hand) > 5:
                break
            else:
                 self.hit("player")
            
        while self.update_score("dealer") < 17 and self.bust == False:
            if len(self.dealer_hand) > 5:
                break
            else:
                self.hit("dealer")
        
        if self.bust is True :
            pass
        elif self.dealer_bust is True:
            pass
        else:
            self.compare()
            
    def deal_card_twenty(self):
        self.dealer_hand = []
        self.player_hand = []
        self.set_asset(20)
        shuffle(self.cards)
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")
        
        while self.update_score("player") < 17:
            if len(self.player_hand) > 5:
                break
            else:
                 self.hit("player")
            
        while self.update_score("dealer") < 17 and self.bust == False:
            if len(self.dealer_hand) > 5:
                break
            else:
                self.hit("dealer")
        
        if self.bust is True :
            pass
        elif self.dealer_bust is True:
            pass
        else:
            self.compare()
    
    def hit(self, user): # hit the card if player's scores no bust
        if user == "player":
            self.deal_card("player")
            score = self.update_score("player")
            if score>21:
                self.bust = True                              
        elif user == "dealer":
            self.deal_card("dealer")
            score = self.update_score("dealer")
            if score>21:
                self.win = True
                self.dealer_bust = True
                if self.bet10 is True:
                    self.set_asset(-20)
                else:
                    self.set_asset(-40)

    def compare(self): # if no one bust, then compare each one scores
        p = self.update_score("player")
        d = self.update_score("dealer")
        if p>d:
            self.win = True
            if self.bet10 == True:
                self.set_asset(-20)
            else:
                self.set_asset(-40)
        elif p==d:
            self.draw = True
            self.win = 'draw'
            if(self.bet10):
                self.set_asset(-10)
            else:
                self.set_asset(-20)
        else:
            pass
                
    def reset(self):  # start the new game
        if len(self.cards) < 11:
            self.cards = cards()
        self.bust = False 
        self.dealer_bust = False
        self.win = False
        self.draw = False
        self.bet10 = False # if bet 10
        
    def reset_all_game(self): # start the new round
        self.get_goal_or_not = False
        self.count = 0
        self.cards = cards()
        self.bust = False 
        self.dealer_bust = False
        self.bet10 = False # if bet 10
        self.win = False
        self.draw = False
        self.asset = 100
        
    def step(self, action): # present the results under the action for reinforcement learning
        
        self.count += 1
        
        current_cards_state = []
        lo = []
        zero = []
        high = []
        for card in self.cards:
            if card == 2 or card == 3 or card == 4 or card == 5 or card == 6:
                lo.append(card)
            elif card == 7 or card == 8 or card == 9:
                zero.append(card)
            else:
                high.append(card)
        current_cards_state.append(len(lo))
        current_cards_state.append(len(zero))
        current_cards_state.append(len(high))
        
        current_asset = self.asset
        
        if action == 0: 
            self.deal_card_none()
        elif action == 1:   
            self.deal_card_ten()
        elif action == 2:   
            self.deal_card_twenty()
                        
        if self.asset >= 200:
            self.get_goal += 1
            self.get_goal_or_not = True
            reward = 2 # guickly win
            done = True
            s_ = 'terminal'
            with open('strategy.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([current_cards_state, action, self.win, current_asset, self.asset, 'achieve goal assets'])

        elif self.asset < 10:
            reward = -2 # lose too quickly
            done = True
            s_ = 'terminal'
            with open('strategy.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([current_cards_state, action, self.win, current_asset, self.asset, 'assets return to zero'])
                
        #---------limitation of playing times----------------
        elif self.count == 20:
            if self.asset > 110: # at least win 20
                self.get_goal += 1
                self.get_goal_or_not = True
                reward = 1
                done = True
                s_ = 'terminal'
                with open('strategy.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([current_cards_state, action, self.win, current_asset, self.asset, 'times out and win'])
                
            else:
                reward = -1
                done = True
                s_ = 'terminal'
                with open('strategy.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([current_cards_state, action, self.win, current_asset, self.asset, 'times out and lose'])
        #----------------------------------------------------
        else:
            reward = 0
            done = False
            s_ = current_cards_state
            with open('strategy.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([current_cards_state, action, self.win, current_asset, self.asset, 'continue'])
               
        self.reset()

        return s_, reward, done
    
def cards():
    
    cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]*4 # 2 decks
    return cards       
        