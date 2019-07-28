# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:34:58 2019

@author: chenmth
"""

from random import shuffle

class Blackjack(object): 
    
    def __init__(self):
         
        super(Blackjack, self).__init__()
        self.get_goal = 0
        self.get_goal_or_not = False
        self.count = 0
        self.hide_card = None
        self.action_space = ['hit', 'stay', 'surrender', 'double', 'hit more']
        self.playerScore = 0
        self.dealerScore = 0
        self.bet = False 
        self.burst = False 
        self.win = False
        self.draw = False
        self.double = False
        self.surrenders = False 
        self.n_actions = len(self.action_space)
        self.asset = 90
        self.cards = cards()

    def set_asset(self, asset_):
        self.asset -= asset_
        
    def get_asset(self):
        return self.asset
        
    def get_burst(self):
        return self.burst
    
    def _play(self):
        
        self.set_asset(10)
        
        if len(self.cards) < 10:
            self.cards = cards()
        shuffle(self.cards)
        
        self.playerScore = 0
        self.dealerScore = 0
        
        self.surrenders = False
        self.bet = False 
        self.burst = False 
        self.win = False
        self.draw = False
        self.double = False
        
        self.dealer_hand = []
        self.player_hand = []
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")

        self.playerScore = self.update_score("player")
    
    def deal_card(self, user):
        card = self.cards.pop(0)
        if user == "dealer":
            self.dealer_hand.append(card)
        elif user == "player":
            self.player_hand.append(card)
        return card
    
    def update_score(self, user):
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
            elif value > 10:
                value = 10
            score += value
            if score > 21 and has_ace:
                score -= 10
                has_ace = False
        return score
    
    def hit(self):
        self.deal_card("player") 
        self.playerScore = self.update_score("player")
        if self.playerScore > 21:
            self.burst = True
        elif len(self.player_hand) == 5:
            self.stand()
                  
    def stand(self):
        self.dealerScore = self.update_score("dealer")
        while self.dealerScore < 17:
            self.deal_card("dealer")
            self.dealerScore = self.update_score("dealer")
            if len(self.dealer_hand) == 5:
                break
        if self.dealerScore > 21:
            if self.double == True:
                self.set_asset(-40)
            else:
                self.set_asset(-20)
            self.win = True
        else:
            self.compare()
   
    def _double(self):
        self.set_asset(10)
        self.double = True
        self.deal_card("player")
        self.playerScore = self.update_score("player")
        if self.playerScore > 21:
            self.burst = True
        else:
            self.stand()
            
    def surrender(self):
        self.surrenders = True
        self.set_asset(-5)
        self.dealerScore = self.update_score("dealer")
         
    def compare(self):
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
        
    def reset_all_game(self):
        self.get_goal_or_not = False
        self.count = 0
        self.cards = cards()
        
        self.dealer_hand = []
        self.player_hand = []
        
        self.playerScore = 0
        self.dealerScore = 0
        
        self.bet = False 
        self.burst = False 
        self.win = False
        self.draw = False
        self.double = False
        self.surrenders = False
        self.asset = 90
        self.start()
        
    def step(self, action):
        
        self.count += 1
        
        current_cards_state = []
        for card in self.cards:
            current_cards_state.append(card)
        current_cards_state.append(self.dealer_hand[1])
        current_cards_state.sort()
        
        player_current_cards_state = []
        player_current_cards_state.append(self.player_hand[0])
        player_current_cards_state.append(self.player_hand[1])
        player_current_cards_state.sort()
        
        if action == 0:
            self.hit()
        elif action == 1: 
            self.stand()
        elif action == 2:
            self.surrender()
        elif action == 3:
            self._double()
        elif action == 4:
            self.hit()
            while self.playerScore < 17:
                self.hit()
        
        if self.get_asset() >= 150:
            print('win')
            self.get_goal += 1
            self.get_goal_or_not = True
            if self.double:
                reward = 2
            else:
                reward = 1
            done = True
            s_ = 'terminal'
        elif self.get_asset() < 5:
            if self.double:
                reward = -2
            else:
                reward = -1
            done = True
            s_ = 'terminal'
        elif self.win:
            if self.double:
                reward = 2
            else:
                reward = 1
            done = False
            s_ = self.dealer_hand[0], player_current_cards_state, current_cards_state
        else:
            if self.surrenders and (self.playerScore < self.dealerScore) and ((self.playerScore + self.cards[0]) > 21):
                reward = 1
            elif self.double:
                reward = -2
            else:
                reward = -1
            done = False
            s_ = self.dealer_hand[0], player_current_cards_state, current_cards_state
            
        self._play()
        
        return s_, reward, done
    
    def start(self):
        self.dealer_hand = []
        self.player_hand = []
        self.set_asset(10)
        shuffle(self.cards)
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")

        self.update_score("player")

def cards():
    
    cards = [0]*52
    p = n = 0
    value = 1
    
    for card in cards:
        cards[cards.index(card)] = value
        if n < 12:
            n += 1
            value += 1
        else:
            n = 0
            value = 1
            p += 1    
        
    return cards       