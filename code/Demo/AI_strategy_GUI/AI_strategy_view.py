# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:34:58 2019

@author: Herng-Shyue, Chen
"""

import tkinter as tk
from random import shuffle

class Blackjack(tk.Tk, object): 
    
    def __init__(self):
         
        super(Blackjack, self).__init__()

        self.back_card = tk.PhotoImage(file="card/back{}".format(get_ext())) # inspired by Daniel P.
        
        self.playerScore = 0
        self.dealerScore = 0
        
        self.bet = False # if bet 10!
        self.bust = False # if player bust
        self.win = False # if player win the game
        self.draw = False # if the game is draw
        self.double = False # bet with double
        self.surrenders = False # bet with surrender 
        
        # origin the basic factors
        self.asset = 100
        self.cards = cards()
        
        self.title('Blackjack')
        self.geometry('600x500+250+180')
        self.build_table()

    def set_asset(self, asset_): # wegar and control player's assets
        self.asset -= asset_
    
    def _play(self): # start the new game
        
        self.judgement.set("")
        
        self.play_.flash()
             
        if len(self.cards) < 11:
            self.cards = cards()
        shuffle(self.cards)
        
        #-----------------------inspired by Daniel P.-------------------------------
        self.table.forget()
        self.table.pack(side="top", fill="both", expand="true")
        self.dealer_cards.destroy()
        self.dealer_cards = tk.Frame(self.table, bg="pink")
        self.dealer_cards.grid(row=0, column=1, rowspan=2, sticky="ew", pady=40)
        self.player_cards.destroy()
        self.player_cards = tk.Frame(self.table, bg="pink")
        self.player_cards.grid(row=2, column=1, rowspan=2, sticky="ew")
        #---------------------------------------------------------------------------
        
        self.playerScore = 0
        self.dealerScore = 0
        
        self.bet = False 
        self.bust = False 
        self.win = False
        self.draw = False
        self.double = False
        self.surrenders = False
        
        self.stand_.configure(state="normal")
        if self.asset > 15:
            self.double_.configure(state="normal")
            self.surrender_.configure(state="normal")
        else:
            pass
        self.hit_.configure(state="normal")
        
        if self.asset < 10 or self.asset >= 150:
            self.hit_.configure(state = 'disabled')
            self.stand_.configure(state = 'disabled')
            self.surrender_.configure(state = 'disabled')
            self.double_.configure(state = 'disabled')
            self.play_.configure(state = 'disabled')
            self.reset_all_.configure(state = 'normal')
        
        #----------------------------inspired by Daniel P.-----------------------------------
        self.dealer_hand = []
        self.player_hand = []
        
        if self.asset > 10:
            self.set_asset(10)
            self.current_asset.set("Current asset is {}".format(self.asset))
        
        for i in range(2):
            self.deal_card("player")
            self.deal_card("dealer")

        self.show_cards("player")
        self.show_cards("dealer")

        self.playerScore = self.update_score("player")
        self.dealer_score.set("?")
        #-------------------------------------------------------------------------------------
        
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        self.play_.configure(state="disabled")
    
    def deal_card(self, user): # inspired be Daniel P.
        card = self.cards.pop(0)
        if user == "dealer":
            self.dealer_hand.append(card)
        elif user == "player":
            self.player_hand.append(card)
        return card
        
    def show_cards(self, user): # inspired be Daniel P.
        if user == "dealer":
            hand = self.dealer_hand
            frame = self.dealer_cards
            for card in hand:
                if card == hand[0]:
                    self.hide_card = tk.Label(frame, image= self.back_card)
                    self.hide_card.pack(side="left", padx=5)
                else:
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
    
    def hit(self):
        
        self.hit_.flash()
        
        self.double_.configure(state="disabled")
        self.surrender_.configure(state="disabled")
        
        #--------------------------inspired by Daniel P.-----------------------
        card = self.deal_card("player")
        frame = self.player_cards
        tk.Label(frame, image=card[1]).pack(side="left", padx=5)
        self.playerScore = self.update_score("player")
        #-----------------------------------------------------------------------
        
        if self.playerScore > 21:
            if self.asset < 10:
                self.hit_.configure(state = 'disabled')
                self.stand_.configure(state = 'disabled')
                self.surrender_.configure(state = 'disabled')
                self.double_.configure(state = 'disabled')
                self.play_.configure(state = 'disabled')
                self.reset_all_.configure(state = 'normal')
            else:
                self.judgement.set("Player busts and loses 10!!")
                self.bust = True
                self.play_.configure(state="normal")
                self.stand_.configure(state="disabled")
                self.hit_.configure(state="disabled")
        elif len(self.player_hand) > 5:  # player cannot own more than 5 cards
            self.stand()
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        
        
                  
    def stand(self): # stand the card
        
        self.stand_.flash()
        
        #--------------------------inspired by Daniel P.-----------------------
        self.hide_card.destroy()
        self.hide_card = tk.Label(self.dealer_cards, image=(self.dealer_hand[0])[1])
        self.hide_card.pack(side="left", padx=5)
        self.dealerScore = self.update_score("dealer")
        #-----------------------------------------------------------------------
        
        while self.dealerScore < 17:
            card = self.deal_card("dealer")
            frame = self.dealer_cards
            tk.Label(frame, image=card[1]).pack(side="left", padx=5)
            self.dealerScore = self.update_score("dealer")
            if len(self.dealer_hand) > 5: # dealer cannot own more than 5 cards
                break
            
        if self.dealerScore > 21:
            if self.double == True:
                self.set_asset(-40)
                self.current_asset.set("Current asset is {}".format(self.asset))
                self.judgement.set("Dealer busts and player wins 20!!")
            else:
                self.set_asset(-20)
                self.current_asset.set("Current asset is {}".format(self.asset))
                self.judgement.set("Dealer busts and player wins 10!!")
            self.win = True
            self.play_.configure(state="normal")
            self.double_.configure(state="disabled")
            self.surrender_.configure(state="disabled")
            self.hit_.configure(state="disabled")
            self.stand_.configure(state="disabled")
        else:
            self.compare()
            self.play_.configure(state="normal")
            self.double_.configure(state="disabled")
            self.surrender_.configure(state="disabled")
            self.hit_.configure(state="disabled")
            self.stand_.configure(state="disabled")
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        if self.asset < 10 or self.asset >= 150:
            self.hit_.configure(state = 'disabled')
            self.stand_.configure(state = 'disabled')
            self.surrender_.configure(state = 'disabled')
            self.double_.configure(state = 'disabled')
            self.play_.configure(state = 'disabled')
            self.reset_all_.configure(state = 'normal')
    
    def _double(self): # double action, player wagers double assets and just can hit one time
        
        self.double = True
        self.double_.flash()
        
        self.set_asset(10)
        self.current_asset.set("Current asset is {}".format(self.asset))
        
        #--------------------------inspired by Daniel P.-----------------------
        card = self.deal_card("player")
        frame = self.player_cards
        tk.Label(frame, image=card[1]).pack(side="left", padx=5)
        self.playerScore = self.update_score("player")
        #-----------------------------------------------------------------------
        
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        if self.playerScore > 21:
            self.bust = True
            self.judgement.set("Player busts and loses 20!!")
            self.hide_card.destroy()
            self.hide_card = tk.Label(self.dealer_cards, image=(self.dealer_hand[0])[1])
            self.hide_card.pack(side="left", padx=5)
            if self.asset < 10:
                self.hit_.configure(state = 'disabled')
                self.stand_.configure(state = 'disabled')
                self.surrender_.configure(state = 'disabled')
                self.double_.configure(state = 'disabled')
                self.play_.configure(state = 'disabled')
                self.reset_all_.configure(state = 'normal')
            else:
                self.play_.configure(state="normal")
                self.stand_.configure(state="disabled")
                self.surrender_.configure(state="disabled")
                self.hit_.configure(state="disabled")
                self.double_.configure(state="disabled")
        else:
            self.stand()
            
    def surrender(self): # surrender action, player calls back half of asset and starts next game directly
        
        self.surrenders = True
        self.surrender_.flash()
        
        self.set_asset(-5)
        self.current_asset.set("Current asset is {}".format(self.asset))
        self.hide_card.destroy()
        self.hide_card = tk.Label(self.dealer_cards, image=self.dealer_hand[0][1])
        self.hide_card.pack(side="left", padx=5)
        self.dealerScore = self.update_score("dealer")
        self.play_.configure(state="normal")
        self.stand_.configure(state="disabled")
        self.hit_.configure(state="disabled")
        self.double_.configure(state="disabled")
        self.surrender_.configure(state="disabled")
        self.judgement.set("Surrender!! But get half of bets!")
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        if self.asset < 5 or self.asset > 150:
            self.hit_.configure(state = 'disabled')
            self.stand_.configure(state = 'disabled')
            self.surrender_.configure(state = 'disabled')
            self.double_.configure(state = 'disabled')
            self.play_.configure(state = 'disabled')
            self.reset_all_.configure(state = 'normal')
         
    def compare(self): # compare dealer and player's scores if player no bust
        
        if self.playerScore > self.dealerScore:
            if self.double == True:
                self.set_asset(-40)
                self.current_asset.set("Current asset is {}".format(self.asset))
                self.judgement.set("Player wins 20!!")
            else:
                self.set_asset(-20)
                self.current_asset.set("Current asset is {}".format(self.asset))
                self.judgement.set("Player wins 10!!")
            self.win = True
        elif self.playerScore == self.dealerScore:
            if self.double == True:
                self.set_asset(-20)
                self.current_asset.set("Current asset is {}".format(self.asset))
                self.judgement.set("The game is draw!!")
            else:
                self.set_asset(-10)
                self.current_asset.set("Current asset is {}".format(self.asset))
                self.judgement.set("The game is draw!!")
                self.draw = True
        else:
            if self.double == True:
                self.judgement.set("Player loses 20!!")
            else:
                self.judgement.set("Player loses 10!!")
            self.win = False
        
    def reset_all_game(self): # start the new round
        
        self.judgement.set("")
        
        self.asset = 100
        self.cards = cards()
        shuffle(self.cards)
        self.reset_all_.flash()
        
        self.table.forget()
        self.table.pack(side="top", fill="both", expand="true")
        self.dealer_cards.destroy()
        self.player_cards.destroy()
        
        self.dealer_hand = []
        self.player_hand = []
        
        self.playerScore = 0
        self.dealerScore = 0
        self.player_score.set(0)
        self.dealer_score.set(0)
        
        self.bet = False 
        self.bust = False 
        self.win = False
        self.draw = False
        self.double = False
        self.surrenders = False 
        
        self.current_asset.set("Current asset is {}".format(self.asset))
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        self.play_.configure(state = 'normal')
        self.reset_all_.configure(state = 'disabled')
        
        
    def build_table(self):
        
        self.table = tk.Frame(self, bg="black") # inpired by Dainel, P.
        self.table.pack(side="top", fill="both", expand="true") # inpired by Dainel, P.
        
        #---------------------------------dealer inspired by Dainel, P.-----------------------------------------
        
        self.dealer_info = tk.Label(self.table, bg="brown", text="Dealer", fg="white")
        self.dealer_info.grid(row=0, column=0, sticky="s") #sticky=s be aligned(south)
        
        self.dealer_cards = tk.Frame(self.table, bg="pink")
        self.dealer_cards.grid(row=0, column=1, rowspan=2, pady=15, sticky="ew")
        
        self.dealer_score = tk.IntVar() # define variables
        self.dealer_score.set(0) # setter
        self.dealer_scores = tk.Label(self.table, bg="brown", textvariable=self.dealer_score, fg="white")
        # fg is the color for the words, bg is the color for the background
        self.dealer_scores.grid(row=1, column=0, sticky="n", pady=10) #sticky=n be aligned(north) 10
        
        #---------------------------------player inspired by Dainel, P.-----------------------------------------
        
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
        
        #---------------------------------judge-----------------------------------------
        
        self.judgement = tk.IntVar()
        self.judgement.set("")
        self.judgement_ = tk.Label(self.table, bg="yellow", textvariable=self.judgement, fg="blue",
                                  font=("impact",16))
        self.judgement_.grid(row=4, column=1, sticky="n", pady=10)
        
        #---------------------------------current card----------------------------------
        self.shoes = tk.IntVar()
        self.shoes.set("Curren cards in the shoes: {}".format(len(self.cards)))
        self.shoes_ = tk.Label(self.table, bg="yellow", textvariable=self.shoes, fg="blue",
                                  font=("impact",16))
        self.shoes_.grid(row=5, column=1, sticky="n", pady=10)
                
        #---------------------------------button----------------------------------------
        
        self.button_frame = tk.Frame(self, bg="grey")
        self.button_frame.pack(side="bottom", fill="x")
        
        self.hit_ = tk.Button(self.button_frame, bg='blue', fg='white', text="hit",
                                         state='disabled', command=self.hit)
        self.hit_.pack(side="left", padx="10")
        
        self.stand_ = tk.Button(self.button_frame, bg='blue', fg='white', text="stand", 
                                            state='disabled', command=self.stand)
        self.stand_.pack(side="left", padx="10")
        
        self.surrender_ = tk.Button(self.button_frame, bg='blue', fg='white', text="surrender",
                                            state='disabled', command=self.surrender)
        self.surrender_.pack(side="left", padx="10")
        
        self.double_ = tk.Button(self.button_frame, text="double", bg='blue', fg='white', state='disabled', 
                                            command=self._double)
        self.double_.pack(side="left", padx="10")
        
        self.play_ = tk.Button(self.button_frame, text="play", bg='blue', fg='white',
                                            command=self._play)
        self.play_.pack(side="left", padx="10")
        
        self.reset_all_ = tk.Button(self.button_frame, text="New", bg='blue', fg='white', state='disabled',
                                            command=self.reset_all_game)
        self.reset_all_.pack(side="left", padx="10")
        
        self.current_asset = tk.StringVar()
        self.current_asset.set("Current asset is {}".format(self.asset))
        self.asset_info = tk.Label(self.button_frame, bg="yellow", 
                                   textvariable=self.current_asset,
                                   fg="black", font=("impact",16))
        self.asset_info.pack(side="right", padx="10")       
        
def get_ext():  # inpired by Dainel, P.
    
    extension = ".png"
    return extension    

def cards():  # inpired by Dainel, P.
    
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