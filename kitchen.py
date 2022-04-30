"""
  kitchen.py
  Description: The kitchen acts as a 2D array that holds appliances
               and players. Control of kitchen mostly comes
               from chefs

  Authors: Patrick Gaughan
"""
from appliance import *


class Kitchen:

    #general width of a kitchen
    WIDTH  = 8 
    #always the height of a kitchen
    HEIGHT = 7 
    # always the total height of a kitchen
    TOTAL_HEIGHT = HEIGHT * 3

    # def __str__(self):
    #     result = ""
    #     for row in self.floor:
    #         for obj in row:
    #             if(obj == None):
    #                 result += "  "
    #             else:
    #                 result += str(obj) + " "
    #         result += "\n"
    #     result += "--------------"
    #     return result

    def __init__(self, width=WIDTH):
        # sets the kitchen width if set
        self.width = width

        self.floor = [[None for i in range(self.width)] \
                      for i in range(Kitchen.HEIGHT)]
        self.player1 = None #remove reference to player

    # puts somthing into the kitchen at the row and
    # col given. If it is out of bounds nothing
    # happens
    def put(self, obj, row, col):
        if(self.outOfBounds(row, col)):
            return
        self.floor[row][col] = obj

    # returns what is at the row and col given
    # returns None if row, col is out of bounds
    def at(self, row, col):
        if(self.outOfBounds(row, col)):
            return None
        return self.floor[row][col]


    # sets the index given in the floor array
    # to none
    # does nothing if row, col is out of bounds
    def remove(self, row, col):
        if(self.outOfBounds(row, col)):
            return
        self.floor[row][col] = None

    # returns False if the floor index is not
    # empty. returns true if the index
    # holds none or if it is out of bounds
    def isEmpty(self, row, col):
        if(self.outOfBounds(row, col)):
            return True
        if self.floor[row][col] != None:
            return False
        return True

    # returns true if the floor index given is out
    # of bounds, false otherwise
    def outOfBounds(self, row, col):
        if(row >= Kitchen.HEIGHT):
            return True
        elif(row < 0):
            return True
        elif(col >= self.width):
            return True
        elif(col < 0):
            return True
        return False

    # returns the total amount of lines that exist
    # in the string representation of the kitchen
    def totalLines(self):
        return Kitchen.HEIGHT * 3

    # returns the string representation of
    # the line index given. returns spaces
    # if lineNum is too largw
    def getLine(self, lineNum):
        row = lineNum // 3
        j   = lineNum % 3 + 1
    
        line = ""
        for col in range(self.width):
            space = self.at(row, col) 
            if(space == None):
                line += "      "
            else:
                line += space.line(j)
        
        return line

    # checks if the appliance at the row and col
    # is equal to the item given
    def isA(self, item, row, col):
        if(self.outOfBounds(row, col)):
            # index out of bounds
            return False
        elif(self.floor[row][col] == None):
            # index is not the appliance
            return False
        elif(self.floor[row][col].name() == item):
            # the appliance is the same as 
            # the given item
            return True

    def isClass(self, clazz, row, col):
        if(self.outOfBounds(row, col)):
            return False
        elif(self.floor[row][col] == None):
            return False
        elif(isinstance(self.floor[row][col], clazz)):
            return True

    # prints the string representation of self
    def printKitchen(self):
        for lineNum in range(0, self.totalLines()):
            line = self.getLine(lineNum)
            print(line)

    # sets up the kitchen by adding appliances needed
    # to create and serve a pizza
    def setUp(self):

        self.put(Oven(), 3, 0)
        self.put(Oven(), 4, 0)

        self.put(Counter(), 0, 2)
        self.put(Counter(), 0, 3)
        self.put(Counter(), 0, 4)

        self.put(Fridge(), 5, 7)

        self.put(DoughStation(), 6, 2)
        self.put(DoughStation(), 6, 3)
        self.put(DoughStation(), 6, 4)

        self.put(Stove(), 6, 5)

        self.put(Tank(), 0, 0)
        self.put(Tank(), 0, 1)

        self.put(ToppingCounter(0), 0, 7)
        self.put(ToppingCounter(1), 1, 7)
        self.put(ToppingCounter(2), 2, 7)

        self.put(TrashCan(), 6, 0)

        self.put(WorkStation(), 3, 3)
        self.put(WorkStation(), 3, 4)
        self.put(WorkStation(), 3, 5)
        self.put(WorkStation(), 3, 6)
        self.put(WorkStation(), 3, 7)


    # # getRow(row)
    # # Returns:  The string of the kitchen board based on the row given
    # # Purpose:  Print the kitchen line by line
    # # Notes:    Assuming zero-indexing!!!
    # def getRow(self, row):
    #     line = ""
        
    #     # loop over the row in the floor
    #     for obj in self.floor[row]:
    #         # based on what's in the row add the corresponding string
    #         if(obj == None):
    #             line += "  "
    #         else:
    #             line += str(obj) + " "

    #     return line





