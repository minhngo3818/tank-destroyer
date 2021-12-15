class Stats:
    def __init__(self, access):

        #   Initialize Instances
        self.access = access
        self.setting = access.setting
        self.player = access.player
        self.spawn = access.spawn
        self.score = self.setting.score
        self.highscore = self.setting.high_score

        #   Groups
        self.bulletGroup_P = access.bullet_group_P
        self.bulletGroup_E = access.bullet_group_E
        self.enemyGroup = access.spawn.enemy_group

        self.delayTime = access.setting.delayTime

    def points(self):
        self.score += self.setting.enemy_point

        #   even-100-point-reward
        if self.score % 100 == 0:
            self.player.life += 1

    def reset_life(self):
        self.player.life -= 1
        if self.player.life < 0:
            self.player.hp = 0
        else:
            self.player.hp = self.setting.player_health

    def reset_game(self):
        #   Reset Player Elements
        self.player.life = self.setting.player_life
        self.player.hp = self.setting.player_health
        self.player.index = 0
        self.player.direction = "up"
        self.player.rect.center = self.access.screen_rect.center

        self.setting.boss_spawn = False

        #   Reset Game Stats
        self.setting.level = 1
        self.score = 0

        #   Remove All Elements in Groups
        for bullet in self.bulletGroup_E:
            self.bulletGroup_E.remove(bullet)
        for bullet in self.bulletGroup_P:
            self.bulletGroup_P.remove(bullet)
        for enemy in self.enemyGroup:
            self.enemyGroup.remove(enemy)
        for boss in self.spawn.boss_group:
            self.spawn.boss_group.remove(boss)


