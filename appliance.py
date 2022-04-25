from color import Color
from pizza import Pizza

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

#sorry bout tis
line1 = "|  |"
line2 = "|  |"
line3 = "|  |"

line1 = "|   |"
line2 = "| + |"
line3 = "|   |"

line1 = "  ()  "
line2 = " -[]- "
line3 = "  /\  "

# lineb1 = "------"
# lineb2 = "|    |"
# lineb3 = "------"
# lineb1 = "+----+"
# lineb2 = "|    |"
# lineb3 = "+----+"
# lineb1 = "/\\/\\/\\"
# lineb2 = "\\/\\/\\/"
# lineb3 = "/\\/\\/\\"

# lineb1 = "------"
# lineb2 = "Dough-"
# lineb3 = "------"

lineb1 = "[_____]"
lineb2 = "[   . ]"
lineb3 = "[     ]"

# linea1 = ">o >0 "
# linea2 = " >o >o"
# linea3 = ">0 >o "

# linea1 = "mmmmmm"
# linea2 = "|    |"
# linea3 = "\\____/"

# linea1 = "|~~~~|"
# linea2 = "|    |"
# linea3 = "\\____/"

# linea1 = "-****-"
# linea2 = "|oven|"
# linea3 = "|____|"

# linea1 = "(    )"
# linea2 = " )  ( "
# linea3 = "(____)"

# linea1 = "(@)(@)"
# linea2 = "      "
# linea3 = "(@)(@)"

linea1 = " \ /  "
linea2 = "  Y   "
linea3 = "  |   "

# lineb1 = " #  # "
# lineb2 = " #  # "
# lineb3 = " #  # "

def formatLine(color, line):
    return color + line + "\033[00m"

string = ""
string += formatLine(Color.chef, line1) + formatLine(Color.fun2, linea1) + formatLine(Color.fun, lineb1) + "\n"
string += formatLine(Color.chef, line2) + formatLine(Color.fun2, linea2) + formatLine(Color.fun, lineb2) + "\n"
string += formatLine(Color.chef, line3) + formatLine(Color.fun2, linea3) + formatLine(Color.fun, lineb3) + "\n"

#string = Color.chef + line1 + "\n" + line2 + "\n" + line3 + "\n" + "\033[00m"
print(string)

#string = Color.toppingCounter + linea1 + "\n" + linea2 + "\n" + linea3 + "\n" + "\033[00m"
#print(string)
#end patrick changes

class Appliance:
    def __init__(self):
        self.shape = "-"
        self.color = "\033[00m"
        self.reset = "\033[00m" 

        # lineb1 = "+----+"
        # lineb2 = "|    |"
        # lineb3 = "+----+"
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

#appliance
class WorkStation(Appliance):

    def __init__(self):
        super().__init__()
        self.shape = "#"
        self.color = Color.workStation
        self.pizza = None

        self.l1 = "+----+"
        self.l2 = "|    |"
        self.l3 = "+----+"

    #holding is always a pizza, this should be the job of a pizza!
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

        # # linea1 = "(    )"
        # # linea2 = " )  ( "
        # # linea3 = "(____)"
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

    #later this will maybe keep track of something?

class Oven(Appliance):
    def __init__(self):
        super().__init__()
        self.shape = "@"
        self.color = Color.oven

        # "-****-"
        # "|oven|"
        # "|____|"
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

        # |~~~~|
        # |    |
        # \____/
        self.l1 = "|~~~~|"
        self.l2 = "|    |"
        self.l3 = "\\____/"
        

    def name(self):
        return "trashCan"

class DoughStation(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "="
        self.color = Color.doughStation

        # self.l1 = "~~~~~~"
        # self.l2 = "|____|"
        # self.l3 = "][ ]["

    def name(self):
        return "doughStation"

class Stove(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "%"
        self.color = Color.stove

        # "(@)(@)"
        # "      "
        # "(@)(@)"
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

        # linea1 = "(    )"
        # linea2 = " )  ( "
        # linea3 = "(____)"
        self.type = type #0, 1, 2
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
#Pantry.ingredientStr["ham"]
#Pantry.ingredientStr["pineapple"]
#Pantry.ingredientStr["pepperoni"]
#Pantry.ingredientStr["olives"]
#Pantry.ingredientStr["onions"]
#Pantry.ingredientStr["green_peppers"]
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

        # ">o >0 "
        # " >o >o"
        # ">0 >o "
        # self.l1 = ">o >0 "
        # self.l2 = " >o >o"
        # self.l3 = ">0 >o "
        self.l1 = "+~~~~+"
        self.l2 = "| >o |"
        self.l3 = "|____|"

    
    def line1(self):
        return self.color + self.l1 + self.reset

    def line2(self):
        return self.color + self.l2 + self.reset

    def line3(self):
        return self.color + self.l3 + self.reset

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