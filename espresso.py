import threading

from kitchen import Kitchen
from cook import Cook
from order_list import OrderList
from order_generator import order_generator

commands = {"w":"moveUp", "s":"moveDown", "a":"moveLeft", "d":"moveRight",\
            "get":"commandGet", "put":"commandPut", "take":"commandTake", \
            "trash":"commandTrash", "bake":"commandBake", "serve":"commandServe", \
            "get_":"get_"}

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
                else:
                    succ, msg = func()
            else:
                command_not_found()

        if(msg != ""):
            print(msg)
        print(player1.inventory())
        print(kitchen)
        print(order_list.toString())

def main():
    kitchen = Kitchen()
    kitchen.setUp() #can have different setUps
    player1 = Cook(kitchen, 4, 3, "Jackson")
    order_list = OrderList()
    #start game
    print("Welcome to Espresso's")
    print(kitchen)
    #run game
    run(kitchen, player1, order_list)

if __name__=="__main__":
    main()




