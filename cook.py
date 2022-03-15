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
        self.pizzaCount = 0 #this will change
        self.holding = None

    def toString(self):
        return "\033[99m*\033[00m"

    def name(self):
        return self.fname

    def givePizza(self):
        self.pizzaCount += 1

    def emptyHands(self):
        item = self.holding
        self.holding = None
        return item

    def give(self, item):
        if(self.holding == None):
            self.holding = item
        else:
            print("My Hands are full!")

    def takePizza(self):
        self.pizzaCount -= 1
    
    def inventory(self):
        return self.name() + " holds " + str(self.holding)

    #these next 2 functions will be made into 1 function
    def nextTo(self, item):
        nextTo = False
        nextTo = nextTo or self.kitchen.isA(item, self.row+1, self.col)
        nextTo = nextTo or self.kitchen.isA(item, self.row-1, self.col)
        nextTo = nextTo or self.kitchen.isA(item, self.row, self.col+1)
        nextTo = nextTo or self.kitchen.isA(item, self.row, self.col-1)
        return nextTo

    def nextToObject(self, item):
        nextTo = False
        item = None

        nextTo = nextTo or self.kitchen.isA(item, self.row+1, self.col)
        if(self.kitchen.isA(item, self.row+1, self.col)):
            item = self.kitchen.floor[self.row+1][self.col].holding

        nextTo = nextTo or self.kitchen.isA(item, self.row-1, self.col)
        if(self.kitchen.isA(item, self.row-1, self.col)):
            item = self.kitchen.floor[self.row-1][self.col].holding

        nextTo = nextTo or self.kitchen.isA(item, self.row, self.col+1)
        if(self.kitchen.isA(item, self.row, self.col+1)):
            item = self.kitchen.floor[self.row][self.col+1].holding

        nextTo = nextTo or self.kitchen.isA(item, self.row, self.col-1)
        if(self.kitchen.isA(item, self.row, self.col-1)):
            item = self.kitchen.floor[self.row][self.col-1].holding

        return item

    # def nextToOven(self):
    #     nextToOven = False
    #     nextToOven = nextToOven or self.kitchen.isOven(self.row+1, self.col)
    #     nextToOven = nextToOven or self.kitchen.isOven(self.row-1, self.col)
    #     nextToOven = nextToOven or self.kitchen.isOven(self.row, self.col+1)
    #     nextToOven = nextToOven or self.kitchen.isOven(self.row, self.col-1)
    #     return nextToOven

    # def nextToCounter(self):
    #     nextTo = False
    #     nextTo = nextTo or self.kitchen.isCounter(self.row+1, self.col)
    #     nextTo = nextTo or self.kitchen.isCounter(self.row-1, self.col)
    #     nextTo = nextTo or self.kitchen.isCounter(self.row, self.col+1)
    #     nextTo = nextTo or self.kitchen.isCounter(self.row, self.col-1)
    #     return nextTo

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
