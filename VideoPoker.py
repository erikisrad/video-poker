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
nothing = "NOTHING"
lowPair = "LOW PAIR"
jb = "JACKS OR BETTER"
twoPair = "TWO PAIR"
three = "SET"
straight = "STRAIGHT"
flush = "FLUSH"
fullHouse = "FULL HOUSE"
quads = "QUADS"
straightFlush = "STRAIGHT FLUSH"
royalFlush = "ROYAL FLUSH"

suits = {
    0: "s",  # spades
    1: "c",  # clubs
    2: "d",  # diamonds
    3: "h"  # hearts
}

ranks = {
    2: "2", 3: "3", 4: "4",
    5: "5", 6: "6", 7: "7",
    8: "8", 9: "9", 10: "10",
    11: "J", 12: "Q", 13: "K",
    14: "A"
}

payout = { #hand name + payout multiplier
    nothing: 0,
    lowPair: 0,
    jb: 1,
    twoPair: 2,
    three: 3,
    straight: 4,
    flush: 6,
    fullHouse: 9,
    quads: 25,
    straightFlush: 50,
    royalFlush: 250
}

if __name__ == '__main__':
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()  # Width of the screen
    screen_height = window.winfo_screenheight()  # Height of the screen
    window.geometry("+5+5")
    window.title("poker")
    window.mainloop()

    input("Press any key to end")
