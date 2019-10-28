# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:00:25 2019

@author: Herng-Shyue Chen
"""

from random import shuffle

class Blackjack(object): 
    
    def __init__(self):
         
        super(Blackjack, self).__init__()
        
        self.get_goal = 0 # for calculating winning rate
        self.get_goal_or_not = False # for deciding the way of record (win or lose)
        
        self.count = 0 #  for calculating the playing times in each round
        
        self.bet = False # if no bet
        self.bust = False  # if player bust
        self.win = False # if player win 
        self.draw = False # if the game is draw
        
        #--------------for the test of reinforcement learning------------------
        self.action_space = ['bet 10', 'bet 20']
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
    
    #-------------------------- bet or not bet----------------------------------
    
    def deal_card_none(self): 
        self.dealer_hand = []
        self.player_hand = []
        self.bet = True
        shuffle(self.cards)
        self.win = 'no play'
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")
        
    def deal_card_ten(self):
        self.bet == True
        self.dealer_hand = []
        self.player_hand = []
        self.set_asset(10)
        shuffle(self.cards)
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")
        
        while self.update_score("player") < 12:
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
        elif self.win is True:
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
                self.set_asset(-20)

    def compare(self): # if no one bust, then compare each one scores
        p = self.update_score("player")
        d = self.update_score("dealer")
        if p>d and p<22:
            self.win = True
            self.set_asset(-20)
        elif p==d:
            self.draw = True
            self.set_asset(-10)
        else:
            pass
                
    def reset(self):  # start the new game
        if len(self.cards) < 11:
            self.cards = cards()
        self.bust = False 
        self.win = False
        self.draw = False
        self.bet = False
        
    def reset_all_game(self): # start the new round
        self.get_goal_or_not = False
        self.count = 0
        self.cards = cards()
        self.bust = False 
        self.bet = False
        self.win = False
        self.draw = False
        self.asset = 100
        
    def step(self, action): # present the results under the action for reinforcement learning
        
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
        
        if action == 0: 
            self.deal_card_none()
        elif action == 1:   
            self.deal_card_ten()
                        
        if self.asset >= 200:
            self.get_goal += 1
            self.get_goal_or_not = True
            reward = 1
            done = True
            s_ = 'terminal'

        elif self.asset < 10:
            reward = -1
            done = True
            s_ = 'terminal'
                
        #---------limitation of playing times----------------
        elif self.count == 20:
            if self.asset > 100:
                self.get_goal += 1
                self.get_goal_or_not = True
                reward = 1
                done = True
                s_ = 'terminal'
                
            else:
                reward = -1
                done = True
                s_ = 'terminal'
        #----------------------------------------------------
                    
        elif self.bet == True:
            if self.win == True:
                reward = 1
                done = False
                s_ = self.asset, current_cards_state

            else:
                reward = -1
                done = False
                s_ = self.asset, current_cards_state

        else:
            reward = 0
            done = False
            s_ = self.asset, current_cards_state
               
        self.reset()

        return s_, reward, done
    
def cards():
    
    cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]*4
    return cards       