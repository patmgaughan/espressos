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
            return True, ""
        else:
            return False, "My Hands are full!"
    
    def inventory(self):
        if(isinstance(self.holding, Pizza)):
            return self.name() + " holds " + self.holding.toString()
        return self.name() + " holds " + str(self.holding)

    def get_(self, ingredient):
        if(not (ingredient in Pantry.pantry)):
            return False, "Ingredient \"" + ingredient + "\" unknown: try \"-h\""
        if(not self.nextTo(Pantry.pantry[ingredient])):
            return False, "Can't get " + str(ingredient) + ", not standing next to " + \
                   str(Pantry.pantry[ingredient])

        return self.give(ingredient)

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
            return False, "Sorry, must be next to an appliance to get things"
        elif(len(thingsToGet) > 1):
            return False, "Possible things to get: " + str(thingsToGet)

        return self.give(thingsToGet[0])

    def commandPut(self):
        if(not self.nextTo(WorkStation)):
            return False, "Can't put down item, not next to workstation"

        workstation = self.nextToObject("workStation") # this function is the same funct but returns the object
        if(self.holding == None):
            return False, "You're not holding anything"


        item = self.emptyHands() 
        #player gets what ever the workstation returns
        self.holding = workstation.put(item) # put what I was holding at the workstation
        if(self.holding != None): 
            return False, "Workstation is full"

        return True, ""


    def commandTake(self):
        if(not self.nextTo(WorkStation)):
            return False, "Error not next to workstation"

        workstation = self.nextToObject("workStation")
        item = workstation.myPizza()

        if(item == None):
            return False, "Error workstation empty"

        succ, msg = self.give(workstation.myPizza())
        workstation.setPizza(None)
        return succ, msg


    def commandBake(self):
        if(not self.nextTo(Oven)):
            return False, "Must be next to Oven to bake"

        pizza = self.emptyHands()
        if(not isinstance(pizza, Pizza)):
            self.give(pizza)
            return False, "Sorry, can only bake Pizza in oven"
        elif(pizza.baked == True):
            self.give(pizza)
            return False, "Pizza already baked!"
        
        pizza.baked = True
        print("Baking Pizza") #must fix
        oven = self.nextToObject("oven")
        oven.setColor(Color.stove)
        self.kitchen.print() #must fix
        oven.setColor(Color.oven)
        time.sleep(1)
                
        self.give(pizza)
        return True, "Pizza baked!"

    def commandTrash(self):
        if(not self.nextTo(TrashCan)):
            return False, "Nothing to throw out"

        self.emptyHands()
        return True, ""

    def commandServe(self):
        if(not self.nextTo(Counter)):
            return False, "must be next to counter to serve"

        if(not isinstance(self.holding, Pizza)):
            return False, "Must hold a pizza to serve"

        pizza = self.emptyHands()
        if(pizza.baked != True):
            self.give(pizza)
            return False, "Must bake pizza before you serve it!"

        return True, "Pizza has been served"
        #is there an order on the queue that matches the pizza we order
        

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
            return False, ""
        if(not self.kitchen.isEmpty(row, col)):
            return False, ""

        self.kitchen.remove(self.row, self.col) 
        self.row = row
        self.col = col
        self.kitchen.put(self, self.row, self.col)

        return True, ""

    def moveDown(self):
        return self.move(self.row+1, self.col)

    def moveUp(self):
        return self.move(self.row-1, self.col)

    def moveRight(self):
        return self.move(self.row, self.col+1)

    def moveLeft(self):
        return self.move(self.row, self.col-1)

