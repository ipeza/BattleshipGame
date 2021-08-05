import random

class SuperComputerUser():
    # "M" missed
    # "s" hit but not sinked
    # "S" sinked

    def __init__(self):
        self.status_board = [[" " for _ in range(10)] for _ in range(10)]
        self.hited_ship = []

    def make_move(self):
        if len(self.hited_ship) > 0:
            for i in self.hited_ship:
                r = i // 10
                c = i % 10
                allowed_places = {"1": [max(0, r-1), c], "2": [min(r+1, 9), c], "3": [r, max(0, c-1)], "4": [r, min(c+1, 9)]}
                
                while len(allowed_places) > 0:
                    place = random.choice(list(allowed_places.keys()))
                    random_r = allowed_places[place][0]
                    random_c = allowed_places[place][1]
                    del allowed_places[place]
                    if self.status_board[random_r][random_c] == " ":
                        return random_r, random_c

        while True:
            row = random.randrange(10)
            col = random.randrange(10)
            if self.status_board[row][col] == " ":
                return row, col

    def sink_hited(self, row, col):
        for r in range(max(0, row-1), min(row + 1, 9)+1):
            for c in range(max(0, col-1), min(col+1, 9)+1):
                if self.status_board[r][c] == "s":
                    self.status_board[r][c] = "S"
                    self.hited_ship.remove(r*10 + c)
                    self.sink_hited(r, c)
                elif self.status_board[r][c] == " ":
                    self.status_board[r][c] = "M"

    def update_board(self, row, col, value):
        if value == "missed":
            self.status_board[row][col] = "M"
        elif value == "hited":
            self.status_board[row][col] = "s"
            self.hited_ship.append(row*10 + col)
        elif value == "sinked":
            self.status_board[row][col] = "S"
            self.sink_hited(row, col)
