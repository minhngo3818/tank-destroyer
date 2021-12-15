import random
import sys

import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite

# Cannot copy code from another --> syntax inconsistent use of tabs and spaces in indentation
# link solve: https://stackoverflow.com/questions/5685406/inconsistent-use-of-tabs-and-spaces-in-indentation
# complete the projectile sample
"""IMPORTANCE NOTE"""


#### PLAYER MOVEMENT
# If auto movement -- create update method in player class and set the increment
# If single press movement -- set increments in keys condition inside the main loop
#### Four UDLR Shooting


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((54, 236, 255))
        self.rect = self.image.get_rect(center=(1200 / 2, 800 / 2))
        self.direction = Vector2(0, -1)


class Enemy(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill((255, 51, 255))
        self.rect = self.image.get_rect()


class Projectile(Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.pos = Vector2(pos_x, pos_y)
        self.vel = direction * 8

    def update(self):
        self.pos += self.vel  # Update speeds (*)
        self.rect.center = self.pos  # Update position (*)

        if self.rect.y < 0 and self.rect.y > 800 and self.rect.x < 0 and self.rect.x > 1200:
            self.kill()


pygame.init()
screen_w, screen_h = 1200, 800
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("projectile sample")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# Group
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

enemy_group = pygame.sprite.Group()
for i in range(10):
    enemy = Enemy()

    enemy.rect.x = random.randrange(1200)
    enemy.rect.y = random.randrange(800)

    enemy_group.add(enemy)

bullet_group = pygame.sprite.Group()

score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            player.center = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_SPACE:
                bullet = Projectile(player.rect.x + 25, player.rect.y + 25, player.direction)
                bullet_group.add(bullet)

    for bullet in bullet_group:

        # Create a collision group
        enemy_hit_group = pygame.sprite.spritecollide(bullet, enemy_group, True)

        # For each enemy hit bullet, remove bullet
        for enemy in enemy_hit_group:
            bullet_group.remove(bullet)
            score += 1
            print(score)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
        player.direction = Vector2(-1, 0)

    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
        player.direction = Vector2(1, 0)

    elif keys[pygame.K_UP]:
        player.rect.y -= 5
        player.direction = Vector2(0, -1)

    elif keys[pygame.K_DOWN]:
        player.rect.y += 5
        player.direction = Vector2(0, 1)

    screen.fill((0, 0, 0))
    bullet_group.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)
    bullet_group.update()
    pygame.display.flip()
    clock.tick(120)
