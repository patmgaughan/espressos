#applience
class TrashCan:

    def __init__(self, kitchen, row, col):
        self.kitchen = kitchen
        self.row = row
        self.col = col
        self.kitchen.put(self, row, col)

    def toString(self):
        return "\033[93mX\033[00m"

    def name(self):
        return "trashCan"