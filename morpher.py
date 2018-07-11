

def main():


	all_sprites = pygame.sprite.Group()

	#Game loop
	running = True
	while running:
		clock.tick(FPS)

		
		screen.fill(BLACK)
		all_sprites.draw(screen)

		pygame.display.flip()

	pygame.quit()

if __name__ == '__main__':
    main()