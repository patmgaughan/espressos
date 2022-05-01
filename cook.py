"""
  cook.py
  Description: Definition of a cook. They mainly move by their
               command functions being run. They can move around the
               kitchen, get things from appliance, and do all the 
               things that are needed to create and serve a pizza

  Authors: Patrick Gaughan
"""

from kitchen import Kitchen
from pizza import Pizza
from color import Color
from pantry import Pantry
from appliance import *
from random import randint

class Cook:
    def __init__(self, kitchen, row, col, fname):
        self.kitchen = kitchen
        self.row = row
        self.col = col
        self.kitchen.put(self, row, col) # add player to kitchen
        self.kitchen.player1 = self
        self.fname = fname
        self.holding = None
        self.color = Color.chef
        self.reset = "\033[00m"
        self.count = 0
        self.up = True

        self.msg = ""

        self.hat = False
        j = randint(0, 2)
        if(j == 2):
            self.hat = True

        self.duck = False
        j = randint(0, 5)
        if(j == 5):
            self.duck = True

        self.right = True
        self.justAte = False

        self.standingLegs     = "  ||  "

        # strings for characters
        self.duckHatRight  = "  MmM "
        self.duckHeadRight = "  (o> "
        self.duckArmsRight = "<(__)"

        self.duckHatLeft = " MmM  "
        self.duckHeadLeft = " >o)  "
        self.duckArmsLeft =  "(__)>"

        self.chefsHat = " MmmM "
        self.head     = " (oo) "
        i = randint(0, 1)
        self.arms     = " -[]-"
        if(i == 1):
            self.arms = " -/\-"

        self.feet     = "  ||  "

        self.line1 = " (oo) "
        self.line2 = " -[]-"
        self.line3 = "  ||  "

    # changes eyes to be blue
    def mileyCyrus(self):
        self.head          = " (" + Color.CYAN + "oo" + Color.reset + ") "
        self.duckHeadRight = "  (" + Color.CYAN + "o" + Color.reset + "> "
        self.duckHeadLeft  = " >" + Color.CYAN + "o" + Color.reset + ")  "
        return True, "Better to see you with my dear"

    # changes eyes back to white
    def noMileyCyrus(self):
        self.head          = " (oo) "
        self.duckHeadRight = "  (o> "
        self.duckHeadLeft  = " >o)  "
        return True, "Well look at that"

    # makes the person wear a dress
    def wearDress(self):
        self.arms = " -/\-"
        return True, "I feel pretty"

    #makes the person wear a shirt
    def wearShirt(self):
        self.arms = " -[]-"
        return True, "Is this shirt a bit too boxy?"

    # toggels if the person is wearing a hat
    def toggleHat(self):
        self.hat = not self.hat
        if(self.hat):
            return True, "Looking Good!"
        else:
            return True, "Looking Good!"

    # toggles if the person is a chef
    def toggleDuck(self):
        self.duck = not self.duck
        if(self.duck):
            return True, "Quack, Quack, Quack"
        else:
            return True, "Hello, Hello, Hello"

    # command for player to eat. If they are holding anything
    # it is removed from their hands and shown to be in their
    # stomach
    def commandEat(self):
        item = self.emptyHands()
        if(item != None):
            if(isinstance(item, Pizza)):
                if(item.isBaked()):
                    item = "pizza"
                else:
                    item = "raw pizza"

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
            return False, "There's nothing to eat :("

    # prints the first line of a cook
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

    # prints the first line of a cook
    def line1Simple(self):
        if(self.duck and self.hat):
            return self.duckHatRight

        elif(self.duck):
            return self.duckHeadRight

        if(self.hat):
            return self.chefsHat
        else:
            return self.head

    # prints the 2nd line of a cook
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

    def line2Simple(self):
        if(self.duck and self.hat):
            return self.duckHeadRight

        elif(self.duck):
            return "<(__) "

        if(self.hat):
            return self.head
        else: #fix
            if("[" in self.arms):
                return " -[]- "
            else:
                return " -/\- "

    # print the 3rd line of a cook
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


    # print the 3rd line of a cook sans animations
    def line3Simple(self):
        if(self.duck and self.hat):

            return "<(__) "

        elif(self.duck):
            return self.standingLegs

        if(self.hat): #fix
            if("[" in self.arms):
                return " -[]- "
            else:
                return " -/\- "
        else:
            #only change walking when not wearing hat
            return self.standingLegs

    # returns the string rep of a cook's arms for
    # people and ducks facing right
    def stringArms(self, arms):
        if(len(arms) == 5): 
            return arms + self.stringHolding()
        else:
            return arms

    # returns the string rep of a cook's arms for
    # ducks facing left
    def stringArmsLeft(self, arms):

        if(len(arms) == 5): 
            return self.stringHolding() + arms
        else:
            return arms

    # remove the food the character ate
    # by chaning the string that represents
    # their arm
    def resetArms(self):
        self.justAte = False
        if(" -[" in self.arms):
            self.arms = " -[]-"
        else:
            self.arms = " -/\-"
        self.duckArmsRight = "<(__)"
        self.duckArmsLeft  =  "(__)>"

    # returns a string of the item the character is holding
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

    # returns string rep of the cook's legs
    def stringLegs(self):
        if(self.count == -1):
            return "  /|  "
        elif(self.count == 0):
            return "  ||  "
        else:
           return "  |\  " 

    # returns one of the third lines that represent
    # a cook when printing based on the input num
    # if num isnt 1,2, or 3 it return ""
    def line(self, num):
        string = ""
        if(num == 1):
            string = self.stringline1()
        elif(num == 2):
            string = self.stringline2()
        elif(num == 3):
            string = self.stringline3()

        return self.color + string + self.reset

    # returns the name of a cook
    def name(self):
        return self.fname

    # emptys the hands of a cook
    def emptyHands(self):
        item = self.holding
        self.holding = None
        return item

    # gives the cook the item listed
    # this will fail if the cook is already
    # holding somthing
    def give(self, item):
        self.resetArms()

        if(self.holding == None):
            self.holding = item
            return True, ""
        elif(self.holding in Pizza.possibleToppings and \
             item in Pizza.possibleToppings):
            self.holding = item
            return True, ""
        elif(self.holding in Pizza.possibleCheese and \
            item in Pizza.possibleCheese):
            self.holding = item
            return True, ""
        else:
            return False, "My Hands are full!"
    
    # returns a string that represnts the cook's inventory
    def inventory(self):
        if(isinstance(self.holding, Pizza)):
            return self.name() + " holds " + self.holding.toString()
        if(self.holding == None):
            return self.name()
        return self.name() + " holds " + str(self.holding)

    def setMsg(self, msg):
        self.msg = msg

    # returns a string that msg response from the last command
    def msgString(self):
        return self.msg

    # commands
    # allows a gook to attempt to get an ingredient from
    # any appliances that they are next to
    # the ingredient given is the only possible ingrenident 
    # the cook can get
    def get_(self, ingredient):
        self.resetArms()
        if(not (ingredient in Pantry.pantry)):
            return False, "I don't know the ingreident \"" + ingredient +\
                           "\", type \"h\" for help"
        if(not self.nextTo(Pantry.pantry[ingredient])):
            return False, "I can't get " + str(ingredient) +\
                    ", not standing next to " + \
                   str(Pantry.pantry[ingredient])

        return self.give(ingredient)

    # command
    # sees what limitless appliances we are around
    # if we are around any, then we get a random item
    # that is contined in the applience.
    # if this fails, an error message is returned
    def commandGet(self):
        self.resetArms()
        thingsToGet = []
        # see if we can get anything
        appliances = self.nextToAnyObject()
        for appliance in appliances:
            for ingredient in Pantry.pantry:
                if(isinstance(appliance, Pantry.pantry[ingredient])):
                    thingsToGet.append(ingredient)
        if(len(thingsToGet) == 0):
            return False, "I have to be next to an appliance to get things"
        elif(len(thingsToGet) > 1):
            item = self.emptyHands()
            if(item == None):
                self.give(thingsToGet[0])
            elif(item in thingsToGet):
                i = randint(0, (len(thingsToGet) - 1))
                self.give(thingsToGet[i])
            else:
                self.give(item)

            msg = "I could also get "
            for thing in thingsToGet:
                msg += str(thing) + ", "
            return True, msg 

        return self.give(thingsToGet[0])

    # command
    # cook is able to run this command when next to workstation in
    # the kitchen. If they are holding dough or something that can
    # be added to the pizza on the workstation then it is added
    # and removed from cook's hand. Else it is not added to the workstation
    def commandPut(self):
        if(not self.nextTo(WorkStation)):
            return False, "I can't put this, I'm not next to a workstation"

        workstation = self.nextToObject("workStation")
        if(self.holding == None):
            return False, "I'm not holding anything"


        item = self.emptyHands() 
        #player gets what ever the workstation returns
         # put what I was holding at the workstation
        self.holding = workstation.put(item)
        if(self.holding != None): 
            return False, "The workstation is full"

        return True, "" #add workstation is holding

    # command
    # command for a cook to take something from a workstation
    # if cook is next to a workstation than they pick up
    # whatever is at that workstation if their hands are empty
    def commandTake(self):
        self.resetArms()
        if(not self.nextTo(WorkStation)):
            return False, "I need to be next to workstation"

        workstation = self.nextToObject("workStation")
        item = workstation.myPizza()

        if(item == None):
            return False, "This workstation is empty"

        succ, msg = self.give(workstation.myPizza())
        workstation.setPizza(None)
        return succ, msg

    # command
    # if the cook is next to an oven and the cook is 
    # hodling a raw pizza, then the pizza becomes baked
    def commandBake(self):
        if(not self.nextTo(Oven)):
            return False, "I must be next to Oven to bake"

        pizza = self.emptyHands()
        if(not isinstance(pizza, Pizza)):
            self.give(pizza)
            return False, "I can bake Pizza in the oven"
        elif(pizza.baked == True):
            self.give(pizza)
            return False, "My pizza already baked!"
        
        pizza.baked = True
                
        self.give(pizza)
        return True, "Smells Good!"

    # command
    # if the cook is next to a trash can then
    # they throw out the item that they are holding
    def commandTrash(self):
        if(not self.nextTo(TrashCan)):
            return False, "I have nothing to throw out"

        self.emptyHands()
        return True, ""

    # command
    # if the cook is next to the counter and holding
    # a pizza that is on the order list, then the
    # pizza is removed from the players hand.
    # else the player keeps the pizza
    def commandServe(self):
        if(not self.nextTo(Counter)):
            return False, "I must be next to counter to serve"

        if(not isinstance(self.holding, Pizza)):
            return False, "I must hold a pizza to serve"

        if(self.holding.baked != True):
            return False, "I can't serve a raw pizza, let me go bake it"

        return True, "Enjoy!"
        
    # looks at the four spaces in the kitchen that the cook is next to
    # and returns true if any of them are have the same class as the 
    # class given
    def nextTo(self, clazz):
        nextTo = False
        nextTo = nextTo or self.kitchen.isClass(clazz, self.row+1, self.col)
        nextTo = nextTo or self.kitchen.isClass(clazz, self.row-1, self.col)
        nextTo = nextTo or self.kitchen.isClass(clazz, self.row, self.col+1)
        nextTo = nextTo or self.kitchen.isClass(clazz, self.row, self.col-1)
        return nextTo

    # looks at the four items that the cook is next to in
    # the kitchen and returns the first item that is the
    # same as the item listed
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

    # return None if not next to anything
    # otherwise return the array of objects that you are next to
    # within the kitchen
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

    # move cook to the row and col given within
    # the kitchen
    def move(self, row, col):
        
        if(self.kitchen.outOfBounds(row, col)):
            #change look
            self.count = 0
            self.line3 = "  ||  "
            #end change look
            return False, "Something's in my way"
        if(not self.kitchen.isEmpty(row, col)):
            #change look
            self.count = 0
            self.line3 = "  ||  "
            #end change look
            return False, "Something's in my way"

        #we will be moving
        self.resetArms()
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

    # move down in the kitchen
    def moveDown(self):
        return self.move(self.row+1, self.col)

    # move up in the kitchen
    def moveUp(self):
        return self.move(self.row-1, self.col)

    # move right in the kitchen
    def moveRight(self):
        self.right = True
        return self.move(self.row, self.col+1)

    # move right in the kitchen
    def moveLeft(self):
        self.right = False
        return self.move(self.row, self.col-1)

