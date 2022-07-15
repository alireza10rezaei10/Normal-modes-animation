'''
پروژه ی درس موج
استاد فرجی

درسا نجفی پناه
علیرضا رضایی
'''


import pygame
import numpy as np
from numpy import pi, sin, cos, exp


# --------------- configs -----------------------

k1, k2, k3, k4 = 1, 2, 3, 4
m = 1

# delta t
dt = 0.05

# radius of the wheel
R = 80

# radius of the balls
R_OF_BALLS = 10

COLORS = ['white', 'blue', 'red', 'green', 'yellow', 'orange']

run = True

# frame per second
FPS = 60

clock = pygame.time.Clock()

# window size
WIDTH, HEIGHT = 900, 600


# --------------- initiate window ---------------

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Wave Project')


# --------------- data --------------------------

def W(n):
    '''frequency finder of nth mode'''
    return 1/m * (k1 - 2*k2*cos(pi*n/3) - 2*k3*cos(2*pi*n/3) - ((-1)**n)*k4)


def A(n):
    return np.array([1, exp(2*pi*1j*n/6), exp(4*pi*1j*n/6),
                    exp(6*pi*1j*n/6), exp(8*pi*1j*n/6), exp(10*pi*1j*n/6)])


normal_modes = {
    1: {
        'W': W(1),
        'A': (A(1)+A(5)).real
    },
    2: {
        'W': W(2),
        'A': (A(2)+A(4)).real
    },
    3: {
        'W': W(3),
        'A': [1, -1, 1, -1, 1, -1]
    },
    4: {
        'W': W(4),
        'A': (A(2)-A(4)).imag
    },
    5: {
        'W': W(5),
        'A': (A(1)-A(5)).imag
    },
    6: {
        'W': W(6),
        'A': [1, 1, 1, 1, 1, 1]
    }
}


# --------------- balls -----------------------

class Ball:
    def __init__(self, j, phi_0):
        self.j = j
        self.phi_0 = phi_0
        self.phi = phi_0

    def draw(self, n):
        '''drawing nth normal mode of the ball'''

        if n <= 3:
            center_x = (2*n-1)*150
            center_y = 150
        else:
            center_x = (2*n-7)*150
            center_y = 450

        pygame.draw.circle(
            surface=win,
            color=COLORS[self.j],
            center=(center_x + R*cos(self.phi), center_y + R*sin(self.phi)),
            radius=R_OF_BALLS
        )


def makeBalls(number_of_balls):
    theta = 2*pi / number_of_balls
    all_balls = []

    for j in range(number_of_balls):
        all_balls.append(Ball(
            j=j,
            phi_0=j*theta
        ))

    return all_balls


balls = makeBalls(6)


# --------------- main loop ---------------------

def draw(n, t):
    '''drawing nth normal mode in time t'''

    for ball in balls:
        A = normal_modes[n]['A'][ball.j]
        W = normal_modes[n]['W']

        # dar 10 zarb mikonim ta behtar dide shavad
        ball.phi = ball.phi_0 + 10*(A/R)*cos(W*t)
        ball.draw(n)


t = 0

while run:
    win.fill('black')

    for n in range(1, 7):
        draw(n, t)

    t += dt

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
