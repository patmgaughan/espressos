from color import Color

class Pizza:

    possibleToppings = {"ham", "peperoni", "anchovies", \
                        "green_peppers", "olives", "onions", \
                        "pineapple"} #set

    # starts as just a dought
    def __init__(self, sauced = False, cheese = None, \
                       baked = False, toppings = None):
        if(toppings == None):
            self.toppings = set()
        else:
            self.toppings = toppings #set
        self.baked    = baked #bool
        self.sauced   = sauced #bool
        self.cheese   = cheese #string

        self.lastTopping = None #used for anchovie printing

    def __eq__(self, obj):
        if(not isinstance(obj, Pizza)):
            return False

        return (self.toppings == obj.toppings)    and \
               (self.baked == obj.baked)          and \
               (self.sauced == obj.sauced)        and \
               (self.cheese == obj.cheese)

    #works!
    def isDough(self):
        return (self.sauced == False) and \
               (self.cheese == None) and \
               (self.toppings == set())

    #lets make this cleaner :)
    def __str__(self):
        shape = "#"
        color = "\033[95m"

        if(self.baked):
            shape = "0"

        if(self.isDough()):
            color = Color.doughStation
        elif(self.cheese != None and self.toppings == set()):
            color = Color.cheese
        elif(self.sauced == True and self.toppings == set()):
            color = Color.stove
        elif("anchovies" == self.lastTopping):
            color = Color.tank
        else:
            color = Color.topped

        return color + shape + "\033[00m"

    # this can be much better
    # this is also wrong lol
    def toString(self):
        output = ""
        if(self.baked == False):
            output += "raw "
        
        if(self.isDough()):
            output += "pizza dough"
        elif(self.cheese != None):
            output += "cheesy pizza"
        else:
            output += "sauced pizza"

        if(self.toppings != set()):
            output += (" " + str(self.toppings))

        return output

    def name(self):
        return "Pizza"

    # takes in the topping as a string
    # an error if the topping is not a possible topping
    #return topping if it can't be added, None otherwise
    def addTopping(self, topping):
        print("Pizza about to add topping!")
        #None
        #see if it exists in topping
        if(not (topping in Pizza.possibleToppings)):
            print("ERROR: This is not a possible topping")
            return topping
            #else, there was an error with fun calls
        elif(topping in self.toppings):
            print("This topping has already been added to the Pizza")
            return topping
        else:
            self.lastTopping = topping
            self.toppings.add(topping)
            return None

def test_answer():
    pizza1 = Pizza(sauced=True, baked=False, \
                   cheese="vegan_cheese", \
                   toppings={"green_peppers", "olives"})

    pizza2 = Pizza(sauced=True, baked=False, \
                   cheese="vegan_cheese", \
                   toppings={"olives", "green_peppers"})

    assert pizza1 == pizza2

    pizza3 = Pizza(sauced=True, baked=False, \
                   cheese="cheese", \
                   toppings={"olives", "green_peppers"})

    assert pizza1 != pizza3
