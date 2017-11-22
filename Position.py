from random import *


class Position(object):
    def __init__(self, height, width, x_perso, y_perso):
        #super(Position, self).__init__()
        self.stones = []
        self.height = height
        self.width = width
        self.empty_cells = []
        for x in range(0, self.width): # add all the cells, they are empty, stones are not generated yet
            for y in range(0, self.height):
                if (self.is_exist((x,y))):
                    self.empty_cells.append((x,y))
        self.x_perso = x
        self.y_perso = y
        self.empty_cells.remove((self.x_perso,self.y_perso)) #
