# import modules
import random
import sys
import math
import pygame
from pygame.locals import *

# definitions
GAME_RUNNING = True
SQUARE_SIZE = 30
DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_RIGHT = 3
DIRECTION_LEFT = 4
FOOD_TIMER = 10
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 43, 255)
COLOR_PINK = (255, 51, 255)
COLOR_WHITE = (255, 255, 255)

# initiates pygame
pygame.init()
pygame.font.init()

# title
pygame.display.set_caption('Snake')


# main window class
class window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.lost = False


w = window(600, 600)


# dividing the window to squares
class square:
    def __init__(self, x, y, rows, columns):
        self.x = x
        self.y = y
        self.rows = rows
        self.columns = columns
        self.can_add_more = True
        self.count = 0
        self.is_snake = False
        self.list_x = []
        self.list_y = []


s = square(0, 0, (w.height//SQUARE_SIZE), (w.width//SQUARE_SIZE))


# calls whenever the snake hit himself
def game_lost():
    w.lost = True
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render('Game Lost', True, COLOR_RED, COLOR_BLACK)
    text_rect = text.get_rect()
    text_rect.center = (w.width // 2, w.height // 2)
    w.screen.blit(text, text_rect)
    pygame.display.update()


# constantly updates the score board
def update_score_label():
    font = pygame.font.Font('freesansbold.ttf', 24)
    text_string = "Score: "+str(sn.size-1)
    text = font.render(text_string, True, COLOR_WHITE, COLOR_BLACK)
    text_rect = text.get_rect()
    text_rect.center = (w.width-70, w.height-20)
    w.screen.blit(text, text_rect)
    pygame.display.update()


# snake class
class snake:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.last_x = []
        self.last_y = []
        self.direction = direction
        self.size = 1

    # moves the snake to its given direction
    def move_snake(self, direction):
        if not w.lost:
            lost = False
            # Removing the old draws
            pygame.draw.rect(w.screen, COLOR_BLACK, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(w.screen, COLOR_WHITE, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE), 1)
            # Appending coordinates to X,Y list

            self.last_x.append(self.x)
            self.last_y.append(self.y)
            if len(self.last_x) >= self.size:
                pygame.draw.rect(w.screen, COLOR_BLACK, (self.last_x[0], self.last_y[0], SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(w.screen, COLOR_WHITE, (self.last_x[0], self.last_y[0], SQUARE_SIZE, SQUARE_SIZE), 1)
                del self.last_x[0]
                del self.last_y[0]

            # Directions
            if direction == DIRECTION_UP:
                self.y -= SQUARE_SIZE
            elif direction == DIRECTION_DOWN:
                self.y += SQUARE_SIZE
            elif direction == DIRECTION_RIGHT:
                self.x += SQUARE_SIZE
            elif direction == DIRECTION_LEFT:
                self.x -= SQUARE_SIZE

            # Drawing the snake
            pygame.draw.rect(w.screen, COLOR_RED, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))
            if sn.size > 1:
                for i in range(sn.size - 1):
                    pygame.draw.rect(w.screen, COLOR_RED, (self.last_x[i], self.last_y[i], SQUARE_SIZE, SQUARE_SIZE))
                    if self.last_y[i] == self.y and self.last_x[i] == self.x:
                        lost = True  # if hit himself

            if self.x > w.width:
                self.x = 0
            elif self.y > w.height:
                self.y = 0
            elif self.x < 0:
                self.x = w.width-SQUARE_SIZE
            elif self.y < 0:
                self.y = w.height-SQUARE_SIZE

            if lost:
                game_lost()

            print(self.last_x, self.last_y)


sn = snake((w.width//2), (w.height//2), DIRECTION_RIGHT)


class food:
    def __init__(self, timer):
        self.timer = timer
        self.x = 0
        self.y = 0
        self.created = False

    def create_food(self):
        if self.timer <= 0:
            self.timer = FOOD_TIMER
            random_food_x = random.choice(s.list_x)
            random_food_y = random.choice(s.list_y)
            if not self.created:
                self.x = random_food_x
                self.y = random_food_y
                pygame.draw.rect(w.screen, COLOR_PINK, (random_food_x, random_food_y, SQUARE_SIZE, SQUARE_SIZE))
                self.created = True
        else:
            self.timer -= 1

    def check_food(self):
        if sn.x == self.x and sn.y == self.y:
            sn.size += 1
            self.created = False


f = food(FOOD_TIMER)


def calculate_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def display_window():
    w.screen.fill((0, 0, 0))
    pygame.display.update()


def display_squares():
    s.rows = (w.height//SQUARE_SIZE)
    s.columns = (w.width//SQUARE_SIZE)
    while s.can_add_more:
        if s.count > s.rows:
            s.can_add_more = False
        else:
            for r in range(s.rows):
                s.y = (r * SQUARE_SIZE)
                for c in range(s.columns):
                    s.x = (c * SQUARE_SIZE)
                    s.list_x.append(s.x)
                    s.list_y.append(s.y)
                    pygame.draw.rect(w.screen, COLOR_WHITE, (s.x, s.y, SQUARE_SIZE, SQUARE_SIZE), 1)

            pygame.display.update()
            s.count += 1


display_window()
display_squares()

while GAME_RUNNING:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if not sn.direction == DIRECTION_RIGHT:
            sn.direction = DIRECTION_LEFT

    elif keys[pygame.K_RIGHT]:
        if not sn.direction == DIRECTION_LEFT:
            sn.direction = DIRECTION_RIGHT

    elif keys[pygame.K_UP]:
        if not sn.direction == DIRECTION_DOWN:
            sn.direction = DIRECTION_UP

    elif keys[pygame.K_DOWN]:
        if not sn.direction == DIRECTION_UP:
            sn.direction = DIRECTION_DOWN

    elif keys[pygame.K_SPACE] and w.lost:
        pygame.quit()
        sys.exit()

    update_score_label()
    f.check_food()
    f.create_food()
    sn.move_snake(sn.direction)
    pygame.display.update()