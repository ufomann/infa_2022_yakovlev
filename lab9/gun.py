import math
from random import *
import numpy as np

import pygame

TIME_UNTIL_DYING = 30
FPS = 60
TARGETTING_TIME = 100
DUMPING = 0.5
POWER = 30
GUN_LEN = 200
GRAVITY = 3000
TIME_PERIOD = 1 / FPS
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1200
HEIGHT = 800

def equal_arr(arr1, arr2):
    '''True, если arr1 == arr2'''
    flag = True
    for i in range(len(arr1)):
        if (arr1[i] != arr2[i]):
            flag = False
            break
    return flag

def create_vec(ang):
    return np.array([np.cos(ang), np.sin(ang)])

def vec_len(vec):
    return np.dot(vec, vec) ** 0.5

def bounce1(currBall):

    '''Моделирование отскока'''
    
    spd = currBall.get_spd()
    new_spd = np.copy(spd)
    if (currBall.get_coords()[0] < currBall.get_rad()):
            new_spd[0] = abs(spd[0])
    if (currBall.get_coords()[0] > WIDTH- currBall.get_rad()):
            new_spd[0] = -abs(spd[0])
    if (currBall.get_coords()[1] < currBall.get_rad()):
            new_spd[1] = abs(spd[1])
    if (currBall.get_coords()[1] > HEIGHT - currBall.get_rad()):
            new_spd[1] = -abs(spd[1])
    if (not equal_arr(new_spd, spd)):
        new_spd *= DUMPING
        if (vec_len(new_spd) < GRAVITY * TIME_PERIOD * 3):
            new_spd = np.array([0., 0.])
    currBall.set_spd(new_spd)

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.__screen = screen
        self.__coords = np.array([x, y], dtype=float)
        self.__r = 10
        self.__spd = np.array([0., 0.])
        self.__color = choice(GAME_COLORS)
        self.__live = -1
        self.__dead = False

    '''getters'''
    def get_scrn(self):
        return self.__screen

    def get_coords(self):
        return self.__coords

    def get_color(self):
        return self.__color

    def get_rad(self):
        return self.__r

    def get_spd(self):
        return self.__spd

    '''setters'''
    def set_spd(self, spd):
        self.__spd = spd

    def set_rad(self, r):
        self.__r = r
    
    def set_coords(self, coords):
        self.__coords = coords

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.coord с учетом скоростей self.spd, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна WIDHTxHEIGHT).
        """
        self.__spd[1] += GRAVITY * TIME_PERIOD
        bounce1(self)
        if (vec_len(self.__spd) == 0 and not self.__dead):
                self.__live = TIME_UNTIL_DYING
                self.__dead = True
        self.__coords += self.__spd * TIME_PERIOD

    def draw(self):
        pygame.draw.circle(
            self.__screen,
            self.__color,
            self.__coords,
            self.__r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        dist = vec_len(obj.get_coords() - self.__coords)
        if (dist < obj.get_rad() + self.__r):
            return True
        return False

    def death(self):
        if self.__live == -1:
            return False
        self.__live -= 1
        if self.__live <= 0:
            return True
        return False

class Gun:
    def __init__(self, screen):
        self.__screen = screen
        self.__f2_power = 10
        self.__f2_on = 0
        self.__ang = 1
        self.__color = GREY
        self.__coords = np.array([10, HEIGHT / 2])

    def fire2_start(self, event):
        self.__f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.__screen)
        new_ball.set_rad(new_ball.get_rad() + 5)
        self.__ang = math.atan2((event.pos[1]-self.__coords[1]), (event.pos[0]-self.__coords[0]))
        new_ball.set_spd(np.array([self.__f2_power * math.cos(self.__ang), self.__f2_power * math.sin(self.__ang)]))
        new_ball.set_coords(np.copy(self.__coords))
        balls.append(new_ball)
        self.__f2_on = 0
        self.__f2_power = 0.1 * TARGETTING_TIME * POWER

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.__ang = math.atan((event.pos[1] - self.__coords[1]) / (event.pos[0] - self.__coords[0]))
        if self.__f2_on:
            self.__color = RED
        else:
            self.__color = GREY

    def draw(self):
        pygame.draw.line(screen, self.__color, self.__coords, self.__coords + create_vec(self.__ang) * self.__f2_power / (TARGETTING_TIME * POWER) * GUN_LEN, 20)

    def power_up(self):
        if self.__f2_on:
            if self.__f2_power < TARGETTING_TIME * POWER:
                self.__f2_power += POWER
            self.__color = RED
        else:
            self.__color = GREY

class Target:

    def __init__(self):
        self.__points = 0
        self.__live = 1
        self.__color = GAME_COLORS[randint(1, len(GAME_COLORS) - 1)]
        self.__coords = np.array([randint(WIDTH - 300, WIDTH), randint(0, HEIGHT)])
        self.__r = 100


    '''setters'''
    def set_live(self, live):
        self.__live = live

    '''getters'''
    def get_rad(self):
        return self.__r

    def get_coords(self):
        return self.__coords

    def get_live(self):
        return self.__live
    
    def get_points(self):
        return self.__points

    def new_target(self):
        """ Инициализация новой цели. """
        self.__coords = np.array([randint(WIDTH - 300, WIDTH), randint(0, HEIGHT)])
        self.__r = randint(2, 50)
        self.__color = GAME_COLORS[randint(1, len(GAME_COLORS) - 1)]
        self.__live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.__points += points

    def draw(self):
        pygame.draw.circle(screen, self.__color, self.__coords, self.__r)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.death():
            balls.remove(b)
        if b.hittest(target) and target.get_live():
            target.set_live(0)
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
