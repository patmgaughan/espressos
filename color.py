"""
  color.py
  Description: Holds the strings needed to change the color 
               of strings when printed to the terminal.
               Holds the color of various objects as well 
               as all possible colors for classes to use

  Authors: Patrick Gaughan
"""

# keeps track of what color things should be when printing
BLACK = "\033[90m"
RED = "\033[91m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
BLUE = "\033[34m"
PINK = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

BLACK_BACK = "\033[40m"
GREEN_BACK = "\u001b[42m"
YELLOW_BACK = "\u001b[43m"
BLUE_BACK = "\033[44m"
PINK_BACK = "\033[45m"
CYAN_BACK = "\033[46m"
WHITE_BACK = "\033[47m"


BRIGHT_RED = "\033[91;1m"

class Color:
    BLACK = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[32m"
    YELLOW = "\033[93m"
    BLUE = "\033[34m"
    PINK = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    BLACK_BACK = "\033[40m"
    GREEN_BACK = "\u001b[42m"
    YELLOW_BACK = "\u001b[43m"
    BLUE_BACK = "\033[44m"
    PINK_BACK = "\033[45m"
    CYAN_BACK = "\033[46m"
    WHITE_BACK = "\033[47m"

    reset = "\033[00m"
    workStation = PINK
    doughStation = YELLOW
    counter = BLACK
    #oven = BRIGHT_RED
    oven = BLACK
    trashCan = BLACK
    cheese = WHITE
    stove = RED
    fridge = "\033[7;47;40m"
    toppingCounter = GREEN_BACK
    topped = GREEN
    tank = CYAN_BACK
    chef = WHITE

    fun2 = CYAN_BACK
    fun = GREEN_BACK
    whiteBack = WHITE_BACK
