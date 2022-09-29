import pygame


class Interface:
    def __init__(self, access):
        self.access = access
        self.player = access.player
        self.stats = access.stats
        self.setting = access.setting
        self.screen = access.screen
        self.screen_rect = self.screen.get_rect()

        #   Scores Font
        self.score_font = pygame.font.SysFont('ROG Fonts', 24, True)
        self.hs_font = pygame.font.SysFont('ROG Fonts', 40, True)
        self.lv_font = pygame.font.SysFont('ROG Fonts', 24, True)

        #   Player_Health
        self.start_width = 200
        self.h_width = 200
        self.h_height = 20
        self.pos_x = 30
        self.pos_y = 40

    def update_scores(self, score):
        scores_image = self.score_font.render(str(score), True, self.setting.white)
        rect_scores = scores_image.get_rect()

        rect_scores.right = self.screen_rect.right - 20
        rect_scores.top = self.screen_rect.top + 60

        self.screen.blit(scores_image, rect_scores)

    def update_high_scores(self, score):
        highscore = 0
        if score > self.stats.highscore:
            self.stats.highscore = score
        else:
            highscore = self.stats.highscore

        hs_image = self.hs_font.render(str(highscore), True, self.setting.white)
        rect_hs_image = hs_image.get_rect()
        rect_hs_image.centerx = self.screen_rect.centerx
        rect_hs_image.top = self.screen_rect.top + 20

        self.screen.blit(hs_image, rect_hs_image)

    def update_health(self, hp):

        #   Calculate decrement of health bar width
        width_decrease = self.start_width - (self.start_width / self.setting.player_health) * \
                         (self.setting.player_health - hp)

        outer_hp = pygame.Surface((self.h_width + 10, self.h_height + 10))
        outer_hp.fill(self.setting.gray)
        rect_outer = outer_hp.get_rect(midleft=(self.pos_x - 5, self.pos_y))

        #   Carry out when player HP > 0
        try:
            inner_hp = pygame.Surface((width_decrease, self.h_height))
            inner_hp.fill(self.setting.blue)
            rect_inner = inner_hp.get_rect(midleft=(self.pos_x, self.pos_y))

            self.screen.blit(outer_hp, rect_outer)
            self.screen.blit(inner_hp, rect_inner)

        except pygame.error:  # When player HP == 0
            self.screen.blit(outer_hp, rect_outer)

    def update_life(self, lives):
        for life_number in range(lives):
            life = pygame.image.load('./data/images/tank_up(1).png').convert_alpha()
            size = life.get_size()
            image_smaller = pygame.transform.smoothscale(life, (int(size[0] * 0.5), int(size[1] * 0.5)))
            rect = image_smaller.get_rect()
            rect.x = 30 + life_number * (rect.width + 20)
            rect.y = rect.width + self.pos_y

            self.screen.blit(image_smaller, (rect.x, rect.y))

    def update_level(self, level):
        level_image = self.lv_font.render('Level ' + str(level), True, self.setting.blue)
        rect_lv_image = level_image.get_rect()
        rect_lv_image.right = self.screen_rect.right - 20
        rect_lv_image.top = self.screen_rect.top + 20

        self.screen.blit(level_image, rect_lv_image)

    def run_updates(self, hp, lives, level, score):
        self.update_scores(score)
        self.update_high_scores(score)
        self.update_health(hp)
        self.update_life(lives)
        self.update_level(level)
