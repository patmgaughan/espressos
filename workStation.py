#applience
class WorkStation:

    def __init__(self, kitchen, row, col):
        self.kitchen = kitchen
        self.row = row
        self.col = col
        self.kitchen.put(self, row, col)

    def toString(self):
        return "\033[96m#\033[00m"
        #return "\u001b[46m#\033[00m"

    def name(self):
        return "workStation"