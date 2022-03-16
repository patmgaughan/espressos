#applience
class DoughStation:

    def __init__(self, kitchen, row, col):
        self.kitchen = kitchen
        self.row = row
        self.col = col
        if(kitchen != None):
            self.kitchen.put(self, row, col)

    def toString(self):
        return "\033[95m=\033[00m"

    def name(self):
        return "doughStation"