import pygame
from pygame.draw import *

pygame.init()

def eyes(dist, hei, rz, r1, r2):
    pos1 = (200 - dist, 200 - hei)
    pos2 = (200 + dist, 200 - hei)
    circle(screen, red, pos1, r1)
    circle(screen, black, pos1, r1, 1)
    circle(screen, black, pos1, rz)
    circle(screen, red, pos2, r2)
    circle(screen, black, pos2, r2, 1)
    circle(screen, black, pos2, rz)

def brow(dist, hei, deltax, deltay, thkness):
    pos1st = (200 - dist, 200 - hei)
    pos1fn = (200 - dist - deltax, 200 - hei - deltay)
    pos2st = (200 + dist, 200 - hei)
    pos2fn = (200 + dist + deltax, 200 - hei - deltay)
    line(screen, black, pos1st, pos1fn, thkness)
    line(screen, black, pos2st, pos2fn, thkness)

FPS = 30
screen = pygame.display.set_mode((400, 400))

yellow = (255, 239, 7)
light_grey = (170, 170, 170)
red = (250, 0, 0)
black = (0, 0, 0)
rect(screen, light_grey, (0, 0, 400, 400))
circle(screen, yellow, (200, 200),100, 0)
circle(screen, black, (200, 200), 100, 1)
eyes(50, 30, 10, 20, 25)
brow(20, 50, 80, 40, 15)
line(screen, black, (150, 250), (250, 250), 20)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()