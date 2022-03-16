#applience
from pizza import Pizza

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
        if(self.holding == None):
            return "\033[93m#\033[00m"
        elif(self.holding.toString() == "pizza dough"):
            #search up what the color with via
            #pizza last ingreduent
            #then search that up in the pantry
            #then search up that color
            #in the applience and its color
            return "\033[95m#\033[00m"
        else:
            return "\033[91m#\033[00m"
            #return "\u001b[46m#\033[00m"

    #item must be dough or a pizza
    #return what the player was holding or None
    def put(self, item):
        #if the item isn't dough AND we dont hold a pizza
        pizza = self.holding
        if((item != "dough") and (pizza == None)):
            print("Error cannot put this on workstaton")
            return item

        if(item == "dough"):
            #workstation must be null
            #pizza is created at workstation
            if(pizza == None):
                self.holding = Pizza() #which is just dough
                item = None
        if(item == "sauce"):
            #pizza must be unsauced
            #add check
            pizza.sauced = True
            item = None
        #item is now a pizza
        #self.holding = item

        #say what we hold
        #only prints if we are holding something which is a pizza
        print("Workstation holds " + self.holding.toString())
        return item #always return what you had, maybe this is changed to null

    def name(self):
        return "workStation"