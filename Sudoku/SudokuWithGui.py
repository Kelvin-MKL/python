import pygame as py
from random import shuffle
from random import randint

py.init()

#board = 3

class Grid():
    def __init__(self):
        self.visible = True #determine whether the grid can be seen
        self.temp_value = None


class Board():
    def __init__(self):
        self.cols = 9
        self.rows = 9
        self.grid = [[Grid() for i in range(self.cols)] for i in range(self.rows)]
        self.width = 40
        self.empty_num = 25 #missing grid
        self.state = "playing"
        self.board = self.boardGenerator()
        #print(self.board)
        self.solve(self.board)
        self.answer = self.board
        self.player_board(self.grid)


    def set_temp(self,x,y, value):
        self.grid[x][y].temp_value = value

    def player_board(self, board):
        for n in range(self.empty_num):
            while True:
                x = randint(0, len(board) - 1)
                y = randint(0, len(board[0]) - 1)
                if board[x][y].visible:
                    board[x][y].visible = False
                    break
        return board

    def boardGenerator(self):
        x = [i for i in range(1, 10)]
        shuffle(x)

        board = [
            x,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        shuffle(board)

        return board


    def valid(self, board, num, pos):
        # check row, no duplicate number in the row as just inserted
        for i in range(len(board[0])):
            if board[pos[0]][i] == num and pos[1] != i:
                # pos[1] is the column that the number is just inserted
                return False

        # check culumn
        for i in range(len(board)):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # check 3*3 grid
        # mathmatically x = col and y = row, so a bit of swapped in here
        grid_x = pos[1] // 3
        grid_y = pos[0] // 3
        for i in range(grid_y * 3, grid_y * 3 + 3):
            for j in range(grid_x * 3, grid_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def solve(self, board):
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(board, i, (row, col)):
                board[row][col] = i

                # recursive + backtracking
                if self.solve(board):
                    return True

                board[row][col] = 0
        return False

class Gui:
    def __init__(self, board):
        self.board = board
        self.cols = self.board.cols
        self.rows = self.board.rows
        self.width = self.board.width
        (self.WIDTH, self.HEIGHT) = (self.cols * self.width, self.rows * self.width)  # relates to width
        self.screen = py.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font = py.font.SysFont('arial',20)
        self.green = (0,255,0)
        self.blue = (0,0,128)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.x = None
        self.y = None
        self.key = None
        self.draw()

    def selected(self, x, y):
        if self.board.grid[y][x].visible == False:
            self.draw()
            py.draw.rect(self.screen, self.green, (x*40, y*40, 38, 38),3)
            py.display.update()
            return True

    def compare_answer(self,x, y):
        if self.board.answer[y][x] == self.board.grid[y][x].temp_value:
            self.board.grid[y][x].visible = True

        self.draw()

    def register(self, x, y, value):
        if self.board.grid[y][x].visible == False:
            self.board.grid[y][x].temp_value = value
            self.draw()
            py.draw.rect(self.screen, self.green, (x * 40, y * 40, 38, 38), 3)

            py.display.update()

    def draw(self):
        self.screen.fill(self.black)
        if self.board.state == "playing":
            y = 0
            num_y = 0
            for row in self.board.grid:
                x = 0
                num_x = 0
                for tile in row:
                    if tile.visible == True:
                        #self.screen.blit(bomb, (x, y))
                        #print(self.board.answer[num_y][num_x])
                        text = self.font.render(str(self.board.answer[num_y][num_x]),True,self.green)
                        py.draw.rect(self.screen,(210,105,30),(x,y,38,38))
                        self.screen.blit(text, (x+13,y+8))
                    elif tile.temp_value != None:
                        #print(self.board.answer[num_y][num_x])
                        text = self.font.render(str(self.board.grid[num_y][num_x].temp_value),True,(0,0,0))
                        py.draw.rect(self.screen,self.white,(x,y,38,38))
                        self.screen.blit(text, (x+13,y+8))

                    else:
                        #print("0")
                        py.draw.rect(self.screen, self.white, (x, y, 38, 38))
                    x += self.width
                    num_x += 1
                y += self.width
                num_y += 1

            py.draw.rect(self.screen,(0,0,0),(self.width*3-3,0,5,self.width*self.rows))
            py.draw.rect(self.screen,(0,0,0),(self.width*6-3,0,5,self.width*self.rows))
            py.draw.rect(self.screen,(0,0,0),(0,self.width*3-3,self.width*self.rows,5))
            py.draw.rect(self.screen,(0,0,0),(0,self.width*6-3,self.width*self.rows,5))

        py.display.update()


    def run(self):
        running = True
        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False

                if event.type == py.MOUSEBUTTONDOWN:
                    self.x = py.mouse.get_pos()[0]//self.width
                    self.y = py.mouse.get_pos()[1]//self.width
                    self.selected(self.x,self.y)
                    #print(self.x,self.y)
                    #print(self.board.answer[self.y][self.x])
                if event.type == py.KEYDOWN:
                    if event.key == py.K_1:
                        self.key = 1
                        self.register(self.x, self.y, self.key)

                    if event.key == py.K_2:
                        self.key = 2
                        self.register(self.x, self.y, self.key)
                    if event.key == py.K_3:
                        self.key = 3
                        self.register(self.x, self.y, self.key)
                    if event.key == py.K_4:
                        self.key = 4
                        self.register(self.x, self.y, self.key)
                    if event.key == py.K_5:
                        self.key = 5
                        self.register(self.x, self.y, self.key)
                    if event.key == py.K_6:
                        self.key = 6
                        self.register(self.x, self.y, self.key)
                    if event.key == py.K_7:
                        self.key = 7
                        self.register(self.x, self.y, self.key)
                    if event.key == py.K_8:
                        self.key = 8
                        self.register(self.x, self.y, self.key)
                    if event.key == py.K_9:
                        self.key = 9
                        self.register(self.x, self.y, self.key)
                    if event.key == py.K_KP_ENTER:
                        try:
                            self.compare_answer(self.x, self.y)
                        except:
                            pass

if __name__ == '__main__':
    board = Board()
    player = Gui(board)

    player.run()


