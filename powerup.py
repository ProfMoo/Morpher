import pygame as pg

from settings import *

class Pow(pg.sprite.Sprite):
	def __init__(self, game, x, y, powType):
		self.groups = game.all_sprites, game.powerups
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.type = powType
		self.image = self.game.spritesheet.get_image(602, 648, 17, 17, 2, 2)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y

		# for collision and timing
		self.active = True
		self.hit_time = pg.time.get_ticks() - 100

		#mask for collision checking
		self.mask = pg.mask.from_surface(self.image)

	#the powerup update
	def update(self):
		now = pg.time.get_ticks()
		if (now - self.hit_time > 1000):
			self.active = True


	# when the player hits a powerup
	def hit(self, player):
		if (self.active):
			self.active = False
			self.hit_time = pg.time.get_ticks()
			player.vel[0] = 100