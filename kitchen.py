from appliance import *


class Kitchen:
    WIDTH  = 8
    HEIGHT = 7

    def __str__(self):
        result = ""
        for row in self.floor:
            for obj in row:
                if(obj == None):
                    result += "  "
                else:
                    result += str(obj) + " "
            result += "\n"
        result += "--------------"
        return result

    def __init__(self):
        self.floor = [[None for i in range(Kitchen.WIDTH)] \
                      for i in range(Kitchen.HEIGHT)]
        self.player1 = None #remove reference to player

    def put(self, obj, row, col):
        self.floor[row][col] = obj

    def at(self, row, col):
        return self.floor[row][col]

    def remove(self, row, col):
        self.floor[row][col] = None

    def isEmpty(self, row, col):
        return self.floor[row][col] == None

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
        elif(self.floor[row][col] == None):
            return False
        #its an appliance CHECK
        elif(self.floor[row][col].name() == item):
            return True

    def isClass(self, clazz, row, col):
        if(self.outOfBounds(row, col)):
            return False
        elif(self.floor[row][col] == None):
            return False
        elif(isinstance(self.floor[row][col], clazz)):
            return True

    def setUp(self):

        self.put(Oven(), 3, 0)
        self.put(Oven(), 4, 0)

        self.put(Counter(), 0, 2)
        self.put(Counter(), 0, 3)
        self.put(Counter(), 0, 4)

        #self.put(Fridge(), 4, 7)
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

        self.put(ToppingCounter(0), 0, 7)
        self.put(ToppingCounter(1), 1, 7)
        self.put(ToppingCounter(2), 2, 7)

        self.put(TrashCan(), 6, 0)

        self.put(WorkStation(), 3, 3)
        self.put(WorkStation(), 3, 4)
        self.put(WorkStation(), 3, 5)
        self.put(WorkStation(), 3, 6)
        self.put(WorkStation(), 3, 7)


    # getRow(row)
    # Returns:  The string of the kitchen board based on the row given
    # Purpose:  Print the kitchen line by line
    # Notes:    Assuming zero-indexing!!!
    def getRow(self, row):
        line = ""
        
        # loop over the row in the floor
        for obj in self.floor[row]:
            # based on what's in the row add the corresponding string
            if(obj == None):
                line += "  "
            else:
                line += str(obj) + " "

        return line





