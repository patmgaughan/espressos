# keeps track of what color things should be when printing
BLACK = "\033[90m"
RED = "\033[91m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
BLUE = "\033[34m"
PINK = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GREEN_BACK = "\u001b[42m"
BRIGHT_RED = "\033[91;1m"

class Color:
    workStation = PINK
    doughStation = YELLOW
    counter = PINK
    #oven = BRIGHT_RED
    oven = BLACK
    trashCan = PINK
    cheese = WHITE
    stove = RED
    fridge = BLUE
    toppingCounter = GREEN_BACK
    topped = GREEN
    tank = CYAN
    chef = WHITE
