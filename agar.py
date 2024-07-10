import pygame, os, math
from random import randint

pygame.init()
os.chdir('./Game Files/Agar.io')

class Screen(pygame.Rect):

	def __init__ (self, screen):
		self.screen = screen
		self.scaled_screen = self.screen
		self.scale = 1.2
		self.min_scale = 2

	def zoom (self):
		scaled = (int(self.scaled_screen.get_width() * self.scale), int(self.scaled_screen.get_height() * self.scale))
		if scaled[0] <= self.screen.get_width() / self.min_scale:
			self.scaled_screen = pygame.transform.smoothscale(self.scaled_screen, scaled)	
	
	def refresh(self):
		self.screen.fill(black)
		self.scaled_screen.fill(white)

class Pellet(pygame.sprite.Sprite):
	
	def __init__ (self, pos, group):
		super().__init__(group)
		self.image = pygame.transform.scale(pygame.image.load('./Images/yellow_circle.png').convert_alpha(), (20, 20))
		self.rect = self.image.get_rect(center = pos)

class Player(pygame.sprite.Sprite):

	og_size = size = 100

	def __init__ (self, pos, group):
		super().__init__(group)
		self.image = pygame.transform.scale(pygame.image.load('./Images/circle.png').convert_alpha(), (self.og_size, self.og_size))
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 3

	# Player's controls
	def input(self):
		key = pygame.key.get_pressed()

		if (self.rect.center[1] + self.rect.width//2 >= 2000 or self.rect.center[1] - self.rect.width//2 <= -2000):
			self.direction.y *= -1
		elif key[pygame.K_w]:
			self.direction.y = -1
		elif key[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if (self.rect.center[0] + self.rect.width//2 >= 2000 or self.rect.center[0] - self.rect.width//2 <= -2000):
			self.direction.x *= -1
		elif key[pygame.K_d]:
			self.direction.x = 1
		elif key[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0
	
	# Player's movement
	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed

	def growth(self):
		self.size += 1
		self.image = pygame.transform.scale(pygame.image.load('./Images/circle.png').convert_alpha(), (self.size, self.size))
		self.rect = self.rect.inflate(1, 1)

class Camera(pygame.sprite.Group):

	def __init__(self):
		super().__init__()
		self.display = pygame.display.get_surface()

		self.offset = pygame.math.Vector2()
		self.half_w = self.display.get_size()[0] // 2
		self.half_h = self.display.get_size()[1] // 2

	def center_target(self, target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h
	
	def draw_objects(self, player):
		self.center_target(player)
		
		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.display.blit(sprite.image, offset_pos)

def spawn():
	screen.fill(white)

	global pellets
	pellets = []

	for i in range(2000):
		random_x = randint(-2000, 2000)
		random_y = randint(-2000, 2000)
		pellet = Pellet((random_x, random_y), camera)
		pellets.append(pellet)

	global player
	rand_x = randint (-1900, 1900)
	rand_y = randint (-1900, 1900)
	player = Player((rand_x, rand_y),camera)

# Colour variables
white = '#FFFFFF'
black = '#000000'

# Screen Variables
width = height = 800

screen = pygame.display.set_mode((width, height))
main_screen = Screen(screen)
pygame.display.set_caption("Agar.io")

# Set up camera and objects on screen
camera = Camera()

spawn()

zoom_counter = 1

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	
	main_screen.refresh()

	camera.update()
	camera.draw_objects(player)

	if player.rect.collidelist(pellets) >= 0:
		index = player.rect.collidelist(pellets)
		pellets[index].kill()
		pellets.pop(index)
		player.growth()

	###if player.rect.width//100 > zoom_counter:
	# 	zoom_counter += 1
	#	main_screen.zoom()

	pygame.display.update()