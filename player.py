import pygame as pg
import numpy as np
from settings import *

class Player(pg.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)

		#reference to game
		self.game = game

		#important game metrics
		self.extraJumps = 1

		#for images
		self.walking = False
		self.jumping = False
		self.crouching = False
		self.current_frame = 0
		self.last_update = 0
		self.load_images()
		self.image = self.standing_frames[0]
		self.image.set_colorkey(BLACK)

		#make rectangle for collision checking and all references
		self.rect = pg.Rect(WIDTH/2, HEIGHT/2, 50, 60)

		#mask for collision checking
		self.mask = pg.mask.from_surface(self.image)

		#movement [x, y]
		self.pos = np.array([WIDTH/2, HEIGHT/2], dtype = np.float64)
		self.vel = np.array([0, 0], dtype = np.float64)
		self.acc = np.array([0, 0], dtype = np.float64)

	def load_images(self):
		self.standing_frames = [self.game.spritesheet.get_image(441, 95, 17, 20, 3.3, 3),
								self.game.spritesheet.get_image(464, 95, 17, 20, 3.3, 3)]
		# self.standing_frames = [self.game.spritesheet.get_image(441, 95, 19, 20, 3.3, 3),
		# 						self.game.spritesheet.get_image(441, 95, 19, 20, 3.3, 3)]
		self.walk_frames_r = [self.game.spritesheet.get_image(648, 95, 16, 20, 3.3, 3),
								self.game.spritesheet.get_image(671, 95, 16, 20, 3.3, 3)]
		self.walk_frames_l = []
		for frame in self.walk_frames_r:
			self.walk_frames_l.append(pg.transform.flip(frame, True, False))
		self.jump_frame = self.game.spritesheet.get_image(460, 95, 17, 20, 3.3, 3)

	def crouch(self):
		if (self.onPlatform):
			self.rect.height = 40
			self.crouching = True

	def update(self):
		self.animate()
		self.acc = np.array([0, PLAYER_GRAVITY], dtype = np.float64)
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			if (self.crouching is False):
				self.acc[0] = -(PLAYER_ACC)
		if keys[pg.K_RIGHT]:
			if (self.crouching is False):
				self.acc[0] = PLAYER_ACC

		if keys[pg.K_DOWN]:
			self.crouch()
		else:
			self.rect.height = 60
			self.crouching = False

		#add in friction
		self.acc[0] += self.vel[0] * PLAYER_FRICTION	
		#omg some actual physics!
		self.vel += self.acc
		if (-1 < self.vel[0] < 1):
			self.vel[0] = 0

		#changing x pos and checking collision
		self.pos[0] += self.vel[0] + (0.5*self.acc[0])
		self.rect.midbottom = self.pos
		self.collision('x')

		#changing y pos and checking collision
		self.pos[1] += self.vel[1] + (0.5*self.acc[1])
		self.rect.midbottom = self.pos
		self.collision('y')

		self.rect.midbottom = self.pos

	def animate(self):
		#getting current time
		now = pg.time.get_ticks()

		#seeing if player is walking or standing
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

		#show idle animations	
		if (self.jumping is False and self.walking is False):
			if (now - self.last_update > 600):
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
				self.image = self.standing_frames[self.current_frame]

		self.image.set_colorkey(BLACK) #to reduce lag, move this to only when you update the image??
		self.mask = pg.mask.from_surface(self.image)

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
		elif (dir == 'y'):
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

	# a check to see if there is a platform underneath to jump on
	def onPlatform(self):
		self.rect[1] += 1
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect[1] -= 1
		if (hits):
			return True
		else:
			return False

	# the short hop
	def jump_cut(self):
		if (self.jumping):
			if (self.vel[1] < -15):
				self.vel[1] = -15

	# player jumping function
	def jump(self):
		#jump only if standing on a platform
		if (self.onPlatform()):
			self.game.jump_sound.play()
			self.vel[1] = PLAYER_JUMP
			self.jumping = True
		elif (self.extraJumps == 1):
			self.extraJumps -= 1
			self.game.jump_sound.play()
			self.vel[1] = PLAYER_JUMP
			self.jumping = True