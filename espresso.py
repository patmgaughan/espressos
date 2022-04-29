import threading

from color import Color

from sequence import *

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

def printGame(players, kitchen):
    for lineNum in range(0, kitchen.totalLines()):
        line = kitchen.getLine(lineNum)
        linesBefore = 4
        if(lineNum == 0):
            print(line)
        elif(lineNum == 1):
            print(line + " ---------------------")
        elif(lineNum == 2):
            print(line + "      Order Queue")
        elif(lineNum == 3):
            print(line + " ---------------------")
        elif ((lineNum - linesBefore) < 5) and ((lineNum - linesBefore) >= 0):
            print(line + str(lineNum-linesBefore+1) + ") ")
        elif(lineNum >= 10 and lineNum < 10 + len(players)):

            print(line + players[lineNum - 10].inventory())
        else:
            print(line)
         



    
# i think most manipulation is
# done through the cooks
def run(kitchen, player1, order_list):
    
    printGame([player1, player1], kitchen)

    while True:
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
                    # if(succ):
                    #     pizza = player1.emptyHands()
                    #     succ, msg = order_list.fulfillOrder(pizza)
                    #     if succ:
                    #         completed_orders += 1
                    #     else:
                    #         player1.give(pizza)
                    # else:
                    #     None
                    #     #orders serve added!
                else:
                    succ, msg = func()
            else:
                command_not_found()

        if(msg != ""):
            print(msg)

        # expired_orders += order_list.removeExpired()

        printGame([player1, player1], kitchen)

        
    #check end game via orderlist?
    printGame([player1, player1], kitchen)

#basically just run
def runWaitingRoom(kitchen, player1, order_list):
    
    kitchen.printKitchen()

    while True:
        succ = False
        msg = ""
        
        #get_ command
        command = input("Command: ")
        arg1 = ""
        if(command.startswith("get_")):
            arg1 = command.replace('get_', '')
            command = "get_"
        #get_ command

        if(command == "ready"):
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
                else:
                    succ, msg = func()
            else:
                command_not_found()

        if(msg != ""):
            print(msg)

        # expired_orders += order_list.removeExpired()
        kitchen.printKitchen()

        
    #check end game via orderlist?
    kitchen.printKitchen()

def main():
    kitchen = Kitchen()
    kitchen.setUp() #can have different setUps
    # player1 = Cook(kitchen, 4, 3, "Jackson")
    order_list = OrderList()

    waitingRoom = Kitchen(width=20)
    waitingRoom.setUpWaitingRoom()

    player1 = Cook(waitingRoom, 4, 3, "Player 1") #player starts in kitchen
    runWaitingRoom(waitingRoom, player1, order_list)
    #start game
    player1.changeKitchen(kitchen, 4, 3)
    #openingSeq()
    print("Welcome to Espresso's")
    #run game
    run(kitchen, player1, order_list)
    closingSeq(7, 89)

if __name__=="__main__":
    main()

    




