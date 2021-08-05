import random
import copy

class Board:
    def __init__(self):
        self.board = [[" " for _ in range(10)] for _ in range(10)]
        
class ComputerBoard(Board):
    def __init__(self):
        super().__init__()
        
    def neighbour_ships_list(self, row, column): 
        return [self.board[r][c] for r in range(max(0, row-1), min(row+1, 9)+1) for c in range(max(0, column-1), min(column+1, 9)+1)]
        
    def choose_random_place(self):
        random_board_number = random.randrange(100)
        row = random_board_number//10
        column = random_board_number%10
        neighbour_ships = self.neighbour_ships_list(row, column)
    
        return row, column, neighbour_ships

    def choose_next_place(self, row, column):
        while True:
            next_row, next_column = random.choice(([row-1, column], [row+1, column], [row, column-1], [row, column+1]))
            next_neighbour_ships = self.neighbour_ships_list(next_row, next_column)
            
            if 0 <= next_row <= 9 and 0 <= next_column <= 9:
                return next_row, next_column, next_neighbour_ships
    
    def generate_board(self):
        # generate four single-masted ships
        for _ in range(4):
            while True:
                row, column, neighbour_ships = self.choose_random_place()
        
                if neighbour_ships.count("S") == 0:
                    self.board[row][column] = "S"
                    break  
            
        # generate three two-masted ships
        for _ in range(3):
            while True:
                row, column, neighbour_ships = self.choose_random_place()
            
                if neighbour_ships.count("S") == 0:
                    second_row, second_column, second_neighbour_ships = self.choose_next_place(row, column)
                
                    if second_neighbour_ships.count("S") == 0:
                        self.board[row][column] = "S"
                        self.board[second_row][second_column] = "S"
                        break 
                
        # generate two three-masted ships
        for _ in range(2):
            while True:
                row, column, neighbour_ships = self.choose_random_place()
            
                if neighbour_ships.count("S") == 0:
                    second_row, second_column, second_neighbour_ships = self.choose_next_place(row, column)
                
                    if second_neighbour_ships.count("S") == 0:
                        third_row, third_column, third_neighbour_ships = self.choose_next_place(second_row, second_column)
                    
                        if third_neighbour_ships.count("S") == 0 and (row != third_row and column != third_column):
                            self.board[row][column] = "S"
                            self.board[second_row][second_column] = "S"
                            self.board[third_row][third_column] = "S"
                            break  
    
        # generate one four-masted ships
        while True:
            row, column, neighbour_ships = self.choose_random_place()
        
            if neighbour_ships.count("S") == 0:
                second_row, second_column, second_neighbour_ships = self.choose_next_place(row, column)
            
                if second_neighbour_ships.count("S") == 0:
                    third_row, third_column, third_neighbour_ships = self.choose_next_place(second_row, second_column)
                
                    if third_neighbour_ships.count("S") == 0 and (row != third_row and column != third_column):
                        fourth_row, fourth_column, fourth_neighbour_ships = self.choose_next_place(third_row, third_column)
                    
                        if fourth_neighbour_ships.count("S") == 0 and (second_row != fourth_row and second_column != fourth_column):                    
                            self.board[row][column] = "S"
                            self.board[second_row][second_column] = "S"
                            self.board[third_row][third_column] = "S"
                            self.board[fourth_row][fourth_column] = "S"
                            break                               

        return self.board

class UserBoard(Board):
    def __init__(self):
        super().__init__()
        
    def isneighbours(self, row, col, board_to_check_copy, error_place):
        neighbours = 0
            
        for r, c in ([max(0, row-1), col], [min(row+1, 9), col], [row, max(0, col-1)], [row, min(col+1, 9)]):
            if board_to_check_copy[r][c] == "S":
                board_to_check_copy[r][c] = " "
                neighbours += 1
                next_neighbours, board_to_check_copy, error_place = self.isneighbours(r, c, board_to_check_copy, error_place)
                neighbours += next_neighbours
                
        for r, c in ([max(0, row-1), min(col+1, 9)], [min(row+1, 9), max(0, col-1)], [max(0, row-1), max(0, col-1)], [min(row+1, 9), min(col+1, 9)]):
            if board_to_check_copy[r][c] == "S":
                error_place = True
                        
        return neighbours, board_to_check_copy, error_place        
        
    def board_check(self, board_to_check):
        board_to_check_copy = copy.deepcopy(board_to_check)
        dictionary = {"1": 0, "2": 0, "3": 0, "4": 0}
        wanted_dictionary = {"1": 4, "2": 3, "3": 2, "4": 1}
        error_place = False
        
        for row in range(10):
            for col in range(10):
                if board_to_check_copy[row][col] == "S":
                    board_to_check_copy[row][col] = " "
                    num = 1
                    neighbours, board_to_check_copy, error_place = self.isneighbours(row, col, board_to_check_copy, error_place)
                    num += neighbours
                    
                    if error_place: break
                    
                    try:
                        dictionary[str(num)] += 1
                    except KeyError:
                        dictionary[str(num)] = 1
        
        if error_place: return False
        return dictionary == wanted_dictionary

