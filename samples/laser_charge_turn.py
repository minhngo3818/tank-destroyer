import pygame
import random
from pygame.sprite import Sprite

#	Set-up
pygame.init()
width, height = 800, 540
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Test Laser + Charge Turn")


#	Classes
class Square(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.cube = pygame.Surface((50, 50))
        self.cube.fill((0, 255, 255))
        self.rect = self.cube.get_rect()
        self.direction = "up"

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def update(self):
        if self.up and self.rect.y >= 0:
            self.direction = "up"
            self.rect.y -= 5
        elif self.down and self.rect.y <= self.screen_rect.height:
            self.direction = "down"
            self.rect.y += 5
        elif self.left and self.rect.x >= 0:
            self.direction = "left"
            self.rect.x -= 5
        elif self.right and self.rect.x <= self.screen_rect.width:
            self.direction = "right"
            self.rect.x += 5

        self.screen.blit(self.cube, (self.rect.x, self.rect.y))


class Laser(Sprite):
    def __init__(self, screen, lx, ly, lw, lh, ldir):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = lw  # laser width
        self.height = lh  # laser height
        self.dir = ldir  # direction signals
        self.laser = pygame.Surface((self.width, self.height))
        self.laser.fill((66, 245, 147))
        self.rect = self.laser.get_rect()
        self.rect.x = lx  # laser x-pos
        self.rect.y = ly  # laser y-pos

    def update(self):

        angle = 0
        if self.dir == "up":
            angle = 0
            self.rect.y -= 20
        elif self.dir == "down":
            angle = 180
            self.rect.y += 20
        elif self.dir == "left":
            angle = 90
            self.rect.x -= 20
        elif self.dir == "right":
            angle = 270
            self.rect.x += 20

        if (self.rect.x <= 0 or self.rect.x >= self.screen_rect.width
                or self.rect.y <= 0 or self.rect.y >= self.screen_rect.height):
            self.kill()

        rotate_image = pygame.transform.rotate(self.laser, angle)
        rotate_rect = rotate_image.get_rect(center=self.laser.get_rect(center=(self.rect.x, self.rect.y)).center)

        # Get the rectangle of rotated image and set the center
        # of original rectangle of the image
        # return the new rotated image and new position

        self.screen.blit(rotate_image, (rotate_rect.x, rotate_rect.y))


class LaserCharge(Sprite):
    def __init__(self, screen, x, y, x_gather, y_gather, direction):
        super().__init__()
        self.screen = screen
        self.dust = pygame.Surface((10, 10))
        self.dust.fill((173, 3, 252))
        self.rect = self.dust.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_gather = x_gather
        self.y_gather = y_gather
        self.direction = direction
        self.speed = 1  # if less than 1 case up and left cannot work

    def destroy(self):
        if ((self.direction == "up" and self.rect.y >= self.y_gather - 20) or
                (self.direction == "down" and self.rect.y <= self.y_gather + 20) or
                (self.direction == "left" and self.rect.x >= self.x_gather - 20) or
                (self.direction == "right" and self.rect.x <= self.x_gather + 20)):
            self.kill()

    def update(self):
        dx = self.x_gather - self.rect.x
        dy = self.y_gather - self.rect.y

        # Error: gather position does not update when the object moves !!!!
        # If the object stop, it cause no problem

        # Method 1 - Diagonal movement
        if dx < 0:
            self.rect.x -= self.speed  # max(self.dx, -2)
        else:
            self.rect.x += self.speed  # min(self.dx, 2)

        if dy < 0:
            self.rect.y -= self.speed  # max(self.dy, -2)
        else:
            self.rect.y += self.speed  # min(self.dy, 2)

        self.destroy()

        # Method 2 - Parabola movement
        # ......

        self.screen.blit(self.dust, (self.rect.x, self.rect.y))


# Initializing Section
run = True
host = Square(screen)

laserGroup = pygame.sprite.Group()
chargeGroup = pygame.sprite.Group()

density = 10


# Function

# Problem: Initialize random start pos of charge effect
# Problem: Initialize start pos of Laser depending on Object
# Problem: Time count set-up, laser trigger.


def ChargeArea(direction):
    pos_x = 0
    pos_y = 0
    pos_gather_x = 0
    pos_gather_y = 0

    # Issue:
    # reason 2:

    if direction == "up":
        pos_x = random.randrange(host.rect.x - 50, host.rect.x + 100)
        pos_y = random.randrange(host.rect.y - 50, host.rect.y - 10)
        (pos_gather_x, pos_gather_y) = host.rect.midtop

    elif direction == "down":
        pos_x = random.randrange(host.rect.x - 50, host.rect.x + 100)
        pos_y = random.randrange(host.rect.y + 50, host.rect.y + 100)
        (pos_gather_x, pos_gather_y) = host.rect.midbottom

    elif direction == "left":
        pos_x = random.randrange(host.rect.x - 50, host.rect.x - 10)
        pos_y = random.randrange(host.rect.y - 50, host.rect.y + 100)
        (pos_gather_x, pos_gather_y) = host.rect.midleft

    elif direction == "right":
        pos_x = random.randrange(host.rect.x + 50, host.rect.x + 100)
        pos_y = random.randrange(host.rect.y - 50, host.rect.y + 100)
        (pos_gather_x, pos_gather_y) = host.rect.midright

    for i in range(density):
        chargeGroup.add(LaserCharge(screen, pos_x, pos_y, pos_gather_x, pos_gather_y, direction))


# Run Section
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                host.up = True
            elif event.key == pygame.K_DOWN:
                host.down = True
            elif event.key == pygame.K_LEFT:
                host.left = True
            elif event.key == pygame.K_RIGHT:
                host.right = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                host.up = False
            elif event.key == pygame.K_DOWN:
                host.down = False
            elif event.key == pygame.K_LEFT:
                host.left = False
            elif event.key == pygame.K_RIGHT:
                host.right = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        ChargeArea(host.direction)
        # chargeGroup.empty()
        laser = Laser(screen, host.rect.centerx, host.rect.centery, 5, 20, host.direction)
        laserGroup.add(laser)
    else:
        chargeGroup.empty()

    for c in chargeGroup:
        if (c.rect.x == (host.rect.left + 10) or c.rect.x == host.rect.right
                or c.rect.y == (host.rect.top + 10) or c.rect.y == host.rect.bottom):
            chargeGroup.remove(c)

    # Update Section
    screen.fill((0, 0, 0))
    host.update()
    laserGroup.update()
    chargeGroup.update()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
