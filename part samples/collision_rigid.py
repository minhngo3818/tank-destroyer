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
        self.speed = 2
        self.direction = ''


class Enemy(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect(center=(800 // 4, 560 // 2))


player = Players()
player_group = pygame.sprite.Group()
player_group.add(player)
enemy = Enemy()
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)

"""COLLISION"""


def collision():
    if pygame.sprite.collide_rect(player, enemy) == True:
        if player.direction == "left":
            player.rect.left = enemy.rect.right
        if player.direction == "right":
            player.rect.right = enemy.rect.left
        if player.direction == "up":
            player.rect.top = enemy.rect.bottom
        if player.direction == "down":
            player.rect.bottom = enemy.rect.top


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.direction = "left"
        player.rect.x -= player.speed
    elif keys[pygame.K_RIGHT]:
        player.direction = "right"
        player.rect.x += player.speed
    elif keys[pygame.K_UP]:
        player.direction = "up"
        player.rect.y -= player.speed
    elif keys[pygame.K_DOWN]:
        player.direction = "down"
        player.rect.y += player.speed

    screen.fill((0, 0, 0))
    player.update()
    player_group.draw(screen)
    enemy_group.draw(screen)
    collision()
    pygame.display.flip()
    clock.tick(200)
