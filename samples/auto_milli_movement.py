import random
import sys

import pygame
from pygame.sprite import Sprite

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
        self.rect = self.image.get_rect(center=(800 / 2, 500 / 2))
        self.speed = 10
        self.stoptime = 100
        self.movetime = 0
        self.randomDir = random.randrange(4)

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
            self.direction = self.randomDir
            self.update()

            self.movetime += 1

    def update(self):
        if self.direction == 0:  # MOVE UP
            if self.rect.top > 0:
                self.rect.x += 0
                self.rect.y -= self.speed
        elif self.direction == 1:  # MOVE DOWN
            if self.rect.bottom < height:
                self.rect.x += 0
                self.rect.y += self.speed
        elif self.direction == 2:  # MOVE LEFT
            if self.rect.left > 0:
                self.rect.x -= self.speed
                self.rect.y += 0
        elif self.direction == 3:  # MOVE RIGHT
            if self.rect.right < width:
                self.rect.x += self.speed
                self.rect.y += 0


player = Players()
player_group = pygame.sprite.Group()
player_group.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))
    player_group.draw(screen)
    player.move_interval()
    pygame.display.flip()
    clock.tick(200)
