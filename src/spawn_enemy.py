import pygame
from pygame.sprite import Sprite

from src.enemy import Enemy
from src.enemy import Boss


class Spawn(Sprite):
    def __init__(self, access):
        super().__init__()
        self.screen = access.screen
        self.setting = access.setting
        self.player = access.player
        self.enemy_group = pygame.sprite.Group()
        self.boss = None
        self.limit = self.setting.enemy_limit

    def update_spawn(self):
        if self.setting.spawn_time == 0:
            if len(self.enemy_group) < self.limit:
                if self.setting.level == 5 and not self.setting.boss_spawn:
                    self.setting.boss_spawn = True
                    self.boss = Boss(self)
                else:
                    self.enemy_group.add(Enemy(self))
                self.setting.spawn_time = 80

            self.check_level_spawn()
        else:
            self.setting.spawn_time -= 1

        if self.setting.boss_spawn:
            self.boss.update(self.screen)

        self.enemy_group.update(self.screen)

    def check_level_spawn(self):
        if not self.setting.boss_spawn:
            if len(self.enemy_group) == 0:
                self.setting.enemy_limit += 1
                self.limit = self.setting.enemy_limit
                self.setting.level += 1
        else:
            if self.boss.hp <= 0:
                self.setting.gameover_on = True
