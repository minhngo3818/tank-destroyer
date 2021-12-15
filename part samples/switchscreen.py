import pygame
from pygame import mixer
colours = {"white": (255,255,255), "black": (0,0,0), "red": (255,0,0), "green": (0,255,0), "magneta": (255,255, 0)}

class Screen():
	def __init__(self, title, fill):
		self.title = title
		self.width = 800
		self.height = 500
		self.fill = fill
		self.current = False

	def makeCurrent(self):
		pygame.display.set_caption(self.title)
		self.current = True
		self.screen = pygame.display.set_mode((self.width, self.height))

	def endCurrent(self):
		self.current = False
		return self.current

	def checkUpdate(self):
		return self.current

	def screenUpdate(self):
		if self.current:
			self.screen.fill(self.fill)

	def returnTitle(self):
		return self.screen

class Button():
	def __init__(self, x, y, sx, sy, bcolor, fbcolor, font, fontsize, fcolor, text):
		self.x = x
		self.y = y
		self.sx = sx
		self.sy = sy
		self. bcolor = bcolor
		self.fbcolor = fbcolor
		self.fcolor = fcolor
		self.fontsize = fontsize
		self.text = text
		self.current = False
		self.button = pygame.font.SysFont(font, fontsize)


	def showButton(self, display):
		if self.current:
			pygame.draw.rect(display, self.fbcolor, (self.x, self.y, self.sx, self.sy))

		else:
			pygame.draw.rect(display, self.bcolor, (self.x, self.y, self.sx, self.sy))

		textsurface = self.button.render(self.text, False, self.fcolor)
		display.blit(textsurface, (self.x + (self.sx/2) - (self.fontsize/2)*(len(self.text)/2) -5, self.y + (self.sy/2) - (self.fontsize/2) - 4))

	def focusCheck(self, mousepos, mouseclick):
		if (mousepos[0] >= self.x and mousepos[0] <= self.x + self.sx and mousepos[1] >= self.y and mousepos[1] <= self.y + self.sy):
			self.current = True
			return mouseclick[0]

		else:
			self.current = False
			return False

pygame.init()
pygame.font.init()

menuScreen = Screen("Menu", colours["white"])
gameonScreen = Screen("Gameon", colours["black"])


win = menuScreen.makeCurrent()

testButton = Button(0,0, 150, 50, colours["black"], colours["red"], "arial", 20, colours["white"], "Test")
returnButton = Button(100,100, 150, 50, colours["white"], colours["green"], "arial", 20, colours["black"], "Return")

toggle = False

done = False

while not done:
	menuScreen.screenUpdate()
	gameonScreen.screenUpdate()
	mouse_pos = pygame.mouse.get_pos()
	mouse_click = pygame.mouse.get_pressed()
	keys = pygame.key.get_pressed()

	
	if menuScreen.checkUpdate():
		screen2button = testButton.focusCheck(mouse_pos, mouse_click)
		testButton.showButton(menuScreen.returnTitle())

		if screen2button:
			win = gameonScreen.makeCurrent()
			mixer.music.stop()
			menuScreen.endCurrent()


	elif gameonScreen.checkUpdate():
		returnm = returnButton.focusCheck(mouse_pos, mouse_click)
		returnButton.showButton(gameonScreen.returnTitle())

		if returnm:
			win = menuScreen.makeCurrent()
			mixer.music.stop()
			gameonScreen.endCurrent()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	pygame.display.update()
	pygame.time.Clock().tick(80)


pygame.quit()











