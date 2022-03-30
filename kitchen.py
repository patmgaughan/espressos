from appliance import *

class SquareFoot:
    def __init__(self):
        self.empty = True
        self.holding = None

    def __str__(self):
        if(self.empty):
            return "\033[30m \033[00m"
        else: #will always hold an appliance
            return self.holding.__str__()

class Kitchen:
    WIDTH  = 8
    HEIGHT = 7

    def __str__(self):
        result = ""
        # assumes player1 is not null currently
        if (self.player1 != None):
            result += self.player1.inventory() + "\n"
        for row in self.floor:
            for sqft in row:
                result += str(sqft) + " "
            result += "\n"
        result += "--------------\n"
        return result


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

    def isClass(self, clazz, row, col):
        if(self.outOfBounds(row, col)):
            return False
        elif(self.floor[row][col].empty):
            return False
        elif(isinstance(self.floor[row][col].holding, clazz)):
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