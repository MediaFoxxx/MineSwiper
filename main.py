import numpy as np


class Cell:
    def __init__(self, x, y, is_mined):
        self.x = x
        self.y = y
        self.mines_num = 0
        self.is_mined = is_mined

    def __str__(self):
        if not self.is_mined:
            return str(self.mines_num)
        else:
            return '*'

    def __repr__(self):
        if not self.is_mined:
            return str(self.mines_num)
        else:
            return '*'


class Field:
    def __init__(self, x_size, y_size, mines):
        self.x_size = x_size
        self.y_size = y_size
        self.mines_num = mines
        self.field_arr = np.zeros((x_size * y_size), dtype=int)
        for i in range(mines):
            self.field_arr[i] = 1
        np.random.shuffle(self.field_arr)
        temp = []
        for i in range(x_size * y_size):
            temp.append(Cell(i % x_size, i // x_size, self.field_arr[i]))

        self.field_arr = np.array(temp)
        self.field_arr = np.reshape(self.field_arr, (x_size, y_size))

        for i in range(x_size):
            for j in range(y_size):
                # print(i, j)
                nghbs = self.get_nghbs(i, j)
                temp = 0
                for nghb in nghbs:
                    temp += self.field_arr[nghb].is_mined
                self.field_arr[i][j].mines_num = temp

    def __str__(self):
        return str(self.field_arr)

    def get_nghbs(self, y, x):
        nghbs = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if y + i in range(0, self.y_size) and x + j in range(0, self.x_size):
                    nghbs.append((y + i, x + j))
        return nghbs


if __name__ == '__main__':
    fld = Field(6, 6, 10)
    print(fld)
    print(fld.get_nghbs(5, 5))
