from kitchen import Kitchen
from cook import Cook
from oven import Oven
from counter import Counter
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
            if(player1.nextToOven()):
                player1.givePizza()
            else:
                print("Can't make pizza, not next to oven")
        elif(command == "serve_pizza"):
            if(player1.nextToCounter()):
                if(player1.pizzaCount == 0):
                    print("Player 1 has no pizzas to serve")
                else:
                    player1.takePizza()
            else:
                print("Can't serve pizza, not next to counter")
        elif(command == "q"):
            print("Pini's Pizza has bought Espressos")
            break
        kitchen.print()

def main():
    kitchen = Kitchen()
    kitchen.print()
    player1 = Cook(kitchen, 3, 3, "player1")
    #add ovens
    Oven(kitchen, 6, 6)
    Oven(kitchen, 6, 5)
    Counter(kitchen, 2, 0)
    Counter(kitchen, 3, 0)

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

