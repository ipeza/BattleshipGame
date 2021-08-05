import tkinter as tk
from InsideBoards import ComputerBoard, UserBoard
from SuperComputerUser import SuperComputerUser
import Rules
import random
import time
import copy

def create_root(size):
    root3 = tk.Tk()
    root3.geometry(size)
    root3.title("BattleshipGame")
    
    return root3

def create_info_label(col, text):
    label = tk.Label(root3, bg = "blue", fg = "white", font = (5))
    label.grid(row = 0, column = col, columnspan = 10, ipadx = 10, pady = 10)
    label["text"] = text
    
    return label

def create_status_panel(col):
    status_panel = tk.Label(root3, bg = "gray", fg = "white", font = (2))
    status_panel.grid(row = 1, column = col, columnspan = 10, ipadx = 2, pady = 2)
    
    return status_panel

def create_top_panel():
    user_label = create_info_label(1, "Your Ships")
    opponents_label = create_info_label(12, "Opponents Battleships")
    global status_panel_left
    status_panel_left = create_status_panel(1)
    global status_panel_right
    status_panel_right = create_status_panel(12)
    
    top_panel = [opponents_label, user_label, status_panel_left, status_panel_right]
    return top_panel

def create_number(current_root, start_row, start_column):
    board_top_number = [tk.Label(current_root) for _ in range(10)]
    board_side_number = [tk.Label(current_root) for _ in range(10)]
    alphabet = "ABCDEFGHIJ"
    
    for col in range(10):
        board_top_number[col].grid(row = start_row, column = col + 1 + start_column)
        board_top_number[col]["text"] = alphabet[col]
        
    for row in range(10):
        board_side_number[row].grid(row = row + start_row + 1, column = 0 + start_column)
        board_side_number[row]["text"] = row + 1
        
    return [board_top_number, board_side_number]

def create_one_board(current_root, start_row, start_column):
    one_board = [tk.Button(current_root) for _ in range(100)]
    for row in range(10):
        for col in range(10):
            one_board[row*10 + col].grid(row = row + 1 + start_row, column = col + 1 + start_column)
            one_board[row*10 + col]["width"] = 2
            
    return one_board

def create_boards():
    numbers = create_number(root3, 2, 0) + create_number(root3, 2, 11)
    
    global user_board
    user_board = create_one_board(root3, 2, 0)
    for row in range(10):
        for col in range(10):    
            user_board[row*10 + col].configure(state = tk.DISABLED, border = 2, highlightcolor = "black")
            if inside_user_board.board[row][col] == " ":
                user_board[row*10 + col]["bg"] = "blue"
            else:
                user_board[row*10 + col]["bg"] = "orange"    
    
    global opponent_board
    opponent_board = create_one_board(root3, 2, 11)
    for row in range(10):
        for col in range(10):
            opponent_board[row*10 + col].bind("<Button-1>", lambda event, b = opponent_board[row*10 + col], inside_date = inside_opponents_board.board[row][col], x = row*10 + col: left_click(b, inside_date, x))    
    
    boards = [numbers, user_board, opponent_board]
    return boards
    
def isneighbours(x, checking_board):
    row = x // 10
    col = x % 10
    neighbours = 0
    
    for r in range(max(0, row-1), min(row+1, 9) + 1):
        for c in range(max(0, col-1), min(col+1, 9) + 1):
            if checking_board[r][c] == "S":
                neighbours += 1
                checking_board[r][c] = " "
            elif checking_board[r][c] == "H":
                checking_board[r][c] = " "
                neighbours += isneighbours(r*10 + c, checking_board)
                
    return neighbours

def left_click(button, inside_date, x):
    global opponent_ship
    global user_move
    
    if user_move:
        button.unbind("<Button-1>")
        if inside_date == "S":
            opponent_ship -= 1
            button["bg"] = "red"
            inside_opponents_board.board[x//10][x%10] = "H"
            temp_board = copy.deepcopy(inside_opponents_board.board)
        
            if opponent_ship <= 0:
                status_panel_right["text"] = "HIT, YOU WIN!"
                game_end()
            elif isneighbours(x, temp_board) > 0: 
                status_panel_right["text"] = "HIT! BUT NOT SUNK"
            else:
                status_panel_right["text"] = "HIT AND SUNK!"
            
        elif inside_date == " ": 
            button["bg"] = "blue"
            status_panel_right["text"] = "MISS"
            user_move = False
            
    button.configure(state = tk.DISABLED, border = 2, highlightbackground = "black") 
    
def computer_turn():
    global user_move
    global user_ship
    
    if not user_move:
        time.sleep(1)
        row, column = computer_user.make_move()
        x = row*10 + column
                
        if user_board[x]["bg"] == "orange":
            user_board[x]["bg"] = "black"
            inside_user_board.board[x//10][x%10] = "H"
            user_ship -= 1
            temp_board = copy.deepcopy(inside_user_board.board)
            
            if user_ship <= 0:
                status_panel_left["text"] = "HIT, COMPUTER WINS!"
                game_end()
            elif isneighbours(x, temp_board) > 0: 
                status_panel_left["text"] = "HIT! BUT NOT SUNK"
                computer_user.update_board(x//10, x%10, "hited")
            else: 
                status_panel_left["text"] = "HIT AND SUNK!"
                computer_user.update_board(x//10, x%10, "sinked")
                    
        else:
            user_board[x]["bg"] = "black"
            status_panel_left["text"] = "MISS"
            computer_user.update_board(x//10, x%10, "missed")
            user_move = True
    
    root3.after(1000, computer_turn)

def game_end():
    user_move = False
    for i in range (100):
        if isinstance(opponent_board[i], tk.Button) and opponent_board[i]["state"] != tk.DISABLED:
            opponent_board[i].configure(state = tk.DISABLED, border = 2, highlightbackground = "black")
            opponent_board[i].unbind("<Button-1>")
            
    play_again()

def play_again():
    def yes():
        root4.destroy()
        root3.destroy()        
        input_date()
    
    def no():
        root4.destroy()
        root3.destroy()
    
    root4 = create_root("485x200")
    for row in range(7):
        root4.grid_rowconfigure(row, weight=1)
    for col in range(3):
        root4.grid_columnconfigure(col, weight=1)
    
    label = tk.Label(root4, fg = "black", font = (5), text = "Do you want to continue?")
    label.grid(row = 2, column = 1)
    button_yes = tk.Button(root4, bg = "green", fg = "white", font = (5), text = "Yes", command = lambda : yes())
    button_yes.grid(row = 4, column = 0, ipadx = 20) 
    button_no = tk.Button(root4, bg = "grey", fg = "white", font = (5), text = "No", command = lambda : no())
    button_no.grid(row = 4, column = 2, ipadx = 20)     
    
    root4.mainloop()      
    
def play():
    global inside_opponents_board 
    inside_opponents_board = ComputerBoard()
    inside_opponents_board.generate_board()
    
    global opponent_ship
    opponent_ship = 20
    global user_ship
    user_ship = 20
    global user_move
    user_move = random.choice([True, False])
    global computer_user
    computer_user = SuperComputerUser()
    
    global root3
    root3 = create_root("525x370")
    create_top_panel()
    create_boards()
    
    if user_move:
        status_panel_left["text"] = "Computer's waiting"
        status_panel_right["text"] = "User's starting"
    else:
        status_panel_left["text"] = "Computer started"
        status_panel_right["text"] = "User's turn"    
    
    computer_turn()

    root3.mainloop()  

def input_click(r, c, b, original_color):
    if b["bg"] == original_color:
        b["bg"] = "orange"
        inside_user_board.board[r][c] = "S"
    elif b["bg"] == "orange":
        b["bg"] = original_color
        inside_user_board.board[r][c] = " "        

def input_date():  
    root2 = create_root("265x380")
    original_color = root2.cget("background")
    
    label = tk.Label(root2, bg = "blue", fg = "white", font = (5), text = "Create your own board")
    label.grid(row = 0, column = 1, columnspan = 10, ipadx = 20, pady = 10)
    
    numbers = create_number(root2, 1, 0)
    global input_board
    input_board = create_one_board(root2, 1, 0)
    global inside_user_board
    inside_user_board = UserBoard()
    for row in range(10):
        for col in range(10):
            input_board[row*10 + col].bind("<Button-1>", lambda event, r = row, c = col, b = input_board[row*10 + col], oc = original_color: input_click(r, c, b, oc))    
    
    def start_game_2():
        root2.destroy()
        if inside_user_board.board_check(inside_user_board.board):
            play()
        else: 
            text_root("485x175", Rules.rules_ships, "Create board")
    
    button = tk.Button(root2, bg = "green", fg = "white", font = (5), text = "Save board", command = lambda : start_game_2())
    button.grid(row = 12, column = 1, columnspan = 10, ipadx = 20, pady = 10)
    
    root2.mainloop()

def text_root(size, text, button_text):
    def start_game():
        root1.destroy()
        input_date()
    
    root1 = create_root(size)
    root1.grid_columnconfigure(0, weight=1)
    
    rules = tk.Label(root1, padx = 40, pady = 10, wraplength = 450, justify = tk.CENTER)
    rules["text"] = text
    rules.grid(row = 0, column = 0)
    
    button = tk.Button(root1, bg = "green", fg = "white", font = (5), text = button_text, command = lambda : start_game())
    button.grid(row = 1, column = 0, ipadx = 40, pady = 10)
    
    root1.mainloop()

def battleship_game():
    text_root("485x280", Rules.rules, "Start Game!")
    
if __name__ == "__main__":
    battleship_game()   
      