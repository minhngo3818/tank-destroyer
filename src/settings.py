class Settings:
    def __init__(self):
        #   Gameplay
        self.scr_width = 1120
        self.scr_height = 630
        self.FPS = 80
        self.delayTime = 500
        self.frame_rate = 0.3

        #   Player
        self.player_health = 2
        self.player_speed = 2
        self.player_life = 2
        self.collision_damage = 0.001

        # Enemy
        self.enemy_health1 = 10
        self.enemy_health2 = 50
        self.enemy_speed = 3
        self.stop_time = 200
        self.start_time = 0
        self.move_time = 50
        self.enemy_limit = 3
        self.spawn_time = 120

        #   Boss
        self.boss_speed = 2
        self.boss_health = 1000
        self.boss_laser_speed = 50
        self.boss_gatling_speed = 50
        self.boss_gatling_allow = 6
        self.boss_gatling_damage = 2
        self.boss_cannon_speed = 10
        self.boss_cannon_damage = 20
        self.boss_laser_damage = 1
        self.boss_charge_particle_speed = 2
        self.boss_charge_density = 10
        self.boss_cooldown = 200
        self.boss_laser_time = 80
        self.boss_laser_chargetime = 50
        self.boss_stoptime = 200
        self.boss_movetime = 50
        self.boss_starttime = 0

        #   Scoreboard
        self.level = 1
        self.score = 0
        self.high_score = 0
        self.enemy_point = 1
        self.boss_point = 50

        #   Bullet
        self.bullet_speed = 10
        self.bullet_allowed = 5

        #   Colors
        self.blue = (0, 128, 255)
        self.blue_steel = (80, 130, 180)
        self.red = (255, 0, 0)
        self.red_med = (255, 65, 65)
        self.red_lite = (255, 170, 170)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.gray = (96, 96, 96)
        self.gray_light = (160, 160, 160)
        self.gray_stale = (119, 136, 150)

        #   Flags
        self.run_game = False
        self.game_on = False
        self.menu_on = True
        self.pause_on = False
        self.gameover_on = False

        self.boss_spawn = False

        #   Menus Option Amounts
        self.amountOptionMain = 2
        self.amountOptionPause = 3
        self.amountOptionGameOver = 2

