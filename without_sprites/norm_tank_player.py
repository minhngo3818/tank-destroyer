import pygame


class Player:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = 2

        # Movement Set
        self.imgleft = pygame.image.load('images/tank_left_1.png')
        self.imgright = pygame.image.load('images/tank_right_1.png')
        self.imgup = pygame.image.load('images/tank_up_1.png')
        self.imgdown = pygame.image.load('images/tank_down_1.png')
        self.rect = self.imgup.get_rect()

        # Flag
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.standing = True

    def tank_animation(self, win):
        if not (self.standing):
            if self.left:
                win.blit(self.imgleft, (self.pos_x, self.pos_y))
            elif self.right:
                win.blit(self.imgright, (self.pos_x, self.pos_y))
            elif self.up:
                win.blit(self.imgup, (self.pos_x, self.pos_y))
            elif self.down:
                win.blit(self.imgdown, (self.pos_x, self.pos_y))
        else:
            if self.left:
                win.blit(self.imgleft, (self.pos_x, self.pos_y))
            elif self.right:
                win.blit(self.imgright, (self.pos_x, self.pos_y))
            elif self.up:
                win.blit(self.imgup, (self.pos_x, self.pos_y))
            elif self.down:
                win.blit(self.imgdown, (self.pos_x, self.pos_y))
            else:
                win.blit(self.imgup, (self.pos_x, self.pos_y))
