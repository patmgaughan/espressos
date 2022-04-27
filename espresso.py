import threading

from color import Color

import time

from kitchen import Kitchen
from cook import Cook
from order_list import OrderList
from order_generator import order_generator

commands = {"w":"moveUp", "s":"moveDown", "a":"moveLeft", "d":"moveRight",\
            "get":"commandGet", "put":"commandPut", "take":"commandTake", \
            "trash":"commandTrash", "bake":"commandBake", "serve":"commandServe", \
            "get_":"get_",\
            #new commands!
            "change hat":"toggleHat", "hat":"toggleHat",
            "wear shirt":"wearShirt", "shirt":"wearShirt",
            "wear dress":"wearDress", "dress":"wearDress",
            "miley":"mileyCyrus", "noah":"noMileyCyrus", 
            "eat":"commandEat",
            "duck":"toggleDuck"}

# printGame(player, kitchen, order_list)
# Returns:  nothing, evaluated for printing side effect
# Pupose:   Prints the entire game to the console 
# Notes:    Prints game like:
#           player1 holds blah
#           - - - - - ^ ^ - -    Orders Queue
#           - - - - - - - - -  ---------------
#           - - - - - - - - -  1) orders here
#           command: 
def printGame(player, kitchen, order_list, order_counts):
    board = [""] * (Kitchen.HEIGHT + 1)

    topFive = order_list.topFive()
    white = Color.whiteBack + "  " + Color.reset
    black = "  "

    for row in range(kitchen.HEIGHT):
        for j in range(1, 4):
            line = ""
            for col in range(kitchen.WIDTH):
                space = kitchen.at(row, col) 
                if(space == None):
                    #line += "      "
                    if(j == 0 or j == 2):
                        #line += white + black + white
                        line += "      "
                    else:
                        #line += black + white + black
                        line += "      "
                else:
                    line += space.line(j)
            lineNum = (row * 3) + (j - 1)
            linesBefore = 4
            if(lineNum == 0):
                print(line + player.inventory())
            elif(lineNum == 1):
                print(line + " ---------------------")
            elif(lineNum == 2):
                print(line + "      Order Queue")
            elif(lineNum == 3):
                print(line + " ---------------------")
            elif ((lineNum - linesBefore) < 5) and ((lineNum - linesBefore) >= 0):
                print(line + str(lineNum-linesBefore+1) + ") "+ topFive[lineNum - linesBefore])
            else:
                print(line)
            
            
    # board = [""] * (Kitchen.HEIGHT + 1)
    
    # # board[0] = player.inventory()
    
    # for i in range(Kitchen.HEIGHT):
    #     board[i + 1] = kitchen.getRow(i)
   
    
    # board[1] += "      Order Queue" + "      Completed Orders: \033[32m{}".format(order_counts[0])
    # board[2] += " ---------------------" + " Expired Orders:   \033[91m{}".format(order_counts[1])
    # # for i in range(Kitchen.HEIGHT):
    # #     board[i + 1] = kitchen.getRow(i)
    
    # board[1] += "      Order Queue"
    # board[2] += " ---------------------"
  
    #topFive = order_list.topFive()
    #for i in range(len(topFive)):
    #     board[i + 3] += " {}) {}".format(i + 1, topFive[i]) 

    # for i in range(len(board)):
    #     print(board[i]) 


    
# i think most manipulation is
# done through the cooks
def run(kitchen, player1, order_list):
    game_over = threading.Event()
    
    # Create thread as a daemon so we do not have to wait for it 
    # to finish
    order_thread = threading.Thread(target=order_generator, 
                                    args=("hard", order_list, game_over), 
                                    daemon=True)
    order_thread.start()

    completed_orders = 0
    expired_orders = 0
    while expired_orders < 10:
        succ = False
        msg = ""
        
        #get_ command
        command = input("Command: ")
        arg1 = ""
        if(command.startswith("get_")):
            arg1 = command.replace('get_', '')
            command = "get_"
        #get_ command

        if(command == "q"):
             print("Pini's Pizza has bought Espressos")
             break
        if(command == "-h"):
            string = "Possible Commands: "
            for c in commands:
                string += c + "|"
            print(string)
        else: #all other commands
            def command_not_found(): # just in case we dont have the function
                print("Command \"" + command + "\" unknown: try \"-h\"")
            if(command in commands):
                func_name = commands[command] #makes string in case its none, FIX
                func = getattr(player1,func_name,command_not_found) 
                if(command == "get_"):
                    succ, msg = func(arg1) # <-- this should work, and just pass in a value if needed
                elif(command == "serve"):
                    succ, msg = func()
                    if(succ):
                        pizza = player1.emptyHands()
                        succ, msg = order_list.fulfillOrder(pizza)
                        if succ:
                            completed_orders += 1
                        else:
                            player1.give(pizza)
                    else:
                        None
                        #orders serve added!
                else:
                    succ, msg = func()
            else:
                command_not_found()

        if(msg != ""):
            print(msg)

        expired_orders += order_list.removeExpired()

        printGame(player1, kitchen, order_list, (completed_orders, expired_orders))

    game_over.set()
        
    #check end game via orderlist?
    printGame(player1, kitchen, order_list)

def main():
    kitchen = Kitchen()
    kitchen.setUp() #can have different setUps
    player1 = Cook(kitchen, 4, 3, "Jackson")
    order_list = OrderList()
    #start game
    print("Welcome to Espresso's")
    printGame(player1, kitchen, order_list, (0, 0))
    #run game
    run(kitchen, player1, order_list)


def openingSeq():
    #an array of string of some size that is empty

    l1 = "___________                                                  /\      "
    l2 = "\_   _____/ ___________________   ____   ______ __________   )/______"
    l3 = " |    __)_ /  ___/\____ \_  __ \_/ __ \ /  ___//  ___/  _ \   /  ___/"
    l4 = " |        \\\___ \ |  |_> >  | \/\  ___/ \___ \ \___ (  <_> )  \___ \ "
    l5 = "/_______  /____  >|   __/|__|    \___  >____  >____  >____/  /____  >"
    l6 = "        \/     \/ |__|               \/     \/     \/             \/ "

    x1 = "___________                                           "
    x2 = "\_   _____/__  ________________   ____   ______ ______"
    x3 = " |    __)_\  \/  /\____ \_  __ \_/ __ \ /  ___//  ___/"
    x4 = " |        \>    < |  |_> >  | \/\  ___/ \___ \ \___ \ "
    x5 = "/_______  /__/\_ \|   __/|__|    \___  >____  >____  >"
    x6 = "        \/      \/|__|               \/     \/     \/ "

    leftOfExpressos = 10
    rightOfExpressos = 10

    screenLength = leftOfExpressos + rightOfExpressos + len(l1)
    personLength = 5

    expressPadding = (screenLength - len(x1)) // 2

    c1 = " MmmM "
    cx = " |  | "
    c2 = " |__| "
    c3 = " (oo) "
    c4 = " -[]- "

    standingLegs = "  ||  "
    walkingLegs  = "  /|  "
    c5 = standingLegs

    sleepSpeed = 0.2

    for i in range(0, screenLength + personLength):
        print((" " * leftOfExpressos) + l1 + (" " * rightOfExpressos))
        print((" " * leftOfExpressos) + l2 + (" " * rightOfExpressos))
        print((" " * leftOfExpressos) + l3 + (" " * rightOfExpressos))
        print((" " * leftOfExpressos) + l4 + (" " * rightOfExpressos))
        print((" " * leftOfExpressos) + l5 + (" " * rightOfExpressos))
        print((" " * leftOfExpressos) + l6 + (" " * rightOfExpressos))

        if(i >= (screenLength / 3)):
            if(sleepSpeed == 1):
                sleepSpeed = 0.05
            if(sleepSpeed == 0.2):
                sleepSpeed = 1
            
            print((" " * expressPadding) + x1 + (" " * expressPadding))
            print((" " * expressPadding) + x2 + (" " * expressPadding))
            print((" " * expressPadding) + x3 + (" " * expressPadding))
            print((" " * expressPadding) + x4 + (" " * expressPadding))
            print((" " * expressPadding) + x5 + (" " * expressPadding))
            print((" " * expressPadding) + x6 + (" " * expressPadding)) 
        else:
            for j in range(0, 6):
                print(" " * screenLength)
        print(" " * i + c1)
        print(" " * i + cx)
        print(" " * i + c2)
        print(" " * i + c3)
        print(" " * i + c4)
        print(" " * i + c5)

        time.sleep(sleepSpeed)


    # c1 = " MmmM "
    # c2 = " |__| "
    # c3 = " (oo) "
    # c4 = " -/\- "
    # c5 = "  ||  "

openingSeq()
# if __name__=="__main__":
#     main()
    




