#applience
from pizza import Pizza

#everything that just gives 

class WorkStation:

    #name = "workStation"

    def __init__(self, kitchen, row, col):
        self.kitchen = kitchen
        self.row = row
        self.col = col
        self.kitchen.put(self, row, col)
        self.holding = None

    #holding is always a pizza
    def toString(self):

        shape = "#"

        if(self.holding == None):
            return "\033[93m" + shape + "\033[00m"

        pizzaName = self.holding.toString()
        if(not pizzaName.startswith("raw")):
            shape = "0"

        pizzaName = pizzaName.replace("raw ", "")

        if(pizzaName == "pizza dough"):
 
            return "\033[95m" + shape + "\033[00m"
        elif(pizzaName == "cheesy pizza"):

            return "\033[34m" + shape + "\033[00m"
        elif(pizzaName == "sauced pizza"):
            return "\033[91m" + shape + "\033[00m"
        else:
            return "\033[92m" + shape + "\033[00m"

    #item must be dough or a pizza
    #return what the player was holding or None
    def put(self, item):
        #if the item isn't dough AND we dont hold a pizza
        pizza = self.holding

        #if item is pizza and counter empty
        if((isinstance(item, Pizza)) and (pizza == None)):
            self.holding = item
            print("Workstation holds " + self.holding.toString())
            return None

        #make sure workstation has a pizza or were adding dough
        if((item != "dough") and (pizza == None)):
            print("Error cannot put this on workstaton")
            return item

        #change this later to be a part of addTopping()
        if(item == "dough"):
            #workstation must be null
            #pizza is created at workstation
            if(pizza == None):
                self.holding = Pizza() #which is just dough
                item = None
        elif(item == "sauce"):
            if(pizza.cheese != None):
                print("cannot add sauce, this pizza already has cheese")
                return item
            pizza.sauced = True
            item = None
        elif(item == "cheese" or item == "vegan_cheese"):  
            if(pizza.cheese != None):
                print("Pizza already has cheese, and Espressos is not made of cheese")
                return item
            pizza.cheese = item
            item = None
        else:
            item = pizza.addTopping(item)

            #make sure the pizza doesn't already have this topping
        #item is now a pizza
        #self.holding = item

        #say what we hold
        #only prints if we are holding something which is a pizza
        print("Workstation holds " + self.holding.toString())
        return item #always return what you had, maybe this is changed to null

    def name(self):
        return "workStation"