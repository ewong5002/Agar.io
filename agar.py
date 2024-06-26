import pygame, os
from random import randint

pygame.init()
os.chdir('./Game Files/Agar.io')

class Pellet(pygame.sprite.Sprite):
	
	def __init__ (self, pos, group):
		super().__init__(group)
		self.image = pygame.transform.scale(pygame.image.load('./Images/yellow_circle.png').convert_alpha(), (20, 20))
		self.rect = self.image.get_rect(center = pos)

class Player(pygame.sprite.Sprite):

	def __init__ (self, pos, group):
		super().__init__(group)
		self.original_image = pygame.transform.scale(pygame.image.load('./Images/circle.png').convert_alpha(), (100, 100))
		self.image = pygame.transform.scale(pygame.image.load('./Images/circle.png').convert_alpha(), (100, 100))
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 3

	def input(self):
		key = pygame.key.get_pressed()

		if key[pygame.K_w]:
			self.direction.y = -1
		elif key[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if key[pygame.K_d]:
			self.direction.x = 1
		elif key[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0
	
	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed

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

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.image.get_width):
			offset_pos = sprite.rect.topleft - self.offset
			self.display.blit(sprite.image, offset_pos)

# Colour variables
white = '#FFFFFF'

# Screen Variables
width = height = 800

screen = pygame.display.set_mode((width, height))

# Set up camera and objects on screen
camera = Camera()
player = Player((400, 400),camera)

for i in range(20):
	random_x = randint(0, 750)
	random_y = randint(0, 750)
	Pellet((random_x, random_y), camera)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	
	screen.fill(white)

	camera.update()
	camera.draw_objects(player)


	pygame.display.update()