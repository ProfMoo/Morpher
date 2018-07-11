import pygame as pg
import random
import sys
import time
import math

from settings import *
from sprites import *

class Morpher:
	def __init__(self):
		#initialize game window, etc
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption("Morpher")
		self.clock = pg.time.Clock()
		self.running = True
		self.font_name = pg.font.match_font(FONT_NAME)

	def new(self):
		#resets game, initialize game
		self.deaths = 0
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.player = Player(self)
		self.all_sprites.add(self.player)
		
		for plat in PLATFORM_LIST:
			p = Platform(*plat)
			self.all_sprites.add(p)
			self.platforms.add(p)

	def run(self):
		#game loop
		self.playing = True
		while (self.playing):
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def events(self):
		#game loop (events)
		for event in pg.event.get():
			#checking for close window
			if event.type == pg.QUIT:
				self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.player.jump()
			if event.type == pg.KEYUP:
				if event.key == pg.K_ESCAPE:
					self.terminate()

	def update(self):
		#game loop (update)
		self.all_sprites.update()
		
		#print("self.player.pos[0]0:", self.player.pos[0])
		#print("self.player.vel[0]0: ", self.player.vel[0])
		#print("self.player.acc[0]0: ", self.player.acc[0])

		#if player reacher area where camera needs to move
		if self.player.rect.right >= WIDTH*(2/3.):
			# print("self.player.pos[0]1:", self.player.pos[0])
			# print("self.player.vel[0]1: ", self.player.vel[0])
			self.player.pos[0] -= math.trunc(self.player.vel[0])
			# print("self.player.pos[0]2:", self.player.pos[0])
			# print("self.player.vel[0]2: ", self.player.vel[0])
			for plat in self.platforms:
				plat.rect[0] -= math.trunc(self.player.vel[0])
		elif self.player.rect.left <= WIDTH*(1/3.):
			self.player.pos[0] -= math.trunc(self.player.vel[0])
			for plat in self.platforms:
				plat.rect[0] -= math.trunc(self.player.vel[0])

		#if player dies
		if (self.player.rect.bottom > HEIGHT + 100):
			self.deaths += 1
			self.playing = False


	def draw(self):
		#game loop (draw)
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		self.draw_text(str(self.deaths), 22, WHITE, WIDTH/2, 15)
		pg.display.flip()

	def show_start_screen(self):
		#game start screen
		pass

	def show_go_screen(self):
		#game over / continue
		pass

	def draw_text(self, text, size, color, x, y):
		font = pg.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color) #true is anti aliasing
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)

	def terminate(self):
		pg.quit()
		sys.exit()

def main():
	m = Morpher()
	m.show_start_screen()
	while m.running:
		m.new()
		m.run()
		m.show_go_screen()

	pg.quit()

if __name__ == '__main__':
    main()