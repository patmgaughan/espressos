from color import Color
from pizza import Pizza

class Appliance:
    def __init__(self):
        self.shape = "-"
        self.color = "\033[00m"
        self.reset = "\033[00m"

    def __str__(self):
        return self.color + self.shape + self.reset

    def setShape(self, shape):
        self.shape = shape

    def setColor(self, color):
        self.color = color

#appliance
class WorkStation(Appliance):

    def __init__(self):
        super().__init__()
        self.shape = "#"
        self.color = Color.workStation
        self.pizza = None

    #holding is always a pizza, this should be the job of a pizza!
    def __str__(self):
        if(self.pizza != None):
            return self.pizza.__str__()
        else:
            return super().__str__()

    def myPizza(self):
        return self.pizza

    def setPizza(self, pizza):
        self.pizza = pizza
        if((not isinstance(pizza, Pizza)) and (pizza != None)):
            raise RuntimeError("ERROR: Pizza set to non pizza")


    #item must be dough or a pizza
    #return what the player was holding or None
    def put(self, item):
        print("Workstation is about to put")
        #if the item isn't dough AND we dont hold a pizza
        #pizza = self.pizza

        #if item is pizza and counter empty
        if((isinstance(item, Pizza)) and (self.pizza == None)):
            self.pizza = item
            print("Workstation holds " + self.pizza.toString())
            return None

        #make sure workstation has a pizza or were adding dough
        if((item != "dough") and (self.pizza == None)):
            print("Error cannot put this on workstaton")
            return item

        # change this later to be a part of addTopping()
        if(item == "dough"):
            #workstation must be null
            #pizza is created at workstation
            if(self.pizza == None):
                self.pizza = Pizza() #which is just dough
                item = None
        elif(item == "sauce"):
            if(self.pizza.cheese != None):
                print("cannot add sauce, this pizza already has cheese")
                return item
            self.pizza.sauced = True
            item = None
        elif(item == "cheese" or item == "vegan_cheese"):  
            if(self.pizza.cheese != None):
                print("Pizza already has cheese, and Espressos is not made of cheese")
                return item
            self.pizza.cheese = item
            item = None
        else:
            #returns the item if it can not be added, None otherwise
            #item = self.pizza.addTopping(item) #it didn't work when i pasted in 
            # this code
            #try 1, still doesnt work
            self.pizza.toppings.add(item)
            item = None
            #end try 1
            #pizza.toppings = {item}, this works thou??

        print("Workstation holds " + self.pizza.toString())
        return item #always return what you had, maybe this is changed to null

    def name(self):
        return "workStation"

class Counter(Appliance):

    def __init__(self):
        super().__init__()
        self.shape = "_"
        self.color = Color.counter
        self.holding = None #i actually dont think it will hold an object...

    def name(self):
        return "counter"

    #later this will maybe keep track of something?

class Oven(Appliance):
    def __init__(self):
        super().__init__()
        self.shape = "@"
        self.color = Color.oven

    def name(self):
        return "oven"

#just to help classify objects
class limitLessAppliance(Appliance):
    def __init__(self):
        super().__init__()

class TrashCan(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "X"
        self.color = Color.trashCan

    def name(self):
        return "trashCan"

class DoughStation(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "="
        self.color = Color.doughStation

    def name(self):
        return "doughStation"

class Stove(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "%"
        self.color = Color.stove

    def name(self):
        return "stove"

class ToppingCounter(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "]"
        self.color = Color.toppingCounter

    def name(self):
        return "toppingCounter"

class Tank(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = ">"
        self.color = Color.tank

    def name(self):
        return "tank"

class Fridge(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "["
        self.color = Color.fridge

    def name(self):
        return "fridge"