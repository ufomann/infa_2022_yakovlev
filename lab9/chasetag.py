from math import *
from random import *
import numpy as np
import pygame

FPS = 60
TIME_PERIOD = 1 / FPS
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
BLACK = 0x000000
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
WIDTH = 1200
HEIGHT = 800
REDSHIPIMG = ["graphics/redship1.png", "graphics/redship2.png", "graphics/redship3.png"]
BLUESHIPIMG = ["graphics/blueship1.png", "graphics/blueship2.png", "graphics/blueship3.png"]
REDSHIPSTR = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_n, pygame.K_m]
BLUESHIPSTR = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_t, pygame.K_g]
YOUDIED = ["graphics/youdied.png"]
MAX_SPD_FOR_RED = 400
MAX_SPD_FOR_BLUE = 200
SCALE = 5
FORCE_FOR_RED = 1000
FORCE_FOR_BLUE = 600
OMEGA = 200
TIMELEFT = 60 * FPS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False

def vec_len(vec):
    return np.dot(vec, vec)**0.5

def ed_vec(angle):
    return np.array([np.cos(radians(angle)), np.sin(radians(angle))])

def bounce1(ship):
    spd = ship.get_spd()
    new_spd = spd
    touchesx = False
    touchesy = False
    if (ship.get_coord()[0] < ship.get_rad()) and spd[0] < 0:
        new_spd[0] = 0
        touchesx = True
    if (ship.get_coord()[0] > WIDTH - ship.get_rad()) and spd[0] > 0:
        new_spd[0] = 0
        touchesx = True
    if (ship.get_coord()[1] < ship.get_rad()) and spd[1] < 0:
        new_spd[1] = 0
        touchesy = True
    if (ship.get_coord()[1] > HEIGHT - ship.get_rad()) and spd[1] > 0:
        new_spd[1] = 0
        touchesy = True
    ship.set_spd(new_spd)
    ship.set_touchesx(touchesx)
    ship.set_touchesy(touchesy)

def radius_vector(ship1, ship2):
    '''return radius vector from ship1 to ship2
        ship1 -----> ship2'''
    return ship2.get_coord() - ship1.get_coord()

#DELETE THIS
cal = [0, 0]
def get_caught(ship1, ship2):
    if not cal[(currtime + 1) % 2] and collizionCheck(ship1, ship2) and not((ship1.get_path() == YOUDIED) or (ship2.get_path() == YOUDIED)):
        temp1 = ship1.get_path()
        temp2 = ship2.get_path()
        print(temp1)
        print(temp2)
        ship1.set_path(temp2)
        ship2.set_path(temp1)
#DELETE THIS

def collizionCheck(ship1, ship2):
    '''checks if there is collizion between ship1 and ship2'''
    rad_vec = radius_vector(ship1, ship2)
    dist = vec_len(rad_vec)
    if (dist > ship1.get_rad() + ship2.get_rad()):
        cal[currtime] = False
        return False
    cal[currtime] = True
    return True

def center_mass_speed(ship1, ship2):
    return (ship1.get_spd() * ship1.get_mass() + ship2.get_spd() * ship2.get_mass()) / (ship1.get_mass() + ship2.get_mass())

def collizion(ships):
    '''reverses velocities for collided ships'''
    for i in range(len(ships)):
        for j in range(i + 1, len(ships)):
            if (collizionCheck(ships[i], ships[j])):
                vcm = center_mass_speed(ships[i], ships[j])
                if (np.dot(ships[i].get_spd() - vcm, radius_vector(ships[i], ships[j])) > 0):
                    v1cm = ships[i].get_spd() - vcm
                    v2cm = ships[j].get_spd() - vcm
                    erv1 = radius_vector(ships[i], ships[j])/vec_len(radius_vector(ships[i], ships[j]))
                    erv2 = -erv1
                    v1cmt = np.dot(v1cm, erv1) * erv1
                    v1cmn = v1cm - v1cmt
                    v2cmt = np.dot(v2cm, erv2) * erv2
                    v2cmn = v2cm - v2cmt
                    vcmt = (v1cmt + v2cmt) / 2
                    v1 = v1cmn + vcmt + vcm
                    v2 = v2cmn + vcmt + vcm
                    if (ships[i].get_touchesx() or ships[j].get_touchesx()):
                        v1[0] = v2[0] = 0
                    if (ships[i].get_touchesy() or ships[j].get_touchesy()):
                        v1[1] = v2[1] = 0
                    ships[i].set_spd(v1)
                    ships[j].set_spd(v2)

class Steering:
    def __init__(self, buttons):
        self.up = buttons[0]
        self.down = buttons[1]
        self.left = buttons[2]
        self.right = buttons[3]
        self.shoot = buttons[4]
        self.ulta = buttons[5]

class Image:
    def __init__(self, path):
        self.__image = pygame.image.load(path).convert_alpha()
        self.__SIZE = np.array([self.__image.get_width(), self.__image.get_height()])

    def draw(self, angle, coords, scale):
        temp = pygame.transform.scale(self.__image, self.__SIZE * scale)
        temp = pygame.transform.rotate(temp, angle)
        screen.blit(temp, (coords[0] -temp.get_width() // 2, coords[1] -temp.get_height() // 2))
    
    def get_image(self):
        return self.__image

class Ship:
    def __init__(self, coords, paths, steering):
        self.__paths = paths
        self.__coords = np.array(coords, dtype=float)
        self.__angle = 0
        self.__spd = 0
        self.__MASS = 1
        self.__force = ed_vec(0) * 0
        self.__steer = Steering(steering)
        self.__spd = np.array([0, 0], dtype=float)
        self.__image = Image(self.__paths[0])
        self.__heatrad = 0
        self.__touchesx = False
        self.__touchesy = False
        self.__timeleft = TIMELEFT

    def __normSpd(self):
        if (self.__paths[0] == "graphics/redship1.png"):
            MAX_SPD = MAX_SPD_FOR_RED
        else:
            MAX_SPD = MAX_SPD_FOR_BLUE
        if (vec_len(self.__spd) >=  MAX_SPD):
            self.__spd = self.__spd / vec_len(self.__spd) * MAX_SPD 

    def changespd(self):
        if (self.__paths[0] == "graphics/redship1.png"):
            FORCE = FORCE_FOR_RED
        else:
            FORCE = FORCE_FOR_BLUE
        keystatus = pygame.key.get_pressed()
        if keystatus[self.__steer.left]:
            self.__angle -= OMEGA * TIME_PERIOD
        if keystatus[self.__steer.right]:
            self.__angle += OMEGA * TIME_PERIOD
        self.__force = ed_vec(self.__angle) * FORCE
        self.__spd += self.__force / self.__MASS * TIME_PERIOD
        self.__normSpd()

    def move(self, scale):
        self.__image = Image(self.__paths[0])
        if (self.__paths[0] == "graphics/redship1.png"):
            self.__timeleft -= 1
        if (self.__timeleft < 0):
            self.set_path(YOUDIED)
        self.__coords += self.__spd * TIME_PERIOD
        self.__heatrad = self.__image.get_image().get_width() // 2 * scale * 1
        self.__image.draw(-self.__angle - 90, self.__coords, scale)

    def get_spd(self):
        return self.__spd
    
    def get_coord(self):
        return self.__coords
    
    def get_rad(self):
        return self.__heatrad
    
    def set_spd(self, spd):
        self.__spd = spd

    def get_mass(self):
        return self.__MASS

    def get_touchesx(self):
        return self.__touchesx

    def get_touchesy(self):
        return self.__touchesy

    def set_touchesx(self, touchesx):
        self.__touchesx = touchesx
    
    def set_touchesy(self, touchesy):
        self.__touchesy = touchesy

    def set_path(self, path):
        self.__paths = path
    
    def get_path(self):
        return self.__paths

    def get_timeleft(self):
        return self.__timeleft

redship = Ship([200, 200], REDSHIPIMG, REDSHIPSTR)
blueship = Ship([200, 200], BLUESHIPIMG, BLUESHIPSTR)
ships = [redship, blueship]

currtime = 0
while not finished:
    get_caught(ships[1], ships[0])
    font1 = pygame.font.SysFont(None, 40)
    font2 = pygame.font.SysFont(None, 40)
    img1 = font1.render(str(round(ships[0].get_timeleft() /FPS, 1)), True, (255, 0, 0))
    img2 = font2.render(str(round(ships[1].get_timeleft()/FPS, 1)), True, (0, 0, 255))
    screen.blit(img1, (WIDTH - 100, 40))
    screen.blit(img2, (40, 40))
    currtime += 1
    currtime %= 2
    for i in ships:
        i.changespd()
    for i in ships:
        bounce1(i)
    collizion(ships)
    for i in ships:
        i.move(SCALE)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
