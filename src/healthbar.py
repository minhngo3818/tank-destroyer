import pygame


class HealthBar:
    def __init__(self, asset):
        #   Initialize params
        self.setting = asset.setting
        self.rect = asset.rect

        #   Creeps Health Bar
        self.width_start = 32
        self.width_boss_start = 800

    def enemy_health(self, win, hp):  # HP is called in __init__ only take one time reference no update
        width_decrease = self.width_start - (self.width_start / self.setting.enemy_health1) * (
                self.setting.enemy_health1 - hp)
        outer_hp = pygame.Surface((self.width_start + 6, 11))
        outer_hp.fill(self.setting.gray)
        rect_outer = outer_hp.get_rect(midleft=(self.rect.x, self.rect.y - 7))

        inner_hp = pygame.Surface((width_decrease, 5))
        inner_hp.fill(self.setting.red)
        rect_inner = inner_hp.get_rect(midleft=(self.rect.x + 3, self.rect.y - 7))

        win.blit(outer_hp, rect_outer)
        win.blit(inner_hp, rect_inner)

    def boss_health(self, win, hp):
        width_decrease = self.width_boss_start - (self.width_boss_start / self.setting.boss_health) * (
                self.setting.boss_health - hp)

        outer_hp = pygame.Surface((self.width_boss_start + 10, 40))
        outer_hp.fill(self.setting.gray)
        rect_outer = outer_hp.get_rect(midleft=((self.setting.scr_width - self.width_boss_start) // 2,
                                                self.setting.scr_height - 40))

        inner_hp = pygame.Surface((width_decrease, 30))
        inner_hp.fill(self.setting.red)
        rect_inner = inner_hp.get_rect(midleft=((self.setting.scr_width - self.width_boss_start) // 2 + 5,
                                                self.setting.scr_height - 40))

        win.blit(outer_hp, rect_outer)
        win.blit(inner_hp, rect_inner)
