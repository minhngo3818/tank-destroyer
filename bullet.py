import pygame

from pygame.sprite import Sprite
from settings import Settings


class Bullet(Sprite):

    #   Without image rotation engine
    def __init__(self, b_x, b_y, direction):
        super().__init__()
        self.setting = Settings()
        self.bullet_images = {"left": pygame.image.load("Pics/bullet_left.png"),
                              "right": pygame.image.load("Pics/bullet_right.png"),
                              "up": pygame.image.load("Pics/bullet_up.png"),
                              "down": pygame.image.load("Pics/bullet_down.png")}
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

        self.keysources = {"giant": [pygame.image.load("Pics/Boss_Mega_Bullet.png"), self.setting.boss_cannon_speed],
                           "gatling": [pygame.image.load("Pics/boss_gatl_bullet.png"), self.setting.boss_gatling_speed]}

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


class Laser(Sprite):
    def __init__(self, x, y, w, h, color, direction):
        super().__init__()

        self.setting = Settings()
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.angle = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self, win):
        if self.direction == "left":
            self.angle = 90
            self.rect.x -= self.setting.boss_laser_speed
        elif self.direction == "right":
            self.angle = 270
            self.rect.x += self.setting.boss_laser_speed
        elif self.direction == "up":
            self.angle = 0
            self.rect.y -= self.setting.boss_laser_speed
        elif self.direction == "down":
            self.angle = 180
            self.rect.y += self.setting.boss_laser_speed

        if self.rect.x < 0 or self.rect.x > self.setting.scr_width \
                or self.rect.y < 0 or self.rect.y > self.setting.scr_height:
            self.kill()

        rotated_image = pygame.trasnform.rotate(self.image, self.angle)
        win.blit(rotated_image, (self.rect.x, self.rect.y))


class LaserCharge(Sprite):
    def __init__(self, x, y, color):
        super().__init__()

        self.setting = Settings()

        self.x = x
        self.y = y
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.dx = 0
        self.dy = 0
        self.speed = self.setting.boss_charge_particle_speed

    def update(self, cannon_pos_x, cannon_pos_y, win):
        self.dx = cannon_pos_x - self.x
        self.dy = cannon_pos_y - self.y

        if self.dx <= 0:
            self.rect.x += max(self.dx, -self.speed)
        elif self.dx > 0:
            self.rect.x += min(self.dx, self.speed)

        if self.dy <= 0:
            self.rect.y += max(self.dy, -self.speed)
        elif self.dy > 0:
            self.rect.y += min(self.dy, self.speed)

        win.blit(self.image, (self.rect.x, self.rect.y))
