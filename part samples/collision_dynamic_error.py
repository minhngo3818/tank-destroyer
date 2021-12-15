import math
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
    # Automatic Movement Prototype --Succeeded
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=(800 / 2, 500 / 2))
        self.speed = 20
        self.stoptime = 200
        self.movetime = 0

    def update(self):  # upgrade to follow the player
        self.direction = random.randrange(0, 4)

        if self.stoptime == 0:
            #   UP
            if self.direction == 0 and self.rect.top > 0:
                self.rect.x += 0
                self.rect.y -= self.speed
            #   DOWN
            elif self.direction == 1 and self.rect.bottom < 560:
                self.rect.x += 0
                self.rect.y += self.speed
            #   LEFT
            elif self.direction == 2 and self.rect.left > 0:
                self.rect.x -= self.speed
                self.rect.y += 0
            #   RIGHT
            elif self.direction == 3 and self.rect.right < 800:
                self.rect.x += self.speed
                self.rect.y += 0

            self.stoptime = 200
        else:
            self.stoptime -= 1


player = Players()
player_group = pygame.sprite.Group()
player_group.add(player)


class Enemy(Sprite):
    global width, height

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 51, 255))
        self.rect = self.image.get_rect()
        self.speed = random.randrange(40, 120)
        self.move_interval = 200
        self.movetime = 20
        self.edge_location()  # Remember to define method

    def edge_location(self):
        self.edge = random.randrange(4)
        if self.edge == 0:  # Top
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = 0
        elif self.edge == 1:  # Down
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = height
        elif self.edge == 2:  # Left
            self.rect.x = 0
            self.rect.y = random.randrange(height - self.rect.height)
        elif self.edge == 3:  # Right
            self.rect.x = width
            self.rect.y = random.randrange(height - self.rect.height)

    def update(self, player):
        # Must be place in here
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist

        if self.move_interval == 0:
            self.direction = random.randrange(2)
            if self.direction == 0:
                if self.rect.x >= 0 and self.rect.x <= width:
                    self.rect.x += self.speed * dx
                    self.rect.y += 0
            elif self.direction == 1:
                if self.rect.y >= 0 and self.rect.y <= height:
                    self.rect.x += 0
                    self.rect.y += self.speed * dy

            self.move_interval = 200

        else:
            self.move_interval -= 1


class Spawn(Sprite):
    global player

    def __init__(self):
        super().__init__()
        self.enemy_group = pygame.sprite.Group()
        self.spawn_time = 120
        self.spawn_limit = 5

    def update(self):
        self.enemy_group.update(player)
        if self.spawn_time == 0:
            self.spawn_enemy()
            self.spawn_time = 120
            if len(self.enemy_group) == 0:
                self.spawn_limit += 5  # 30 is half sec, 120 is 2 secs
        else:
            self.spawn_time -= 1

    def spawn_enemy(self):
        if len(self.enemy_group) < self.spawn_limit:
            new_enemy = Enemy()
            self.enemy_group.add(new_enemy)


enemy = Spawn()

"""COLLISION"""


def collision():
    # PLAYER VS ENEMY
    for enemy_t in enemy.enemy_group:
        if pygame.sprite.collide_rect(player, enemy_t) == True:
            if player.direction == 0:
                player.rect.top = enemy_t.rect.bottom
            if player.direction == 1:
                player.rect.bottom = enemy_t.rect.top
            if player.direction == 2:
                player.rect.left = enemy_t.rect.right
            if player.direction == 3:
                player.rect.right = enemy_t.rect.left

    for enemy_s in enemy.enemy_group:
        enemy.enemy_group.remove(enemy_s)

        for enemy_d in enemy.enemy_group:
            if pygame.sprite.spritecollide(enemy_s, enemy.enemy_group, False):
                if enemy_s.direction == 0:
                    if enemy_s.rect.x < 0:
                        enemy_s.rect.left = enemy_d.rect.right
                    elif enemy_s.rect.y > 0:
                        enemy_s.rect.right = enemy_d.rect.left
                elif enemy_s.direction == 1:
                    if enemy_s.rect.y < 0:
                        enemy_s.rect.top = enemy_d.rect.bottom
                    elif enemy_s.rect.y > 0:
                        enemy_s.rect.bottom = enemy_d.rect.top

        enemy.enemy_group.add(enemy_s)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))
    enemy.update()
    player.update()
    player_group.draw(screen)
    enemy.enemy_group.draw(screen)
    collision()
    pygame.display.flip()
    clock.tick(300)
