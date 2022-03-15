#applience
class WorkStation:

    def __init__(self, kitchen, row, col):
        self.kitchen = kitchen
        self.row = row
        self.col = col
        self.kitchen.put(self, row, col)
        self.holding = None

    def toString(self):
        if(self.holding == None):
            return "\033[93m#\033[00m"
        else:
            return "\033[94m#\033[00m"
            #return "\u001b[46m#\033[00m"

    def name(self):
        return "workStation"