"""
  appliance.py
  Description: appliances are objects that chefs can interact with
               limitless appliances allow chefs to get various
               ingredients

  Authors: Patrick Gaughan
"""
from color import Color
from pizza import Pizza

# the ascii representation of each ingredient
ingredientStr = {
        "dough":Color.YELLOW + "*" + Color.reset, 
        "sauce":Color.RED + "~" + Color.reset,
        "cheese":Color.WHITE + "#" + Color.reset,
        "vegan_cheese":Color.YELLOW + "#" + Color.reset,

        "anchovies":Color.CYAN + "~" + Color.reset,
        #toppings counter
        "ham":Color.PINK + "<" + Color.reset,
        "pineapple":Color.YELLOW + ">" + Color.reset,
        "pepperoni":Color.PINK + "o" + Color.reset,
        "olives":Color.GREEN + "%" + Color.reset,
        "onions":Color.RED + "&" + Color.reset,
        "green_peppers":Color.GREEN + "{" + Color.reset,
        #end toppings counter

        "pizza":Color.YELLOW + "@" + Color.reset
    }

class Appliance:
    def __init__(self):
        self.shape = "-"
        self.color = Color.BLACK
        self.reset = Color.reset 

        self.l1 = "+----+"
        self.l2 = "|    |"
        self.l3 = "|____|"

    def line1(self):
        return self.color + self.l1 + self.reset

    def line2(self):
        return self.color + self.l2 + self.reset

    def line3(self):
        return self.color + self.l3 + self.reset

    def line(self, num):
        if(num == 1):
            return self.line1()
        elif(num == 2):
            return self.line2()
        elif(num == 3):
            return self.line3()

        return ""

    def __str__(self):
        return self.color + self.shape + self.reset

    def setShape(self, shape):
        self.shape = shape

    def setColor(self, color):
        self.color = color

# appliance
class WorkStation(Appliance):

    def __init__(self):
        super().__init__()
        self.shape = "#"
        self.color = Color.workStation
        self.pizza = None

        self.l1 = "+----+"
        self.l2 = "|    |"
        self.l3 = "+----+"

    # holding is always a pizza, this should be the job of a pizza!
    def __str__(self):
        if(self.pizza != None):
            return self.pizza.__str__()
        else:
            return super().__str__()

    def line2(self):

        if(self.pizza == None):
            return self.color + "|    |" + self.reset
        else:
            string = ""
            string += self.color + "|" + self.reset
            string += self.pizza.toStringLength4()
            string += self.color + "|" + self.reset
            return string

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
                print("Pizza already has cheese, and \
                       Espressos is not made of cheese")
                return item
            self.pizza.cheese = item
            item = None
        else:
            self.pizza.addTopping(item)
            item = None

        print("Workstation holds " + self.pizza.toString())
        return item #always return what you had, maybe this is changed to null

    def name(self):
        return "workStation"

class Counter(Appliance):

    def __init__(self):
        super().__init__()
        self.shape = "_"
        self.color = Color.counter

        self.l1 = "______"
        self.l2 = "[$][$]"
        self.l3 = "^^^^^^"

    def line2(self):

        string = ""
        string += self.color + "[" + self.reset
        string += Color.GREEN + "$" + Color.reset
        string += self.color + "]" + self.reset

        string += self.color + "[" + self.reset
        string += Color.GREEN + "$" + Color.reset
        string += self.color + "]" + self.reset

        return string

    def name(self):
        return "counter"

class Oven(Appliance):
    def __init__(self):
        super().__init__()
        self.shape = "@"
        self.color = Color.oven

        self.l1 = "-****-"
        self.l2 = "|oven|"
        self.l3 = "|____|"

    def line1(self):

        string = ""
        string += self.color + "-" + self.reset
        string += Color.RED + "****" + Color.reset
        string += self.color + "-" + self.reset

        return string

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

        self.l1 = "|~~~~|"
        self.l2 = "|    |"
        self.l3 = "\\____/"
        

    def name(self):
        return "trashCan"

class DoughStation(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "="
        self.color = Color.BLACK

        self.l1 = "|*  *|"
        self.l2 = "|____|"
        self.l3 = " /  \ "

    def line1(self):
        return self.color + "|" + Color.YELLOW + "*  *" \
               + self.color + "|" + Color.reset

    def name(self):
        return "doughStation"

class Stove(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "%"
        self.color = Color.stove

        self.l1 = "(@)(@)"
        self.l2 = "      "
        self.l3 = "(@)(@)"

    def name(self):
        return "stove"

class ToppingCounter(limitLessAppliance):
    def __init__(self, type=0):
        super().__init__()
        self.shape = "]"
        self.color = Color.toppingCounter

        self.type = type # can be 0, 1, 2
        self.l1 = "(====|"
        self.l2 = " ) * |"
        self.l3 = "(====|"

    def line1(self):
        if(self.type == 0):
                return "------"
        elif(self.type == 1):
                return "| " + ingredientStr["ham"] + "  |"
        elif(self.type == 2):
                return "|" + ingredientStr["pineapple"] + "   |"

        return self.l1

    def line2(self):
        if(self.type == 0):
                return "|  " + ingredientStr["pepperoni"] + " |"
        elif(self.type == 1):
                return "|  " + ingredientStr["olives"] + " |"
        elif(self.type == 2):
                return "|  " + ingredientStr["onions"] + " |"

        return self.l1

    def line3(self):
        if(self.type == 0):
                return "|    |"
        elif(self.type == 1):
                return "|  " + ingredientStr["green_peppers"] + " |"
        elif(self.type == 2):
                return "------"

        return self.l1
        

    def name(self):
        return "toppingCounter"

class Tank(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = ">"
        self.color = Color.tank

        self.l1 = "║~~~~║"
        self.l2 = "║ >o ║"
        self.l3 = "╚════╝"

    def name(self):
        return "tank"

class Fridge(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "["
        self.color = Color.fridge

        self.l1 = "[____]"
        self.l2 = "|  . |"
        self.l3 = "|    |"

    def name(self):
        return "fridge"