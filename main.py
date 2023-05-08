import numpy as np


class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mines_num = 0
        self.is_mined = 0

    def __str__(self):
        return str(self.is_mined)


class Field():
    def init(self, x_size, y_size, mines):
        self.x_size = x_size
        self.y_size = y_size
        self.mines_num = mines
        self.field_arr = [Cell(i % self.x_size, i // self.x_size) for i in range(self.x_size * self.y_size)]
        for i in range(mines):
            self.field_arr[i].is_mined = 1

    def str(self):
        return self.field_arr

# n = m = 20
# mines_num = 50
# field = np.zeros((n * m), dtype = str)
# for i in range(mines_num):
#   field[i] = '*'
# np.random.shuffle(field)
# field = field.reshape(n, m)
# for i in range(n):
#   for j in range(m):


if __name__ == '__main__':
    fld = Field(20, 30, 100)
    print(fld)
    132
