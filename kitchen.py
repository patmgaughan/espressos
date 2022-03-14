from operator import truediv

#make a monitor

# this is just a container that
# holds a cook or an applience
class SquareFoot:
    def __init__(self):
        self.empty = True
        self.holding = None

    def __str__(self):
        if(self.empty):
            return "\033[30m \033[00m"
        else:
            return self.holding.toString()

# this should be a singleton
# i.e. there should only ever be one kitchen
class Kitchen:
    WIDTH  = 8
    HEIGHT = 7

    def __init__(self):
        self.floor = [[SquareFoot()for i in range(Kitchen.WIDTH)] \
                      for i in range(Kitchen.HEIGHT)]
        self.player1 = None

    def print(self):
        #assumes player1 is not null currently
        if(self.player1 != None):
            print(self.player1.inventory())
        for row in self.floor:
            for sqft in row:
                print(sqft,end = " ")
            print()
        print("--------------")

    def put(self, obj, row, col):
        sqft = self.floor[row][col]
        # change the values of the sqft
        sqft.empty = False
        sqft.holding = obj

    # will remove anything
    def remove(self, row, col):
        self.floor[row][col].empty = True 

    def isEmpty(self, row, col):
        return self.floor[row][col].empty

    def outOfBounds(self, row, col):
        if(row >= Kitchen.HEIGHT):
            return True
        elif(row < 0):
            return True
        elif(col >= Kitchen.WIDTH):
            return True
        elif(col < 0):
            return True
        return False

    def isOven(self, row, col):
        #print("checking if oven")
        if(self.outOfBounds(row, col)):
            #print("out of bounds")
            return False
        elif(self.floor[row][col].empty):
            #print("twas empty")
            return False
        elif(self.floor[row][col].holding.name() == "oven"):
            #print("found oven!")
            return True

    def isCounter(self, row, col):
        #print("checking if oven")
        if(self.outOfBounds(row, col)):
            #print("out of bounds")
            return False
        elif(self.floor[row][col].empty):
            #print("twas empty")
            return False
        elif(self.floor[row][col].holding.name() == "counter"):
            #print("found oven!")
            return True

    def nextToOven(self, playerName):
        #first check of self.player1 is None
        #print("in next to oven")
        if(playerName != self.player1.name()):
            #print(self.player1.name())
            #print(playerName)
            #print("player not on board")
            return False #player is not on board
        else:
            return self.player1.nextToOven()
