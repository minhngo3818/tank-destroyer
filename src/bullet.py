import pygame
import math
import random

from pygame.sprite import Sprite
from settings import Settings


class Bullet(Sprite):

    #   Without image rotation engine
    def __init__(self, b_x, b_y, direction):
        super().__init__()
        self.setting = Settings()
        self.bullet_images = {"left": pygame.image.load("images/bullet_left.png"),
                              "right": pygame.image.load("images/bullet_right.png"),
                              "up": pygame.image.load("images/bullet_up.png"),
                              "down": pygame.image.load("images/bullet_down.png")}
        self.direction = direction
        self.image = self.bullet_images[self.direction].convert()
        self.rect = self.image.get_rect()
        self.rect.x = b_x
        self.rect.y = b_y
        self.speed = self.setting.bullet_speed  # Access Settings Files Later

    def update(self, win):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        if self.rect.x < 0 or self.rect.x > self.setting.scr_width or \
                self.rect.y < 0 or self.rect.y > self.setting.scr_height:
            self.kill()

        self.image = self.bullet_images[self.direction]
        win.blit(self.image, (self.rect.x, self.rect.y))


class BossBullet(Sprite):

    #   With Rotate Engine
    def __init__(self, g_x, g_y, bullet_type, direction):
        super().__init__()

        self.setting = Settings()

        self.keysources = {"giant": [pygame.image.load("images/Boss_Mega_Bullet.png"), self.setting.boss_cannon_speed],
                           "gatling": [pygame.image.load("images/boss_gatl_bullet.png"), self.setting.boss_gatling_speed]}

        self.bullet_type = bullet_type
        self.image = self.keysources[self.bullet_type][0]
        self.rect = self.image.get_rect()
        self.direction = direction
        self.angle = 180
        self.rect.x = g_x
        self.rect.y = g_y
        self.speed = self.keysources[self.bullet_type][1]

    def update(self, win):
        if self.direction == "left":
            self.rect.x -= self.speed
            self.angle = 90
        elif self.direction == "right":
            self.rect.x += self.speed
            self.angle = 270
        elif self.direction == "up":
            self.rect.y -= self.speed
            self.angle = 0
        elif self.direction == "down":
            self.rect.y += self.speed
            self.angle = 180

        if self.rect.x < 0 or self.rect.x > self.setting.scr_width or \
                self.rect.y < 0 or self.rect.y > self.setting.scr_height:
            self.kill()

        rotate = pygame.transform.rotate
        rotate_image = rotate(self.image, self.angle)

        win.blit(rotate_image, (self.rect.x, self.rect.y))


def render_laser(win, rotated_list):
    for rotated_laser in rotated_list:
        win.blit(rotated_laser[0], (rotated_laser[1].x, rotated_laser[1].y))


class Laser(Sprite):
    def __init__(self, x, y, w, h, direction):
        super().__init__()

        self.setting = Settings()
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.direction = direction
        self.angle = 0
        self.laser_list = []

    # Add multiple layer object
    class LaserLayer(object):
        def __init__(self, color, width, height):
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
            self.rect = self.image.get_rect()

    def create_laser(self):
        self.laser_list.append(self.LaserLayer((204, 0, 0), self.width, self.height))     # Outer
        self.laser_list.append(self.LaserLayer((255, 51, 51), self.width, self.height))     # Mid
        self.laser_list.append(self.LaserLayer((255, 204, 204), self.width, self.height))     # Inner

    def rotate_laser(self, x, y, angle):
        rotated_list = []
        for laser in self.laser_list:
            rotated_image = pygame.transform.rotate(laser.image, angle)
            rotated_rect = rotated_image.get_rect(center=laser.image.get_rect(center=(x, y)).center)
            rotated_list.append((rotated_image, rotated_rect))

        return rotated_list

    def update(self, win):
        self.create_laser()

        angle = 0

        if self.direction == "up":
            angle = 0
            self.y -= 20
        elif self.direction == "down":
            angle = 180
            self.y += 20
        elif self.direction == "left":
            angle = 90
            self.x -= 20
        elif self.direction == "right":
            angle = 270
            self.x += 20

        if (self.x <= 0 or self.x >= self.setting.scr_width
                or self.y <= 0 or self.y >= self.setting.scr_height):
            self.kill()

        rotated_list = self.rotate_laser(self.x, self.y, angle)

        for rotated_laser in rotated_list:
            win.blit(rotated_laser[0], (rotated_laser[1].x, rotated_laser[1].y))


class Particles(Sprite):
    def __init__(self, x, y, target_x, target_y, color, direction):
        Sprite.__init__(self)
        self.radius = 10
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2))
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.target_x = target_x
        self.target_y = target_y
        self.direction = direction
        self.speed = 3

    def draw_circle(self, win):
        pygame.draw.circle(win, self.color, (self.rect.x, self.rect.y), self.radius)

    # Helper functions for update() aka position update
    # Helper function: updates linear x or y for horizontal or vertical tendencies
    def _left_right_y_update(self):
        if self.rect.y < self.target_y:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed

    def _up_down_x_update(self):
        if self.rect.x < self.target_x:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    # Helper functions: different direction cases
    def _move_left(self, dx, dy):
        para_center = (self.rect.x, self.target_y)  # center(x,y) of parabolic
        self._left_right_y_update()

        self.rect.x = para_center[0] + abs(dx) * math.sqrt(
            abs(1 - ((self.rect.y - para_center[1]) / abs(dy)) ** 2))

    def _move_right(self, dx, dy):
        para_center = (self.rect.x, self.target_y)
        self._left_right_y_update()

        self.rect.x = para_center[0] - abs(dx) * math.sqrt(
            abs(1 - ((self.rect.y - para_center[1]) / abs(dy)) ** 2))

    def _move_up(self, dx, dy):
        para_center = (self.target_x, self.rect.y)
        self._up_down_x_update()

        self.rect.y = para_center[1] + abs(dy) * math.sqrt(
            abs(1 - ((self.rect.x - para_center[0]) / abs(dx)) ** 2))

    def _move_down(self, dx, dy):
        para_center = (self.target_x, self.rect.y)
        self._up_down_x_update()

        self.rect.y = para_center[1] - abs(dy) * math.sqrt(
            abs(1 - ((self.rect.x - para_center[0]) / abs(dx)) ** 2))

    # Position update function
    def update(self, win):
        dx = self.rect.x - self.target_x
        dy = self.rect.y - self.target_y

        if abs(dx) > 0 and abs(dy) > 0:
            if self.direction == 'up':
                self._move_up(dx, dy)
            elif self.direction == 'down':
                self._move_down(dx, dy)
            elif self.direction == 'left':
                self._move_left(dx, dy)
            elif self.direction == 'right':
                self._move_right(dx, dy)

        elif dx < 0 and dy == 0:
            self.rect.x += self.speed
        elif dx > 0 and dy == 0:
            self.rect.x -= self.speed
        elif dx == 0 and dy < 0:
            self.rect.y += self.speed
        elif dx == 0 and dy > 0:
            self.rect.y -= self.speed

        self.draw_circle(win)


def spawn_particles(charge_group, density, player):
    pos_x = 0
    pos_y = 0
    pos_gather_x = 0
    pos_gather_y = 0

    if player.direction == "up":
        pos_x = random.randrange(player.rect.x - 50, player.rect.x + 100)
        pos_y = random.randrange(player.rect.y - 50, player.rect.y - 10)
        (pos_gather_x, pos_gather_y) = player.rect.midtop

    elif player.direction == "down":
        pos_x = random.randrange(player.rect.x - 50, player.rect.x + 100)
        pos_y = random.randrange(player.rect.y + 50, player.rect.y + 100)
        (pos_gather_x, pos_gather_y) = player.rect.midbottom

    elif player.direction == "left":
        pos_x = random.randrange(player.rect.x - 50, player.rect.x - 10)
        pos_y = random.randrange(player.rect.y - 50, player.rect.y + 100)
        (pos_gather_x, pos_gather_y) = player.rect.midleft

    elif player.direction == "right":
        pos_x = random.randrange(player.rect.x + 50, player.rect.x + 100)
        pos_y = random.randrange(player.rect.y - 50, player.rect.y + 100)
        (pos_gather_x, pos_gather_y) = player.rect.midright

    for i in range(density):
        charge_group.add(Particles(pos_x, pos_y, pos_gather_x, pos_gather_y, (255, 0, 255), player.direction))


def remove_particles(charge_group, boss):
    for c in charge_group:
        if (pygame.sprite.collide_rect(c, boss) or (
                (boss.direction == 'up' and c.rect.y >= boss.rect.midtop[1]) or
                (boss.direction == 'down' and c.rect.y <= boss.rect.midbottom[1]) or
                (boss.direction == 'left' and c.rect.x >= boss.rect.midleft[0]) or
                (boss.direction == 'right' and c.rect.x <= boss.rect.midright[0])
        )):
            charge_group.remove(c)