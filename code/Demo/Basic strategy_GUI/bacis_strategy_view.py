# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:00:25 2019

@author: Herng-Shyue Chen
"""

import tkinter as tk
from random import shuffle

class Blackjack(tk.Tk, object): 
    
    def __init__(self):
         
        super(Blackjack, self).__init__()

        self.bet = False # if bet 20!
        self.bust = False # if player bust
        self.win = False # if player win the game
        self.draw = False # if the game is draw

        # origin the basic factors
        self.asset = 100
        self.cards = cards()
        
        self.title('Blackjack')
        self.geometry('500x450+250+180')
        self.build_table()

    def set_asset(self, asset_): # wegar and control player's assets
        self.asset -= asset_
    
    def deal_card(self, user): # deal cards to player and dealer, inspired be Danie P.
        card = self.cards.pop(0)
        if user == "dealer":
            self.dealer_hand.append(card)
        elif user == "player":
            self.player_hand.append(card)
        return card
        
    def show_cards(self, user): #inspired be Daniel P.
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
    
    def update_score(self, user): # inspired be Daniel P.
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
        
        self.dealer_hand = [] # clear dealer and player's hands
        self.player_hand = []
        
        self.bet_ten_.flash() # when button is clicked, it will flash
        
        self.bet = True # bet ten
        self.bet_twenty_.configure(state='disabled')
        self.set_asset(10) # wager 10 to play game
        self.current_asset.set("Current assets are {}".format(self.asset))
        
        shuffle(self.cards)  # before dealing, the cards have to be shuffled
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")

        self.show_cards("player")
        self.show_cards("dealer")

        self.update_score("player")
        self.update_score("dealer")
        
        while self.update_score("player") < 17: # dealer strategy
            self.hit("player")
            
        while self.update_score("dealer") < 17 and self.bust == False: # dealer strategy
            self.hit("dealer")
        
        if self.bust is True :
            pass
        elif self.win is True:
            pass
        else:
            self.compare()
        
        #---------------------set button state---------------------------
        self.reset_button_.configure(state='normal')
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        self.bet_ten_.configure(state='disabled')
        
    def deal_card_twenty(self):
        
        self.dealer_hand = []
        self.player_hand = []
        
        self.bet_twenty_.flash()
        
        self.bet_ten_.configure(state='disabled')
        self.set_asset(20) # wager 20 to play game
        self.current_asset.set("Current assets are {}".format(self.asset))
        
        shuffle(self.cards) # before dealing, the cards have to be shuffled
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")
            
        self.show_cards("player")
        self.show_cards("dealer")
        
        while self.update_score("player") < 17: # dealer strategy
            if len(self.player_hand) < 5: # player cannot own more than 5 cards
                self.hit("player")
            else:
                break
            
        while self.update_score("dealer") < 17 and self.bust == False: # dealer strategy
            if len(self.player_hand) < 5: # dealer cannot own more than 5 cards
                self.hit("dealer")
            else:
                break
        
        if self.bust is True :
            pass
        elif self.win is True:
            pass
        else:
            self.compare()
        
        #---------------------set button state---------------------------
        self.reset_button_.configure(state='normal')
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        self.bet_twenty_.configure(state='disabled')
    
    def hit(self, user): # inspired be Daniel P.
        if user == "player":
            card = self.deal_card("player")
            frame = self.player_cards
            tk.Label(frame, image=card[1]).pack(side="left", padx=5)
            score = self.update_score("player")
            if score>21:
                if self.bet:
                    self.judgement.set("Player busts and loses 10!!")
                else:
                    self.judgement.set("Player busts and loses 20!!")
                self.bust = True           
                
        elif user == "dealer":
            card = self.deal_card("dealer")
            frame = self.dealer_cards
            tk.Label(frame, image=card[1]).pack(side="left", padx=5)
            score = self.update_score("dealer")
            if score>21:
                self.win = True
                if self.bet:
                    self.judgement.set("Dealer busts and player wins 10!!")
                else:
                    self.judgement.set("Dealer busts and player wins 20!!")
                if(self.bet):
                    self.set_asset(-20)
                    self.current_asset.set("Current assets are {}".format(self.asset))
                else:
                    self.set_asset(-40)
                    self.current_asset.set("Current assets are {}".format(self.asset))
     
    def compare(self):
        p = self.update_score("player")
        d = self.update_score("dealer")
        if p>d and p<22:
            if self.bet:
                self.judgement.set("Player wins 10!!")
            else:
                self.judgement.set("Player wins 20!!")
            self.win = True
            if(self.bet):
                self.set_asset(-20)
                self.current_asset.set("Current assets are {}".format(self.asset))
            else:
                self.set_asset(-40)
                self.current_asset.set("Current assets are {}".format(self.asset))
        elif p==d:
            self.draw = True
            self.judgement.set("The game is draw!!")
            if(self.bet):
                self.set_asset(-10)
                self.current_asset.set("Current assets are {}".format(self.asset))
            else:
                self.set_asset(-20)
                self.current_asset.set("Current assets are {}".format(self.asset))
        else:
            if self.bet:
                self.judgement.set("Player loses 10!!")
            else:
                self.judgement.set("Player loses 20!!")
                
    def reset(self): # start new game
        
        self.judgement.set("")
        
        if len(self.cards) < 11: # if current cards in the deck less than 11, the deck has to be renew to 52 cards
            self.cards = cards()
            
        self.reset_button_.flash()
        
        self.bet = False 
        self.bust = False 
        self.win = False
        self.draw = False
        
        #-----------------------inspired by Daniel P.-------------------------------
        self.bet_ten_.configure(state='normal')
        self.bet_twenty_.configure(state='normal')
        self.dealer_score.set(0)
        self.player_score.set(0)
        self.dealer_cards.destroy()
        self.dealer_cards = tk.Frame(self.table, bg="pink")
        self.dealer_cards.grid(row=0, column=1, rowspan=2, pady=15, sticky="ew")
        self.player_cards.destroy()
        self.player_cards = tk.Frame(self.table, bg="pink")
        self.player_cards.grid(row=2, column=1, rowspan=2, pady=15, sticky="ew")
        #----------------------------------------------------------------------------
        
        if self.asset < 20:
            self.bet_twenty_.configure(state = 'disabled')
        if self.asset < 10:
            self.bet_ten_.configure(state = 'disabled')
            self.reset_button_.configure(state = 'disabled')
            self.reset_all_.configure(state = 'normal')
        if self.asset >= 200:
            self.bet_twenty_.configure(state = 'disabled')
            self.bet_ten_.configure(state = 'disabled')
            self.reset_button_.configure(state = 'disabled')
            self.reset_all_.configure(state = 'normal')
        self.current_cards_state = []
        
        for card in self.cards:
            self.current_cards_state.append(card[0])
        self.current_cards_state.sort()
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        self.reset_button_.configure(state='disabled')
        
    def reset_all_game(self): # start new round
        
        self.judgement.set("")
        self.cards = cards()
        
        self.reset_all_.flash()
        
        self.bet = False 
        self.bust = False 
        self.win = False
        self.draw = False
        
        self.bet_twenty_.configure(state = 'normal')
        self.bet_ten_.configure(state = 'normal')
        self.asset = 100
        self.current_asset.set("Current assets are {}".format(self.asset))
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        self.reset_all_.configure(state = 'disabled')
        
    def build_table(self):
        
        self.table = tk.Frame(self, bg="black") # inpired by Dainel, P.
        self.table.pack(side="top", fill="both", expand="true") # inpired by Dainel, P.
        
        #---------------------------------dealer inpired by Dainel, P.-----------------------------------------
        
        self.dealer_info = tk.Label(self.table, bg="brown", text="Dealer", fg="white")
        self.dealer_info.grid(row=0, column=0, sticky="s") #sticky=s be aligned(south)
        
        self.dealer_cards = tk.Frame(self.table, bg="pink")
        self.dealer_cards.grid(row=0, column=1, rowspan=2, pady=15, sticky="ew")
        
        self.dealer_score = tk.IntVar() #define variable
        self.dealer_score.set(0) #setter
        self.dealer_scores = tk.Label(self.table, bg="brown", textvariable=self.dealer_score, fg="white")
        #fg is the color for the words, bg is the color for the background
        self.dealer_scores.grid(row=1, column=0, sticky="n", pady=10) #sticky=n (north) interval is 10
        
        #---------------------------------player inpired by Dainel, P.-----------------------------------------
        
        self.player_info = tk.Label(self.table, bg="brown", text="Player", fg="white")
        self.player_info.grid(row=2, column=0, sticky="s")
        
        self.player_cards = tk.Frame(self.table, bg="pink")
        self.player_cards.grid(row=2, column=1, rowspan=2, pady=15, sticky="ew")
        
        self.player_score = tk.IntVar()
        self.player_score.set(0)
        self.player_score_label = tk.Label(self.table, bg="brown", textvariable=self.player_score, fg="white")
        self.player_score_label.grid(row=3, column=0, sticky="n", pady=10)
        
        self.player_info = tk.Label(self.table, bg="brown", text="Player", fg="white")
        self.player_info.grid(row=2, column=0, sticky="s")
        
        self.player_cards = tk.Frame(self.table, bg="pink")
        self.player_cards.grid(row=2, column=1, rowspan=2, pady=15, sticky="ew")
        
        self.player_score = tk.IntVar()
        self.player_score.set(0)
        self.player_score_label = tk.Label(self.table, bg="brown", textvariable=self.player_score, fg="white")
        self.player_score_label.grid(row=3, column=0, sticky="n", pady=10)
        
        #---------------------------------judge--------------------------------------------------------
        self.judgement = tk.IntVar()
        self.judgement.set("")
        self.judgement_ = tk.Label(self.table, bg="yellow", textvariable=self.judgement, fg="blue",
                                  font=("impact",16))
        self.judgement_.grid(row=4, column=1, sticky="n", pady=10)
        
        #---------------------------------current card------------------------------------------------
        self.shoes = tk.IntVar()
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        self.shoes_ = tk.Label(self.table, bg="yellow", textvariable=self.shoes, fg="blue",
                                  font=("impact",16))
        self.shoes_.grid(row=5, column=1, sticky="n", pady=10)
                
        #---------------------------------button------------------------------------------------------
        
        self.button_frame = tk.Frame(self, bg="grey")
        self.button_frame.pack(side="bottom", fill="x")
        
        self.bet_ten_ = tk.Button(self.button_frame, bg='blue', fg='white', text="Bet 10!",
                                         command=self.deal_card_ten)
        self.bet_ten_.pack(side="left", padx="10")
        
        self.bet_twenty_ = tk.Button(self.button_frame, bg='blue', fg='white', text="Bet 20!", 
                                            command=self.deal_card_twenty)
        self.bet_twenty_.pack(side="left", padx="10")
        
        self.reset_button_ = tk.Button(self.button_frame, bg='blue', fg='white', text="Continue", 
                                            state='disabled', command=self.reset)
        self.reset_button_.pack(side="left", padx="10")
        
        self.reset_all_ = tk.Button(self.button_frame, text="New", bg='blue', fg='white', 
                                             state='disabled',command=self.reset_all_game)
        self.reset_all_.pack(side="left", padx="10")
        
        self.current_asset = tk.StringVar()
        self.current_asset.set("Current assets are {}".format(self.asset))
        self.asset_info = tk.Label(self.button_frame, bg="yellow", 
                                   textvariable=self.current_asset,
                                   fg="black", font=("impact",16))
        self.asset_info.pack(side="right", padx="10")
        
def get_ext(): # inpired by Dainel, P.
    
    extension = ".png"
    return extension    

def cards(): # inpired by Dainel, P.
    
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
        
if __name__ == '__main__':  # inpired by Dainel, P.
    env = Blackjack()
    env.mainloop()