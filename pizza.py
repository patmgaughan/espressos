class Pizza:

    #I was thinking about the order of things, and it made
    # most sense to seperate the sauce and cheese for ease
    # Sorry Dylan!

    possibleToppings = {"ham", "peperoni", "anchovies", \
                        "green peppers", "olives", "onions", \
                        "pineapple"} #set

    # starts as just a dought
    def __init__(self, sauced = False, cheese = None, \
                       baked = False, toppings = set()):
        self.toppings = toppings #set
        self.baked = baked #bool
        self.sauced = sauced #bool
        self.cheese = cheese #string

    #works!
    def isDough(self):
        return (self.sauced == False) and \
               (self.cheese == None) and \
               (self.toppings == set())

    #I'll fix
    def toString(self):
        #fi
        if(self.isDough()):
            return "pizza dough"
        else:
            return "pizza"

    def name(self):
        return "Pizza"

    # takes in the topping as a string
    # an error if the topping is not a possible topping
    def addTopping(self, topping):
        None
        #see if it exists in topping
            #else, there was an error with fun calls

        #if sauce
            #make sure toppings and cheese empty -> else ruined

        #if cheese
            #make sure toppings empty -> else ruined

        #if it already has that topping
            #make ruined

        #add topping
        #self.toppings.add(topping)

    #can't add sauce

    #can't add cheese if it has "ham", \
                        #"peperoni", "green peppers", "anchovis", \
                        #"olives", "pineapple"