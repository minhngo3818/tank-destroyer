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


class Enemy(Sprite):
    global width

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 51, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = -self.rect.height
        self.vel_x = 0
        self.vel_y = 5

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y


class Spawn(Sprite):
    def __init__(self):
        self.enemy_group = pygame.sprite.Group()
        self.spawn_time = 120

    def update(self):
        self.enemy_group.update()
        if self.spawn_time == 0:
            self.spawn_enemy()
            self.spawn_time = 120  # 30 is half sec, 120 is 2 secs
        else:
            self.spawn_time -= 1

    def spawn_enemy(self):
        new_enemy = Enemy()
        self.enemy_group.add(new_enemy)


enemy = Spawn()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))
    enemy.update()
    enemy.enemy_group.draw(screen)
    pygame.display.flip()
    clock.tick(120)
