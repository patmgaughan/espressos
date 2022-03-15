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
        elif(command == "make_pizza"):
            if(player1.nextTo("oven")):
                player1.givePizza()
            else:
                print("Can't make pizza, not next to oven")
        elif(command == "get_dough"):
            if(player1.nextTo("doughStation")):
                player1.give("dough")
            else:
                print("Can't get dough, not next to dough Station")
        elif(command == "get_sauce"):
            if(player1.nextTo("stove")):
                player1.give("sauce")
            else:
                print("Can't get sauce, not next to stove")
        elif(command == "get_cheese"):
            if(player1.nextTo("fridge")):
                player1.give("cheese")
            else:
                print("Can't get cheese, not next to fridge")
        elif(command == "get_vegan_cheese"):
            if(player1.nextTo("fridge")):
                player1.give("vegan_cheese")
            else:
                print("Can't get cheese, not next to fridge")
        elif(command == "get_anchovies"):
            if(player1.nextTo("tank")):
                player1.give("anchovies")
            else:
                print("Can't get anchovies, not next to fish Tank")
        elif(command == "serve_pizza"):
            if(player1.nextTo("counter")):
                if(player1.pizzaCount == 0):
                    print("Player 1 has no pizzas to serve")
                else:
                    player1.takePizza()
            else:
                print("Can't serve pizza, not next to counter")
        elif(command == "put"): #trys to put whatever you hold down at the workstation
            #this is a more complex command
            if(player1.nextTo("workStation")):
                workstation = player1.nextToObject("workStation") # this function is the same funct but returns the object
                if(player1.holding != None):
                    #should give us a string
                    item = player1.emptyHands()
                    print("Player 1 is holding " + item)
                    if(workstation == None):
                        print("ERROR workstation is null!!!")
                    #workstation.holding = item # put what I was holding at the workstation
                else: 
                    print("You're not holding anything")
            else:
                print("Can't put down item, not next to workstation")
        elif(command == "q"):
            print("Pini's Pizza has bought Espressos")
            break
        kitchen.print()

def setUpKitchen(kitchen):
    player1 = Cook(kitchen, 4, 3, "player1")
    #add ovens
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

# adds for the week 3/13
# Jackson
# function that can take in a 
#     row and col, and find a path
#     to it if possible, then
#     move to that path, otherwise
#     say i cant go there

# Dylan
# nicer print function
#    -maybe one that also takes an order list / queue?
#    -could also take up more space

# Patrick
# -orders, will be its own thread
# -make oven take a few seconds to make a pizza
# -make pizza's more complicated to make

# questions
# functionaility first or add another player?

#another thread will generate orders

