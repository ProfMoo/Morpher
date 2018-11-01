import pygame as pg

from settings import *

class Platform(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		self.groups = game.all_sprites, game.platforms
		pg.sprite.Sprite.__init__(self, self.groups)
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