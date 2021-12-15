import pygame
from pygame.sprite import Sprite

from enemy import Enemy
from enemy import Boss


class Spawn(Sprite):
    def __init__(self, access):
        super().__init__()
        self.screen = access.screen
        self.setting = access.setting
        self.player = access.player
        self.enemy_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()

        self.limit = self.setting.enemy_limit

    def update_spawn(self):
        if self.setting.spawn_time == 0:
            if len(self.enemy_group) < self.limit:
                if self.setting.level == 1 and not self.setting.boss_spawn:
                    self.boss = Boss(self)
                    self.setting.boss_spawn = True
                    self.boss_group.add(self.boss)
                else:
                    new_enemy = Enemy(self)
                    self.enemy_group.add(new_enemy)
                self.setting.spawn_time = 80

            self.check_level_spawn()
        else:
            self.setting.spawn_time -= 1

        if len(self.boss_group) != 0:
            self.boss_group.update(self.screen)

        self.enemy_group.update(self.screen)

    def check_level_spawn(self):
        if len(self.enemy_group) == 0 and len(self.boss_group) == 0:
            self.setting.enemy_limit += 1
            self.limit = self.setting.enemy_limit
            self.setting.level += 1
