# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:00:25 2019

@author: chenmth
"""

import tkinter as tk
from random import shuffle
import time

class Blackjack(tk.Tk, object): 
    
    def __init__(self):
         
        super(Blackjack, self).__init__() 
        self.action_space = ['bet 10', 'bet 20']
        self.bet = False #if bet 20!
        self.burst = False #if player burst
        self.win = False
        self.draw = False
        self.n_actions = len(self.action_space)
        self.asset = 100
        self.cards = cards()
        self.title('Blackjack')
        self.geometry('600x500+250+180')
        self.build_table()

    def set_asset(self, asset_):
        self.asset -= asset_
        
    def get_asset(self):
        return self.asset
        
    def get_burst(self):
        return self.burst
    
    def deal_card(self, user):
        card = self.cards.pop(0)
        if user == "dealer":
            self.dealer_hand.append(card)
        elif user == "player":
            self.player_hand.append(card)
        #update_score(user)
        return card
        
    def show_cards(self, user):
        if user == "dealer":
            hand = self.dealer_hand
            frame = self.dealer_cards
            for card in hand:
                tk.Label(frame, image=card[1]).pack(side="left", padx=5) #because 1 is image, 0 is value
        elif user == "player":
            hand = self.player_hand
            frame = self.player_cards
            for card in hand:
                tk.Label(frame, image=card[1]).pack(side="left", padx=5)
    
    def update_score(self, user):
        score = 0
        has_ace = False
        if user == "dealer":
            hand = self.dealer_hand
            score_label = self.dealer_score
        elif user == "player":
            hand = self.player_hand
            score_label = self.player_score
        for card in hand:
            value = card[0]
            if value == 1:
                value = 11
                has_ace = True
            elif value > 10:
                value = 10
            score += value
            if score > 21 and has_ace:
                score -= 10
                has_ace = False
        score_label.set(score)
        return score
    
    def deal_card_ten(self):
        self.dealer_hand = []
        self.player_hand = []
        dealer_card=[]
        player_card=[]
        print('bet 10')
        self.bet_ten_.flash()
        self.bet = True #now i bet the ten
        #self.bet_twenty_.configure(state='disabled')
        self.set_asset(10)
        #time.sleep(3)
        self.current_asset.set("Current asset is {}".format(self.get_asset()))
        shuffle(self.cards)
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")

        self.show_cards("player")
        self.show_cards("dealer")

        self.update_score("player")
        self.update_score("dealer")
        
        while self.update_score("player") < 17:
            self.hit("player")
            
        while self.update_score("dealer") < 17 and self.burst == False:
            self.hit("dealer")
            
        for i in self.dealer_hand:
            dealer_card.append(i[0])
        for j in self.player_hand:
            player_card.append(j[0])
            
        for i in range(len(dealer_card)):
            if(dealer_card[i]==1):
                dealer_card[i] = 'Ace'
            elif(dealer_card[i]==11):
                dealer_card[i] = 'Jack'
            elif(dealer_card[i]==12):
                dealer_card[i] = 'Queen'
            elif(dealer_card[i]==13):
                dealer_card[i] = 'King'
        for i in range(len(player_card)):
            if(player_card[i]==1):
                player_card[i] = 'Ace'
            elif(player_card[i]==11):
                player_card[i] = 'Jack'
            elif(player_card[i]==12):
                player_card[i] = 'Queen'
            elif(player_card[i]==13):
                player_card[i] = 'King'
            
        print(dealer_card)
        print(player_card)
        
        self.compare()
        
        #self.bet_ten_.configure(state='disabled')
        
    def deal_card_twenty(self):
        self.dealer_hand = []
        self.player_hand = []
        dealer_card=[]
        player_card=[]
        print("bet 20")
        self.bet_twenty_.flash()
        #self.bet_ten_.configure(state='disabled')
        self.set_asset(20)
        self.current_asset.set("Current asset is {}".format(self.get_asset()))
        #time.sleep(3)
        shuffle(self.cards)
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")
            
        self.show_cards("player")
        self.show_cards("dealer")
        
        while self.update_score("player") < 17:
            self.hit("player")
            
        while self.update_score("dealer") < 17 and self.burst == False:
            self.hit("dealer")
            
        for i in self.dealer_hand:
            dealer_card.append(i[0])
        for j in self.player_hand:
            player_card.append(j[0])
            
        for i in range(len(dealer_card)):
            if(dealer_card[i]==1):
                dealer_card[i] = 'Ace'
            elif(dealer_card[i]==11):
                dealer_card[i] = 'Jack'
            elif(dealer_card[i]==12):
                dealer_card[i] = 'Queen'
            elif(dealer_card[i]==13):
                dealer_card[i] = 'King'
        for i in range(len(player_card)):
            if(player_card[i]==1):
                player_card[i] = 'Ace'
            elif(player_card[i]==11):
                player_card[i] = 'Jack'
            elif(player_card[i]==12):
                player_card[i] = 'Queen'
            elif(player_card[i]==13):
                player_card[i] = 'King'
        
        print(dealer_card)
        print(player_card)
        
        self.compare()
        
        
        #self.bet_twenty_.configure(state='disabled')
    
    def hit(self, user):
        if user == "player":
            card = self.deal_card("player")
            frame = self.player_cards
            tk.Label(frame, image=card[1]).pack(side="left", padx=5)
            score = self.update_score("player")
            if score>21:
                self.burst = True
                print("Burst with {}!!".format(score))                 
                
        elif user == "dealer":
            card = self.deal_card("dealer")
            frame = self.dealer_cards
            tk.Label(frame, image=card[1]).pack(side="left", padx=5)
            score = self.update_score("dealer")
            if score>21:
                self.win = True
                if(self.bet):
                    self.set_asset(-20)
                    self.current_asset.set("Current asset is {}".format(self.get_asset()))
                else:
                    self.set_asset(-40)
                    self.current_asset.set("Current asset is {}".format(self.get_asset()))
     
    def compare(self):
        p = self.update_score("player")
        d = self.update_score("dealer")
        if p>d and p<22:
            self.win = True
            if(self.bet):
                self.set_asset(-20)
                self.current_asset.set("Current asset is {}".format(self.get_asset()))
            else:
                self.set_asset(-40)
                self.current_asset.set("Current asset is {}".format(self.get_asset()))
        elif p==d:
            self.draw = True
            if(self.bet):
                self.set_asset(-10)
                self.current_asset.set("Current asset is {}".format(self.get_asset()))
            else:
                self.set_asset(-20)
                self.current_asset.set("Current asset is {}".format(self.get_asset()))
                
    def render(self):
        #time.sleep(1200)
        self.reset_button_.invoke()
        self.reset_button_.configure(state="disabled")
        self.reset_button_.configure(state="disabled")
                
    def reset(self):
        #time.sleep(2)
        if len(self.cards) < 10:
            self.cards = cards()
        self.reset_button_.flash()
        self.bet = False #if bet 20!
        self.burst = False #if player burst
        self.win = False
        self.draw = False
        self.bet_ten_.configure(state='normal')
        self.bet_twenty_.configure(state='normal')
        self.dealer_score.set(0)
        self.player_score.set(0)
#        self.table.forget()
#        self.table.pack(side="top", fill="both", expand="true")
        self.dealer_cards.destroy()
        self.dealer_cards = tk.Frame(self.table, bg="pink")
        self.dealer_cards.grid(row=0, column=1, rowspan=2, pady=15, sticky="ew")
        self.player_cards.destroy()
        self.player_cards = tk.Frame(self.table, bg="pink")
        self.player_cards.grid(row=2, column=1, rowspan=2, pady=15, sticky="ew")
#        if self.get_asset() < 20:
#            self.bet_twenty_.configure(state = 'disabled')
#        if self.get_asset() < 10:
#            self.bet_ten_.configure(state = 'disabled')
#        if self.get_asset() >= 200:
#            self.bet_twenty_.configure(state = 'disabled')
#            self.bet_ten_.configure(state = 'disabled')
#        self.current_cards_state = []
#        for card in self.cards:
#            self.current_cards_state.append(card[0])
#        self.current_cards_state.sort()
#        return self.current_cards_state, self.asset
        
    def reset_all_game(self):
        self.cards = cards()
        self.reset_all_.flash()
#        self.reset()
        self.bet = False #if bet 20!
        self.burst = False #if player burst
        self.win = False
        self.draw = False
        self.bet_twenty_.configure(state = 'normal')
        self.bet_ten_.configure(state = 'normal')
        #time.sleep(1000)
        self.asset = 100
        self.current_asset.set("Current asset is {}".format(self.get_asset()))
        
    def step(self, action):
        
        if action == 0 or self.asset<20:   # bet 10
            self.deal_card_ten()
            #self.bet_ten_.invoke()
        elif action == 1:   # bet 20
            self.deal_card_twenty()
            #self.bet_twenty_.invoke() 
        print("Current asset is {}".format(self.asset))
        #print("Have cards {}".format(len(self.cards)))
        
        current_cards_state = []
        for card in self.cards:
            current_cards_state.append(card[0])
        current_cards_state.sort()
        
        if self.get_asset() >= 110:
            reward = 5
            done = True
            s_ = 'terminal'
        elif self.get_asset() < 10:
            reward = -5
            done = True
            s_ = 'terminal'
        elif self.win == True:
            reward = 3
            done = False
            s_ = current_cards_state, self.asset
        elif self.draw == True:
            reward = 0
            done = False
            s_ = current_cards_state, self.asset
        else:
            reward = -3
            done = False
            s_ = current_cards_state, self.asset
            
        self.reset()
        
#        if self.get_asset() >= 110:
#            reward = 1
#            done = True
#            s_ = 'terminal'
#        elif self.get_asset() < 10:
#            reward = -1
#            done = True
#            s_ = 'terminal'
#        else:
#            reward = 0
#            done = False

        return s_, reward, done
        
    def build_table(self):
        
        self.table = tk.Frame(self, bg="black")
        self.table.pack(side="top", fill="both", expand="true")
        
        #---------------------------------dealer-----------------------------------------
        
        self.dealer_info = tk.Label(self.table, bg="brown", text="Dealer", fg="white")
        self.dealer_info.grid(row=0, column=0, sticky="s") #sticky=s 向下對齊(south)
        
        self.dealer_cards = tk.Frame(self.table, bg="pink")
        self.dealer_cards.grid(row=0, column=1, rowspan=2, pady=15, sticky="ew")
        
        self.dealer_score = tk.IntVar() #定義變數
        self.dealer_score.set(0) #setter
        self.dealer_scores = tk.Label(self.table, bg="brown", textvariable=self.dealer_score, fg="white")
        #fg是字的顏色, bg是背景色
        self.dealer_scores.grid(row=1, column=0, sticky="n", pady=10) #sticky=n 向上對齊(north) 然後間隔"10"
        
        #---------------------------------player-----------------------------------------
        
        self.player_info = tk.Label(self.table, bg="brown", text="Player", fg="white")
        self.player_info.grid(row=2, column=0, sticky="s")
        
        self.player_cards = tk.Frame(self.table, bg="pink")
        self.player_cards.grid(row=2, column=1, rowspan=2, pady=15, sticky="ew")
        
        self.player_score = tk.IntVar()
        self.player_score.set(0)
        self.player_score_label = tk.Label(self.table, bg="brown", textvariable=self.player_score, fg="white")
        self.player_score_label.grid(row=3, column=0, sticky="n", pady=10)
                
        #---------------------------------button-----------------------------------------
        
        self.button_frame = tk.Frame(self, bg="grey")
        self.button_frame.pack(side="bottom", fill="x")
        
        self.bet_ten_ = tk.Button(self.button_frame, bg='blue', fg='white', text="Bet 10!",
                                         command=self.deal_card_ten)
        self.bet_ten_.pack(side="left", padx="10")
        
        self.bet_twenty_ = tk.Button(self.button_frame, bg='blue', fg='white', text="Bet 20!", 
                                            command=self.deal_card_twenty)
        self.bet_twenty_.pack(side="left", padx="10")
        
        self.reset_button_ = tk.Button(self.button_frame, bg='blue', fg='white', text="Continue", 
                                            command=self.reset)
        self.reset_button_.pack(side="left", padx="10")
        
        self.reset_all_ = tk.Button(self.button_frame, text="New", bg='blue', fg='white', 
                                            command=self.reset_all_game)
        self.reset_all_.pack(side="left", padx="10")
        
        self.current_asset = tk.StringVar()
        self.current_asset.set("Current asset is {}".format(self.get_asset()))
        self.asset_info = tk.Label(self.button_frame, bg="yellow", 
                                   textvariable=self.current_asset,
                                   fg="black", font=("impact",16))
        self.asset_info.pack(side="right", padx="10")
        
def get_ext():
    
    extension = ".png"
    return extension    

def cards():
    
    numbers = ["ace_", "2_", "3_", "4_", "5_", "6_", "7_", "8_", "9_", "10_", "jack_", "queen_", "king_"]
    patterns = ["spade", "club", "diamond", "heart"]
    extension = get_ext()
    
    cards = [0]*52
    p = n = 0
    value = 1
    
    for card in cards:
        number = numbers[n]
        pattern = patterns[p]
        name = "card/{}{}{}".format(number, pattern, extension)
        image = tk.PhotoImage(file=name)
        cards[cards.index(card)] = (value, image) #each card will give two informations, value and image
        if n < 12:
            n += 1
            value += 1
        else:
            n = 0
            value = 1
            p += 1    
        
    return cards       
        
if __name__ == '__main__':
    env = Blackjack()
    env.mainloop()