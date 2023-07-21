import logging
import sys
import random
import itertools
from copy import deepcopy
from collections import defaultdict
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

def get_card_pic(cardName):
    img = Image.open(f'./resources/cards/{cardName}.png')
    imgW, imgH = img.size
    new_img = img.resize((int(imgW / 4), int(imgH / 4)), Image.LANCZOS)
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
        col_width = 5

        self.cardBack = get_card_pic('default2')

        for i in range(col_width):
            self.root.grid_columnconfigure(i, weight=1)
            self.cardButtons.append(tk.Button(self.root, image=self.cardBack, bd=0))
            self.cardButtons[i].grid(row=1, column=i, sticky=tk.NSEW, padx=5, pady=5)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)

        self.wagerFrame = tk.Frame(self.root)
        self.wagerFrame.grid(row=2, column=0, columnspan=2)

        self.wagerLabel = tk.Label(self.wagerFrame, text='Bet', font=('Segoe UI', 15, 'bold'), anchor=tk.NW)
        self.wagerLabel.pack(side="left", anchor=tk.NW)

        self.wagerValue = tk.Label(self.wagerFrame, text='?', font=('Segoe UI', 15), anchor=tk.NW)
        self.wagerValue.pack(side="left", anchor=tk.NW)

        self.playButton = tk.Button(self.root, text='?', font=('Segoe UI', 15, 'bold'), borderwidth=3, padx=0, pady=0)
        self.playButton.grid(row=2, column=2, sticky=tk.E+tk.W, pady=5)

        self.creditsFrame = tk.Frame(self.root)
        self.creditsFrame.grid(row=2, column=3, columnspan=2)

        self.creditsLabel = tk.Label(self.creditsFrame, text='Credits:', font=('Segoe UI', 15, 'bold'), anchor=tk.NE)
        self.creditsLabel.pack(side="left", anchor=tk.NE)

        self.creditsValue = tk.Label(self.creditsFrame, text='?', font=('Segoe UI', 15), anchor=tk.NE)
        self.creditsValue.pack(side="left", anchor=tk.NE)

        game = Game(self)

        self.root.mainloop()


class Game:
    def __init__(self, gui):
        self.gui = gui
        self.masterDeck = set()
        self.hand = None
        self.card_images = None
        self.deck = None
        self.wager = 100
        self.credits = 2000
        for suit, rank in set(itertools.product(SUITS, RANKS)):
            self.masterDeck.add(Card(suit, rank))

        self.gui.wagerValue.config(text=f"${self.wager}")
        self.gui.creditsValue.config(text=f"${self.credits}")
        self.gui.playButton.config(text="Play", command=self.start_round)

    def update_credits(self, amount):
        self.credits = self.credits + amount
        self.gui.creditsValue.config(text=f"${self.credits}")

    def start_round(self):
        self.update_credits(-abs(self.wager))
        self.deck = list(deepcopy(self.masterDeck))
        random.shuffle(self.deck)
        self.hand = []
        for i in range(5):
            self.hand.append(self.deck.pop())
            self.hand[i].gen_pic()
            self.gui.cardButtons[i].configure(image=self.hand[i].pic, state='normal', command=lambda i=i: self.muck_card(i))
            self.gui.cardButtons[i].image = self.hand[i].pic
            self.gui.root.update()
            time.sleep(.2)
        self.gui.playButton.config(text="Continue", command=self.continue_round)

    def continue_round(self):
        for i in range(5):
            if self.hand[i].mucked:
                self.hand[i] = self.deck.pop()
                self.hand[i].gen_pic()
                self.gui.root.update()
                time.sleep(.2)
            self.unmuck_card(i)
            self.gui.cardButtons[i].config(command=0)
        result = self.evaluate_hand()
        winnings = self.wager * PAYOUT[result]
        print(f"Result: {result}\n"
              f"Winnings: {winnings}\n")
        self.update_credits(winnings)
        self.gui.playButton.config(text="End", command=self.end_round)

    def end_round(self):
        for i in range(5):
            self.gui.cardButtons[i].config(image=self.gui.cardBack)
        self.gui.playButton.config(text="Play", command=self.start_round)

    def muck_card(self, cardNum):
        self.gui.cardButtons[cardNum].configure(image=self.gui.cardBack, command=lambda i=cardNum: self.unmuck_card(i))
        self.gui.cardButtons[cardNum].image = self.gui.cardBack
        self.hand[cardNum].mucked = True

    def unmuck_card(self, cardNum):
        self.gui.cardButtons[cardNum].configure(image=self.hand[cardNum].pic, command=lambda i=cardNum: self.muck_card(i))
        self.gui.cardButtons[cardNum].image = self.hand[cardNum].pic
        self.hand[cardNum].mucked = False

    def evaluate_hand(self):
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

        straight_result = checkStraight(self.hand)
        flush_result = checkFlush(self.hand)

        if straight_result and flush_result:
            if sorted([x.rank for x in self.hand]) == [10, 11, 12, 13, 14]:
                win = ROYALFLUSH
            else:
                win = STRAIGHTFLUSH
        elif straight_result:
            win = STRAIGHT
        elif flush_result:
            win = FLUSH
        else:
            win = checkPairing(self.hand)

        return win


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.prettySuit = SUITS[suit]
        self.rank = rank
        self.prettyRank = RANKS[rank]
        self.mucked = False
        self.pic = None

    def __str__(self):
        return f"{self.prettyRank}{self.prettySuit}"

    def __repr__(self):
        return str(self)

    def gen_pic(self):
        if self.pic is None:
            self.pic = get_card_pic(f"{self.prettyRank}{self.prettySuit}")


if __name__ == '__main__':
    gui = GUI()
