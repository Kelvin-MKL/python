import pygame as py

from board import *
import time, datetime

py.display.set_caption('MineSweeper')
##easy = 5 colums 5 rows 7 bombs
## medium =  9 colums 9 rows 25 bombs
## hard = 15 colums 15 rows 40 bombs
clock = py.time.Clock()

black = (0,0,0)
red = (255,0,0)

bomb1 = py.image.load('./src/1.png')
bomb1 = py.transform.scale(bomb1, (40,40))
bomb2 = py.image.load('./src/2.png')
bomb2 = py.transform.scale(bomb2, (40,40))
bomb3 = py.image.load('./src/3.png')
bomb3 = py.transform.scale(bomb3, (40,40))
bomb4 = py.image.load('./src/4.png')
bomb4 = py.transform.scale(bomb4, (40,40))
bomb5 = py.image.load('./src/5.png')
bomb5 = py.transform.scale(bomb5, (40,40))
bomb6 = py.image.load('./src/6.png')
bomb6 = py.transform.scale(bomb6, (40,40))
bomb7 = py.image.load('./src/7.png')
bomb7 = py.transform.scale(bomb7, (40,40))
bomb8 = py.image.load('./src/8.png')
bomb8 = py.transform.scale(bomb8, (40,40))
press = py.image.load('./src/press.png')
press = py.transform.scale(press, (40,40))
bomb = py.image.load('./src/bomb.png')
bomb = py.transform.scale(bomb, (40, 40))
coverImg = py.image.load('./src/0.png')
coverImg = py.transform.scale(coverImg, (40, 40))
flagged = py.image.load('./src/flagged.png')
flagged = py.transform.scale(flagged, (40, 40))
winner = py.image.load('./src/youwin.jpg')
winner = py.transform.scale(winner, (200, 120))
loser = py.image.load('./src/youlose.jpg')
loser = py.transform.scale(loser, (140, 100))

class Gui:
    def __init__(self, board):
        self.board = board
        self.cols = self.board.cols
        self.rows = self.board.rows
        self.width = self.board.width
        (self.WIDTH, self.HEIGHT) = (self.cols * self.width, self.rows * self.width + 100)  # relates to width
        self.screen = py.display.set_mode((self.WIDTH, self.HEIGHT))  ##built in function of displaying screen
        self.counter = 0

    def run(self):

        py.time.set_timer(py.USEREVENT, 1000)


        running = True
        while running:


            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                if event.type == py.USEREVENT:
                    self.timer()


                if event.type == py.MOUSEBUTTONDOWN:
                    if py.mouse.get_pressed()[0]:
                        self.x = (py.mouse.get_pos()[0]//self.board.width)
                        self.y = (py.mouse.get_pos()[1]//self.board.width)
                        self.xx = (py.mouse.get_pos()[0])
                        self.yy = (py.mouse.get_pos()[1])
                        self.board.winorlose(self.x,self.y)
                        self.update_info()
                        self.update_board()
                        self.choose_level()

                    elif py.mouse.get_pressed()[2]:
                        self.x1 = (py.mouse.get_pos()[0] // self.board.width)
                        self.y1 = (py.mouse.get_pos()[1] // self.board.width)
                        self.board.flag(self.x1,self.y1)
                        self.update_info()
                        self.update_board()




    def choose_level(self):

        if self.board.level == "Easy":
            if self.xx > 0 and self.xx < 50 and self.yy > 205 and self.yy < 230:
                self.board.level = "Easy"
                self.board.reset()   #reset to different level
                self.infobar()   #draw infor bar
                self.draw()  #draw grid

            if self.xx > 60 and self.xx < 140 and self.yy > 205 and self.yy < 230:
                self.board.level = "Medium"
                self.board.reset()
                self.infobar()
                self.draw()

            if self.xx > 150 and self.xx < 200 and self.yy > 205 and self.yy < 230:
                self.board.level = "Hard"
                self.board.reset()
                self.infobar()
                self.draw()

        if self.board.level == "Medium":
            if self.xx > 0 and self.xx < 50 and self.yy > 365 and self.yy < 390:
                self.board.level = "Easy"
                self.board.reset()
                self.infobar()
                self.draw()

            if self.xx > 140 and self.xx < 220 and self.yy > 365 and self.yy < 390:
                self.board.level = "Medium"
                self.board.reset()
                self.infobar()
                self.draw()

            if self.xx > 310 and self.xx < 360 and self.yy > 365 and self.yy < 390:
                self.board.level = "Hard"
                self.board.reset()
                self.infobar()
                self.draw()

        if self.board.level == "Hard":
            if self.xx > 0 and self.xx < 50 and self.yy > 605 and self.yy < 630:
                self.board.level = "Easy"
                self.board.reset()
                self.infobar()
                self.draw()

            if self.xx > 260 and self.xx < 340 and self.yy > 605 and self.yy < 630:
                self.board.level = "Medium"
                self.board.reset()
                self.infobar()
                self.draw()

            if self.xx > 550 and self.xx < 600 and self.yy > 605 and self.yy < 630:
                self.board.level = "Hard"
                self.board.reset()
                self.infobar()
                self.draw()

    def draw(self):
        if self.board.state == "playing":
            y = 0
            for row in self.board.grid:
                x = 0
                for tile in row:
                    if tile.bomb == True:
                        #self.screen.blit(bomb, (x, y))
                        self.screen.blit(coverImg, (x, y))
                    else:
                        self.screen.blit(coverImg, (x, y))
                    x += self.width
                y += self.width
        py.display.update()
        if self.board.state == "WON":
            self.screen.blit(winner, (self.WIDTH / 4, self.HEIGHT / 4))
            py.display.update()

    def update_board(self):
        if self.board.state == "playing":
            y1 = 0
            for row in self.board.grid:
                x1 = 0
                for tile in row:
                    if tile.visible == True:
                        if tile.label == 1:
                            self.screen.blit(bomb1, (x1, y1))
                            py.display.update()

                        elif tile.label == 2:
                            self.screen.blit(bomb2, (x1, y1))
                            py.display.update()

                        elif tile.label == 3:
                            self.screen.blit(bomb3, (x1, y1))
                            py.display.update()

                        elif tile.label == 4:
                            self.screen.blit(bomb4, (x1, y1))
                            py.display.update()

                        elif tile.label == 5:
                            self.screen.blit(bomb5, (x1, y1))
                            py.display.update()

                        elif tile.label == 6:
                            self.screen.blit(bomb6, (x1, y1))
                            py.display.update()

                        elif tile.label == 7:
                            self.screen.blit(bomb7, (x1, y1))
                            py.display.update()

                        elif tile.label == 8:
                            self.screen.blit(bomb8, (x1, y1))
                            py.display.update()

                        elif tile.label == False:
                            self.screen.blit(press, (x1, y1))
                            py.display.update()
                    if tile.visible == False:
                        if tile.marked == False:
                            self.screen.blit(coverImg, (x1, y1))
                            py.display.update()
                        elif tile.marked == True:
                            self.screen.blit(flagged, (x1, y1))
                            py.display.update()

                    x1 += self.width
                y1 += self.width
        if self.board.state == "Lose":
            y1 = 0
            for row in self.board.grid:
                x1 = 0
                for tile in row:
                    if tile.bomb == True:
                        self.screen.blit(bomb, (x1, y1))
                        py.display.update()

                    x1 += self.width
                y1 += self.width
            self.screen.blit(loser, ((self.board.cols * self.board.width / 2) - 70, self.HEIGHT / 4))
            py.display.update()
            self.board.state = "None"

        if self.board.state =="WON":
            self.screen.blit(winner, ((self.board.cols * self.board.width / 2) - 70, self.HEIGHT / 4))
            self.update_info()
            py.display.update()

    def infobar(self):
        self.image_setup()
        py.draw.rect(self.screen, (0,0,0), (0, self.board.rows*self.width, self.board.cols*self.width, 5))
        py.draw.rect(self.screen,(180,180,180), (0, self.board.rows*self.width+5, self.board.cols*self.width, 95))

        self.screen.blit(self.text_easy, (0, self.board.rows * self.width + 5))
        self.screen.blit(self.text_medium, (self.board.cols*self.width//2 - self.text_m_x //2, self.board.rows*self.width+5))
        self.screen.blit(self.text_hard, (self.board.cols*self.width - self.text_h_x, self.board.rows*self.width+5))

        self.text_mines = self.font.render('Mines: ' + str(self.board.num_bombs - self.board.count_flag), True, black)
        self.screen.blit(self.text_mines, (0, self.board.rows * self.width + 60))
        self.text_time = self.font.render('Time: ' + str(self.counter), True, black)
        self.screen.blit(self.text_time, (self.board.cols * self.width - 100, self.board.rows * self.width + 60))
        py.display.update()

    def update_info(self):
        if self.board.state == "playing":
            self.text_mines = self.font.render('Mines: ' + str(self.board.num_bombs - self.board.count_flag), True, black)
            self.text_mine_x = self.text_mines.get_rect().width
            self.text_mine_y = self.text_mines.get_rect().height

            py.draw.rect(self.screen, (180,180,180), (0, self.board.rows*self.width+60, self.text_mine_x + 15, self.text_mine_y))
            self.screen.blit(self.text_mines, (0, self.board.rows*self.width+60))
            py.display.update()

    def image_setup(self):
        self.font = py.font.Font("HighlandGothicFLF.ttf", 20)
        self.text_easy = self.font.render('Easy', True, black)  ## + str ( cols)
        self.text_e_x = self.text_easy.get_rect().width  # create  a rect object for text surface object
        self.text_e_y = self.text_easy.get_rect().height
        self.text_medium = self.font.render('Medium', True, black)
        self.text_m_x = self.text_medium.get_rect().width
        self.text_m_y = self.text_medium.get_rect().height
        self.text_hard = self.font.render('Hard', True, black)
        self.text_h_x = self.text_hard.get_rect().width
        if self.board.level == "Easy":
            self.text_easy = self.font.render('Easy', True, red)
        elif self.board.level == "Medium":
            self.text_medium = self.font.render('Medium', True, red)
        elif self.board.level == "Hard":
            self.text_hard = self.font.render('Hard', True, red)

        py.display.flip()
        clock.tick(60)

    def timer(self):
        if self.board.timer and self.board.state == "playing":
            self.counter += 1
        elif self.board.state == "None":

           pass
        elif self.board.timer == False:

            self.counter = 0

        py.draw.rect(self.screen, (180, 180, 180),(self.board.cols * self.width - 50, self.board.rows * self.width + 60,50,30))

        self.text_time = self.font.render('Time: ' + str(self.counter), True, black)
        self.screen.blit(self.text_time, (self.board.cols * self.width - 100, self.board.rows * self.width + 60))
        py.display.update()



if __name__ == '__main__':
    board = Board()
    player = Gui(board)

    player.image_setup()
    player.draw()
    player.infobar()
    player.run()