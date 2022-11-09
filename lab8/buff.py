def collizionCheck(ball1, ball2):
    '''checks if there is collizion between ball1 and ball2'''
    if (ball1.getr() + ball2.getr())**2 < (ball1.getx() - ball2.getx())**2 + (ball1.gety() - ball2.gety())**2:
        return True
    return False

def display_balls(balls):
    '''draws all balls from "ball storage" balls
       balls - ball list'''
    for currBall in balls:
        circle(screen, currBall.getcolor(), (currBall.getx(), currBall.gety()), currBall.getr())

def move_balls(balls):
    '''voves balls from "ball storage" balls according to their velocities
       balls - ball list'''
    for currBall in balls:
        currBall.setx(currBall.getx() + currBall.getvx() * TIME_PERIOD)
        currBall.sety(currBall.gety() + currBall.getvy() * TIME_PERIOD)

def collizion(balls):
    '''reverses velocities for collided balls'''
    for i in range(len(balls)):
        for j in range(len(balls)):
            if (i != j):
                if collizionCheck(balls[i], balls[j]):
                    balls[i].setvx(-balls[i].getvx)
                    balls[i].setvy(-balls[i].getvy)
                    balls[j].setvx(-balls[j].getvx)
                    balls[j].setvy(-balls[j].getvy)

def bounce(balls):
    '''makes bounce if ball touches eadge of field
       balls - ball list'''
    for currBall in balls:
        if (currBall.getx() < currBall.getr()) or (currBall.getx() > SCRN_SZ_X - currBall.getr()):
            currBall.setvx(-currBall.getvx())
        if (currBall.gety() < currBall.getr()) or (currBall.gety() > SCRN_SZ_Y - currBall.getr()):
            currBall.setvy(-currBall.getvy())