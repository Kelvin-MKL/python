
try:
    import pygame as py
except ImportError:
    raise ImportError("Please install pygame to run the program")

from random import randint

py.init()



class Tile:
    def __init__(self):           ## Default no bomb in tile
        self.bomb = False          ## The number of adjacent bomb
        self.label = None         ## Default is false, it will be true if it gets through the search function
        self.visible = False        ## Default not flagged
        self.marked = False


class Board():
    def __init__(self):
        self.cols = 5
        self.rows = 5
        self.num_bombs = 7
        self.level = "Easy"
        self.state = "playing"
        self.count_flag = 0
        self.width = 40
        self.grid =[ [ Tile() for n in range(self.cols)] for n in range(self.rows) ]
        self.timer = False
        ## Put bombs into tiles.
        #   It stops when it successfully assigns a bomb
        #   @var num_bombs
        self.draw_bomb()


    def draw_bomb(self):
        for n in range(self.num_bombs):
            while True:
                x = randint(0, self.cols - 1)
                y = randint(0, self.rows - 1)
                if self.grid[y][x].bomb == False:
                    self.grid[y][x].bomb = True
                    break

    ## Draw and update the board.
    #    If the state == "WON", show winning pic.

    ##   Right click triggers this function that a flag is marked on current tile (current coordinates)
    ##   If all the bombs are marked as flag, change the state to "WON"
    ##   @precondition: tile is not flagged
    def flag(self,x1, y1):
        if self.state == "playing":

            if self.boundary(x1, y1):
                flag = self.grid[y1][x1]
                if flag.visible == False:
                    if flag.marked == False :
                        flag.marked = True
                        self.count_flag += 1

                    elif flag.marked == True:

                        flag.marked = False
                        self.count_flag -= 1

                    #print(self.num_bombs, self.count_flag)
                    #global state
                    game_won = True
                    for row in self.grid:
                        for t in row:
                            if t.bomb and not t.marked:
                                game_won = False
                                break
                            if self.num_bombs != self.count_flag:
                                game_won = False
                                break

                    if game_won:
                        self.state = "WON"


    ##  Left click event triggers this function.
    ##  If current lcoation is a bomb, shows loser pic,
    ##  else run search function
    def winorlose(self,x,y):
        if self.state == "playing":
            self.timer = True
            if self.boundary(x, y):
                current = self.grid[y][x]

                if current.bomb:
                    y2 = 0
                    for row in self.grid:
                        x2 = 0
                        for i in row:
                            if i.bomb:
                                i.clicked = True
                            x2 += self.width
                        y2 += self.width

                    self.state = "Lose"
                    self.timer = False
                    return

                self.search(x,y)

    ##  open up space if no bomb at surrounding 8 tiles.
    ##  @recursion
    ##  @within boundary
    #  default visible == False, once it is visited it will do nothing on the tile.
    def search(self,x,y):
        if not self.boundary(x,y):
            return
        current = self.grid[y][x]
        if current.visible:
            return
        if current.bomb:
            return
        current.visible = True
        if current.marked == True:
            self.count_flag -= 1
        s = self.openup_num_bombs(x,y)
        current.label = s
        if s > 0 :
            return

        for (dx, dy) in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]:
            self.search(x+dx,y+dy)

    ##  Check the number of bombs around the click
    #     @return the number of bombs
    def openup_num_bombs(self,x, y):   ## 2
        s = 0
        for (dx, dy) in [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]:
            if self.boundary(y+dy, x+dx) and self.grid[y+dy][x+dx].bomb:
                s += 1
        return s

    ##  Check whether the coordinates are inbound
    #
    #    If it is inbound @return True
    def boundary(self,x, y):
        if x >= 0 and x < self.cols and y >= 0 and y < self.rows:
            return True
        return False


    def reset(self):
        self.state = "playing"
        if self.level == "Easy":
            self.cols = 5
            self.rows = 5
            self.num_bombs = 7
            self.count_flag = 0
            self.timer = False


        if self.level == "Medium":
            self.cols = 9
            self.rows = 9
            self.num_bombs = 25
            self.count_flag = 0
            self.timer = False

        if self.level == "Hard":
            self.cols = 15
            self.rows = 15
            self.num_bombs = 40
            self.count_flag = 0
            self.timer = False

        self.grid = [[Tile() for n in range(self.cols)] for n in range(self.rows)]
        (self.WIDTH, self.HEIGHT) = (self.cols * self.width, self.rows * self.width + 100)  # relates to width
        self.screen = py.display.set_mode((self.WIDTH, self.HEIGHT))

        self.draw_bomb()
