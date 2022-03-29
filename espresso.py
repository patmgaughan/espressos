from kitchen import Kitchen
from cook import Cook

commands = {"w":"moveUp", "s":"moveDown", "a":"moveLeft", "d":"moveRight",\
            "get":"commandGet", "put":"commandPut", "take":"commandTake", \
            "trash":"commandTrash", "bake":"commandBake", "serve":"commandServe", \
            "get_":"get_"}

# i think most manipulation is
# done through the cooks
def run(kitchen, player1):
    while True:
        #get command
        command = input("Command: ")
        arg1 = ""
        if(command.startswith("get_")):
            arg1 = command.replace('get_', '')
            command = "get_"
        #get command

        if(command == "q"):
             print("Pini's Pizza has bought Espressos")
             break
        else: #all other commands
            def command_not_found(): # just in case we dont have the function
                print("Command \"" + command + "\" unknown: try \"-h\"")
            if(command in commands):
                func_name = commands[command] #makes string in case its none, FIX
                func = getattr(player1,func_name,command_not_found) 
                if(command == "get_"):
                    func(arg1) # <-- this should work, and just pass in a value if needed
                else:
                    func()
            else:
                command_not_found()

        kitchen.print()

def main():
    kitchen = Kitchen()
    kitchen.setUp() #can have different setUps
    player1 = Cook(kitchen, 4, 3, "Jackson")
    #start game
    print("Welcome to Espresso's")
    kitchen.print()
    #run game
    run(kitchen, player1)

if __name__=="__main__":
    main()




