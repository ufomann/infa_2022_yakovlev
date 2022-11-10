import pygame
from pygame.draw import *
from random import *
import numpy as np
pygame.init()

'''constants'''
SPD = 300
CRAZY_SPD = 10
SPD_INCREASE = 1
FPS = 30
MAXHP = 10
CRAZY_PROBABILITY = 10
CHANGE_SPD_PROB = FPS / 3
CHANGE_COLOR_PROB = 3
NULL = -1
POWER = 2
ZERO = [.0, .0]
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
SCORE_COLOR = (159, 220, 228)
WHITE = (20, 20, 20)
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

def rand_ed_vec(angmin, angmax):
    '''creates random vector with length 1. 
    Angle between vector and x axis is between angmin and angmax
    angmin and angmax must be from [0deg, +inf), angmin < angmax
    ---------> x
    |\ angle
    | 
    |  
    y  
    '''
    ang = random() * (angmax - angmin) + angmin
    ang = np.radians(ang)
    return np.array([np.cos(ang), np.sin(ang)])

class Ball:
    '''variables'''
    __MAX_R = 50
    __MIN_R = 10
    __SPD = SPD

    '''initialization'''    
    def __init__(self):
        self.__color = COLORS[randint(0, len(COLORS) - 1)]
        self.__r = randint(self.__MIN_R, self.__MAX_R)
        self.__coord = np.array([float(randint(self.__MAX_R, SCRN_SZ_X - self.__MAX_R)), 
                                float(randint(self.__MAX_R, SCRN_SZ_Y - self.__MAX_R))])
        self.__spd = np.array([random() * self.__SPD, random() * self.__SPD])
        self.__mass = self.__r**2
        self.__force = np.array([0, 0])
        self.__hitpoint = 1
        self.__score = self.__MAX_R - self.__r

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
        bounce2(balls)
        self.__coord += self.__spd * TIME_PERIOD
    
    def injure(self):
        self.__hitpoint -= 1
        if (self.__hitpoint <= 0):
            return self.__score 
        return NULL
    
    def draw(self):
        circle(screen, self.__color, self.__coord, self.__r)

class CrazyBall(Ball):
    __colorval = 0
    _Ball_SPD = CRAZY_SPD
    def __init__(self):
        super().__init__()
        self._Ball__hitpoint = randint(1, MAXHP)
        self._Ball__score = self._Ball__score * self._Ball__hitpoint

    def draw(self):
        circle(screen, self._Ball__color, self._Ball__coord, self._Ball__r)
        font = pygame.font.SysFont(None, self._Ball__r)
        img = font.render(f'{self._Ball__hitpoint}', True, WHITE)
        screen.blit(img, self._Ball__coord - np.array([self._Ball__r / 3, self._Ball__r / 3]))
    
    def move(self):
        self._Ball__spd += self._Ball__force / self._Ball__mass
        if (randint(1, CHANGE_COLOR_PROB) == CHANGE_COLOR_PROB):
            self.__colorval += 1
            self.__colorval %= len(COLORS)
            self._Ball__color = COLORS[self.__colorval]
        if randint(1, CHANGE_SPD_PROB) == CHANGE_SPD_PROB:
            self._Ball__spd = vec_len(self._Ball__spd) * rand_ed_vec(0, 360)
        bounce2(balls)
        self._Ball__coord += self._Ball__spd * TIME_PERIOD

    def injure(self):
        self._Ball__hitpoint -= 1
        self._Ball__spd *= SPD_INCREASE
        if (self._Ball__hitpoint <= 0):
            return self._Ball__score 
        return NULL

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
        a = randint(1, CRAZY_PROBABILITY)
        if (a == CRAZY_PROBABILITY):
            new_ball = CrazyBall()
        else:
            new_ball = Ball()
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
        currBall.draw()

def move_balls(balls):
    '''voves balls from "ball storage" balls according to their velocities
       balls - ball list'''
    for currBall in balls:
        currBall.move()

def bounce1(balls):

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

def bounce2(balls):
    """advanced bounce"""
    for currBall in balls:
        currCoord = currBall.get_coord()
        currSpd = currBall.get_spd()
        rad = currBall.get_rad()
        if (currCoord[0] < rad) and (currSpd[0] < 0):
            currSpd = -rand_ed_vec(90, 270) * vec_len(currSpd)
        if (currCoord[0] > (SCRN_SZ_X - rad)) and (currSpd[0] > 0):
            currSpd = rand_ed_vec(90, 270) * vec_len(currSpd)
        if (currCoord[1] < rad) and (currSpd[1] < 0):
            currSpd = rand_ed_vec(0, 180) * vec_len(currSpd)
        if (currCoord[1] > SCRN_SZ_Y - rad) and (currSpd[1] > 0):
            currSpd = -rand_ed_vec(0, 180) * vec_len(currSpd)
        currBall.set_spd(currSpd)

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

def checkClick(ball, pos):
    '''checks if dot with coords pos is inside the ball'''
    dist = vec_len(ball.get_coord() - pos)
    if (dist < ball.get_rad()):
        return True
    return False

balls = []
score = 0 

while not finished:
    clock.tick(FPS)
    fill_balls(balls)
    font = pygame.font.SysFont(None, 40)
    img = font.render(f'Score: {score}', True, SCORE_COLOR)
    screen.blit(img, (40, 40))
    display_balls(balls)
    collizion(balls)
    move_balls(balls)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 or event.button == 1:
                pos = event.pos
                for currBall in balls:
                    if (checkClick(currBall, pos)):
                        addit_score = currBall.injure()
                        if (addit_score != NULL):
                            score += addit_score
                            balls.remove(currBall)
                        break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()