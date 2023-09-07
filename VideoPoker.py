import logging
import sys
import random
import itertools
from copy import deepcopy
from collections import defaultdict
import numpy as np
import pandas as pd
import re
import tkinter as tk
import tkinter.font
from PIL import ImageTk, Image
import time
import os

#math
mu = 100
sigma = 25

#misc
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

#strings
NOTHING = "NOTHING"
LOWPAIR = "LOW PAIR"
JORB = "JACKS OR BETTER"
TWOPAIR = "TWO PAIR"
THREE = "SET"
STRAIGHT = "STRAIGHT"
FLUSH = "FLUSH"
FULLHOUSE = "FULL HOUSE"
QUADS = "QUADS"
STRAIGHTFLUSH = "STRAIGHT FLUSH"
ROYALFLUSH = "ROYAL FLUSH"

TITLE = "Jacks or Better"

SUITS = {
    0: "s",  # spades
    1: "c",  # clubs
    2: "d",  # diamonds
    3: "h"  # hearts
}

RANKS = {
    2: "2", 3: "3", 4: "4",
    5: "5", 6: "6", 7: "7",
    8: "8", 9: "9", 10: "10",
    11: "J", 12: "Q", 13: "K",
    14: "A"
}

PAYOUT = { #hand name + payout multiplier
    NOTHING: 0,
    LOWPAIR: 0,
    JORB: 1,
    TWOPAIR: 2,
    THREE: 3,
    STRAIGHT: 4,
    FLUSH: 6,
    FULLHOUSE: 9,
    QUADS: 25,
    STRAIGHTFLUSH: 50,
    ROYALFLUSH: 250
}


def get_card_pic(card_name, shrink=4):
    img = Image.open(f'./resources/cards_squared/{card_name}.png')
    imgW, imgH = img.size
    new_img = img.resize((int(imgW / shrink), int(imgH / shrink)), Image.LANCZOS)
    return ImageTk.PhotoImage(new_img)


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(TITLE)

        try:
            self.root.iconbitmap(f"./resources/poker.ico")
        except Exception as err:
            pass

        self.cardButtons = []
        #create grid
        bonus_height = 3
        bonus_width = 3
        col_width = 5

        self.cardback = get_card_pic('default2')
        self.cardback_small = get_card_pic('default2', 16)
        self.default_bg = self.root.cget('bg')

        self.main_game_frame = tk.Frame(self.root)
        self.main_game_frame.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky=tk.NSEW)
        self.main_game_frame.grid_rowconfigure(0, weight=1)
        self.bonus_game_frame = tk.Frame(self.root)
        self.bonus_game_frame.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky=tk.NSEW)
        self.bonus_game_frame.grid_rowconfigure(0, weight=1)
        for i in range(col_width):
            self.root.grid_columnconfigure(i, weight=1)
            self.main_game_frame.grid_columnconfigure(i, weight=1)
            self.cardButtons.append(tk.Button(self.main_game_frame, image=self.cardback, bd=0,
                                              bg='black', highlightthickness=2))
            self.cardButtons[i].grid(row=0, column=i, sticky=tk.NSEW, padx=5, pady=5)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        bonus_list = []
        for y in range(bonus_height):
            self.bonus_game_frame.grid_rowconfigure(y, weight=1)
            for x in range(bonus_width):
                self.bonus_game_frame.grid_columnconfigure(x, weight=1)
                frame = tk.Frame(self.bonus_game_frame, highlightbackground="black", highlightthickness=2)
                frame.grid(row=x, column=y, sticky=tk.NSEW, padx=15, pady=5)
                frame.grid_rowconfigure(0, weight=1)
                label = tk.Label(frame, text=' ', bd=0)
                label.grid(row=2, column=0, columnspan=5, sticky=tk.NSEW)
                button_list = []
                for i in range(col_width):
                    frame.grid_columnconfigure(i, weight=1)
                    button_list.append(tk.Button(frame, image=self.cardback_small, bd=0))
                    button_list[i].grid(row=0, column=i, sticky=tk.NSEW)
                bonus_list.append({'frame': frame, 'button_list': button_list, 'label': label})
        self.bonus_dataframe = pd.DataFrame(bonus_list)

        self.result_label = tk.Label(self.main_game_frame, text=' ', bd=0, font=tk.font.Font(size=15))
        self.result_label.grid(row=2, column=0, columnspan=5, sticky=tk.NSEW)

        self.wagerFrame = tk.Frame(self.root)
        self.wagerFrame.grid(row=2, column=0, columnspan=2)

        self.wagerLabel = tk.Label(self.wagerFrame, text='Bet', font=('Segoe UI', 15, 'bold'), anchor=tk.NW)
        self.wagerLabel.pack(side="left", anchor=tk.NW)

        self.wagerValue = tk.Label(self.wagerFrame, text='?', font=('Segoe UI', 15), anchor=tk.NW)
        self.wagerValue.pack(side="left", anchor=tk.NW)

        self.playButton = tk.Button(self.root, text='?', width=15, font=('Segoe UI', 15, 'bold'), borderwidth=3, padx=0, pady=0)
        self.playButton.grid(row=2, column=2, sticky=tk.E+tk.W, pady=5)

        self.creditsFrame = tk.Frame(self.root)
        self.creditsFrame.grid(row=2, column=3, columnspan=2)

        self.creditsLabel = tk.Label(self.creditsFrame, text='Credits:', font=('Segoe UI', 15, 'bold'), anchor=tk.NE)
        self.creditsLabel.pack(side="left", anchor=tk.NE)

        self.creditsValue = tk.Label(self.creditsFrame, text='?', font=('Segoe UI', 15), anchor=tk.NE)
        self.creditsValue.pack(side="left", anchor=tk.NE)

        self.winningsValue = tk.Label(self.creditsFrame, text=' ', font=('Segoe UI', 15), anchor=tk.NE)
        self.winningsValue.pack(side="left", anchor=tk.NE)

        game = Game(self)

        self.root.mainloop()


class Game:
    def __init__(self, gui):
        self.gui = gui
        self.masterDeck = set()
        self.hand = None
        self.card_images = None
        self.deck = None
        self.wager = 25
        self.credits = 5000
        for suit, rank in set(itertools.product(SUITS, RANKS)):
            self.masterDeck.add(Card(suit, rank))

        self.gui.wagerValue.config(text=f"${self.wager} x10")
        self.gui.creditsValue.config(text=f"${self.credits}")
        self.gui.playButton.config(text="Play", command=self.start_round)

    def update_credits(self, amount):
        self.credits = self.credits + amount
        self.gui.creditsValue.config(text=f"${self.credits}")

    def start_round(self):
        self.update_credits(-abs(self.wager*10))
        self.deck = list(deepcopy(self.masterDeck))
        random.shuffle(self.deck)
        self.hand = []
        for i in range(5):
            self.hand.append(self.deck.pop())
            self.hand[i].gen_pic()
            self.gui.cardButtons[i].configure(image=self.hand[i].pic, state='normal', command=lambda i=i: self.hold_card(i))
            self.gui.cardButtons[i].image = self.hand[i].pic
            self.gui.root.update()
            time.sleep(.2)
        self.gui.playButton.config(text="Continue", command=self.continue_round)

    def continue_round(self):
        round_winnings = 0
        for i in range(5):
            self.gui.cardButtons[i].configure(bg='black')
            if not self.hand[i].held:
                self.gui.cardButtons[i].configure(image=self.gui.cardback)
                self.gui.cardButtons[i].image = self.hand[i].pic
                self.gui.root.update()
        for index, row in self.gui.bonus_dataframe.iterrows():
            bonus_hand = []
            bonus_deck = list(deepcopy(self.deck))
            random.shuffle(bonus_deck)
            for i in range(5):
                if self.hand[i].held:
                    bonus_hand.append(self.hand[i])
                else:
                    bonus_hand.append(bonus_deck.pop())
                    bonus_hand[i].gen_pic()
                    row['button_list'][i].configure(image=bonus_hand[i].pic_small)
                    row['button_list'][i].image = bonus_hand[i].pic_small
                    self.gui.root.update()
                    time.sleep(.2)
            result = evaluate_hand(bonus_hand)
            winnings = self.wager * PAYOUT[result]
            if winnings >= self.wager:
                row['frame'].configure(highlightbackground='green')
            else:
                row['frame'].configure(highlightbackground='red')
            row['label'].configure(text=result)

            round_winnings += winnings
            print(f"Result: {result}\n"
                  f"Winnings: {winnings}\n")
            self.update_credits(winnings)

        for i in range(5):
            if not self.hand[i].held:
                self.hand[i] = self.deck.pop()
                self.hand[i].gen_pic()
                self.gui.cardButtons[i].configure(image=self.hand[i].pic)
                self.gui.cardButtons[i].image = self.hand[i].pic
                self.gui.root.update()
                time.sleep(.2)
        result = evaluate_hand(self.hand)
        winnings = self.wager * PAYOUT[result]

        for i in range(5):
            if winnings >= self.wager:
                self.gui.cardButtons[i].configure(bg='green')
            else:
                self.gui.cardButtons[i].configure(bg='red')

        self.gui.result_label.configure(text=result)

        round_winnings += winnings
        print(f"Result: {result}\n"
              f"Winnings: {winnings}\n")
        self.update_credits(winnings)
        print(f"round winnings: {round_winnings}")
        self.gui.winningsValue.config(text=f"(+${round_winnings})")
        self.gui.playButton.config(text="End", command=self.end_round)

    def end_round(self):
        for index, row in self.gui.bonus_dataframe.iterrows():
            for i in range(5):
                row['button_list'][i].config(image=self.gui.cardback_small)
                row['button_list'][i].image = self.gui.cardback_small
                row['frame'].configure(highlightbackground='black')
                row['label'].configure(text=' ')
        for i in range(5):
            self.gui.cardButtons[i].config(image=self.gui.cardback, bg='black')
            self.gui.cardButtons[i].image = self.gui.cardback_small

        self.gui.winningsValue.config(text=' ')
        self.gui.result_label.config(text=' ')
        self.gui.playButton.config(text="Play", command=self.start_round)
        self.gui.root.update()

    def hold_card(self, cardNum):
        self.gui.cardButtons[cardNum].configure(bg='green', command=lambda i=cardNum: self.release_card(i))
        for x in self.gui.bonus_dataframe['button_list']:
            x[cardNum].configure(image=self.hand[cardNum].pic_small)
            x[cardNum].image = self.hand[cardNum].pic_small
        self.hand[cardNum].held = True

    def release_card(self, cardNum):
        self.gui.cardButtons[cardNum].configure(bg='black', command=lambda i=cardNum: self.hold_card(i))
        for x in self.gui.bonus_dataframe['button_list']:
            x[cardNum].configure(image=self.gui.cardback_small)
            x[cardNum].image = self.gui.cardback_small
        self.hand[cardNum].held = False


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.prettySuit = SUITS[suit]
        self.rank = rank
        self.prettyRank = RANKS[rank]
        self.held = False
        self.pic = None
        self.pic_small = None

    def __str__(self):
        return f"{self.prettyRank}{self.prettySuit}"

    def __repr__(self):
        return str(self)

    def gen_pic(self):
        if self.pic is None:
            self.pic = get_card_pic(f"{self.prettyRank}{self.prettySuit}")
            self.pic_small = get_card_pic(f"{self.prettyRank}{self.prettySuit}", 16)


def evaluate_hand(hand_list):
    def checkFlush(cardList):
        flush = True
        for card in cardList[1:]:
            if card.suit != cardList[0].suit:
                flush = False
                break
        return flush

    def checkStraight(cardList):  # if cards are consecutive - ace can be high or low so check for A,2,3,4,5 as well
        cardList = [x.rank for x in cardList]
        return (len(set(cardList)) == len(cardList) and max(cardList) - min(cardList) == len(cardList) - 1) or \
               (sorted(cardList) == [2, 3, 4, 5, 14])

    def checkPairing(cardList):
        values = ([x.rank for x in cardList])
        value_counts = defaultdict(int)
        for v in values:
            value_counts[v] += 1
        result = []
        for k, v in value_counts.items():
            if v > 1:
                result.append([k, v])

        pairs = 0
        sets = 0
        quads = 0
        jackhigh = False
        for match in result:
            if match[1] == 2:
                pairs += 1
                if match[0] > 10:
                    jackhigh = True
            elif match[1] == 3:
                sets += 1
            elif match[1] == 4:
                quads += 1
        if quads == 1:
            return QUADS
        elif sets == 1 and pairs == 1:
            return FULLHOUSE
        elif pairs == 2:
            return TWOPAIR
        elif sets == 1:
            return THREE
        elif pairs == 1 and jackhigh:
            return JORB
        elif pairs == 1 and not jackhigh:
            return LOWPAIR
        else:
            return NOTHING

    straight_result = checkStraight(hand_list)
    flush_result = checkFlush(hand_list)

    if straight_result and flush_result:
        if sorted([x.rank for x in hand_list]) == [10, 11, 12, 13, 14]:
            win = ROYALFLUSH
        else:
            win = STRAIGHTFLUSH
    elif straight_result:
        win = STRAIGHT
    elif flush_result:
        win = FLUSH
    else:
        win = checkPairing(hand_list)

    return win


if __name__ == '__main__':
    gui = GUI()
