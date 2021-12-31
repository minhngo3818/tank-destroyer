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
        self.boss = Boss(self)
        self.limit = self.setting.enemy_limit

    def update_spawn(self):
        if self.setting.spawn_time == 0:
            if len(self.enemy_group) < self.limit:
                if self.setting.level == 1 and not self.setting.boss_spawn:
                    self.setting.boss_spawn = True
                else:
                    new_enemy = Enemy(self)
                    self.enemy_group.add(new_enemy)
                self.setting.spawn_time = 80

            self.check_level_spawn()
        else:
            self.setting.spawn_time -= 1

        if self.setting.boss_spawn:
            self.boss.update(self.screen)

        self.enemy_group.update(self.screen)

    def check_level_spawn(self):
        if len(self.enemy_group) == 0 and self.setting.boss_spawn:
            self.setting.enemy_limit += 1
            self.limit = self.setting.enemy_limit
            self.setting.level += 1
