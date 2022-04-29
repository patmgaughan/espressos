from appliance import *


class Kitchen:
    WIDTH  = 8 # i think I might want this to change
    HEIGHT = 7
    TOTAL_HEIGHT = HEIGHT * 3

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

    def __init__(self, width=WIDTH):
        self.width = width

        self.floor = [[None for i in range(self.width)] \
                      for i in range(Kitchen.HEIGHT)]
        self.player1 = None #remove reference to player

    def put(self, obj, row, col):
        if(self.outOfBounds(row, col)):
            return
        self.floor[row][col] = obj

    def at(self, row, col):
        return self.floor[row][col]

    def remove(self, row, col):
        self.floor[row][col] = None

    def isEmpty(self, row, col):
        if(self.outOfBounds(row, col)):
            return True
        if self.floor[row][col] != None:
            return False
        return True

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

    def totalLines(self):
        return Kitchen.HEIGHT * 3

    def getLine(self, lineNum):
        row = lineNum // 3
        j   = lineNum % 3 + 1
    
        line = ""
        for col in range(self.width):
            space = self.at(row, col) 
            if(space == None):
                #line += "      "
                if(j == 0 or j == 2):
                    #line += white + black + white
                    line += "      "
                    #line += "░░░░░░"
                else:
                    #line += black + white + black
                    line += "      "
                    #line += "░░░░░░"
            else:
                line += space.line(j)
        
        return line

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

    def setUpWaitingRoom(self):
        # self.put(WorkStation(), 0, 0)
        # self.put(WorkStation(), 0, 1)
        # self.put(WorkStation(), 0, 2)
        # self.put(WorkStation(), 0, 3)
        # self.put(WorkStation(), 0, 4)

        # self.put(DoughStation(), 6, 0)
        # self.put(Fridge(), 6, 1)

        for i in range(0, 13):
            self.put(Express("top", i), 2, 4 + i)
            self.put(Express("bottom", i), 3, 4 + i)

    def printKitchen(self):
        for lineNum in range(0, self.totalLines()):
            line = self.getLine(lineNum)
            print(line)

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





