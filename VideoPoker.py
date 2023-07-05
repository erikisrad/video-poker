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


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(TITLE)

        self.cardButtons = []
        #create grid
        col_width = 5

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        img = Image.open('./resources/cards/default2.png')
        imgW, imgH = img.size
        new_img = img.resize((int(imgW/4), int(imgH/4)), Image.LANCZOS)
        quality_val = 90
        tkImg = ImageTk.PhotoImage(new_img)

        for i in range(col_width):
            self.root.grid_columnconfigure(i, weight=1)
            self.cardButtons.append(tk.Button(self.root, image=tkImg, bd=0))
            self.cardButtons[i].grid(row=1, column=i, sticky=tk.NSEW, padx=5, pady=5)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)

        self.wagerFrame = tk.Frame(self.root)
        self.wagerFrame.grid(row=2, column=0, columnspan=2)

        self.wagerLabel = tk.Label(self.wagerFrame, text='Bet', font=('Segoe UI', 15, 'bold'), anchor=tk.NW)
        self.wagerLabel.pack(side="left", anchor=tk.NW)

        self.wagerValue = tk.Label(self.wagerFrame, text='$100', font=('Segoe UI', 15), anchor=tk.NW)
        self.wagerValue.pack(side="left", anchor=tk.NW)

        self.playButton = tk.Button(self.root, text='Play', font=('Segoe UI', 15, 'bold'), borderwidth=3, padx=0, pady=0)
        self.playButton.grid(row=2, column=2, sticky=tk.E+tk.W, pady=5)

        self.creditsFrame = tk.Frame(self.root)
        self.creditsFrame.grid(row=2, column=3, columnspan=2)

        self.creditsLabel = tk.Label(self.creditsFrame, text='Credits:', font=('Segoe UI', 15, 'bold'), anchor=tk.NE)
        self.creditsLabel.pack(side="left", anchor=tk.NE)

        self.creditsValue = tk.Label(self.creditsFrame, text='$2000', font=('Segoe UI', 15), anchor=tk.NE)
        self.creditsValue.pack(side="left", anchor=tk.NE)

        #self.root.mainloop()

        game = Game()


class Game:
    def __init__(self):
        self.masterDeck = set()
        for suit, rank in set(itertools.product(SUITS, RANKS)):
            self.masterDeck.add(Card(suit, rank))

    def start_round(self):



class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.prettySuit = SUITS[suit]
        self.rank = rank
        self.prettyRank = RANKS[rank]

    def __str__(self):
        return f"{self.prettyRank}{self.prettySuit}"

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    gui = GUI()
