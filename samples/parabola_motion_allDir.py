"""Projectile Parabolic Motion Testing

@author Minh Ngo
@date 12/26/2021
@version 3
@file parabola_motion_allDir.py

Description:

"""
import pygame
from pygame.sprite import Sprite
import math
import random

# Stats

# Screen stats
scr_height = 500
scr_width = 800


class Square(Sprite):
	def __init__(self, screen):
		super().__init__()
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		self.cube = pygame.Surface((50, 50))
		self.cube.fill((0, 255, 255))
		self.rect = self.cube.get_rect()
		self.direction = 'left'

		self.rect.centerx = self.screen_rect.centerx
		self.rect.centery = self.screen_rect.centery

		self.left = False
		self.right = False
		self.up = False
		self.down = False

	def update(self):
		if self.up and self.rect.y >= 0:
			self.direction = 'up'
			self.rect.y -= 5
		elif self.down and self.rect.y <= self.screen_rect.height:
			self.direction = 'down'
			self.rect.y += 5
		elif self.left and self.rect.x >= 0:
			self.direction = 'left'
			self.rect.x -= 5
		elif self.right and self.rect.x <= self.screen_rect.width:
			self.direction = 'right'
			self.rect.x += 5

		self.screen.blit(self.cube, (self.rect.x, self.rect.y))


class Ball(Sprite):
	def __init__(self, x, y, color):
		Sprite.__init__(self)
		self.radius = 10
		self.surface = pygame.Surface((self.radius * 2, self.radius * 2))
		self.rect = self.surface.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.resetX = x
		self.resetY = y
		self.color = color

	def reset_position(self):
		self.rect.x = self.resetX
		self.rect.y = self.resetY

	def draw_circle(self, win):
		pygame.draw.circle(win, self.color, (self.rect.x, self.rect.y), self.radius)


class ParaBall(Ball):

	def __init__(self, win, x, y, color, target_x, target_y, direction):
		super().__init__(x, y, color)
		self.target_x = target_x
		self.target_y = target_y
		self.direction = direction
		self.screen = win
		self.speed = 3

	# Helper functions for update() aka position update
	# Helper function: updates linear x or y for horizontal or vertical tendencies
	def _left_right_y_update(self):
		if self.rect.y < self.target_y:
			self.rect.y += self.speed
		else:
			self.rect.y -= self.speed

	def _up_down_x_update(self):
		if self.rect.x < self.target_x:
			self.rect.x += self.speed
		else:
			self.rect.x -= self.speed

	# Helper functions: different direction cases
	def _move_left(self, dx, dy):
		para_center = (self.rect.x, self.target_y)		# center(x,y) of parabolic
		self._left_right_y_update()

		self.rect.x = para_center[0] - abs(dx) * math.sqrt(
				abs(1 - ((self.rect.y - para_center[1]) / abs(dy))**2))

	def _move_right(self, dx, dy):
		para_center = (self.rect.x, self.target_y)
		self._left_right_y_update()

		self.rect.x = para_center[0] + abs(dx) * math.sqrt(
			abs(1 - ((self.rect.y - para_center[1]) / abs(dy)) ** 2))

	def _move_up(self, dx, dy):
		para_center = (self.target_x, self.rect.y)
		self._up_down_x_update()

		self.rect.y = para_center[1] - abs(dy) * math.sqrt(
			abs(1 - ((self.rect.x - para_center[0]) / abs(dx)) ** 2))

	def _move_down(self, dx, dy):
		para_center = (self.target_x, self.rect.y)
		self._up_down_x_update()

		self.rect.y = para_center[1] + abs(dy) * math.sqrt(
			abs(1 - ((self.rect.x - para_center[0]) / abs(dx)) ** 2))

	# Position update function
	def update(self):
		dx = self.rect.x - self.target_x
		dy = self.rect.y - self.target_y

		if abs(dx) > 0 and abs(dy) > 0:
			if self.direction == 'up':
				self._move_up(dx, dy)
			elif self.direction == 'down':
				self._move_down(dx, dy)
			elif self.direction == 'left':
				self._move_left(dx, dy)
			elif self.direction == 'right':
				self._move_right(dx, dy)

		elif dx < 0 and dy == 0:
			self.rect.x += self.speed
		elif dx > 0 and dy == 0:
			self.rect.x -= self.speed
		elif dx == 0 and dy < 0:
			self.rect.y += self.speed
		elif dx == 0 and dy > 0:
			self.rect.y -= self.speed

		self.draw_circle(self.screen)


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
	player = Square(win)
	target = Ball(player.rect.centerx, player.rect.centery, (0, 255, 255))
	charge_group = pygame.sprite.Group()

	# Initialize stats
	run = True
	move = False

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				move = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.left = True
				elif event.key == pygame.K_RIGHT:
					player.right = True
				elif event.key == pygame.K_UP:
					player.right = True
				elif event.key == pygame.K_DOWN:
					player.right = True


	win.fill((0, 0, 0))
	target.draw_circle(win)

	clock.tick(fps)
	pygame.display.flip()

	pygame.quit()


if __name__ == '__main__':
	main()
