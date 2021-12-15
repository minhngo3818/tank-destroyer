import pygame
from pygame import mixer

pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w, h))

move_sound = mixer.Sound("../sounds/Effects/TankMoving.wav")
move_sound.set_volume(0.4)
track1 = mixer.Sound("sounds/Theme/Battle_IronMan.wav")
track2 = mixer.Sound("sounds/Theme/Boss_ThunderHorse.wav")
channel1 = mixer.Channel(1)
channel2 = mixer.Channel(2)
channel3 = mixer.Channel(3)

run = True
play = True

track = "one"

while run:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				play = True	
				channel1.play(move_sound, -1)


		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				play = False
				channel1.stop()

	pygame.display.flip
	pygame.time.Clock().tick(40)
pygame.quit()