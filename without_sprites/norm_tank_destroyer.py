import sys

import pygame
from Norm.norm_tank_player import Player

background = ".\\P1_TankDestroyers\\images\\tank_field.png"
bg = pygame.image.load(background)
win = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Tank Destroyer")


class Tank:
    def __init__(self):
        self.player = Player(600, 350)


class Bullet(object):

    def __init__(self, bx, by, ver_face, hor_face):
        self.bx = bx
        self.by = by
        self.speed = 10
        self.ver_face = ver_face  # Vertical direction indicator
        self.hor_face = hor_face  # Horizontal direction indicator

    """DRAW BULLET"""

    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.bx, self.by), 4)

    """MOVE BULLET"""

    def move(self):
        if self.hor_face == -1:
            bullet.bx -= self.speed
        elif self.hor_face == 1:
            bullet.bx += self.speed
        elif self.ver_face == -1:
            bullet.by -= self.speed
        elif self.ver_face == 1:
            bullet.by += self.speed

        """do not add player position or its direction in bullet"""


pygame.init()
ver_b = ''  # set up initial indicator
hor_b = ''  # set up initial indicator
tank = Tank()
bullets = []
bullet_trigger = False
clock = pygame.time.Clock()


def reddrawWindow():
    win.blit(bg, (0, 0))
    tank.player.tank_animation(win)
    for bullet in bullets:
        bullet.draw(win)
    clock.tick(120)
    pygame.display.update()


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:  # ==>>>Add Shooting Button here: To let bullet firing separately
            if event.key == pygame.K_SPACE:
                bullet_trigger = True
                """CREATING BULLET"""
                if tank.player.up:  # Bullet direction trigger
                    ver_b = -1
                    hor_b = ''  # Must set to none value to display ver_b and hor_b dicrection
                elif tank.player.down:
                    ver_b = 1
                    hor_b = ''
                elif tank.player.left:
                    hor_b = - 1
                    ver_b = ''
                elif tank.player.right:
                    hor_b = 1
                    ver_b = ''
                elif tank.player.standing:
                    ver_b = -1
                    hor_b = ''

                if len(bullets) < 10:
                    bullet_trigger = True
                    bullets.append(Bullet(tank.player.pos_x + 33, tank.player.pos_y + 32, ver_b, hor_b))

    """DESTROY BULLET"""
    for bullet in bullets:
        if bullet.bx < 1200 and bullet.bx > 0 and bullet.by > 0 and bullet.by < 700:
            bullet.move()
        else:
            bullets.remove(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        sys.exit()

    """PLAYER MOVEMENT"""
    if keys[pygame.K_LEFT] and tank.player.pos_x > 0:
        tank.player.pos_x -= tank.player.speed
        tank.player.left = True
        tank.player.right = False
        tank.player.up = False
        tank.player.down = False
        tank.player.standing = False

    elif keys[pygame.K_RIGHT] and tank.player.pos_x < 1200 - tank.player.rect.width:
        tank.player.pos_x += tank.player.speed
        tank.player.right = True
        tank.player.left = False
        tank.player.up = False
        tank.player.down = False
        tank.player.standing = False

    elif keys[pygame.K_UP] and tank.player.pos_y > 0:
        tank.player.pos_y -= tank.player.speed
        tank.player.up = True
        tank.player.left = False
        tank.player.right = False
        tank.player.down = False
        tank.player.standing = False

    elif keys[pygame.K_DOWN] and tank.player.pos_y < 700 - tank.player.rect.height:
        tank.player.pos_y += tank.player.speed
        tank.player.down = True
        tank.player.left = False
        tank.player.up = False
        tank.player.right = False
        tank.player.standing = False

    reddrawWindow()

    ####--------------Notes for process----------------####
    # se spawn time to know when to delete a bullet
    # Attempt 1:  solve individual directions but projecttile still copy tank's movement
    """Use counting to remove projectile rather than position or find a better solution"""
    """Need to remove copy direction"""
    """Link base: < https://github.com/techwithtim/Pygame-Tutorials/blob/master/Game/Tutorial%20%235.py >"""
    """Link solve : <https://stackoverflow.com/questions/59066124/pygame-shooting-in-all-directions>"""
    """Need to practice Sprite cuz much better embed instance in a class"""
    # Attempt 2: after shooting horizontally, cannot change to vetical
    # Attempt 3: set back value of the horizontal and vertical trigger to none or 0
    # Attempt 4: a bullet appears when there is no left,right,up,down at the beginning, it can not be remove
    """Solve: set a condition whether tank is standing. If it does, no creating bullet """
