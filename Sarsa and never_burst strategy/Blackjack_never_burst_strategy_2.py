# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:58:28 2019

@author: chenmth
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:00:25 2019

@author: chenmth
"""

from random import shuffle

class Blackjack(object): 
    
    def __init__(self):
         
        super(Blackjack, self).__init__()
        self.get_goal = 0
        self.get_goal_or_not = False
        self.count = 0
        self.action_space = ['bet 10', 'bet 20']
        self.bet = False 
        self.win = False
        self.draw = False
        self.n_actions = len(self.action_space)
        self.asset = 100
        self.cards = cards()

    def set_asset(self, asset_):
        self.asset -= asset_
        
    def get_asset(self):
        return self.asset
    
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
    
    def deal_card_ten(self):
        self.dealer_hand = []
        self.player_hand = []
        self.bet = True
        self.set_asset(10)
        shuffle(self.cards)
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")

        self.update_score("player")
        self.update_score("dealer")
        
        while self.update_score("player") < 12:
            self.hit("player")
            
        while self.update_score("dealer") < 17:
            self.hit("dealer")
        
        if self.win is True:
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
        
        while self.update_score("player") < 12:
            self.hit("player")
            
        while self.update_score("dealer") < 17:
            self.hit("dealer")

        if self.win is True:
            pass
        else:
            self.compare()
    
    def hit(self, user):
        if user == "player":
            self.deal_card("player")
            score = self.update_score("player")       
                
        elif user == "dealer":
            self.deal_card("dealer")
            score = self.update_score("dealer")
            if score>21:
                self.win = True
                print('win')
                if(self.bet):
                    self.set_asset(-20)
                else:
                    self.set_asset(-40)

    def compare(self):
        p = self.update_score("player")
        d = self.update_score("dealer")
        if p>d and p<22:
            print('win')
            self.win = True
            if(self.bet):
                self.set_asset(-20)
            else:
                self.set_asset(-40)
        elif p==d:
            self.draw = True
            print('draw')
            if(self.bet):
                self.set_asset(-10)
            else:
                self.set_asset(-20)
        else:
            print('lose')
                
    def reset(self):
        self.count += 1
        if len(self.cards) < 10:
            self.cards = cards()
        self.bet = False 
        self.win = False
        self.draw = False
        
    def reset_all_game(self):
        self.get_goal_or_not = False
        self.count = 0
        self.cards = cards()
        self.bet = False 
        self.win = False
        self.draw = False
        self.asset = 100
        
    def step(self, action):
        
        current_cards_state = []
        for card in self.cards:
            current_cards_state.append(card)
        current_cards_state.sort()
        
        if action == 0 or self.asset<20: 
            self.deal_card_ten()
        elif action == 1:   
            self.deal_card_twenty()
        
        if self.get_asset() >= 200:
            self.get_goal += 1
            self.get_goal_or_not = True
            if self.bet is not True: 
                reward = 1
            else:
                reward = 0
            done = True
            s_ = 'terminal'
        elif self.get_asset() < 10:
            if self.bet is not True: 
                reward = -1
            else:
                reward = 0
            done = True
            s_ = 'terminal'
        elif self.win == True:
            if self.bet is not True: 
                reward = 1
            else:
                reward = -1
            done = False
            s_ = current_cards_state
        elif self.draw == True:
            reward = 0
            done = False
            s_ = current_cards_state
        else:
            if self.bet is not True: 
                reward = -1
            else:
                reward = 1
            done = False
            s_ = current_cards_state
            
        self.reset()

        return s_, reward, done
    
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