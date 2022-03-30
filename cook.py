from tokenize import cookie_re
from kitchen import Kitchen
from pizza import Pizza
from color import Color
from pantry import Pantry
from appliance import *
import time

class Cook:
    def __init__(self, kitchen, row, col, fname):
        #maybe some locking is needed later idk
        self.kitchen = kitchen
        self.row = row
        self.col = col
        self.kitchen.put(self, row, col) #puts self into kitchen
        self.kitchen.player1 = self
        self.row = row
        self.fname = fname
        self.holding = None

    def __str__(self):
        return Color.chef + "*" + "\033[00m"

    def name(self):
        return self.fname

    def emptyHands(self):
        item = self.holding
        self.holding = None
        return item

    def give(self, item):
        if(self.holding == None):
            self.holding = item
        else:
            print("My Hands are full!")
    
    def inventory(self):
        if(isinstance(self.holding, Pizza)):
            return self.name() + " holds " + self.holding.toString()
        return self.name() + " holds " + str(self.holding)

    def get_(self, ingredient):
        if(not (ingredient in Pantry.pantry)):
            print("Ingredient \"" + ingredient + "\" unknown: try \"-h\"")
            return
        if(self.nextTo(Pantry.pantry[ingredient])):
            self.give(ingredient)
        else:
            print("Can't get " + str(ingredient) + ", not standing next to " + \
                   str(Pantry.pantry[ingredient]))

    #this can now make use of limitLessApplinces
    def commandGet(self):
        thingsToGet = []
        #lets see if we can get anything!
        appliances = self.nextToAnyObject()
        for appliance in appliances:
            for ingredient in Pantry.pantry:
                if(isinstance(appliance, Pantry.pantry[ingredient])):
                    thingsToGet.append(ingredient)
        if(len(thingsToGet) == 0):
            print("Sorry, must be next to an appliance to get things")
        elif(len(thingsToGet) == 1):
            self.give(thingsToGet[0])
        else:
            print("Possible things to get: " + str(thingsToGet))

    def commandPut(self):
    #this is a more complex command
        if(self.nextTo(WorkStation)):
            workstation = self.nextToObject("workStation") # this function is the same funct but returns the object
            if(self.holding != None):
                #should give us a string
                #CHANGE
                item = self.emptyHands() # i dont think hands emptied
                #an error if workstation is null
                #player gets what ever the workstation returns
                self.holding = workstation.put(item) # put what I was holding at the workstation
            else: 
                print("You're not holding anything")
        else:
            print("Can't put down item, not next to workstation")


    def commandTake(self):
        if(self.nextTo(WorkStation)):
            workstation = self.nextToObject("workStation")
            item = workstation.myPizza()
            if(item != None):
                self.give(workstation.myPizza())
                workstation.setPizza(None)
            else:
                print("Error workstation empty")
        else:
            print("Error not next to workstation")

    def commandBake(self):
        if(self.nextTo(Oven)):
            pizza = self.emptyHands()
            if(not isinstance(pizza, Pizza)):
                print("Sorry, can only bake Pizza in oven")
                self.give(pizza)
            elif(pizza.baked == True):
                print("Pizza already baked!")
                self.give(pizza)
            else:
                pizza.baked = True
                print("Baking Pizza")
                oven = self.nextToObject("oven")
                oven.setColor(Color.stove)
                self.kitchen.print() #this def wont be null
                oven.setColor(Color.oven)
                time.sleep(1)
                print("Pizza baked!")
                self.give(pizza)

    def commandTrash(self):
        if(self.nextTo(TrashCan)):
            self.emptyHands()
        else:
            print("Nothing to throw out")

    def commandServe(self):
        if(self.nextTo(Counter)):
            if(isinstance(self.holding, Pizza)):
                pizza = self.emptyHands()
                if(pizza.baked == True):
                    print("Pizza has been served")
                else:
                    print("Must bake pizza before you serve it!")
                    self.give(pizza)
            else:
                print("Must hold a pizza to serve")
        else:
            print("must be next to counter to serve")


    #these will all be simplified soon
    def nextTo(self, clazz):
        nextTo = False
        nextTo = nextTo or self.kitchen.isClass(clazz, self.row+1, self.col)
        nextTo = nextTo or self.kitchen.isClass(clazz, self.row-1, self.col)
        nextTo = nextTo or self.kitchen.isClass(clazz, self.row, self.col+1)
        nextTo = nextTo or self.kitchen.isClass(clazz, self.row, self.col-1)
        return nextTo

    def nextToObject(self, item):
  
        if(self.kitchen.isA(item, self.row+1, self.col)):
            return self.kitchen.at(self.row+1, self.col)
        if(self.kitchen.isA(item, self.row-1, self.col)):
            return self.kitchen.at(self.row-1, self.col)
        if(self.kitchen.isA(item, self.row, self.col+1)):
            return self.kitchen.at(self.row, self.col+1)
        if(self.kitchen.isA(item, self.row, self.col-1)):
            return self.kitchen.at(self.row, self.col-1)

        return None

    #return None if not next to anything
    #otherwise return the first object that you are next to
    def nextToAnyObject(self):

        objects = []

        if(not self.kitchen.isEmpty(self.row+1, self.col)):
            objects.append(self.kitchen.at(self.row+1, self.col))
        if(not self.kitchen.isEmpty(self.row-1, self.col)):
            objects.append(self.kitchen.at(self.row-1, self.col))
        if(not self.kitchen.isEmpty(self.row, self.col+1)):
            objects.append(self.kitchen.at(self.row, self.col+1))
        if(not self.kitchen.isEmpty(self.row, self.col-1)):
            objects.append(self.kitchen.at(self.row, self.col-1))

        return objects

    def move(self, row, col):
        if(self.kitchen.outOfBounds(row, col)):
            return
        if(not self.kitchen.isEmpty(row, col)):
            return

        self.kitchen.remove(self.row, self.col) 
        self.row = row
        self.col = col
        self.kitchen.put(self, self.row, self.col)

    def moveDown(self):
        self.move(self.row+1, self.col)

    def moveUp(self):
        self.move(self.row-1, self.col)

    def moveRight(self):
        self.move(self.row, self.col+1)

    def moveLeft(self):
        self.move(self.row, self.col-1)

