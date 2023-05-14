import numpy as np


class Cell:
    def __init__(self, x, y, is_mined):
        self.x = x
        self.y = y
        self.mines_num = 0
        self.is_mined = is_mined
        self.is_shown = 0
        self.is_marked = 0

    def __str__(self):
        if self.is_marked == 1:
            return '^'
        if self.is_shown == 0:
            return '?'
        if not self.is_mined:
            return str(self.mines_num)
        else:
            return '*'

    def __repr__(self):
        if self.is_marked == 1:
            return '^'
        if self.is_shown == 0:
            return '?'
        if not self.is_mined:
            return str(self.mines_num)
        else:
            return '*'


class Field:
    def __init__(self, x_size, y_size, mines):
        # np.random.seed(1)
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
                    temp += nghb.is_mined
                self.field_arr[j][i].mines_num = temp

    def __str__(self):
        return str(self.field_arr)

    def get_nghbs(self, x, y):
        nghbs = []

        for i in range(-1, 2):
            for j in range(-1, 2):

                if i == j == 0:
                    continue

                if y + i > -1 and y + i < self.y_size and x + j > -1 and x + j < self.x_size:
                    if self.field_arr[y + i][x + j].is_shown == 0:
                        nghbs.append(self.field_arr[y + i][x + j])
        return nghbs

    def reveal(self, x, y):
        if self.field_arr[y][x].is_mined == 1:
            print('game_over')
            return
        self.field_arr[y][x].is_shown = 1
        nghbs = self.get_nghbs(x, y)
        for nghb in nghbs:
            nghb.is_shown = 1
            if nghb.mines_num == 0:
                self.reveal(nghb.x, nghb.y)


if __name__ == '__main__':
    fld = Field(9, 9, 10)
    while True:
        print(fld)
        inp = int(input())
        if inp == 0:
            break
        if inp == 1:
            xy = input().split(' ')
            fld.reveal(int(xy[0]), int(xy[1]))
        if inp == 2:
            xy = input().split(' ')
            fld.field_arr[int(xy[1])][int(xy[0])].is_marked = 1
