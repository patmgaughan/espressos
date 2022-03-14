from tokenize import cookie_re
from kitchen import Kitchen


class Cook:
    def __init__(self, kitchen, row, col, fname):
        #maybe some locking is needed later idk
        self.kitchen = kitchen
        self.row = row
        self.col = col
        self.kitchen.put(self, row, col)
        self.kitchen.player1 = self
        self.row = row
        self.fname = fname
        self.pizzaCount = 0

    def toString(self):
        return "\033[99m*\033[00m"

    def name(self):
        return self.fname

    def givePizza(self):
        self.pizzaCount += 1

    def takePizza(self):
        self.pizzaCount -= 1
    
    def inventory(self):
        return self.name() + " holds " + str(self.pizzaCount) + " Pizzas"

    #these next 2 functions will be made into 1 function
    def nextToOven(self):
        nextToOven = False
        nextToOven = nextToOven or self.kitchen.isOven(self.row+1, self.col)
        nextToOven = nextToOven or self.kitchen.isOven(self.row-1, self.col)
        nextToOven = nextToOven or self.kitchen.isOven(self.row, self.col+1)
        nextToOven = nextToOven or self.kitchen.isOven(self.row, self.col-1)
        return nextToOven

    def nextToCounter(self):
        nextTo = False
        nextTo = nextTo or self.kitchen.isCounter(self.row+1, self.col)
        nextTo = nextTo or self.kitchen.isCounter(self.row-1, self.col)
        nextTo = nextTo or self.kitchen.isCounter(self.row, self.col+1)
        nextTo = nextTo or self.kitchen.isCounter(self.row, self.col-1)
        return nextTo

    #cook is gunna move around in the kitchen
    def moveDown(self):
        #if we cant move dont move
        if(self.row + 1 >= Kitchen.HEIGHT):
            return

        if(not self.kitchen.isEmpty(self.row+1, self.col)):
            return
        #change this to a kitchen move
        # instead of 2 things
        #change place in kitchen
        self.kitchen.remove(self.row, self.col) 
        #maybe add self to make sure we remove self
        self.row = self.row + 1 # bc of how we print
        self.kitchen.put(self, self.row, self.col)
        #done moving kitchen

    def moveUp(self):
        if(self.row - 1 < 0):
            return

        if(not self.kitchen.isEmpty(self.row-1, self.col)):
            return

        self.kitchen.remove(self.row, self.col)
        self.row = self.row - 1
        self.kitchen.put(self, self.row, self.col)

    def moveRight(self):
        if(self.col + 1 >= Kitchen.WIDTH):
            return

        if(not self.kitchen.isEmpty(self.row, self.col+1)):
            return

        self.kitchen.remove(self.row, self.col)
        self.col = self.col + 1
        self.kitchen.put(self, self.row, self.col)

    def moveLeft(self):
        if(self.col - 1 < 0):
            return

        if(not self.kitchen.isEmpty(self.row, self.col-1)):
            return

        self.kitchen.remove(self.row, self.col)
        self.col = self.col - 1
        self.kitchen.put(self, self.row, self.col)

    # if ur next to that obj, 
    # used to validate commands
    #def nextTo(class, )
