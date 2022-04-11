import threading

from kitchen import Kitchen
from cook import Cook
from order_list import OrderList
from order_generator import order_generator

commands = {"w":"moveUp", "s":"moveDown", "a":"moveLeft", "d":"moveRight",\
            "get":"commandGet", "put":"commandPut", "take":"commandTake", \
            "trash":"commandTrash", "bake":"commandBake", "serve":"commandServe", \
            "get_":"get_"}

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
    
    board[0] = player.inventory()
    
    for i in range(Kitchen.HEIGHT):
        board[i + 1] = kitchen.getRow(i)
   
    
    board[1] += "      Order Queue" + "      Completed Orders: \033[32m{}".format(order_counts[0])
    board[2] += " ---------------------" + " Expired Orders:   \033[91m{}".format(order_counts[1])
  
    topFive = order_list.topFive()
    for i in range(len(topFive)):
        board[i + 3] += " {}) {}".format(i + 1, topFive[i]) 

    for i in range(len(board)):
        print(board[i]) 


    
# i think most manipulation is
# done through the cooks
def run(kitchen, player1, order_list):
    order_thread = threading.Thread(target=order_generator, args=("hard", order_list,))
    order_thread.start()
    completed_orders = 0
    expired_orders = 0
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
                        if succ:
                            completed_orders += 1
                        else:
                            player1.give(pizza)
                else:
                    succ, msg = func()
            else:
                command_not_found()

        if(msg != ""):
            print(msg)

        expired_orders += order_list.removeExpired()

        printGame(player1, kitchen, order_list, (completed_orders, expired_orders))

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

if __name__=="__main__":
    main()




