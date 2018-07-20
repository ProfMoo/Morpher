#game options
TITLE = "morpher"
WIDTH = 640
HEIGHT = 480
FPS = 30
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet.png"

#across gameplay
PLAYER_DEATHS = 0

#player properties
PLAYER_ACC = 5.0
PLAYER_FRICTION = -0.25
PLAYER_GRAVITY = 5.
PLAYER_JUMP = -40

#starting platforms
PLATFORM_LIST = [[0, HEIGHT - 40, WIDTH*2, 40], \
			[WIDTH/2 - 50, HEIGHT - 120, 100, 20], \
			[125, HEIGHT - 350, 100, 20], \
			[350, 200, 100, 20], \
			[475, 100, 50, 20], \
			[675, 200, 50, 20], \
			[875, 200, 50, 20], \
			[WIDTH*2 + 100, HEIGHT - 40, WIDTH*2, 40]]

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
OBSTACLECOLOR = (110, 110, 110)
USERCOLOR = (200, 210, 45)
BACKGROUNDCOLOR = (210, 210, 210)
SPRITEBACKGROUND = (93, 128, 164)