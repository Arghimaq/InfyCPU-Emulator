import pygame

clock = pygame.time.Clock()

screen_size = 8
window_size = 768
scale = window_size / screen_size

scaled_size = (screen_size * scale, screen_size * scale)
colors = {
	0: (255,255,255),
	1: (122, 122, 122),
	2: (255, 0, 0),
	3: (0, 255, 0),
	4: (0, 0, 255),
	5: (255, 255, 0),
	6: (0, 255, 255),
	7: (255, 0, 255),
	8: (200, 200, 200)
}

color = 0

def initialize():
    pygame.init()

screen = pygame.display.set_mode(scaled_size)
pygame.display.set_caption("Screen Emulator")

clock = pygame.time.Clock()

def draw(x,y,color):
	global colors
	scaled_x = x * scale
	scaled_y = y * scale
	draw_color = colors.get(color)
	pygame.draw.rect(screen,draw_color,(scaled_x,scaled_y,scale,scale))

def erase(x,y):
	scaled_x = x * scale
	scaled_y = y * scale
	pygame.draw.rect(screen,(0,0,0),(scaled_x,scaled_y,scale,scale))

def update_display():
	pygame.display.flip()
	clock.tick(60)
	
def check_quit():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return True
	return False

def clear_screen():
	screen.fill((0,0,0))
	
def listen():
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			return pygame.key.name(event.key)



