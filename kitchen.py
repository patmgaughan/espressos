from operator import truediv
#from cook import Cook
from oven import Oven
from counter import Counter
# from fridge import Fridge
#from doughStation import DoughStation
# from stove import Stove
# from tank import Tank
# from toppingCounter import ToppingCounter
#from trashCan import TrashCan
from limitLessAppliance import TrashCan, DoughStation, ToppingCounter, \
                               Stove, Fridge, Tank
from workStation import WorkStation
import sys
from pizza import Pizza

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
            return self.holding.toString() #change this to __str__

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

    def at(self, row, col):
        sqft = self.floor[row][col]
        # change the values of the sqft
        return sqft.holding

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

    def isA(self, item, row, col):
        if(self.outOfBounds(row, col)):
            return False
        elif(self.floor[row][col].empty):
            return False
        elif(self.floor[row][col].holding.name() == item):
            return True

    def setUp(self):

        self.put(Oven(), 3, 0)
        self.put(Oven(), 4, 0)

        self.put(Counter(), 0, 2)
        self.put(Counter(), 0, 3)
        self.put(Counter(), 0, 4)

        self.put(Fridge(), 4, 7)
        self.put(Fridge(), 5, 7)

        self.put(DoughStation(), 6, 2)
        self.put(DoughStation(), 6, 3)
        self.put(DoughStation(), 6, 4)

        self.put(Stove(), 6, 5)

        #tanks
        self.put(Tank(), 0, 0)
        tank2 = Tank()
        tank2.setShape("Q")
        self.put(tank2, 0, 1)

        self.put(ToppingCounter(), 0, 7)
        self.put(ToppingCounter(), 1, 7)
        self.put(ToppingCounter(), 2, 7)

        self.put(TrashCan(), 6, 0)

        self.put(WorkStation(), 3, 3)
        self.put(WorkStation(), 3, 4)
        self.put(WorkStation(), 3, 5)
        self.put(WorkStation(), 3, 6)
        self.put(WorkStation(), 3, 7)

        # Fridge(self, 4, 7)
        # Fridge(self, 5, 7)

        # DoughStation(self, 6, 2)
        # DoughStation(self, 6, 3)
        # DoughStation(self, 6, 4)

        # Stove(self, 6, 5)
        # Tank(self, 0, 0)
        # Tank(self, 0, 1)

        # ToppingCounter(self, 0, 7)
        # ToppingCounter(self, 1, 7)
        # ToppingCounter(self, 2, 7)

        # TrashCan(self, 6, 0)

        # WorkStation(self, 3, 3)
        # WorkStation(self, 3, 4)
        # WorkStation(self, 3, 5)
        # WorkStation(self, 3, 6)
        # WorkStation(self, 3, 7)

        #return player1