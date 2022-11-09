import pygame
from pygame.draw import *
from random import *
pygame.init()

FPS = 2
SCRNSZX = 1200
SCRNSZY = 900
screen = pygame.display.set_mode((SCRNSZX, SCRNSZY))

'''colors'''
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
'''colors'''

pygame.display.update()
clock = pygame.time.Clock()
finished = False

class ball:
    __RADIUSMAX = 100
    __RADIUSMIN = 10
    __x = randint(__RADIUSMAX, SCRNSZX - __RADIUSMAX)
    __y = randint(__RADIUSMAX, SCRNSZY - __RADIUSMAX)
    __r = randint(__RADIUSMIN, __RADIUSMAX)
    __vx = random() * 10
    __vy = random()
    def setvx(self, vx):
        __vx = vx
    def setvy(self, vy):
        __vy = vy
    def getvx(self):
        return self.__vx
    def getvy(sefl):
        return sefl.__vy

COUNTBALLS = 10
balls = []

while not finished:
    clock.tick(FPS)
    while (len(balls) < COUNTBALLS):
        balls.append(ball)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('click')
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()