import pygame as pg
import math

from settings import *

class Spritesheet(object):
	#utility class for loading and parsing spritesheets
	def __init__(self, filename):
		# if (DEBUG == True):
		# 	self.spritesheet = pg.image.load(filename).convert()
		# else:
		# 	self.spritesheet = pg.image.load(filename).convert_alpha()
		self.spritesheet = pg.image.load(filename).convert_alpha()

	# x: the pixel to start looking for image on spritemap
	# y: the pixel to start looking for image on spritemap
	# width: the width of pixels to grab to the right of x
	# height: the height of pixels to grab below y
	# scalew: the size that we scale the image up (can be changed for larger/smaller maps)
	# scalew: the size that we scale the image up (can be changed for larger/smaller maps) 
	def get_image(self, x, y, width, height, scalew, scaleh):
		#grab an image out of a larger spritesheet
		image = pg.Surface((width, height))
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		#image = pg.transform.scale(image, (math.trunc(width), height))
		image = pg.transform.scale(image, (math.trunc(width * scalew), height * scaleh))
		return image