from random import shuffle
from random import randint

originalBoard = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]
empty_num = 40

def boardGenerator():
    x = [i for i in range(1,10)]
    shuffle(x)

    board = [
    x,
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
    ]

    shuffle(board)

    return board

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- " * (len(board[0]) + len(board[0]) // 3))
        for j in range(len(board[0])): # Length of each row
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == len(board[0])-1: # 8
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            #recursive + backtracking
            if solve(board):
                return True

            board[row][col] = 0
    return False

def valid(board, num, pos):
    #check row, no duplicate number in the row as just inserted
    for i in range(len(board[0])):
        if board[pos[0]][i]  == num and pos[1] != i:
            #pos[1] is the column that the number is just inserted
            return False

    #check culumn
    for i in range(len(board)):
        if board[i][pos[1]]  == num and pos[0] != i:
            return False

    #check 3*3 grid
    #mathmatically x = col and y = row, so a bit of swapped in here
    grid_x = pos[1] // 3
    grid_y = pos[0] // 3
    for i in range(grid_y*3, grid_y*3 + 3 ):
        for j in range(grid_x*3, grid_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j) # row, col
    return None


def player_board(board):
    for n in range(empty_num):
        while True:
            x = randint(0, len(board)- 1)
            y = randint(0, len(board[0]) - 1)
            if board[x][y]:
                board[x][y] = 0
                break
    return board


board = boardGenerator()
print_board(board)
print("                   ")
solve(board)
player_board(board)
print_board(board)

