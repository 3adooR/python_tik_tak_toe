from random import randint, choice


class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0


class TicTacToe:
    FREE_CELL = 0
    HUMAN_CELL = 1
    COMPUTER_CELL = 2

    def __init__(self):
        self._size = 3
        self._win = 0  # 0 - Play / 1 - Win human / 2 - Win computer / 3 - Draw
        self.pole = tuple(tuple(Cell() for _ in range(self._size)) for _ in range(self._size))

    def __check_index(self, index):
        if type(index) not in (tuple, list) or len(index) != 2:
            raise IndexError('Not good index..')
        r, c = index
        if not (0 <= r < self._size) or not (0 <= c < self._size):
            raise IndexError('Bad index..')

    def __update_win_status(self):
        for row in self.pole:
            if all(x.value == self.HUMAN_CELL for x in row):
                self._win = 1
                return
            elif all(x.value == self.COMPUTER_CELL for x in row):
                self._win = 2
                return

        for i in range(self._size):
            if all(x.value == self.HUMAN_CELL for x in (row[i] for row in self.pole)):
                self._win = 1
                return
            elif all(x.value == self.COMPUTER_CELL for x in (row[i] for row in self.pole)):
                self._win = 2
                return

        if all(self.pole[i][i].value == self.HUMAN_CELL for i in range(self._size)) \
                or all(self.pole[i][-1 - i].value == self.HUMAN_CELL for i in range(self._size)):
            self._win = 1
            return

        if all(self.pole[i][i].value == self.COMPUTER_CELL for i in range(self._size)):
            self._win = 2
            return

        if all(x.value != self.FREE_CELL for row in self.pole for x in row):
            self._win = 3

    def __getitem__(self, item):
        self.__check_index(item)
        x, y = item
        return self.pole[x][y].value

    def __setitem__(self, key, value):
        self.__check_index(key)
        x, y = key
        self.pole[x][y].value = value
        self.__update_win_status()

    def init(self):
        for x in range(self._size):
            for y in range(self._size):
                self[x, y] = 0
        self._win = 0
        self.computer_go()

    def human_go(self, x: int, y: int):
        x -= 1
        y -= 1
        if self[x, y] == self.FREE_CELL:
            self[x, y] = self.HUMAN_CELL

    def computer_go(self):
        variants = []
        priority_x = priority_y = dict({key: 0 for key in range(self._size)})

        for x in range(self._size):
            for y in range(self._size):
                if self[x, y] == self.FREE_CELL:
                    variants.append((x, y))
                elif self[x, y] == self.COMPUTER_CELL:
                    priority_x[x] += 2
                    priority_y[y] += 2
                elif self[x, y] == self.HUMAN_CELL:
                    priority_x[x] -= 1
                    priority_y[y] -= 1

        priority_variants = []
        for variant in variants:
            x, y = variant
            if priority_x[x] > 0 or priority_y[y] > 0:
                priority_variants.append((x, y))
        if len(priority_variants) > 0:
            x, y = choice(priority_variants)
            self[x, y] = self.COMPUTER_CELL
        else:
            while True:
                x = randint(0, self._size - 1)
                y = randint(0, self._size - 1)
                if self[x, y] != self.FREE_CELL:
                    continue
                self[x, y] = self.COMPUTER_CELL
                break

    @property
    def fields(self):
        return list(self.pole)

    @property
    def is_human_win(self):
        return self._win == 1

    @property
    def is_computer_win(self):
        return self._win == 2

    @property
    def is_draw(self):
        return self._win == 3

    def __bool__(self):
        return self._win == 0


def format_print(string, symbol='*'):
    if len(string):
        string = ' ' + string + ' '
    print(string.center(50, symbol))
