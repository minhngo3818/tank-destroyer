import pygame
from pygame.sprite import Sprite

from sounds import Sounds


class Menu(Sprite):
    def __init__(self, access):
        super().__init__()

        self.access = access
        self.setting = access.setting
        self.sounds = Sounds(self.access)
        self.bg = access.bg
        self.screen = access.screen
        self.screen_rect = self.access.screen_rect

        #   Load introMenu BackGround
        self.bg_menu = pygame.image.load('../images/bg_introMenu.jpg')  # Ratio: 16/9
        self.bg_size = self.bg_menu.get_size()
        self.bg_menu = pygame.transform.scale(self.bg_menu, (1120, 630))

        #   Key
        self.keyIndex = 0

        #   Font
        self.title_font = pygame.font.SysFont('ROG Fonts', 60, True)
        self.button_font = pygame.font.SysFont('consoles', 36, False)

        #   Initialize buttons
        self.width, self.height = 180, 50
        self.buttonRect = pygame.Rect((self.access.width // 2, self.access.height // 2), (self.width, self.height))

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonSurface.fill(self.setting.gray)

        self.selectSurface = pygame.Surface((self.width, self.height))
        self.selectSurface.fill(self.setting.gray_light)

        self.main_options = ['Play', 'Quit']
        self.pause_options = ['Resume', 'Main Menu', 'Quit Game']
        self.gameover_options = ['Try Again', 'Quit']

        #   PauseMenu
        self.pause_font = pygame.font.SysFont('consoles', 52, True)

        # Background
        self.trsp_bg = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
        self.trsp_bg.fill(self.setting.gray_stale)
        self.trsp_bg.set_alpha(100)

    #   Display Events when Game Stop
    def menuBG(self):
        self.screen.blit(self.bg_menu, (0, 0))

        #   Draw Game Title
        title = self.title_font.render("Tank Destroyer", True, self.setting.white)
        title_rect = title.get_rect()
        title_rect.center = (self.screen_rect.centerx, 200)
        self.screen.blit(title, title_rect)

    def gamestopBG(self, title):
        self.screen.blit(self.trsp_bg, (0, 0))

        announce = self.title_font.render(title, True, self.setting.white)
        announce_rect = announce.get_rect()
        announce_rect.center = (self.screen_rect.centerx, self.screen_rect.centery - 100)
        self.screen.blit(announce, announce_rect)

    def display_buttons(self):
        buttons_amount = 0
        button_group = []

        if self.setting.menu_on:
            buttons_amount = self.setting.amountOptionMain
            button_group = self.main_options
        elif self.setting.pause_on:
            buttons_amount = self.setting.amountOptionPause
            button_group = self.pause_options
        elif self.setting.gameover_on:
            buttons_amount = self.setting.amountOptionGameOver
            button_group = self.gameover_options

        for number in range(buttons_amount):
            button = self.buttonRect
            surface = self.buttonSurface

            if self.keyIndex == number:
                surface = self.selectSurface

            #   Buttons
            gap = 40 + self.screen_rect.centery + (self.height + 40) * number
            button.center = (self.screen_rect.centerx, gap)
            surface_rect = surface.get_rect()
            surface_rect.center = (self.screen_rect.centerx, gap)

            #   Names
            option_name = button_group[number]
            name_image = self.button_font.render(option_name, True, self.setting.white)
            name_rect = name_image.get_rect()
            name_rect.center = surface_rect.center

            self.screen.blit(surface, surface_rect)
            self.screen.blit(name_image, name_rect)
            pygame.draw.rect(self.screen, self.setting.gray_stale, button, 5)
