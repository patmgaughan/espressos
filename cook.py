from tokenize import cookie_re
from kitchen import Kitchen
from pizza import Pizza
from color import Color
from pantry import Pantry
from appliance import *
from random import randint
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
        self.color = Color.chef
        self.reset = "\033[00m"
        self.count = 0
        self.up = True
        self.hat = False
        self.duck = False
        self.right = True
        self.justAte = False

        # self.line1 = " MmmM "
        # self.line2 = " |__| "
        # self.line3 = " (oo) "

        # self.line1 = " qmmp "
        # self.line2 = " |__| "
        # self.line3 = " (oo) "

        # self.line1 = " |mm| "
        # self.line2 = " (oo) "
        # self.line3 = " -/\- "

        # hat me
        # self.line1 = " MmmM "
        # self.line2 = " (oo) "
        # self.line3 = " -[]- "

        self.duckHatRight  = "  MmM "
        self.duckHeadRight = "  (o> "
        self.duckArmsRight = "<(__)"
        #                    "  ||  "

        self.duckHatLeft = " MmM  "
        self.duckHeadLeft = " >o)  "
        self.duckArmsLeft =  "(__)>"
        #                   "  ||  "
        

        # self.line1 = "    " "
        # self.line2 = "\___Q "
        # self.line3 = "/\ /\ "

        # self.line1 = "()__()"
        # self.line2 = "( oo )"
        # self.line3 = "q    p"

        self.chefsHat = " MmmM "
        self.head     = " (oo) "
        self.arms     = " -[]-"
        self.feet     = "  ||  "

        #self.hat  = " qmmp "
        self.line1 = " (oo) "
        self.line2 = " -[]-"
        self.line3 = "  ||  "

        # self.line1 = " (oo) "
        # self.line2 = "  []- "
        # self.line3 = "  ||  "

        # self.line1 = " (oo) "
        # self.line2 = " -/\-"
        # self.line3 = "  ||  "

        # self.line1 = " ('') "
        # self.line2 = " ~{}~ "
        # self.line3 = "  !!  "

        # self.line1 = " (XX) "
        # self.line2 = " -()- "
        # self.line3 = "  YY  "

        # self.line1 = " (o0) "
        # self.line2 = "  Y-  "
        # self.line3 = "  |\  "

    def __str__(self):
        return Color.chef + "*" + "\033[00m"

    def mileyCyrus(self):
        self.head          = " (" + Color.CYAN + "oo" + Color.reset + ") "
        self.duckHeadRight = "  (" + Color.CYAN + "o" + Color.reset + "> "
        self.duckHeadLeft  = " >" + Color.CYAN + "o" + Color.reset + ")  "
        return True, "Lovely Eyes"

    def noMileyCyrus(self):
        self.head          = " (oo) "
        self.duckHeadRight = "  (o> "
        self.duckHeadLeft  = " >o)  "
        return True, "Lovely Eyes"

    def wearDress(self):
        self.arms = " -/\-"
        return True, "Looking Good!"

    def wearShirt(self):
        self.arms = " -[]-"
        return True, "Looking Good!"

    def toggleHat(self):
        self.hat = not self.hat
        return True, "Looking Good!"

    def toggleDuck(self):
        self.duck = not self.duck
        return True, "Quack Quack"

    def commandEat(self):
        item = self.emptyHands()
        if(item != None):
            if(isinstance(item, Pizza)):
                if(item.isBaked()):
                    item = "pizza"
                else:
                    item = "raw pizza"

            print("***********************"+ item)
            s = Pantry.ingredientStr[item]
            self.justAte = True
            if("[" in self.arms):
                self.arms = " -[" + s + "]-"
            else:
                self.arms = " -/" + s + "\-"
            self.duckArmsRight = "<(__" + s + ")"
            self.duckArmsLeft =  "(" + s + "__)>"
            return True, "Yum"
        else:
            return False, "Nothing to Eat!"

    def stringline1(self):
        if(self.duck and self.hat):
            if(self.right):
                return self.duckHatRight
            else:
                return self.duckHatLeft
        elif(self.duck):
            if(self.right):
                return self.duckHeadRight
            else:
                return self.duckHeadLeft

        if(self.hat):
            return self.chefsHat
        else:
            return self.head

    def stringline2(self):
        if(self.duck and self.hat):
            if(self.right):
                return self.duckHeadRight
            else:
                return self.duckHeadLeft
        elif(self.duck):
            if(self.right):
                return self.stringArms(self.duckArmsRight)
            else:
                return self.stringArmsLeft(self.duckArmsLeft)

        if(self.hat):
            return self.head
        else:
            return self.stringArms(self.arms)

    def stringline3(self):
        if(self.duck and self.hat):
            if(self.right):
                return self.stringArms(self.duckArmsRight)
            else:
                return self.stringArmsLeft(self.duckArmsLeft)
        elif(self.duck):
            return self.stringLegs()

        if(self.hat):
            return self.stringArms(self.arms)
        else:
            #only change walking when not wearing hat
            return self.stringLegs()

    def stringArms(self, arms):
        if(self.justAte):
            self.resetArms()
            self.justAte = False
            return arms
        return arms + self.stringHolding()

    def stringArmsLeft(self, arms):
        if(self.justAte):
            self.resetArms()
            self.justAte = False
            return arms
        return self.stringHolding() + arms

    def resetArms(self):
        if(" -[" in self.arms):
            self.arms = " -[]-"
        else:
            self.arms = " -/\-"
        self.duckArmsRight = "<(__)"
        self.duckArmsLeft  =  "(__)>"

    def stringHolding(self):
        if(self.holding == None):
            return " "
        elif(isinstance(self.holding, Pizza)):
            if(self.holding.isBaked()):
                return Pantry.ingredientStr["pizza"]
            else:
                return Pantry.ingredientStr["raw pizza"]
        elif(self.holding in Pantry.ingredientStr):
            return Pantry.ingredientStr[self.holding]
        else:
            return "*"

    def stringLegs(self):

        if(self.count == -1):
            return "  /|  "
        elif(self.count == 0):
            return "  ||  "
        else:
           return "  |\  " 

        

    def line(self, num):
        string = ""
        if(num == 1):
            string = self.stringline1()
        elif(num == 2):
            string = self.stringline2()
        elif(num == 3):
            string = self.stringline3()

        return self.color + string + self.reset

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
        elif(self.holding in Pizza.possibleToppings and item in Pizza.possibleToppings):
            self.holding = item
            return True, ""
        elif(self.holding in Pizza.possibleCheese and item in Pizza.possibleCheese):
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
            item = self.emptyHands()
            if(item == None):
                self.give(thingsToGet[0])
            elif(item in thingsToGet):
                i = randint(0, (len(thingsToGet) - 1))
                self.give(thingsToGet[i])
            else:
                self.give(item)
            return True, "Possible things to get: " + str(thingsToGet)

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

        return True, "" #add workstation is holding


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
        #print(self.kitchen) #must fix
        oven.setColor(Color.oven)
        #time.sleep(1)
                
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

        if(self.holding.baked != True):
            return False, "Must bake pizza before you serve it!"

        return True, ""
        

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
            #change look
            self.count = 0
            self.line3 = "  ||  "
            #end change look
            return False, ""
        if(not self.kitchen.isEmpty(row, col)):
            #change look
            self.count = 0
            self.line3 = "  ||  "
            #end change look
            return False, ""

        self.kitchen.remove(self.row, self.col) 
        self.row = row
        self.col = col
        self.kitchen.put(self, self.row, self.col)
        #change look
        if(self.up):
            self.count +=1
        else:
            self.count -=1

        if(self.count == 1):
            self.up = False
        elif(self.count == -1):
            self.up = True
        #done changing look
        return True, ""

    def moveDown(self):
        return self.move(self.row+1, self.col)

    def moveUp(self):
        return self.move(self.row-1, self.col)

    def moveRight(self):
        self.right = True
        return self.move(self.row, self.col+1)

    def moveLeft(self):
        self.right = False
        return self.move(self.row, self.col-1)

