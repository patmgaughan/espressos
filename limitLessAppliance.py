# This is where all of our limitless apliances will live

class Appliance:
    def __init__(self):
        self.shape = "-"
        self.color = "\033[00m"
        self.reset = "\033[00m"

    def toString(self):
        return self.color + self.shape + self.reset

#just to help classify objects
class limitLessAppliance(Appliance):
    def __init__(self):
        super().__init__()

class TrashCan(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "X"
        self.color = "\033[93m"

    def name(self):
        return "trashCan"

class DoughStation(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "="
        self.color = "\033[95m"

    def name(self):
        return "doughStation"

class Stove(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "%"
        self.color = "\033[91m"

    def name(self):
        return "stove"

class ToppingCounter(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = "!"
        self.color = "\u001b[42m"

    def name(self):
        return "toppingCounter"

class Tank(limitLessAppliance):
    def __init__(self):
        super().__init__()
        self.shape = ">"
        self.color = "\033[96m"

    def setShape(self, shape):
        self.shape = shape

    def name(self):
        return "tank"

class Fridge(limitLessAppliance):

    def __init__(self):
        super().__init__()
        self.shape = "["
        self.color = "\033[34m"

    def name(self):
        return "fridge"