import time
import pygame
import sys
import numpy as np
import keyword_spotting_service
import record
from tkinter import *
from tkinter import messagebox
from keyword_spotting_service import _Keyword_Spotting_Service
sys.path.append(".")

pygame.init()
COLUMNS = 3
ROWS = 3
pygame.display.set_caption('TicTacToe')
player = 1
game_over = False
# board
board = np.zeros((ROWS, COLUMNS))
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
TEAL = (28, 170, 156)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
screen.fill(TEAL)

Tk().wm_withdraw()
messagebox.showinfo('Available commands', 'Available voice commands:\n'
                                          '\n'
                                          'Left'+'       '+'-'+'       '+'move left\n'
                                          'Right'+'    '+'-'+'       '+'move right \n'
                                          'Up'+'        '+'-'+'       '+'move up\n'
                                          'Down'+'   '+'-'+'       '+'move down\n'
                                          'Go'+'        '+'-'+'       '+'mark square\n'
                                          'Stop'+'     '+'-'+'       '+'reset game')


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('rec.PNG').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print('Clicked')
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("frame_t.png").convert_alpha()
        self.rect = self.image.get_rect(center=(100, 100))

    def update(self, x, y):
        self.rect.center = (x, y)
        return self.rect


class FigureO(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.CIRCLE_RADIUS = 60
        self.CIRCLE_WIDTH = 15
        self.RED = (255, 0, 0)
        self.image = pygame.draw.circle(screen, RED, (int(col * 200 + 200 / 2), int(row * 200 + 200 / 2)), self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)


class FigureX(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        image1 = pygame.draw.line(screen, GREEN, (col * 200 + 30, row * 200 + 200 - 30),
                                  (col * 200 + 200 - 30, row * 200 + 20), 30)
        image2 = pygame.draw.line(screen, GREEN, (col * 200 + 30, row * 200 + 30),
                                  (col * 200 + 200 - 30, row * 200 + 200 - 30), 30)


def draw_lines():
    LINE_WIDTH = 15
    LINE_COLOR = (23, 145, 135)

    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)


def refresh(x, y, player):
    cursor.update(x, y)
    screen.fill(TEAL)
    draw_lines()
    cursor_group.draw(screen)
    check_win(player)


# Sprite groups
cursor = Cursor()
cursor.update(300, 300)
cursor_group = pygame.sprite.Group()
figures_group = pygame.sprite.Group()
cursor_group.add(cursor)
cursor_group.draw(screen)
draw_lines()


def draw_figures():
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 1:
                FigureO(row, col)
            elif board[row][col] == 2:
                FigureX(row, col)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    if board[row][col] == 0:
        return True
    else:
        return False


def is_board_full():
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 0:
                return False
    return True


def check_win(player):
    for col in range(COLUMNS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    for row in range(ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_ascending_diagonal(player)
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_descending_diagonal(player)
        return True
    return False


def draw_vertical_winning_line(col, player):
    pos_x = col * 200 + 100
    if player == 1:
        color = RED
    elif player == 2:
        color = GREEN
    pygame.draw.line(screen, color, (pos_x, 15), (pos_x, HEIGHT - 15), 15)
    pygame.display.flip()
    pygame.display.update()


def draw_horizontal_winning_line(row, player):
    pos_y = row * 200 + 100
    if player == 1:
        color = RED
    elif player == 2:
        color = GREEN
    pygame.draw.line(screen, color, (15, pos_y), (WIDTH - 15, pos_y), 15)
    pygame.display.flip()
    pygame.display.update()


def draw_ascending_diagonal(player):
    if player == 1:
        color = RED
    elif player == 2:
        color = GREEN
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)
    pygame.display.flip()
    pygame.display.update()


def draw_descending_diagonal(player):
    if player == 1:
        color = RED
    elif player == 2:
        color = GREEN
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)
    pygame.display.flip()
    pygame.display.update()


def restart():
    player_rect.center = (300, 300)
    screen.fill(TEAL)
    cursor = Cursor()
    cursor.update(300, 300)
    cursor_group = pygame.sprite.Group()
    cursor_group.add(cursor)
    cursor_group.draw(screen)
    draw_lines()
    player = 1
    for row in range(ROWS):
        for col in range(COLUMNS):
            board[row][col] = 0


record_button = Button(0, 0)


def voice_command(keyword):
    if keyword == 'stop':
        restart()

    elif keyword == 'left':
        player_rect.x = (player_rect.x - 100)
        if player_rect.x <= 0:
            player_rect.x = (player_rect.x + 200)
        refresh(player_rect.x+75, player_rect.y+75, player)

    elif keyword == 'right':
        player_rect.x = (player_rect.x + 100)
        if player_rect.x > 600:
            player_rect.x = (player_rect.x - 200)
        refresh(player_rect.x + 75, player_rect.y + 75, player)

    elif keyword == 'up':
        player_rect.y = (player_rect.y - 100)
        if player_rect.y < 0:
            player_rect.y = (player_rect.y + 200)
        refresh(player_rect.x+75, player_rect.y+75, player)

    elif keyword == 'down':
        player_rect.y = (player_rect.y + 100)
        if player_rect.y > 600:
            player_rect.y = (player_rect.x - 200)
        refresh(player_rect.x + 75, player_rect.y + 75, player)

    return player_rect


def left_side():
    rec = pygame.draw.rect(screen, (0, 0, 255), (0, 0, 50, 600))
    return rec


def right_side():
    rec = pygame.draw.rect(screen, (0, 0, 255), (550, 0, 50, 600))
    return rec


def fill_gradient(surface, color, gradient, rect, vertical=True, forward=True):
    if rect is None:
        rect = surface.get_rect()
    x1, x2 = rect.left, rect.right
    y1, y2 = rect.top, rect.bottom
    if vertical:
        h = y2 - y1
    else:
        h = x2 - x1
    if forward:
        a, b = color, gradient
    else:
        b, a = color, gradient
    rate = (
        float(b[0] - a[0]) / h,
        float(b[1] - a[1]) / h,
        float(b[2] - a[2]) / h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1, y2):
            color = (
                min(max(a[0] + (rate[0] * (line - y1)), 0), 255),
                min(max(a[1] + (rate[1] * (line - y1)), 0), 255),
                min(max(a[2] + (rate[2] * (line - y1)), 0), 255)
            )
            fn_line(surface, color, (x1, line), (x2, line))
    else:
        for col in range(x1, x2):
            color = (
                min(max(a[0] + (rate[0] * (col - x1)), 0), 255),
                min(max(a[1] + (rate[1] * (col - x1)), 0), 255),
                min(max(a[2] + (rate[2] * (col - x1)), 0), 255)
            )
            fn_line(surface, color, (col, y1), (col, y2))


fill_gradient(screen, RED, (28, 170, 156), left_side(), vertical=False, forward=True)
fill_gradient(screen, RED, (28, 170, 156), right_side(), vertical=False, forward=False)


image = pygame.image.load("frame_t.png").convert_alpha()
player_rect = image.get_rect(center=(300, 300))

# mainloop
while True:
    record_button.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if record_button.draw():
            record.record_word()
            kss = keyword_spotting_service.Keyword_Spotting_Service()
            keyword = kss.predict("demo.wav")
            if not game_over:
                if not keyword == 'stop' or 'go':
                    voiceX = voice_command(keyword).x
                    voiceY = voice_command(keyword).y
                    voiced_row = int(voiceY // 200)
                    voiced_col = int(voiceX // 200)
                    if player == 2:
                        fill_gradient(screen, GREEN, (28, 170, 156), left_side(), vertical=False, forward=True)
                        fill_gradient(screen, GREEN, (28, 170, 156), right_side(), vertical=False, forward=False)
                    else:
                        fill_gradient(screen, RED, (28, 170, 156), left_side(), vertical=False, forward=True)
                        fill_gradient(screen, RED, (28, 170, 156), right_side(), vertical=False, forward=False)
                if available_square(voiced_row, voiced_col):
                    if player == 1:
                        if keyword == 'go':
                            mark_square(voiced_row, voiced_col, 1)
                            check_win(player)
                            player = 2
                            fill_gradient(screen, GREEN, (28, 170, 156), left_side(), vertical=False, forward=True)
                            fill_gradient(screen, GREEN, (28, 170, 156), right_side(), vertical=False, forward=False)
                        else:
                            player = 1
                            fill_gradient(screen, RED, (28, 170, 156), left_side(), vertical=False, forward=True)
                            fill_gradient(screen, RED, (28, 170, 156), right_side(), vertical=False, forward=False)
                    elif player == 2:
                        if keyword == 'go':
                            mark_square(voiced_row, voiced_col, 2)
                            check_win(player)
                            player = 1
                            fill_gradient(screen, RED, (28, 170, 156), left_side(), vertical=False, forward=True)
                            fill_gradient(screen, RED, (28, 170, 156), right_side(), vertical=False, forward=False)
                        else:
                            player = 2
                            fill_gradient(screen, GREEN, (28, 170, 156), left_side(), vertical=False, forward=True)
                            fill_gradient(screen, GREEN, (28, 170, 156), right_side(), vertical=False, forward=False)
                draw_figures()
            elif voice_command(keyword) == 'stop':
                restart()
    pygame.display.flip()
