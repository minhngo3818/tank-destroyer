import pygame
from pygame.sprite import Sprite
from sounds import Sounds


class Player(Sprite):
    def __init__(self, access):
        super().__init__()

        self.access = access
        self.setting = access.setting
        self.screen = self.access.screen
        self.screen_rect = self.screen.get_rect()
        self.gameover_on = self.setting.gameover_on
        self.sounds = Sounds(self)

        self.player_images = {"left": [pygame.image.load("../images/tank_left(1).png"),
                                       pygame.image.load("../images/tank_left(2).png"),
                                       pygame.image.load("../images/tank_left(3).png"),
                                       pygame.image.load("../images/tank_left(4).png")],
                              "right": [pygame.image.load("../images/tank_right(1).png"),
                                        pygame.image.load("../images/tank_right(2).png"),
                                        pygame.image.load("../images/tank_right(3).png"),
                                        pygame.image.load("../images/tank_right(4).png")],
                              "up": [pygame.image.load("../images/tank_up(1).png"),
                                     pygame.image.load("../images/tank_up(2).png"),
                                     pygame.image.load("../images/tank_up(3).png"),
                                     pygame.image.load("../images/tank_up(4).png")],
                              "down": [pygame.image.load("../images/tank_down(1).png"),
                                       pygame.image.load("../images/tank_down(2).png"),
                                       pygame.image.load("../images/tank_down(3).png"),
                                       pygame.image.load("../images/tank_down(4).png")]}
        self.direction = "up"
        self.index = 0
        self.image = self.player_images[self.direction][self.index].convert()
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center  # Center an object with center point
        self.frame_rate = self.access.setting.frame_rate
        self.speed = self.access.setting.player_speed
        self.run_frame = False

        #   Move Frags
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.standing = True

        #   Life
        self.hp = self.access.setting.player_health
        self.life = self.access.setting.player_life

    def update(self, win):
        self.movement()
        if self.run_frame:
            self.index += self.frame_rate
            if self.index > 3:
                self.index = 0
        else:
            self.index = 0

        self.image = self.player_images[self.direction][int(self.index)]
        win.blit(self.image, (self.rect.x, self.rect.y))

    def movement(self):
        if self.left and self.rect.left > 0:
            self.direction = "left"
            self.rect.x -= self.speed
            self.run_frame = True
        elif self.right and self.rect.right < self.access.width:
            self.direction = "right"
            self.rect.x += self.speed
            self.run_frame = True
        elif self.up and self.rect.top > 0:
            self.direction = "up"
            self.rect.y -= self.speed
            self.run_frame = True
        elif self.down and self.rect.bottom < self.access.height:
            self.direction = "down"
            self.rect.y += self.speed
            self.run_frame = True




