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


class ParaBall:
	def __init__(self, x, y, radius, color):
		self.x = x
		self.y = y
		self.resetX = x
		self.resetY = y
		self.radius = radius
		self.color = color

	def reset_position(self):
		self.x = self.resetX
		self.y = self.resetY

	def pos_update(self, speed, verDist, horDist, centerX, centerY):
		
		if verDist != 0 and horDist != 0:
			self.x += speed
			if 0 < verDist <= horDist:		# 	b < a in elipse equation
				self.y = centerY - verDist * math.sqrt(abs(1 - ((self.x - centerX)**2 / horDist**2)))
			elif 0 < horDist < verDist: 						# 	a < b and include cirle case
				self.y = centerY - horDist * math.sqrt(abs(1 - ((self.x - centerX)**2 / verDist**2)))

		# Same x/y position with target
		elif verDist != 0 and horDist == 0:
			self.y -= speed
		elif horDist != 0 and verDist == 0:
			self.x += speed

	def draw_circle(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def estDistance(pos1, pos2):
	return abs(pos1 - pos2)


# Function spawn_balls()
# Create a list of ball
# Parameters: a tuple of position x range,
# 	position y, number of balls, color
# Return: a list of circles
def spawn_circles(range_x, pos_y, num_of_ball, color):
	circle_list = []
	for _ in num_of_ball:
		circle_list.append(ParaBall(random.randrange(
			range_x[0], range_x[1]), pos_y, 10, color))
	return circle_list
	pass


# Function ellipse_move()
# Check and update position of circles in parabolic movement
# Parameters: a list of circles, a circle target object
# Return: a boolean of movement
def ellipse_move(circle_list, target):
	move = True
	for circle in circle_list:
		if circle.x <= target.x:
			circle.pos_update()
		else:
			circle.reset_position()
	return move
	pass


# Function draw_circles
def draw_circles(circle_list, win):
	for circle in circle_list:
		circle.draw_circle(win)
	pass


# Main function
def main():

	# Game Display
	pygame.init()
	win = pygame.display.set_mode((scr_width, scr_height))
	pygame.display.set_caption('Parabola Motion')

	# Game FPS
	clock = pygame.time.Clock()
	fps = 60

	ball1 = ParaBall(100, 400, 10, (255, 0, 255))			# magneta ball
	ball2 = ParaBall(200, 400, 10, (255, 255, 0))			# yellow ball
	ball3 = ParaBall(500, 400, 10, (0, 100, 255))			# blue ball
	ball4 = ParaBall(200, 100, 10, (255, 100, 100))			# Orange
	target = ParaBall(500, 100, 10, (0, 255,255))
	
	# Calculate distance between balls and target ball
	verDist1 = estDistance(ball1.y, target.y)
	horDist1 = estDistance(ball1.x, target.x)

	verDist2 = estDistance(ball2.y, target.y)
	horDist2 = estDistance(ball2.x, target.x)

	verDist3 = estDistance(ball3.y, target.y)   # On vertical line with target
	horDist3 = estDistance(ball3.x, target.x)  

	verDist4 = estDistance(ball4.y, target.y)   # On horizontal line with target
	horDist4 = estDistance(ball4.x, target.x)

	# Find center of Ellipse
	centerX = target.x
	centerY = ball1.y

	# Initialize stats
	run = True          # A boolean to run loop
	speed = 5
	angle = 0
	move = False

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				move = True

		if move:
			if ball1.x <= target.x or ball2.x <= target.x:
				ball1.pos_update(speed, verDist1, horDist1, centerX, centerY)
				ball2.pos_update(speed, verDist2, horDist2, centerX, centerY)
				ball3.pos_update(speed, verDist3, horDist3, centerX, centerY)
				ball4.pos_update(speed, verDist4, horDist4, centerX, centerY)
			else:
				ball1.reset_position()
				ball2.reset_position()
				ball3.reset_position()
				ball4.reset_position()
				move = False		

		win.fill((0,0,0))

		ball1.draw_circle(win)
		ball2.draw_circle(win)
		ball3.draw_circle(win)
		ball4.draw_circle(win)
		target.draw_circle(win)
		clock.tick(fps)
		pygame.display.flip()

	pygame.quit()


if __name__ == '__main__':
	main()
