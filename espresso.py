from kitchen import Kitchen
from cook import Cook
# from oven import Oven
# from counter import Counter
# from fridge import Fridge
# from doughStation import DoughStation
# from stove import Stove
# from tank import Tank
# from toppingCounter import ToppingCounter
# from trashCan import TrashCan
# from workStation import WorkStation
import sys
from pizza import Pizza
import time
# make an appliacne thing that holds all the applinces


# global read only pantry
# maps ingredients to locations
# you get them from
pantry = {
    "dough":"doughStation", 
    "sauce":"stove",
    "cheese":"fridge",
    "vegan_cheese":"fridge",
    "anchovies":"tank",
    "ham":"toppingCounter",
    "pepperoni":"toppingCounter",
    "olives":"toppingCounter",
    "onions":"toppingCounter",
    "green_peppers":"toppingCounter"
}

#error if its given a non ingredient
#command function
#this will do the formating of the ingredient
#there can be one get command that will see if you type anything after it..?
def get_(ingredient, player):
    if(not (ingredient in pantry)):
        print("Ingredient \"" + ingredient + "\" unknown: try \"-h\"")
        return
    if(player.nextTo(pantry[ingredient])):
        player.give(ingredient)
    else:
        print("Can't get " + str(ingredient) + ", not standing next to " + \
               str(pantry[ingredient]))

#command
def commandPut(player):
#this is a more complex command
    if(player.nextTo("workStation")):
        workstation = player.nextToObject("workStation") # this function is the same funct but returns the object
        if(player.holding != None):
            #should give us a string
            #CHANGE
            item = player.emptyHands() # i dont think hands emptied
            #an error if workstation is null
            #player gets what ever the workstation returns
            player.holding = workstation.put(item) # put what I was holding at the workstation
        else: 
            print("You're not holding anything")
    else:
        print("Can't put down item, not next to workstation")


def commandTake(player):
    if(player.nextTo("workStation")):
        workstation = player.nextToObject("workStation")
        item = workstation.holding
        if(item != None):
            player.give(workstation.holding)
            workstation.holding = None
        else:
            print("Error workstation empty")
    else:
        print("Error not next to workstation")

def commandBake(player):
    if(player.nextTo("oven")):
        pizza = player.emptyHands()
        if(not isinstance(pizza, Pizza)):
            print("Sorry, can only bake Pizza in oven")
            player.give(pizza)
        elif(pizza.baked == True):
            print("Pizza already baked!")
            player.give(pizza)
        else:
            pizza.baked = True
            print("Baking Pizza")
            player.kitchen.print() #this def wont be null
            time.sleep(1)
            print("Pizza baked!")
            player.give(pizza)

def commandTrash(player):
    if(player.nextTo("trashCan")):
        player.emptyHands()
    else:
        print("Nothing to throw out")

def commandServe(player):
    if(player.nextTo("counter")):
        if(isinstance(player.holding, Pizza)):
            pizza = player.emptyHands()
            if(pizza.baked == True):
                print("Pizza has been served")
            else:
                print("Must bake pizza before you serve it!")
                player.give(pizza)
        else:
            print("Must hold a pizza to serve")
    else:
        print("must be next to counter to serve")

# i think most manipulation is
# done through the cooks
def run(kitchen, player1):
    while True:
        command = input("Command: ")
        #add a command that takes in a row and col
        # maybe change this with a dict?
        #this can now be a dict
        #this could just be player.do(command)
        if(command == "w"):
            player1.moveUp()
        elif(command == "s"):
            player1.moveDown()
        elif(command == "a"):
            player1.moveLeft()
        elif(command == "d"):
            player1.moveRight()
        elif(command == "get"):
            player1.commandGet()
        elif(command.startswith("get_")):
            get_(command.replace('get_', ''), player1)
        elif(command == "put"):
            commandPut(player1)
        elif(command == "take"):
            commandTake(player1)
        elif(command == "trash"):
            commandTrash(player1)
        elif(command == "bake"):
            commandBake(player1)
        elif(command == "serve"):
            commandServe(player1)
        elif(command == "q"):
            print("Pini's Pizza has bought Espressos")
            break
        else:
            print("Command \"" + command + "\" unknown: try \"-h\"")
        kitchen.print()


def main():
    kitchen = Kitchen()
    kitchen.print()
    kitchen.setUp() #can have different setUps
    player1 = Cook(kitchen, 4, 3, "Sean")

    print("Welcome to Espresso's")
    kitchen.print()

    #run game
    run(kitchen, player1)


if __name__=="__main__":
    main()




