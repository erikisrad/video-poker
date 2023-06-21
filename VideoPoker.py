import logging
import sys
import random
import itertools
from copy import deepcopy
from collections import defaultdict
import re
import tkinter as tk
from PIL import ImageTk, Image

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

        #create grid
        col_width = 5
        row_width = 3
        for i in range(col_width):
            self.root.grid_columnconfigure(i, weight=0)
        for i in range(row_width):
            self.root.grid_rowconfigure(i, weight=0)

        self.cardFrame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1, padx=5, pady=5)


if __name__ == '__main__':
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()  # Width of the screen
    screen_height = window.winfo_screenheight()  # Height of the screen
    window.geometry("+5+5")
    window.title("poker")
    window.mainloop()

    input("Press any key to end")
