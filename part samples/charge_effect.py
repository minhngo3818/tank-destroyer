import pygame, random, math
from pygame.sprite import Sprite


#	Phrase 1: Charge Effect with random particles in an area
#	Phrase 2: Change Effect with random particle in an remained area

pygame.init()

width = 800
height = 450
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()
print(screen_rect.centerx)
print(screen_rect.centery)
pygame.display.set_caption("Test Canon Charge Effect")


class Area(Sprite):	# Range of randomized particles that are created

	def __init__(self, screen):
		super().__init__()

		self.screen = screen
		self.screen_rect = screen.get_rect()

		self.area = pygame.Surface((100, 100))
		self.area.fill((0, 255, 255))
		self.area_rect = self.area.get_rect()
		self.area_rect.x = self.screen_rect.centerx - self.area_rect.width//2
		self.area_rect.y = self.screen_rect.centery - self.area_rect.height//2

	def display(self):
		self.screen.blit(self.area, (self.area_rect.x, self.area_rect.y))

class Particle(Sprite):
	def __init__(self, x, y, screen):
		super().__init__()

		self.screen = screen

		self.particle = pygame.Surface((5,5))
		self.particle.fill((255, 0, 255))
		self.particle_rect = self.particle.get_rect()
		self.particle_rect.x = x
		self.particle_rect.y = y

	def update(self, screen):
		self.dx = 400- self.particle_rect.x
		self.dy = 225 - self.particle_rect.y

		#dist = math.hypot(dx, dy)
		#anglex = dx/dist
		#angley = dy/dist
		if self.dx <= 0:
			self.particle_rect.x += max(self.dx, -2)
		elif self.dx > 0:
			self.particle_rect.x += min(self.dx, 2)

		if self.dy <= 0:
			self.particle_rect.y += max(self.dy, -2)
		elif self.dy > 0:
			self.particle_rect.y += min(self.dy, 2)

		screen.blit(self.particle, (self.particle_rect.x, self.particle_rect.y))


area = Area(screen)
particle_group = pygame.sprite.Group()
run = True

while run:
 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	#keys = pygame.key.get_pressed()
	#if keys[pygame.K_SPACE]:
	for n in range(5):		#	50 particles are created simultaneously
		a = random.randrange(350, 450)
		b = random.randrange(175, 200)
		particle1 = Particle(a, b, screen)
		particle_group.add(particle1)
	

	for p in particle_group:
		if 395- p.particle_rect.x - 5 == 0 and 220 - p.particle_rect.y - 5 == 0:
			particle_group.remove(p)


	screen.fill((0,0,0))
	area.display()
	particle_group.update(screen)
	pygame.display.flip()
	pygame.time.Clock().tick(80)

pygame.quit()
