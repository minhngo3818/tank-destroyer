"""Projectile Motion for Gravity Motion 

@author MinhNgo
@date 06/03/2021
@version 1
@file projectile_gravity_motion.py

Reference: TechwithTime

"""

import pygame
import math

pygame.init()
width, height = 1000, 500;
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Projectile Motion")

class Ball:
	def __init__(self, x, y, radius, color):
		self.x = x
		self.y = y 
		self.radius = radius 
		self.color = color

	def drawCircle(self, screen):

		# Draw a circle 
		pygame.draw.circle(screen, (0, 255,0), (self.x, self.y), self.radius)
		
		# Draw a filled circle with a shorter radius by 1 pixel
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius - 1)

	def ballPath(self, start_x, start_y, power, ang, time):
		velX = math.cos(angle) * power
		velY = math.sin(angle) * power

		distX = velX * time
		distY = velY * time + ((-9.81 * (time**2) )/2)

		newX = round(distX + start_x)
		newY = round(start_y - distY)

		return (newX, newY)
		

run = True
x, y = 0,0
time = 0
power = 0
angle = 0
shoot = False

ball = Ball(300, 450, 10, (255,0,0))

def findAngle(pos):
	sX = ball.x 
	sY = ball.y 

	try:
		angle = math.atan( (sY - pos[1]) / (sX - pos[0]))
	except:	# catch undefine tangent
		angle = math.pi/2

	# TR trig circle
	if pos[1] < sY and pos[0] > sX:
		angle = abs(angle)

	# TL trig circle
	elif pos[1] < sY and pos[0] < sX:
		angle = math.pi - angle

	# BL trig circle
	elif pos[1] > sY and pos[0] < sX:
		angle = math.pi + abs(angle)

	# BR trig circle
	elif pos[1] > sY and pos[0] > sX:
		angle = math.pi * 2 - angle

	return angle

def redDraw():
	screen.fill((0,0,0))
	ball.drawCircle(screen)
	pygame.draw.line(screen, (255,255,255), line[0], line[1])
	pygame.draw.line(screen, (70, 245, 129), (0, 450 + 10), (width, 450 + 10))
	pygame.display.flip()
	pygame.time.Clock().tick(88)

while run:

	if shoot:
		if ball.y < 460:
			time += 0.05
			po = ball.ballPath(x, y, power, angle, time)
			ball.x = po[0]
			ball.y = po[1]
		else:
			shoot = False
			ball.y = 450

	pos = pygame.mouse.get_pos()
	line = [(ball.x, ball.y), pos]
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = false

		if event.type == pygame.MOUSEBUTTONDOWN:
			if shoot == False:
				shoot = True
				x = ball.x 
				y = ball.y 
				time = 0 
				power = math.sqrt( (line[1][1] - line[0][1])**2 + (line[1][0] - line[0][0])**2)/7
				angle = findAngle(pos)
	redDraw()

pygame.quit()	
