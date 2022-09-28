import sys
# import pygame

# from settings import Settings
from menu import Menu
from src.interface import Interface
from player import Player
from spawn_enemy import Spawn
from bullet import *
from stats import Stats
from sounds import Sounds


class TankDestroyer:
    """INITIALIZATION"""

    def __init__(self):
        pygame.init()

        #   Initialize Foundation
        self.setting = Settings()
        self.width = self.setting.scr_width
        self.height = self.setting.scr_height

        self.bg = pygame.image.load("../images/tank_field.png")
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
        self.laser_group_B = []  # Boss laser bullet
        self.laser_charge_group = pygame.sprite.Group()  # Boss laser charge effect
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
        collision_tolerance = 10  # The area triggers collisions
        self.collision_player_enemy(collision_tolerance)
        self.collision_enemy_enemy(collision_tolerance)
        self.collision_projectiles()

        if self.setting.boss_spawn:
            self.collision_boss_player(collision_tolerance)
            self.collision_boss_enemy(collision_tolerance)

    # Collision helper functions:
    def collision_two_single_obj(self, obj1, obj2, collision_tolerance):
        if pygame.sprite.collide_rect(obj1, obj2):

            if abs(obj1.rect.right - obj2.rect.left) < collision_tolerance:
                self.player.left = False
                obj1.move = False
                obj1.rect.right = obj2.rect.left

                # (*) Prevent pushing over \left edge
                if obj1.rect.left <= 0:
                    obj1.rect.left = 0

            if abs(obj1.rect.left - obj2.rect.right) < collision_tolerance:
                obj2.right = False
                obj1.move = False
                obj1.rect.left = obj2.rect.right

                # (*) Prevent pushing over right edge
                if obj1.rect.right >= self.width:
                    obj1.rect.right = self.width

            if abs(obj1.rect.bottom - obj2.rect.top) < collision_tolerance:
                obj2.up = False
                obj1.move = False
                obj1.rect.bottom = obj2.rect.top

                # (*) Prevent pushing over bottom edge
                if obj1.rect.top <= 0:
                    obj1.rect.top = 0

            if abs(obj1.rect.top - obj2.rect.bottom) < collision_tolerance:
                obj2.down = False
                obj1.rect.top = obj2.rect.bottom

                # (*)
                if obj1.rect.bottom >= self.height:
                    obj1.rect.bottom = self.height

            obj2.hp -= self.setting.collision_damage
        pass

    # Player Collides Enemy
    def collision_player_enemy(self, collision_tolerance):
        for enemy_x in self.spawn.enemy_group:
            self.collision_two_single_obj(enemy_x, self.player, collision_tolerance)

    # Collision Boss vs Player
    def collision_boss_player(self, collision_tolerance):
        self.collision_two_single_obj(self.spawn.boss, self.player, collision_tolerance)

    # Collision Boss vs Enemy group
    def collision_boss_enemy(self, collision_tolerance):
        for enemy in self.spawn.enemy_group:
            self.collision_two_single_obj(enemy, self.spawn.boss, collision_tolerance)

    #   Enemy Collides Enemy
    def collision_enemy_enemy(self, collision_tolerance):

        for enemy in self.spawn.enemy_group:
            self.spawn.enemy_group.remove(enemy)

            enemy_group_hit = pygame.sprite.spritecollide(enemy, self.spawn.enemy_group, False)

            for enemy_remain in enemy_group_hit:
                enemy.move = False
                enemy_remain.move = False
                # Check impact direction
                if enemy.direction_number == 0:

                    # Check impact tolerance
                    if abs(enemy_remain.rect.left - enemy.rect.right) < collision_tolerance:

                        enemy.rect.right = enemy_remain.rect.left

                    elif abs(enemy_remain.rect.right - enemy.rect.left) < collision_tolerance:
                        enemy.rect.left = enemy_remain.rect.right

                if enemy.direction_number == 1:

                    if abs(enemy_remain.rect.top - enemy.rect.bottom) < collision_tolerance:

                        enemy.rect.bottom = enemy_remain.rect.top

                    elif abs(enemy_remain.rect.bottom - enemy.rect.top) < collision_tolerance:

                        enemy.rect.top = enemy_remain.rect.bottom

            self.spawn.enemy_group.add(enemy)

    # PROJECTILE COLLISION
    # Helper functions
    def enemy_get_hit(self):
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

    def player_get_hit(self):
        # Check collision with normal bullet
        for bullet in self.bullet_group_E:
            if pygame.sprite.collide_rect(bullet, self.player):
                self.bullet_group_E.remove(bullet)
                self.player.hp -= self.setting.bullet_normal

        # Check collision with big bullet from boss
        for bullet in self.bullet_group_B:
            if pygame.sprite.collide_rect(bullet, self.player):
                self.bullet_group_B.remove(bullet)
                self.player.hp -= self.setting.bullet_giant

        # Check collision with gatling guns bullets from boss
        gatling_hit = pygame.sprite.spritecollideany(self.player, self.gatling_group_B)
        if gatling_hit is not None:
            self.gatling_group_B.remove(gatling_hit)
            self.player.hp -= self.setting.bullet_gatling

        # Check collision with laser from boss
        if len(self.laser_group_B) != 0:
            for laser in self.laser_group_B:
                if len(laser.laser_list) != 0:
                    laser_hit = pygame.sprite.spritecollideany(self.player, laser.laser_list)
                    if laser_hit is not None:
                        self.laser_group_B.remove(laser)
                        self.player.hp -= self.setting.bullet_laser

                    count_collide_screen = 0
                    for layer in laser.laser_list:
                        if layer.rect.x <= 0 or layer.rect.x >= self.width or \
                                layer.rect.y <= 0 or layer.rect.y >= self.height:
                            laser.laser_list.remove(layer)
                            count_collide_screen += 1
                    if count_collide_screen == 3:
                        self.laser_group_B.remove(laser)

    def boss_get_hit(self, boss):
        for bullet in self.bullet_group_P:
            if pygame.sprite.collide_rect(boss, bullet):
                self.bullet_group_P.remove(bullet)
                self.spawn.boss.hp -= (self.setting.bullet_normal * 10)

                if self.spawn.boss.hp <= 0:
                    self.setting.boss_spawn = False
                    self.spawn.boss.kill()

    def collision_projectiles(self):
        self.enemy_get_hit()
        self.player_get_hit()
        self.check_player_stats()

        if self.setting.boss_spawn:
            self.boss_get_hit(self.spawn.boss)

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
        # Select a gun before stop time count down
        if self.setting.boss_spawn:
            upper_bound = 3
            if self.spawn.boss.hp <= self.setting.boss_health * 0.5:
                upper_bound = 4

            if self.spawn.boss.move_time == self.setting.boss_movetime:
                self.setting.boss_gun_select = 3  # random.randrange(1, upper_bound)
            # selections: 1 - gbullet, 2 - gatling gun, 3 - laser

            if self.setting.boss_spawn and self.spawn.boss.rect.y >= 0 and \
                    self.spawn.boss.stop_time > 0:

                if self.setting.boss_gun_select == 1 and \
                        self.spawn.boss.stop_time % 200 == 0:
                    self.create_boss_gbullet(self.spawn.boss)

                elif self.setting.boss_gun_select == 2 and \
                        50 <= self.spawn.boss.stop_time <= 300 and \
                        self.spawn.boss.stop_time % 5 == 0:
                    self.create_boss_gatl(self.spawn.boss)

                elif self.setting.boss_gun_select == 3:
                    self.create_boss_laser(self.spawn.boss)

    def create_boss_gbullet(self, boss):
        #   Condition for limit bullet
        if len(self.bullet_group_B) <= 5:
            x_b = boss.rect.x + (56 / 128) * boss.rect.width
            y_b = boss.rect.y + (56 / 128) * boss.rect.height
            self.bullet_group_B.add(BossBullet(x_b, y_b, "giant", boss.direction))
            self.sounds.shootPlayer()

    def create_boss_gatl(self, boss):
        x1_g, x2_g, y1_g, y2_g = 0, 0, 0, 0

        #   Condition for limit gatling bullets
        if len(self.gatling_group_B) <= self.setting.boss_gatling_allow:
            if boss.direction == "up" or boss.direction == "down":
                x1_g = boss.rect.x + (34 / 128) * boss.rect.width
                x2_g = boss.rect.x + (74 / 128) * boss.rect.width
                y1_g = boss.rect.centery
                y2_g = y1_g

            elif boss.direction == "left" or boss.direction == "right":
                y1_g = boss.rect.y + (34 / 128) * boss.rect.width
                y2_g = boss.rect.y + (74 / 128) * boss.rect.width
                x1_g = boss.rect.centerx
                x2_g = x1_g

            bullet_left = BossBullet(x1_g, y1_g, "gatling", boss.direction)
            bullet_right = BossBullet(x2_g, y2_g, "gatling", boss.direction)
            self.gatling_group_B.add(bullet_left)
            self.gatling_group_B.add(bullet_right)
            self.sounds.machineGun()

    def create_boss_laser(self, boss):
        #    Condition for limit bullet
        if self.setting.boss_laser_cooldown <= 0 and boss.stop_time > 250:
            # Keep reset stop time while firing laser
            boss.stop_time = self.setting.boss_stoptime

            if self.setting.boss_laser_chargetime > 0:
                spawn_particles(self.laser_charge_group,
                                self.setting.boss_charge_density,
                                boss)
                self.sounds.chargeSound()
                self.setting.boss_laser_chargetime -= 1

            else:
                self.laser_charge_group.empty()
                if self.setting.boss_laser_time > 0:
                    x_boss, y_boss = 0, 0

                    # Indicate mid-edge positions
                    if boss.direction == 'up':
                        x_boss = boss.rect.midtop[0]
                        y_boss = boss.rect.midtop[1]
                    elif boss.direction == 'down':
                        x_boss = boss.rect.midbottom[0]
                        y_boss = boss.rect.midbottom[1] - 5
                    elif boss.direction == 'left':
                        x_boss = boss.rect.midleft[0]
                        y_boss = boss.rect.midleft[1] - 10
                    elif boss.direction == 'right':
                        x_boss = boss.rect.midright[0]
                        y_boss = boss.rect.midright[1] - 10

                    self.laser_group_B.append(LaserLayers(x_boss, y_boss,
                                                          self.setting.boss_laser_width,
                                                          self.setting.boss_laser_height,
                                                          boss.direction))
                    self.sounds.shootLaser()
                    self.setting.boss_laser_time -= 1

                else:
                    self.laser_group_B.clear()
                    # add reset time
                    self.setting.boss_laser_chargetime = 50
                    self.setting.boss_laser_time = 80
                    self.setting.boss_laser_cooldown = 200
        else:
            self.setting.boss_laser_cooldown -= 1

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
        self.laser_charge_group.update(self.screen)
        remove_particles(self.laser_charge_group, self.spawn.boss)
        update_laser(self.laser_group_B, self.screen)
        self.player.update(self.screen)
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

                #   Turn on Pause Menu or Game-over BG Menu
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
    ai = TankDestroyer()
    ai.main_loop()
