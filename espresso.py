from kitchen import Kitchen
from cook import Cook
from oven import Oven
from counter import Counter
from fridge import Fridge
from doughStation import DoughStation
from stove import Stove
from tank import Tank
from toppingCounter import ToppingCounter
from trashCan import TrashCan
from workStation import WorkStation
import sys
from pizza import Pizza
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
    "ham":"toppingsCounter",
    "pepperoni":"toppingCounter",
    "olives":"toppingCounter",
    "onions":"toppingCounter",
    "green_peppers":"toppingCounter"
}

#error if its given a non ingredient
#command function
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
def put(player):
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

# i think most manipulation is
# done through the cooks
def run(kitchen, player1):
    while True:
        command = input("Command: ")
        #add a command that takes in a row and col
        # maybe change this with a dict?
        if(command == "w"):
            player1.moveUp()
        elif(command == "s"):
            player1.moveDown()
        elif(command == "a"):
            player1.moveLeft()
        elif(command == "d"):
            player1.moveRight()
        elif(command.startswith("get_")):
            get_(command.replace('get_', ''), player1)
        #have another function that is just get, that sees if were
        #next to somthing that we can get, and then if it gives 1 thing
        # get it, otherwise, list the things that it holds
        elif(command == "put"): #trys to put whatever you hold down at the workstation
            put(player1)
        #inspect function to look at what is as a workstation
        #take, to take something from a work bench
            #next thing to write
            #when you take somthing you will become the color of that thing
            #you 
        elif(command == "take"):
            if(player1.nextTo("workStation")):
                workstation = player1.nextToObject("workStation")
                item = workstation.holding
                if(item != None):
                    player1.give(workstation.holding)
                    workstation.holding = None
                else:
                    print("Error workstation empty")
            else:
                print("Error not next to workstation")
        #command to give to the counter
        elif(command == "trash"):
            if(player1.nextTo("trashCan")):
                player1.emptyHands()
            else:
                print("Nothing to throw out")
        elif(command == "q"):
            print("Pini's Pizza has bought Espressos")
            break
        else:
            print("Command \"" + command + "\" unknown: try \"-h\"")
        kitchen.print()

def setUpKitchen(kitchen):
    #have it ask for your name
    player1 = Cook(kitchen, 4, 3, "Dylan")
    # add ovens
    Oven(kitchen, 3, 0)
    Oven(kitchen, 4, 0)

    Counter(kitchen, 0, 2)
    Counter(kitchen, 0, 3)
    Counter(kitchen, 0, 4)

    Fridge(kitchen, 4, 7)
    Fridge(kitchen, 5, 7)

    DoughStation(kitchen, 6, 2)
    DoughStation(kitchen, 6, 3)
    DoughStation(kitchen, 6, 4)

    Stove(kitchen, 6, 5)
    Tank(kitchen, 0, 0)
    Tank(kitchen, 0, 1)

    ToppingCounter(kitchen, 0, 7)
    ToppingCounter(kitchen, 1, 7)
    ToppingCounter(kitchen, 2, 7)

    TrashCan(kitchen, 6, 0)

    WorkStation(kitchen, 3, 3)
    WorkStation(kitchen, 3, 4)
    WorkStation(kitchen, 3, 5)
    WorkStation(kitchen, 3, 6)
    WorkStation(kitchen, 3, 7)

    return player1

def main():
    kitchen = Kitchen()
    kitchen.print()
    player1 = setUpKitchen(kitchen)

    print("Welcome to Espresso's")
    kitchen.print()

    #run game
    run(kitchen, player1)


if __name__=="__main__":
    main()




