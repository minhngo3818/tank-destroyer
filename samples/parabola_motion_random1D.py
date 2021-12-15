"""Projectile Parabola Motion Testing

@author Minh Ngo
@date 09/11/2021
@version 2
@file projectile_parabola_motion.py

Description: The code will display the parabola motions 
by randoms points. All objects will gather at target point. 
Spawn random area is the rectangle area below the target point.

"""

import pygame
import math
import random


# Stats

	# Screen stats
scr_height = 500
scr_width = 800

	# Motion stats
ACCELERATION = 3.5

class Ball:
	def __init__(self, x, y, radius, color):
		self.x = x
		self.y = y
		self.resetX = x
		self.resetY = y
		self.radius = radius
		self.color = color


	def resetPosition(self):
		self.x = self.resetX
		self.y = self.resetY


	def posUpdate(self, time, verDist, horDist, centerX, centerY):
		
		if verDist != 0 and horDist != 0:
			self.x += time
			if 0 < verDist <= horDist:		# 	b < a in elipse equation
				self.y = centerY - verDist * math.sqrt(abs(1 - ((self.x - centerX)**2 / horDist**2)))
			elif 0 < horDist < verDist: 						# 	a < b and include cirle case
				self.y = centerY - horDist * math.sqrt(abs(1 - ((self.x - centerX)**2 / verDist**2)))

		# Same x/y position with target
		elif verDist != 0 and horDist == 0:
			self.y -= time
		elif horDist != 0 and verDist == 0:
			self.x += time


	def drawCircle(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)



def estDistance(pos1, pos2):
	return abs(pos1 - pos2)


# Main function
def main():

	# Game Display
	pygame.init()
	win = pygame.display.set_mode((scr_width,scr_height))
	pygame.display.set_caption('Parabola Motion')

	# Game FPS
	clock = pygame.time.Clock()
	fps = 60

	ball1 = Ball(100, 400, 10, (255, 0, 255))			# magneta ball
	ball2 = Ball(200, 400, 10, (255, 255, 0))			# yellow ball
	ball3 = Ball(500, 400, 10, (0, 100, 255))			# blue ball
	ball4 = Ball(200, 100, 10, (255, 100, 100))			# Orange
	target = Ball(500, 100, 10, (0, 255,255))
	
	#Calculate distance between balls and target ball
	verDist1 = estDistance(ball1.y, target.y)
	horDist1 = estDistance(ball1.x, target.x)

	verDist2 = estDistance(ball2.y, target.y)
	horDist2 = estDistance(ball2.x, target.x)

	verDist3 = estDistance(ball3.y, target.y)   # On vertical line with target
	horDist3 = estDistance(ball3.x, target.x)  

	verDist4 = estDistance(ball4.y, target.y)   # On horizontal line with target
	horDist4 = estDistance(ball4.x, target.x)


	# Find center of Elipse
	centerX = target.x
	centerY = ball1.y

	# Initialize stats
	run = True          # A boolean to run loop
	speed = 5
	angle = 0
	move = False

	while run:

		# Setup reset position


		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				move = True
		
		if move == True:
			if (ball1.x <= target.x or ball2.x <= target.x):
				ball1.posUpdate(speed, verDist1, horDist1, centerX, centerY)
				ball2.posUpdate(speed, verDist2, horDist2, centerX, centerY)
				ball3.posUpdate(speed, verDist3, horDist3, centerX, centerY)
				ball4.posUpdate(speed, verDist4, horDist4, centerX, centerY)
			else:
				ball1.resetPosition()
				ball2.resetPosition()
				ball3.resetPosition()
				ball4.resetPosition()
				move = False		


		win.fill((0,0,0))

		ball1.drawCircle(win)
		ball2.drawCircle(win)
		ball3.drawCircle(win)
		ball4.drawCircle(win)
		target.drawCircle(win)
		clock.tick(fps)
		pygame.display.flip()


	pygame.quit()

if __name__ == '__main__':
	main()
