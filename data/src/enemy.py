import pygame
import random
from pygame.sprite import Sprite
from .healthbar import HealthBar
from .sounds import Sounds


class Enemy(Sprite):
    def __init__(self, access):
        super().__init__()
        self.setting = access.setting
        self.player = access.player
        self.sounds = Sounds(access)

        # Initiation
        self.image_list = [pygame.image.load("./data/images/enemy(1).png"),
                           pygame.image.load("./data/images/enemy(2).png"),
                           pygame.image.load("./data/images/enemy(3).png"),
                           pygame.image.load("./data/images/enemy(4).png")]
        self.index = 0
        self.angle = 0
        self.image = self.image_list[self.index].convert()
        self.rect = self.image.get_rect()

        #   Direction
        self.randomDir = random.randrange(2)
        self.direction_number = 0
        self.direction = "up"

        #   Display & Update
        self.stop_time = self.setting.stop_time
        self.move_time = self.setting.start_time
        self.speed = self.setting.enemy_speed
        self.run_frame = False

        #   Life
        self.hp = self.setting.enemy_health1

        self.start_pos()
        self.healthbar = HealthBar(self)  # Must be initialized after calling methods and rect

    def start_pos(self):
        edge = random.randrange(4)
        if edge == 0:  # Top
            self.rect.x = random.randrange(self.setting.scr_width - self.rect.width)
            self.rect.y = 0  # -self.rect.height
        elif edge == 1:  # Down
            self.rect.x = random.randrange(self.setting.scr_width - self.rect.width)
            self.rect.y = self.setting.scr_height - self.rect.height  # self.rect.height + self.asset.scr_height
        elif edge == 2:  # Left
            self.rect.x = 0  # -self.rect.width
            self.rect.y = random.randrange(self.setting.scr_height - self.rect.height)
        elif edge == 3:  # Right
            self.rect.x = self.setting.scr_width - self.rect.width  # self.rect.width + self.asset.scr_width
            self.rect.y = random.randrange(self.setting.scr_height - self.rect.height)

    def update(self, win):
        self.animation()
        self.healthbar.enemy_health(win, self.hp)

        #   Rotate Images
        rotate = pygame.transform.rotate
        rotated_image = rotate(self.image, self.angle)

        win.blit(rotated_image, (self.rect.x, self.rect.y))

    def animation(self):
        self.move_rest()
        if self.run_frame:
            self.index += self.setting.frame_rate
            if self.index > 3:
                self.index = 0
        else:
            self.index = 0

        self.image = self.image_list[int(self.index)]

    def move_rest(self):
        if self.stop_time == 0:
            self.move_going()
        else:
            self.stop_time -= 1

    def move_going(self):

        if self.move_time == self.setting.move_time:  # 20
            self.run_frame = False
            self.randomDir = random.randrange(2)
            self.move_time = self.setting.start_time  # 0
            self.stop_time = self.setting.stop_time  # 200

        elif self.move_time < self.setting.move_time:
            self.run_frame = True
            self.direction_number = self.randomDir
            self.move_update()
            self.move_time += 1

    def move_update(self):
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y

        if self.direction_number == 0:
            if 0 <= self.rect.x <= self.setting.scr_width:
                if dx < 0:
                    self.direction = "left"
                    self.angle = 90
                    self.rect.x += max(-self.speed, dx)
                elif dx > 0:
                    self.direction = "right"
                    self.angle = 270
                    self.rect.x += min(self.speed, dx)

        if self.direction_number == 1:
            if 0 <= self.rect.y <= self.setting.scr_height:
                if dy < 0:
                    self.direction = "up"
                    self.angle = 0
                    self.rect.y += max(-self.speed, dy)
                elif dy > 0:
                    self.direction = "down"
                    self.angle = 180
                    self.rect.y += min(self.speed, dy)


class Boss(Sprite):
    def __init__(self, access):
        super().__init__()
        self.angle = 180
        self.setting = access.setting
        self.player = access.player
        self.screen = access.screen
        self.screen_rect = self.screen.get_rect()

        self.image_list = [pygame.image.load("../images/Boss_Move_1.png"),
                           pygame.image.load("../images/Boss_Move_2.png"),
                           pygame.image.load("../images/Boss_Move_3.png"),
                           pygame.image.load("../images/Boss_Move_4.png")]
        self.index = 0
        self.angel = 180
        self.image = self.image_list[self.index].convert()
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = -self.rect.height
        self.direction = "down"

        #   Boss Instances
        self.hp = self.setting.boss_health
        self.speed = self.setting.boss_speed
        self.start_time = 0
        self.move_time = self.setting.boss_movetime
        self.stop_time = self.setting.boss_stoptime
        self.run_frame = False

        self.healthbar = HealthBar(self)

    def update(self, win):
        self.move_animation()
        self.healthbar.boss_health(win, self.hp)

        rotate = pygame.transform.rotate
        rotated_image = rotate(self.image, self.angle)

        win.blit(rotated_image, (self.rect.x, self.rect.y))

    def move_animation(self):
        self.move_rest()
        if self.run_frame:
            self.index += self.setting.frame_rate
            if self.index > 3:
                self.index = 0
        else:
            self.index = 0

        self.image = self.image_list[int(self.index)]

    def move_rest(self):
        if self.stop_time == 0:
            self.move_going()
        else:
            self.stop_time -= 1

    def move_going(self):
        if self.move_time == self.setting.boss_movetime:
            self.run_frame = False
            self.move_time = 0
            self.stop_time = self.setting.boss_stoptime
        elif self.move_time < self.setting.boss_movetime:
            self.run_frame = True
            self.move_update()
            self.move_time += 1

    def move_update(self):                                          # ISSUE: Double Code Lines compare to enemy class

        # NOTICE: Needs precise indication to shoot player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        #   L-Movement
        if 0 <= self.rect.x <= self.setting.scr_width \
                and 0 <= self.rect.y <= self.setting.scr_height:
            if abs(dx) < abs(dy):
                if dx < 0:
                    self.angle = 90
                    self.rect.x += max(-self.speed, dx)
                elif dx > 0:
                    self.angle = 270
                    self.rect.x += min(self.speed, dx)
                elif dx == 0:
                    if dy < 0:
                        self.angle = 0
                        self.rect.y += max(-self.speed, dy)
                    else:
                        self.angle = 180
                        self.rect.y += min(self.speed, dy)
            else:
                if dy < 0:
                    self.angle = 0
                    self.rect.y += max(-self.speed, dy)
                elif dy > 0:
                    self.angle = 180
                    self.rect.y += min(self.speed, dy)
                elif dy == 0:
                    if dx < 0:
                        self.angle = 90
                        self.rect.x += max(-self.speed, dx)
                    else:
                        self.angle = 270
                        self.rect.x += min(self.speed, dx)

            # Direction Indicator
            if self.angle == 0:
                self.direction = "up"
            elif self.angle == 90:
                self.direction = "left"
            elif self.angle == 180:
                self.direction = "down"
            elif self.angle == 270:
                self.direction = "right"

        #   Appear Moving Downward
        elif self.rect.y < 0:
            self.angle = 180
            self.rect.y += self.speed
