import sys

import pygame
from pygame.sprite import Sprite


class Tank(Sprite):
    def __init__(self, x, y):
        super(Tank, self).__init__()
        # Load image
        self.Player = {"left": [pygame.image.load("images/tank_left(1).png"),
                                pygame.image.load("images/tank_left(2).png"),
                                pygame.image.load("images/tank_left(3).png"),
                                pygame.image.load("images/tank_left(4).png")],
                       "right": [pygame.image.load("images/tank_right(1).png"),
                                 pygame.image.load("images/tank_right(2).png"),
                                 pygame.image.load("images/tank_right(3).png"),
                                 pygame.image.load("images/tank_right(4).png")],
                       "up": [pygame.image.load("images/tank_up(1).png"),
                              pygame.image.load("images/tank_up(2).png"),
                              pygame.image.load("images/tank_up(3).png"),
                              pygame.image.load("images/tank_up(4).png")],
                       "down": [pygame.image.load("images/tank_down(1).png"),
                                pygame.image.load("images/tank_down(2).png"),
                                pygame.image.load("images/tank_down(3).png"),
                                pygame.image.load("images/tank_down(4).png")]}

        # x y coordinator
        self.x = x
        self.y = y

        self.rect = pygame.Rect((x, y), (32, 32))
        self.direction = "up"
        self.index = 0
        self.image = self.Player[self.direction][self.index]
        self.frame_rate = 0.3
        self.run_frame = 0

        # Movement trigger
        self.tank_up = False
        self.tank_down = False
        self.tank_left = False
        self.tank_right = False
        self.tank_animation = False

    def update(self, win):

        if self.tank_animation == True:
            self.index += self.frame_rate

            if self.index > 3:
                self.index = 0

            if self.tank_up:
                self.direction = "up"
            elif self.tank_down:
                self.direction = "down"
            elif self.tank_left:
                self.direction = "left"
            elif self.tank_right:
                self.direction = "right"
        else:
            self.index = 0
            if self.tank_up:
                self.direction = "up"
            elif self.tank_down:
                self.direction = "down"
            elif self.tank_left:
                self.direction = "left"
            elif self.tank_right:
                self.direction = "right"

        self.image = self.Player[self.direction][int(self.index)]
        win.blit(self.image, (self.x, self.y))

    def movement(self):
        if self.tank_up and self.y > 0:
            self.y -= 2
        elif self.tank_down and self.y < 600 - 64:
            self.y += 2
        elif self.tank_left and self.x > 0:
            self.x -= 2
        elif self.tank_right and self.x < 800 - 64:
            self.x += 2


class Projectile(Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__()
        self.Bullet = {"left": pygame.image.load("images/bullet_left.png"),
                       "right": pygame.image.load("images/bullet_right.png"),
                       "up": pygame.image.load("images/bullet_up.png"),
                       "down": pygame.image.load("images/bullet_down.png")}
        self.direction = direction
        self.image = self.Bullet[self.direction]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x + 22
        self.rect.y = pos_y + 22
        self.bullet_speed = 10

    def update(self):
        if self.direction == "up":  # GO UP
            self.rect.x += 0
            self.rect.y -= self.bullet_speed
        elif self.direction == "down":  # GO DOWN
            self.rect.x += 0
            self.rect.y += self.bullet_speed
        elif self.direction == "left":  # GO LEFT
            self.rect.x -= self.bullet_speed
            self.rect.y += 0
        elif self.direction == "right":  # GO RIGHT
            self.rect.x += self.bullet_speed
            self.rect.y += 0


# Settings
"""Screens"""
pygame.init()
win_width = 800  # change the screen dimension bigger
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Tank Destroyer')
bg = pygame.image.load('images/tank_field.png').convert()

"""Gameplay"""
FPS = 60
clock = pygame.time.Clock()
player = Tank(400, 300)
player_group = pygame.sprite.Group(player)

bullet_group = pygame.sprite.Group()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Projectile(player.x, player.y, player.direction)
                    bullet_group.add(bullet)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            sys.exit()

        """PLAYER MOVEMENT"""
        if keys[pygame.K_LEFT]:
            player.tank_left = True
            player.tank_right = False
            player.tank_up = False
            player.tank_down = False

            player.tank_animation = True

        elif keys[pygame.K_RIGHT]:
            player.tank_right = True
            player.tank_left = False
            player.tank_up = False
            player.tank_down = False

            player.tank_animation = True

        elif keys[pygame.K_UP]:
            player.tank_up = True
            player.tank_left = False
            player.tank_right = False
            player.tank_down = False

            player.tank_animation = True

        elif keys[pygame.K_DOWN]:
            player.tank_down = True
            player.tank_left = False
            player.tank_right = False
            player.tank_up = False

            player.tank_animation = True

        else:
            player.tank_left = False
            player.tank_right = False
            player.tank_up = False
            player.tank_down = False
            player.tank_animation = False

        win.blit(bg, (0, 0))
        player.movement()
        bullet_group.draw(win)
        player.update(win)
        bullet_group.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()

####---------------------Process_Note--------------------####
# 1: Player class- 20hrs
#   Issue 1: image of tank movement doesn't update and cannot pass instance to display tank image"""
#       >> solved
#   Task 1: 1 direction-animation--Checked
#   Task 2: 4 direction animation - checked
#   Task 3: movement - checked

# 2: Bullet class - 20hrs
#   Task 1: Create Bullets images
#   Task 2: Create Bullet images for enemies
#           4 type
#   Task 3: Bullet in 1 direction
#   Task 4: Bullet in 4 direction

# 3: Enemy class - 20hrs
#   Task 1: Create Enemies
#       3 Types: High Defense, High Movement, High Power
#       1 Boss: Gatling Guns, Mega Cannon,
#   Task 1: Basic Enemy Class
#   Task 2: Stats and Movement
#   Task 3: Shooting
#   Task 4: Add Enemy Class & Modify for each type of Enemy
# 4: Collision - 20 hrs
#   Task 1: hit by Bullet
#   Task 2: Hit by Other enemies
# 5: Interface - 20 hrs
#   Task 1: New Game Interface
#   Task 2: HP bar
#   Task 3: Score Board
#   Task 4: Level
# EXTRA SECTIONS:
# 6: Upgrade Drops
# 7: Create 5 Stages
# 8: Create More Enemies
# 9: Setting Interface
#   Pausing Interface
# 10: Shopping System
#   Shopping Interface


# References:
# Code 1: <https://stackoverflow.com/questions/34031513/how-do-you-get-sprites-to-appear-within-this-space-invader-game>""" (X)
# Code 2: <https://github.com/kidscancode/pygame_tutorials/blob/master/movement/move_basics.py>""" (X)
# Code 3: <https://stackoverflow.com/questions/54083028/how-to-control-individual-bullets-in-pygame> """
# Code 4: <https://github.com/clear-code-projects/animation> (gitsource)
#           <https://www.youtube.com/watch?v=MYaxPa_eZS0> (video demonstration)
# Code 5: Animation - <https://github.com/techwithtim/Pygame-Tutorials/blob/master/Game/Tutorial%20%233.py>
# Code 6: Animation - <https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images>
# Code 7: Animation - <https://stackoverflow.com/questions/49352990/how-do-i-get-my-images-to-work-as-an-animation-in-pygame> 
# Code 8: Bullet - <https://stackoverflow.com/questions/21441612/python-pygame-shooting-a-bullet-the-direction-the-sprite-is-facing>
