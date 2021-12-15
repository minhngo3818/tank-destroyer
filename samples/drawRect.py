import pygame


pygame.init()	
width, height = 800, 560
screen = pygame.display.set_mode((width, height))
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	pygame.draw.rect(screen, (255,255,255), (100,100,100,100), 5)
	pygame.display.flip()