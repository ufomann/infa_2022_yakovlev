import pygame
from pygame.draw import *
from random import *
import numpy as np
pygame.init()

'''constants'''
POWER = 2
ZERO = [.0, .0]
FPS = 30
SCRN_SZ_X = 1200
SCRN_SZ_Y = 700
TIME_PERIOD = 1 / FPS
CNT_BALLS = 10
FORCE_MEASURE = 1000
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
'''constants'''

screen = pygame.display.set_mode((SCRN_SZ_X, SCRN_SZ_Y))
pygame.display.update()
clock = pygame.time.Clock()
finished = False

def vec_len(vec):
    return np.dot(vec, vec)**0.5

def sign(a):
    return a / abs(a)

class ball:
    '''variables'''
    __MAX_R = 50
    __MIN_R = 10
    __SPD = 200

    '''initialization'''    
    def __init__(self):
        self.__color = COLORS[randint(0, len(COLORS) - 1)]
        self.__r = randint(self.__MIN_R, self.__MAX_R)
        self.__coord = np.array([float(randint(self.__MAX_R, SCRN_SZ_X - self.__MAX_R)), 
                                float(randint(self.__MAX_R, SCRN_SZ_Y - self.__MAX_R))])
        self.__spd = np.array([random() * self.__SPD, random() * self.__SPD])
        self.__mass = self.__r**2
        self.__force = np.array([0, 0])

    '''getters'''
    def get_coord(self):
        return self.__coord
    def get_rad(self):
        return self.__r
    def get_color(self):
        return self.__color
    def get_spd(self):
        return self.__spd
    def get_mass(self):
        return self.__mass

    '''setters'''
    def set_coord(self, coord):
        self.__coord = coord
    def set_spd(self, spd):
        self.__spd = spd

    def move(self):
        self.__spd += self.__force / self.__mass
        bounce(balls)
        self.__coord += self.__spd * TIME_PERIOD

def radius_vector(ball1, ball2):
    '''return radius vector from ball1 to ball2
        ball1 -----> ball2'''
    return ball2.get_coord() - ball1.get_coord()

def collizionCheck(ball1, ball2):
    '''checks if there is collizion between ball1 and ball2'''
    rad_vec = radius_vector(ball1, ball2)
    dist = vec_len(rad_vec)
    if (dist > ball1.get_rad() + ball2.get_rad()):
        return False
    return True

def fill_balls(balls):
    '''creates balls, if there is no enough balls inside
       balls - ball list'''
    while (len(balls) < CNT_BALLS):
        new_ball = ball()
        flag = True
        for i in balls:
            if collizionCheck(new_ball, i):
                flag = False
        if flag:
            balls.append(new_ball)

def display_balls(balls):
    '''draws all balls from "ball storage" balls
       balls - ball list'''
    for currBall in balls:
        circle(screen, currBall.get_color(), currBall.get_coord(), currBall.get_rad())

def move_balls(balls):
    '''voves balls from "ball storage" balls according to their velocities
       balls - ball list'''
    for currBall in balls:
        currBall.move()

def bounce(balls):

    '''makes bounce if ball touches eadge of field
       balls - ball list'''
    for currBall in balls:
        spd = currBall.get_spd()
        new_spd = spd
        if (currBall.get_coord()[0] < currBall.get_rad()):
            new_spd[0] = abs(spd[0])
        if (currBall.get_coord()[0] > SCRN_SZ_X - currBall.get_rad()):
            new_spd[0] = -abs(spd[0])
        if (currBall.get_coord()[1] < currBall.get_rad()):
            new_spd[1] = abs(spd[1])
        if (currBall.get_coord()[1] > SCRN_SZ_Y - currBall.get_rad()):
            new_spd[1] = -abs(spd[1])
        currBall.set_spd(new_spd)

def center_mass_speed(ball1, ball2):
    return (ball1.get_spd() * ball1.get_mass() + ball2.get_spd() * ball2.get_mass()) / (ball1.get_mass() + ball2.get_mass())

def collizion(balls):
    '''reverses velocities for collided balls'''
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if (collizionCheck(balls[i], balls[j])):
                vcm = center_mass_speed(balls[i], balls[j])
                if (np.dot(balls[i].get_spd() - vcm, radius_vector(balls[i], balls[j])) > 0):
                    v1cm = balls[i].get_spd() - vcm
                    v2cm = balls[j].get_spd() - vcm
                    erv1 = radius_vector(balls[i], balls[j])/vec_len(radius_vector(balls[i], balls[j]))
                    erv2 = -erv1
                    v1cmt = np.dot(v1cm, erv1) * erv1
                    v1cmn = v1cm - v1cmt
                    v2cmt = np.dot(v2cm, erv2) * erv2
                    v2cmn = v2cm - v2cmt
                    balls[i].set_spd(v1cmn - v1cmt + vcm)
                    balls[j].set_spd(v2cmn - v2cmt + vcm)

balls = []

while not finished:
    clock.tick(FPS)
    fill_balls(balls)
    display_balls(balls)
    collizion(balls)
    move_balls(balls)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()