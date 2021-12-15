import random
import sys

import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite

# INITIATE GAME BASIC ATTRIBUTES
pygame.init()
width = 800
height = 560
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Enemy")
clock = pygame.time.Clock()


class Players(Sprite):
    global witdh, height

    # Automatic Movement Prototype --Succeeded
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=(800 // 2, 500 // 2))

        # Movement Attributes
        self.speed = 5
        self.stoptime = 100
        self.movetime = 0
        self.randomDir = random.randrange(4)
        self.direction = Vector2(-1, 0)

        # Shooting Attributes
        self.bullet_group = pygame.sprite.Group()

    # upgrade to milli movement ********************
    def move_interval(self):
        if self.stoptime == 0:
            self.keep_moving()
        else:
            self.stoptime -= 1

    def keep_moving(self):
        if self.movetime == 10:
            self.movetime = 0
            self.stoptime = 100
            self.randomDir = random.randrange(4)
        elif self.movetime < 10:
            self.dirKey = self.randomDir
            self.update()

            self.movetime += 1

    def update(self):
        if self.dirKey == 0:  # MOVE UP
            if self.rect.top > 0:
                self.rect.y -= self.speed
                self.direction = Vector2(0, -1)

        elif self.dirKey == 1:  # MOVE DOWN
            if self.rect.bottom < height:
                self.rect.y += self.speed
                self.direction = Vector2(0, 1)

        elif self.dirKey == 2:  # MOVE LEFT
            if self.rect.left > 0:
                self.rect.x -= self.speed
                self.direction = Vector2(-1, 0)

        elif self.dirKey == 3:  # MOVE RIGHT
            if self.rect.right < width:
                self.rect.x += self.speed
                self.direction = Vector2(1, 0)

    def shoot(self, bullet):
        if self.stoptime == 100 / 2:
            self.bullet_group.add(bullet)


class Bullet(Sprite):
    global width, height

    def __init__(self, pos_x, pos_y, direction):
        super().__init__()
        self.width = 20
        self.height = 20
        self.radius = 10
        self.color = ((255, 0, 0))
        self.image = pygame.Surface((self.width, self.height))

        # Should divine width and height by half for centering
        pygame.draw.circle(self.image, self.color, (self.width // 2, self.height // 2), self.radius)

        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.pos = Vector2(pos_x, pos_y)
        self.vel = direction * 10

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos

        if self.rect.top < 0 and self.rect.bottom > height and self.rect.left < 0 and self.rect.right > width:
            self.kill()


# PYGAME GROUPS
player = Players()
player_group = pygame.sprite.Group()
player_group.add(player)

while True:

    # Must Initialize Bullet in while loop to create bullets continuously
    bullet_x = player.rect.x + player.rect.width // 2
    bullet_y = player.rect.y + player.rect.height // 2
    bullet = Bullet(bullet_x, bullet_y, player.direction)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))
    player.shoot(bullet)
    player.bullet_group.draw(screen)
    player.bullet_group.update()
    player.move_interval()
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(80)
