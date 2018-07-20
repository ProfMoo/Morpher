#sprite classes
import pygame as pg
import numpy as np
import math
from random import choice
from settings import *

class Spritesheet(object):
	#utility class for loading and parsing spritesheets
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert_alpha()
		#self.spritesheet = pg.image.load(filename).convert()

	def get_image(self, x, y, width, height):
		#grab an image out of a larger spritesheet
		image = pg.Surface((width, height))
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		image = pg.transform.scale(image, (math.trunc(width * 3.3), height * 3))
		return image

class Player(pg.sprite.Sprite):
	def __init__(self, game):
		#reference to game
		self.game = game

		#for images mostly
		self.walking = False
		self.jumping = False
		self.current_frame = 0
		self.last_update = 0
		self.load_images()

		#player jumps
		self.extraJummps = 1

		pg.sprite.Sprite.__init__(self)
		self.image = self.standing_frames[0]
		self.image.set_colorkey(SPRITEBACKGROUND)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT/2)

		#movement [x, y]
		self.pos = np.array([WIDTH/2, HEIGHT/2], dtype = np.float64)
		self.vel = np.array([0, 0], dtype = np.float64)
		self.acc = np.array([0, 0], dtype = np.float64)

	def load_images(self):
		self.standing_frames = [self.game.spritesheet.get_image(441, 95, 17, 20),
								self.game.spritesheet.get_image(464, 95, 17, 20)]
		self.walk_frames_r = [self.game.spritesheet.get_image(648, 95, 16, 20),
								self.game.spritesheet.get_image(671, 95, 16, 20)]
		self.walk_frames_l = []
		for frame in self.walk_frames_r:
			self.walk_frames_l.append(pg.transform.flip(frame, True, False))
		self.jump_frame = self.game.spritesheet.get_image(460, 95, 17, 20)

	def update(self):
		self.animate()
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

	def animate(self):
		now = pg.time.get_ticks()
		if (self.vel[0] != 0):
			self.walking = True
		else:
			self.walking = False
		#show walk animations
		if (self.walking):
			if (now - self.last_update > 100):
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
				if (self.vel[0] > 0):			
					self.image = self.walk_frames_r[self.current_frame]
				else:			
					self.image = self.walk_frames_l[self.current_frame]
				self.rect = self.image.get_rect() #maybe not needed????

		#show idle animations	
		if (self.jumping is False and self.walking is False):
			if (now - self.last_update > 600):
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
				self.image = self.standing_frames[self.current_frame]

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
				self.jumping = False
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

	def jump_cut(self):
		if (self.jumping):
			if (self.vel[1] < -15):
				self.vel[1] = -15

	def jump(self):
		#jump only if standing on a platform
		self.rect[1] += 1
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect[1] -= 1
		if (hits):
			self.vel[1] = PLAYER_JUMP
			self.jumping = True
		elif (self.extraJumps == 1):
			self.extraJumps -= 1
			self.vel[1] = PLAYER_JUMP
			self.jumping = True

class Platform(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pg.Surface((w, h))
		self.image.fill(OBSTACLECOLOR)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def __str__(self):
		toReturn = ""
		toReturn += str(self.rect.x) + " : " + str(self.rect.y)
		return toReturn