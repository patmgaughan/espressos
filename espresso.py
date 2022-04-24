import threading

from color import Color

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
def printGame(player, kitchen, order_list):
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
    
    # board[0] = player.inventory()
    
    # for i in range(Kitchen.HEIGHT):
    #     board[i + 1] = kitchen.getRow(i)
    
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
    order_thread = threading.Thread(target=order_generator, args=("hard", order_list,))
    order_thread.start()
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
            print("Possible Commands")
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
                        if(not succ):
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
        
        #check end game via orderlist?
        printGame(player1, kitchen, order_list)

def main():
    kitchen = Kitchen()
    kitchen.setUp() #can have different setUps
    player1 = Cook(kitchen, 4, 3, "Jackson")
    order_list = OrderList()
    #start game
    print("Welcome to Espresso's")
    printGame(player1, kitchen, order_list)
    #run game
    run(kitchen, player1, order_list)

if __name__=="__main__":
    main()




