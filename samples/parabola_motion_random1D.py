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

	def reset_position(self):
		self.x = self.resetX
		self.y = self.resetY

	def draw_circle(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


"""	
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
"""


class ParaBall(Ball):

	def __init__(self, x, y, radius, color, target_circle):
		Ball.__init__(self, x, y, radius, color)
		self.target_circle = target_circle
		self.center_x = self.target_circle.x
		self.center_y = self.y
		self.horiz_dist = abs(self.x - self.target_circle.x)
		self.vrt_dist = abs(self.y - self.target_circle.y)
		self.speed = 2

	def pos_update(self):
		if self.vrt_dist > 0 and self.horiz_dist > 0:
			self.x += self.speed
			self.y = self.center_y - self.vrt_dist * math.sqrt(abs(1 - ((self.x - self.center_x)/ self.horiz_dist)**2))
		# Same x/y position with target
		elif self.vrt_dist != 0 and self.horiz_dist == 0:
			self.y -= self.speed
		elif self.horiz_dist != 0 and self.vrt_dist == 0:
			self.x += self.speed


# Function spawn_balls()
# Create a list of ball
# Parameters: a tuple of position x range,
# 	position y, number of balls, color
# Return: a list of circles
def spawn_circles(range_x, pos_y, num_of_ball, color, target):
	circle_list = []
	for i in range(num_of_ball):
		circle_list.append(ParaBall(random.randrange(
			range_x[0], range_x[1]), pos_y, 10, color, target))
	return circle_list


# Function ellipse_move()
# Check and update position of circles in parabolic movement
# Parameters: a list of circles, a circle target object
# Return: a boolean of movement
def ellipse_move(circle_list):
	for circle in circle_list:
		circle.pos_update()


def check_limit(circle_list):
	for circle in circle_list:
		if circle.x >= circle.target_circle.x:
			circle.reset_position()


# Function draw_circles
def draw_circles(circle_list, win):
	for circle in circle_list:
		circle.draw_circle(win)


# Main function
def main():

	# Game Display
	pygame.init()
	win = pygame.display.set_mode((scr_width, scr_height))
	pygame.display.set_caption('Parabola Motion')

	# Game FPS
	clock = pygame.time.Clock()
	fps = 60

	# Initialize list of ball
	target = Ball(500, 100, 10, (0, 255, 255))
	circle_list = spawn_circles((200, 500), 300, 25, (250, 0, 255), target)

	# Initialize stats
	run = True
	move = False

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				move = True

		if move:
			ellipse_move(circle_list)
			check_limit(circle_list)

		win.fill((0,0,0))
		target.draw_circle(win)
		draw_circles(circle_list, win)
		clock.tick(fps)
		pygame.display.flip()

	pygame.quit()


if __name__ == '__main__':
	main()
