"""Projectile Parabolic Motion Testing

@author Minh Ngo
@date 12/26/2021
@version 3
@file parabola_motion_allDir.py

Description:

"""
import pygame
from pygame.sprite import Sprite
import math
import random

# Stats

# Screen stats
scr_height = 500
scr_width = 800


class Square(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.cube = pygame.Surface((50, 50))
        self.cube.fill((0, 255, 255))
        self.rect = self.cube.get_rect()
        self.direction = 'left'

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def update(self):
        if self.up and self.rect.y >= 0:
            self.direction = 'up'
            self.rect.y -= 5
        elif self.down and self.rect.y <= self.screen_rect.height:
            self.direction = 'down'
            self.rect.y += 5
        elif self.left and self.rect.x >= 0:
            self.direction = 'left'
            self.rect.x -= 5
        elif self.right and self.rect.x <= self.screen_rect.width:
            self.direction = 'right'
            self.rect.x += 5

        self.screen.blit(self.cube, (self.rect.x, self.rect.y))


class Ball(Sprite):
    def __init__(self, x, y, color):
        Sprite.__init__(self)
        self.radius = 10
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2))
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.resetX = x
        self.resetY = y
        self.color = color

    def reset_position(self):
        self.rect.x = self.resetX
        self.rect.y = self.resetY

    def draw_circle(self, win):
        pygame.draw.circle(win, self.color, (self.rect.x, self.rect.y), self.radius)


class ParaBall(Ball):

    def __init__(self, win, x, y, target_x, target_y, color, direction):
        super().__init__(x, y, color)
        self.target_x = target_x
        self.target_y = target_y
        self.direction = direction
        self.screen = win
        self.speed = 3

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
    def update(self):
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

        self.draw_circle(self.screen)


def spawn_particles(win, charge_group, density, player):
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
        charge_group.add(ParaBall(win, pos_x, pos_y, pos_gather_x, pos_gather_y, (255, 0, 255), player.direction))


# Main function
def main():
    # Game Display
    pygame.init()
    win = pygame.display.set_mode((scr_width, scr_height))
    pygame.display.set_caption('Parabola Motion')

    # Game FPS
    clock = pygame.time.Clock()
    fps = 60

    # Initialize list of ball
    player = Square(win)
    charge_group = pygame.sprite.Group()
    density = 10

    # Initialize stats
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left = True
                elif event.key == pygame.K_RIGHT:
                    player.right = True
                elif event.key == pygame.K_UP:
                    player.up = True
                elif event.key == pygame.K_DOWN:
                    player.down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.left = False
                elif event.key == pygame.K_RIGHT:
                    player.right = False
                elif event.key == pygame.K_UP:
                    player.up = False
                elif event.key == pygame.K_DOWN:
                    player.down = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            spawn_particles(win, charge_group, density, player)
        else:
            charge_group.empty()

        # Eliminate particles that collide with the player obj
        # Eliminate particles that store old target direction by create a limit of position
        for c in charge_group:
            if (pygame.sprite.collide_rect(c, player) or (
                (player.direction == 'up' and c.rect.y >= player.rect.midtop[1]) or
                (player.direction == 'down' and c.rect.y <= player.rect.midbottom[1]) or
                (player.direction == 'left' and c.rect.x >= player.rect.midleft[0]) or
                (player.direction == 'right' and c.rect.x <= player.rect.midright[0])
            )):
                charge_group.remove(c)

        win.fill((0, 0, 0))
        player.update()
        charge_group.update()

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
