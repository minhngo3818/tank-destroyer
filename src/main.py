import sys
import pygame

from settings import Settings
from menu import Menu
from src.interface import Interface
from player import Player
from spawn_enemy import Spawn
from src.bullet import Bullet, BossBullet
from stats import Stats
from sounds import Sounds


class Tank_Destroyer:

    """INITIALIZATION"""

    def __init__(self):
        pygame.init()

        #   Initialize Foundation
        self.setting = Settings()
        self.bg = pygame.image.load("images/tank_field.png")
        self.width = self.setting.scr_width
        self.height = self.setting.scr_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Tank Destroyer")

        #   Time
        self.clock = pygame.time.Clock()
        self.FPS = self.setting.FPS

        #   Projectile Groups
        self.bullet_group_P = pygame.sprite.Group()  # Player bullet group
        self.bullet_group_E = pygame.sprite.Group()  # Enemy bullet group
        self.bullet_group_B = pygame.sprite.Group()  # Boss canon bullet
        self.laser_group_B = pygame.sprite.Group()   # Boss laser bullet
        self.laser_charge_group = pygame.sprite.Group()
        self.gatling_group_B = pygame.sprite.Group()  # Boss machine gun bullet

        #   Initialize Classes
        self.player = Player(self)
        self.spawn = Spawn(self)
        self.menu = Menu(self)
        self.stats = Stats(self)
        self.interface = Interface(self)
        self.sounds = Sounds(self)

    """COLLISION SECTION"""

    def check_player_stats(self):

        # Check Player Life and Reset Player Stats
        if self.player.hp < 0:  # Player's HP Decrement Threshold not equal 0, or below 0
            pygame.time.wait(self.setting.delayTime)
            self.stats.reset_life()

            if self.player.life < 0:
                self.setting.gameover_on = True

    def check_collision(self):
        self.collision_tolerance = 10 # The area triggers collisions
        self.collision_player_enemy()
        self.collision_enemy_enemy()
        self.collision_projectiles()

    def collision_player_enemy(self):

        # Player Collides Enemy
        for enemy_x in self.spawn.enemy_group:
            if pygame.sprite.collide_rect(self.player, enemy_x):

                if abs(enemy_x.rect.right - self.player.rect.left) < self.collision_tolerance:
                    self.player.left = False
                    enemy_x.move = False
                    enemy_x.rect.right = self.player.rect.left

                    # (*) Prevent pushing over \left edge
                    if enemy_x.rect.left <= 0:
                        enemy_x.rect.left = 0

                if abs(enemy_x.rect.left - self.player.rect.right) < self.collision_tolerance:
                    self.player.right = False
                    enemy_x.move = False
                    enemy_x.rect.left = self.player.rect.right

                    # (*) Prevent pushing over right edge
                    if enemy_x.rect.right >= self.width:
                        enemy_x.rect.right = self.width

                if abs(enemy_x.rect.bottom - self.player.rect.top) < self.collision_tolerance:
                    self.player.up = False
                    enemy_x.move = False
                    enemy_x.rect.bottom = self.player.rect.top

                    # (*) Prevent pushing over bottom edge
                    if enemy_x.rect.top <= 0:
                        enemy_x.rect.top = 0

                if abs(enemy_x.rect.top - self.player.rect.bottom) < self.collision_tolerance:
                    self.player.down = False
                    enemy_x.rect.top = self.player.rect.bottom

                    # (*)
                    if enemy_x.rect.bottom >= self.height:
                        enemy_x.rect.bottom = self.height

                self.player.hp -= self.setting.collision_damage

    def collision_enemy_enemy(self):
        #   Enemy Collides Enemy
        for enemy in self.spawn.enemy_group:
            self.spawn.enemy_group.remove(enemy)

            enemy_group_hit = pygame.sprite.spritecollide(enemy, self.spawn.enemy_group, False)

            for enemy_remain in enemy_group_hit:
                enemy.move = False
                enemy_remain.move = False
                # Check impact direction
                if enemy.direction_number == 0:

                    # Check impact tolerance
                    if abs(enemy_remain.rect.left - enemy.rect.right) < self.collision_tolerance:

                        enemy.rect.right = enemy_remain.rect.left

                    elif abs(enemy_remain.rect.right - enemy.rect.left) < self.collision_tolerance:
                        enemy.rect.left = enemy_remain.rect.right

                if enemy.direction_number == 1:

                    if abs(enemy_remain.rect.top - enemy.rect.bottom) < self.collision_tolerance:

                        enemy.rect.bottom = enemy_remain.rect.top

                    elif abs(enemy_remain.rect.bottom - enemy.rect.top) < self.collision_tolerance:

                        enemy.rect.top = enemy_remain.rect.bottom

            self.spawn.enemy_group.add(enemy)

    def collision_boss_player(self):
        pass

    def collision_boss_enemy(self):
        pass

    def collision_projectiles(self):
        #   Bullet Collision:
        #   Bullets From Player
        for bullet in self.bullet_group_P:
            enemy_hit = pygame.sprite.spritecollide(bullet, self.spawn.enemy_group, False)

            for enemy_b in enemy_hit:
                self.bullet_group_P.remove(bullet)
                enemy_b.hp -= 1

                if enemy_b.hp == 0:
                    self.spawn.enemy_group.remove(enemy_b)

                    #   Decrement of enemy spawn limit per defeated enemy
                    self.spawn.limit -= 1

                    #   Increment of score per defeated enemy
                    self.stats.points()

            #   Bullets From Enemy
        for bullet in self.bullet_group_E:
            if pygame.sprite.collide_rect(bullet, self.player):
                self.bullet_group_E.remove(bullet)
                self.player.hp -= 1

        self.check_player_stats()

    def collision_boss_projectiles(self):
        pass


    """SPAWNING PROJECTILES SECTION"""

    #   Create Creep Bullets
    def create_bullet(self):
        #   Create Bullet for enemies
        if len(self.bullet_group_E) < self.setting.bullet_allowed:
            for enemy in self.spawn.enemy_group:
                if enemy.stop_time == 100:
                    bullet_x = enemy.rect.x + enemy.rect.width / 3.8
                    bullet_y = enemy.rect.y + enemy.rect.height / 3.8
                    bullet = Bullet(bullet_x, bullet_y, enemy.direction)
                    self.bullet_group_E.add(bullet)
                    self.sounds.shootPlayer()

    # Create Boss Projectiles
    def create_boss_projectile(self):
        if self.setting.boss_spawn and self.spawn.boss.rect.y >= 0:
            if self.spawn.boss.stop_time == 50 :
                self.create_boss_gbullet(self.spawn.boss)

            elif 100 <= self.spawn.boss.stop_time <= 180:
                if self.spawn.boss.stop_time % 5 == 0:
                    self.create_boss_gatl(self.spawn.boss)

    def create_boss_gatl(self, boss):
        x1_g, x2_g, y1_g, y2_g = 0, 0, 0, 0

        #   Condition for limit gatling bullets
        if len(self.gatling_group_B) <= self.setting.boss_gatling_allow:
                if boss.direction == "up" or boss.direction == "down":
                    x1_g = boss.rect.x + (34/128) * boss.rect.width
                    x2_g = boss.rect.x + (74/128) * boss.rect.width
                    y1_g = boss.rect.centery
                    y2_g = y1_g

                elif boss.direction == "left" or boss.direction == "right":
                    y1_g = boss.rect.y + (34 / 128) * boss.rect.width
                    y2_g = boss.rect.y + (74 / 128) * boss.rect.width
                    x1_g = boss.rect.centerx
                    x2_g = x1_g

                bulletL = BossBullet(x1_g, y1_g, "gatling", boss.direction)
                bulletR = BossBullet(x2_g, y2_g, "gatling", boss.direction)
                self.gatling_group_B.add(bulletL)
                self.gatling_group_B.add(bulletR)
                self.sounds.machineGun()
        else:
            for bullet in self.gatling_group_B:
                self.gatling_group_B.remove(bullet)


    def create_boss_gbullet(self, boss):
        #   Condition for limit bullet
        if len(self.bullet_group_B) <= 5:
            x_b = boss.rect.x + (56/128) * boss.rect.width
            y_b = boss.rect.y + (56/128) * boss.rect.height
            megabullet = BossBullet(x_b, y_b, "giant", boss.direction)
            self.bullet_group_B.add(megabullet)
            self.sounds.shootPlayer()
            #   Add Sound Effect

    def create_boss_laser(self):
        #    Condition for limit bullet
        if self.setting.boss_cooldown == 0:
            if self.setting.boss_laser_chargetime == 50:
                #   Add Laser Charge Effect
                for amount in range(self.setting.boss_charge_density):
                    #   pass the positions for 4 directions
                    #   need embedding a method
                    #   Create charge effect
                    #   May create a method insides boss object
                    #lasercharge = LaserCharge(...)
                    #self.laser_charge_group.B.add(lasercharge)

                    #if lasercharge.dx == 0 and lasercharge.dy == 0:
                        #self.laser_charge_group.remove(lasercharge)
                    pass

                self.setting.boss_laser_chargetime -= 1
            elif self.setting.boss_laser_chargetime == 0:
                self.setting.boss_laser_chargetime = 50
                self.setting.boss_laser_time = 0

            if self.setting.boss_laser_time == 0:
                x_l = self.boss.rect.x + (56 / 128) * self.boss.rect.width
                y_l = self.boss.rect.y + self.boss.rect.centery
                w_l = 16
                h_l = 50
                #laser1 = Laser(x_l, y_l, w_l, h_l, self.setting,red)
                #laser2 = Laser(x_l - 4, y_l, w_l - 4, self.setting.red_med)
                #laser3 = Laser(x_l - 6, Y_l, w_l - 6, self.setting.red.lite)
                #self.laser_group_B.add(laser1)
                #self.laser_group_B.add(laser2)
                #self.laser_group_B.add(laser3)
                #   Add Sound Here

                self.setting.boss_laser_time += 1
            elif self.setting.boss_laser_time == 80:
                self.setting.boss_cooldown = 200
        else:
            self.setting.boss_cooldown -= 1
        pass

    """KEY SECTIONS"""

    def check_selection(self, event):

        # Set up Option Limits
        limit = 0

        if self.setting.menu_on:
            limit = self.setting.amountOptionMain
        elif self.setting.pause_on:
            limit = self.setting.amountOptionPause
        elif self.setting.gameover_on:
            limit = self.setting.amountOptionGameOver

        # Change Selections
        if not self.setting.game_on:
            if event.key == pygame.K_UP:
                self.menu.keyIndex -= 1
                if self.menu.keyIndex < 0:
                    self.menu.keyIndex = limit - 1
                self.sounds.buttonChange()

            elif event.key == pygame.K_DOWN:
                self.menu.keyIndex += 1
                if self.menu.keyIndex > limit - 1:
                    self.menu.keyIndex = 0
                self.sounds.buttonChange()

        #   Select Option
        if event.key == pygame.K_RETURN:
            self.sounds.buttonAccess()
            pygame.time.delay(500)
            if self.menu.keyIndex == 0:  # 1st Option - Play
                if self.setting.menu_on:
                    self.setting.menu_on = False
                    self.setting.game_on = True

                    #   Reset Game Data When Call
                    self.stats.reset_game()

                elif self.setting.pause_on:
                    self.setting.pause_on = False
                    self.setting.game_on = True

                elif self.setting.gameover_on:
                    self.setting.gameover_on = False
                    self.setting.menu_on = True

                self.menu.keyIndex = 0

            elif self.menu.keyIndex == 1 and self.setting.pause_on:
                self.setting.menu_on = True
                self.setting.pause_on = False

            elif self.menu.keyIndex == limit - 1:  # Last Option - Quit
                if self.setting.menu_on or self.setting.pause_on or self.setting.gameover_on:
                    pygame.quit()
                    sys.exit()

        #   Turn on Pause Menu
        if event.key == pygame.K_BACKSPACE:
            if not self.setting.gameover_on:
                if self.setting.pause_on:
                    self.setting.pause_on = False
                    self.setting.game_on = True

                else:
                    self.setting.pause_on = True

    def key_down(self, event):

        #   Player Movement Flag Triggers
        if event.key == pygame.K_UP:
            self.player.up = True
        elif event.key == pygame.K_DOWN:
            self.player.down = True
        elif event.key == pygame.K_LEFT:
            self.player.left = True
        elif event.key == pygame.K_RIGHT:
            self.player.right = True

        #   Movement sound on when any player's move flags are on
        if self.setting.game_on:
            if self.player.up or self.player.down or self.player.left or self.player.right:
                self.sounds.moveSound()
        else:
            self.sounds.stopmoveSound()

        #   Create Bullet
        if event.key == pygame.K_SPACE:
            if len(self.bullet_group_P) < self.setting.bullet_allowed:
                bullet_x = self.player.rect.x + self.player.rect.width / 3.8
                bullet_y = self.player.rect.y + self.player.rect.height / 3.8
                bullet = Bullet(bullet_x, bullet_y, self.player.direction)
                self.bullet_group_P.add(bullet)
                self.sounds.shootPlayer()

    def key_up(self, event):

        self.player.run_frame = False

        if event.key == pygame.K_UP:
            self.player.up = False
        elif event.key == pygame.K_DOWN:
            self.player.down = False
        elif event.key == pygame.K_LEFT:
            self.player.left = False
        elif event.key == pygame.K_RIGHT:
            self.player.right = False

        #   Move sound turn off
        if self.setting.game_on:
            if not (self.player.left or self.player.right or self.player.up or self.player.down):
                self.sounds.stopmoveSound()

    def _event_(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self.key_down(event)

                #   Check Keys Button
                self.check_selection(event)

                #   Emergency Close Program Button
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYUP:
                self.key_up(event)

    """RED DRAW"""

    def redDrawGamePlay(self):
        self.screen.blit(self.bg, (0, 0))
        self.create_bullet()
        self.create_boss_projectile()
        self.bullet_group_E.update(self.screen)
        self.bullet_group_P.update(self.screen)
        self.bullet_group_B.update(self.screen)
        self.gatling_group_B.update(self.screen)
        self.player.animation(self.screen)
        self.spawn.update_spawn()
        self.check_collision()
        self.interface.run_updates(self.player.hp, self.player.life, self.setting.level, self.stats.score)

    """MAIN"""

    #   Main Loop
    def main_loop(self):
        while True:
            self._event_()
            if self.setting.menu_on:
                self.menu.menuBG()

            elif self.setting.game_on:
                self.sounds.themeTrack()
                self.redDrawGamePlay()

                #   Turn on Pause Menu or Gameover BG Menu
                if self.setting.pause_on:
                    self.menu.gamestopBG("Pause")
                    self.setting.game_on = False
                elif self.setting.gameover_on:
                    self.menu.gamestopBG("GameOver")
                    self.setting.game_on = False

            elif not self.setting.game_on:
                pygame.mixer.Sound.stop(self.sounds.gametrack)

            self.menu.display_buttons()

            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    ai = Tank_Destroyer()
    ai.main_loop()
