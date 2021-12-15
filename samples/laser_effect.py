import pygame
from pygame.sprite import Sprite

pygame.init()
width, height = 800, 450
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Test Laser Effect")


class Laser(Sprite):
	"""docstring for Laser"""
	def __init__(self, x, y, w, h, color):
		super().__init__()

		self.w = w
		self.h = h
		self.surface = pygame.Surface((w, h))
		self.surface.fill(color)
		self.rect = self.surface.get_rect()
		self.x = x - w/2
		self.y = y

	def update(self, screen):
		self.y -= 50

		screen.blit(self.surface, (self.x, self.y))

box = pygame.Surface((50,50))
box.fill((0,255,255))
box_rect = box.get_rect()
box_rect.x = 375
box_rect.y = 350


laser_group = pygame.sprite.Group()
shoot_laser = 100
cooldown = 100
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	#keys = pygame.key.get_pressed()
	#if keys[pygame.K_SPACE]:
	if cooldown == 0:
		
		outer_laser = Laser(400, 350, 50, 50, (255,0,255))
		laser_group.add(outer_laser)
		middle_laser = Laser(400, 350, 40, 50, (255,102,255))
		laser_group.add(middle_laser)
		inner_laser = Laser(400, 350, 20, 50, (255,255,255))
		laser_group.add(inner_laser)
		shoot_laser -= 1
		if shoot_laser == 0:
			cooldown = 100
			shoot_laser = 200
	elif cooldown > 0:
		cooldown -= 1


	for l in laser_group:
		if l.rect.y == -1:
			laser_group.remove(l)

	screen.fill((0,0,0))
	laser_group.update(screen)
	screen.blit(box, (box_rect.x, box_rect.y))
	pygame.display.flip()
	pygame.time.Clock().tick(80)

pygame.quit()

		