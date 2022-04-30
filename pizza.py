"""
  pizza.py
  Description: The definition of a pizza object. Can 
               start with any figuration. Can be baked or 
               raw. Can have cheese or vegan cheese. Can have 
               sauce or no sauce. Has a set that holds strings
               of toppings of a select flew possible toppings.
               Are created by order generators as well as
               cooks in the kitchen

  Authors: Patrick Gaughan
"""
from color import Color

# the ascii representation of each ingredient
ingredientStr = {
        "dough":Color.YELLOW + "*" + Color.reset, 
        "sauce":Color.RED + "~" + Color.reset,
        "cheese":Color.WHITE + "#" + Color.reset,
        "vegan_cheese":Color.YELLOW + "#" + Color.reset,

        "anchovies":Color.CYAN + "~" + Color.reset,

        #toppings counter
        "ham":Color.PINK + "<" + Color.reset,
        "pineapple":Color.YELLOW + ">" + Color.reset,
        "pepperoni":Color.PINK + "o" + Color.reset,
        "olives":Color.GREEN + "%" + Color.reset,
        "onions":Color.RED + "&" + Color.reset,
        "green_peppers":Color.GREEN + "{" + Color.reset,
        #end toppings counter

        "pizza":Color.YELLOW + "@" + Color.reset
    }

class Pizza:

    # possible toppings that can be on a pizza
    possibleToppings = {"ham", "pepperoni", "anchovies", \
                        "green_peppers", "olives", "onions", \
                        "pineapple"} #set

    possibleCheese = {"cheese", "vegan_cheese"} #set

    # pizza starts as just dough
    def __init__(self, sauced = False, cheese = None, \
                       baked = False, toppings = None):
        if(toppings == None):
            self.toppings = set()
        else:
            self.toppings = toppings #set
        self.baked    = baked #bool
        self.sauced   = sauced #bool
        self.cheese   = cheese #string

        self.toppingsPrintOrder = True
        self.secondToLastTopping = None
        self.lastTopping = None #used for anchovie printing

    # tests if two pizzas are equal
    def __eq__(self, obj):
        if(not isinstance(obj, Pizza)):
            return False

        return (self.toppings == obj.toppings)    and \
               (self.baked == obj.baked)          and \
               (self.sauced == obj.sauced)        and \
               (self.cheese == obj.cheese)


    # returns true if the pizza is baked
    def isBaked(self):
        return self.baked

    # returns true if the pizza is only dough
    def isDough(self):
        return (self.sauced == False) and \
               (self.cheese == None) and \
               (self.toppings == set())

    # #okay this could have a two version or a 4 string version
    # def __str__(self):
    #     shape = "#"
    #     color = "\033[95m"

    #     if(self.baked):
    #         shape = "0"

    #     if(self.isDough()):
    #         color = Color.doughStation
    #     elif(self.cheese != None and self.toppings == set()):
    #         color = Color.cheese
    #     elif(self.sauced == True and self.toppings == set()):
    #         color = Color.stove
    #     elif("anchovies" == self.lastTopping):
    #         color = Color.tank
    #     else:
    #         color = Color.topped

    #     return color + shape + Color.reset

    # returns the pizza as a string of length 4 in the
    # look of the pizza it represents
    def toStringLength4(self):
        string = ""
        string += Color.doughStation + "(" + Color.reset #start pizza
        
        if(self.isDough()):
            string += Color.topped + "  " + Color.reset
        elif(self.cheese != None and self.toppings == set()):
            string += Color.cheese + "##" + Color.reset
        elif(self.sauced == True and self.toppings == set()):
            string += Color.stove + "~~" + Color.reset
        else:
            if(self.secondToLastTopping == None):
                string += ingredientStr[self.lastTopping] + \
                          ingredientStr[self.lastTopping]
            elif (self.toppingsPrintOrder):
                string += ingredientStr[self.secondToLastTopping] + \
                          ingredientStr[self.lastTopping]
            else:
                string += ingredientStr[self.lastTopping] + \
                          ingredientStr[self.secondToLastTopping]

        string += Color.doughStation + ")" + Color.reset
        return string

    # def color(self):
    #     color = "\033[95m"

    #     if(self.isDough()):
    #         color = Color.doughStation
    #     elif(self.cheese != None and self.toppings == set()):
    #         color = Color.cheese
    #     elif(self.sauced == True and self.toppings == set()):
    #         color = Color.stove
    #     elif("anchovies" == self.lastTopping):
    #         color = Color.tank
    #     else:
    #         color = Color.topped

    #     return color

    # returns the pizza as a string
    def toString(self):
        output = ""
        if(self.baked == False):
            output += "raw "
        
        if(self.isDough()):
            output += "pizza dough"
        elif(self.cheese != None):
            if(self.cheese == "vegan_cheese"):
                output += "vegan "
            output += "cheesy pizza "
            if(self.sauced == None):
                output += "(no sauce)"
        else:
            output += "sauced pizza"

        if(self.toppings != set()):
            output += Color.reset + "with "
            for i in self.toppings:
                output += str(i) + " (" + ingredientStr[i] + "), "

        return output

    # def name(self):
    #     return "Pizza"

    # takes in the topping as a string
    # an error if the topping is not a possible topping
    # return topping if it can't be added, None otherwise
    def addTopping(self, topping):
        #see if it exists in topping
        if(not (topping in Pizza.possibleToppings)):
            #ERROR: This is not a possible topping
            return topping
        elif(topping in self.toppings):
            # This topping has already been added to the Pizza
            return topping
        else:
            self.toppingsPrintOrder = not self.toppingsPrintOrder
            self.secondToLastTopping = self.lastTopping
            self.lastTopping = topping
            self.toppings.add(topping)
            return None
