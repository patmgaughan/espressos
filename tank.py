#applience
#place to get anchovies
class Tank:

    def __init__(self, kitchen, row, col):
        self.kitchen = kitchen
        self.row = row
        self.col = col
        self.kitchen.put(self, row, col)

    def toString(self):
        return "\033[96m~\033[00m"

    def name(self):
        return "tank"