#sprite classes
import pygame as pg
import numpy as np
from settings import *

class Player(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((30, 40))
		self.image.fill(USERCOLOR)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT/2)

		#movement [x, y]
		self.pos = np.array([WIDTH/2, HEIGHT/2], dtype = np.float64)
		self.vel = np.array([0, 0], dtype = np.float64)
		self.acc = np.array([0, 0], dtype = np.float64)
		self.extraJumps = 1

		#reference to game
		self.game = game

	def update(self):
		self.acc = np.array([0, PLAYER_GRAVITY], dtype = np.float64)
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.acc[0] = -(PLAYER_ACC)
		if keys[pg.K_RIGHT]:
			self.acc[0] = PLAYER_ACC

		#add in friction
		self.acc[0] += self.vel[0] * PLAYER_FRICTION	
		#omg some actual physics!
		self.vel += self.acc
		if (-1 < self.vel[0] < 1):
			self.vel[0] = 0

		self.pos[0] += self.vel[0] + (0.5*self.acc[0])
		self.rect.midbottom = self.pos
		self.collision('x')
		self.pos[1] += self.vel[1] + (0.5*self.acc[1])
		self.rect.midbottom = self.pos
		self.collision('y')

		#wrap around screen
		# if (self.pos[0] > WIDTH):
		# 	self.pos[0] = 0
		# elif (self.pos[0] < 0):
		# 	self.pos[0] = WIDTH

		self.rect.midbottom = self.pos

	def collision(self, dir):
		if (dir == 'x'):
			hits = False
			hits = pg.sprite.spritecollide(self, self.game.platforms, False)
			if hits:
				if self.vel[0] > 0: #moving right
					self.pos[0] = hits[0].rect.left - self.rect.width/2
				if self.vel[0] < 0: #moving left
					self.pos[0] = hits[0].rect.right + self.rect.width/2
				self.vel[0] = 0
				self.rect.x = self.pos[0]
		if (dir == 'y'):
			hits = pg.sprite.spritecollide(self, self.game.platforms, False)
			if hits:
				if self.vel[1] > 0: #moving down
					self.pos[1] = hits[0].rect.top
					self.extraJumps = 1
				if self.vel[1] < 0: #moving up
					self.pos[1] = hits[0].rect.bottom + self.rect.height
				self.vel[1] = 0
				self.rect.y = self.pos[1]

	def debugPlatforms(self, hits):
		for h in hits:
			print(hits)

	def onPlatform(self):
		self.rect[1] += 1
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect[1] -= 1
		if (hits):
			return True
		else:
			return False

	def jump(self):
		#jump only if standing on a platform
		self.rect[1] += 1
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect[1] -= 1
		if (hits):
			self.vel[1] = PLAYER_JUMP
		elif (self.extraJumps == 1):
			self.extraJumps -= 1
			self.vel[1] = PLAYER_JUMP

class Platform(pg.sprite.Sprite):
	def __init__(self, x, y, w, h):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((w, h))
		self.image.fill(OBSTACLECOLOR)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def __str__(self):
		toReturn = ""
		toReturn += str(self.rect.x) + " : " + str(self.rect.y)
		return toReturn