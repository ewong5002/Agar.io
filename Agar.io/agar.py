import pygame, os, math
from random import randint

pygame.init()
os.chdir('./Agar.io')

class Screen(pygame.Rect):

	def __init__ (self, screen):
		self.screen = screen
		self.scaled_screen = self.screen
	
	def refresh(self):
		self.screen.fill(black)
		self.scaled_screen.fill(white)

class Pellet(pygame.sprite.Sprite):
	
	def __init__ (self, pos, group):
		super().__init__(group)
		self.image = pygame.transform.scale(pygame.image.load('./Images/pellet.png').convert_alpha(), (20, 20))
		self.rect = self.image.get_rect(center = pos)

class Player(pygame.sprite.Sprite):

	og_size = size = 100

	def __init__ (self, pos, group):
		super().__init__(group)
		self.image = pygame.transform.scale(pygame.image.load('./Images/player.png').convert_alpha(), (self.og_size, self.og_size))
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 3
		self.zoom = 1

	# Player controls
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

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed

	def growth(self, growth_size):
		self.size += growth_size
		self.image = pygame.transform.scale(pygame.image.load('./Images/player.png').convert_alpha(), (self.size, self.size))
		self.rect = self.rect.inflate(growth_size, growth_size)

class Ai(pygame.sprite.Sprite):
	og_size = size = randint(100, 300)

	def __init__ (self, pos, group):
		super().__init__(group)
		self.image = pygame.transform.scale(pygame.image.load('./Images/computer.png').convert_alpha(), (self.og_size, self.og_size))
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 1

		# Generate random movement pattern for AI
		self.move = randint(0, 1)
		self.moves = 0

	# AI movements
	def movement(self):
		match self.move:
			case 0:
				if self.moves <= 150:
					self.direction.x = -1
					self.direction.y = 0
				elif self.moves <= 300:
					self.direction.x = 0
					self.direction.y = 1
				elif self.moves <= 450:
					self.direction.x = 1
					self.direction.y = 0
				elif self.moves <= 600:
					self.direction.x = 0
					self.direction.y = -1
			case 1:
				if self.moves <= 150:
					self.direction.x = -1
					self.direction.y = 1
				elif self.moves <= 300:
					self.direction.x = 1
					self.direction.y = 1
				elif self.moves <= 450:
					self.direction.x = 1
					self.direction.y = -1
				elif self.moves <= 600:
					self.direction.x = -1
					self.direction.y = -1
			case _:
				self.direction.x = 0
				self.direction.y = 0

		self.moves += 1
		if self.moves > 600:
			self.moves = 0

	def update(self):
		self.movement()
		self.rect.center += self.direction * self.speed

	def growth(self):
		self.size += 1
		self.image = pygame.transform.scale(pygame.image.load('./Images/computer.png').convert_alpha(), (self.size, self.size))
		self.rect = self.rect.inflate(1, 1)

class Camera(pygame.sprite.Group):

	def __init__(self):
		super().__init__()
		self.display = pygame.display.get_surface()

		self.offset = pygame.math.Vector2()
		self.half_w = self.display.get_size()[0] // 2
		self.half_h = self.display.get_size()[1] // 2

	def center_target(self, target):
		self.offset.x = (target.rect.centerx * target.zoom) - self.half_w
		self.offset.y = (target.rect.centery * target.zoom)  - self.half_h
	
	def draw_objects(self, player):
		self.center_target(player)
		
		for sprite in self.sprites():
			image = sprite.image
			dimensions = int(image.get_rect().w * player.zoom)
			offset_pos = sprite.rect.topleft - self.offset
			self.display.blit(pygame.transform.scale(image, (dimensions, dimensions)), offset_pos)

# Initial spawn of all objects
def spawn():
	screen.fill(white)

	camera.empty()

	global pellets
	pellets = []

	for i in range(2000):
		random_x = randint(-2000, 2000)
		random_y = randint(-2000, 2000)
		pellet = Pellet((random_x, random_y), camera)
		pellets.append(pellet)

	global ais
	ais = []
	
	for i in range(3):
		rand_x = randint (-1670, 1670)
		rand_y = randint (-1670, 1670)
		ai = Ai((rand_x, rand_y), camera)
		ais.append(ai)

	global player
	rand_x = randint (-1900, 1900)
	rand_y = randint (-1900, 1900)
	player = Player((rand_x, rand_y),camera)

# Respawn any dead AIs
def ai_spawn(dead_ai):
	for i in range(dead_ai):
		rand_x = randint (-1670, 1670)
		rand_y = randint (-1670, 1670)
		ai = Ai((rand_x, rand_y), camera)
		ais.append(ai)

# Replenish pellet supply
def pellet_spawn():
	for i in range(750):
		random_x = randint(-2000, 2000)
		random_y = randint(-2000, 2000)
		pellet = Pellet((random_x, random_y), camera)
		pellets.append(pellet)

# Colour variables
white = '#FFFFFF'
black = '#000000'

# Text variables
game_font = pygame.font.Font("freesansbold.ttf", 32)
text_pos = (350, 350)

# Screen Variables
width = height = 800

screen = pygame.display.set_mode((width, height))
main_screen = Screen(screen)
pygame.display.set_caption("Agar.io")

# Set up camera and objects on screen
camera = Camera()

spawn()

# Lopp variables
run = True
display = True

while True:
	while run:
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

			if player.zoom > 10:
				player.zoom -= 0.01

			# Unstuck player
			if (player.rect.width//2 + 2 + player.rect.center[0] >= 2000):
				player.rect.move_ip(-3, 0)
			elif (player.rect.width//2 + 2 + player.rect.center[1] >= 2000):
				player.rect.move_ip(0, -3)

			player.growth(1)

		# AI counter variables
		ai_index = 0
		dead_ai = 0

		for ai in ais:
			if ai.rect.collidelist(pellets) >= 0:
				index = ai.rect.collidelist(pellets)
				pellets[index].kill()
				pellets.pop(index)
				ai.growth()
			
			if pygame.sprite.collide_mask(ai, player):
				ai_size = ai.rect.width
				player_size = player.rect.width

				if ai_size < player_size:
					ais[ai_index].kill()
					ais.pop(ai_index)
					dead_ai += 1
					player.growth(ai_size//5)
					
					if player.zoom > 10:
						player.zoom -= (ai_size//500)
						
				elif player_size < ai_size:
					pygame.time.delay(1000)
					run = False

			ai_index += 1

		ai_spawn(dead_ai)

		if len(pellets) < 1000:
			pellet_spawn()

		pygame.display.update()
	
	# Game over display screen
	if display:
		main_screen.screen.fill(black)

		text = ["Game Over", "Your Score was " + str(player.rect.width), "Press the Spacebar to Restart", "Press Esc to Exit"]
		game_over = []

		for line in text:
			game_over.append(game_font.render(line, False, white))
		
		for line in range(len(game_over)):
			main_screen.screen.blit(game_over[line], (340 - (6*len(text[line])), 350+(line*32)+(15*line)))
		pygame.display.update()

		display = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				run = display = True
				spawn()
			elif event.key == pygame.K_ESCAPE:
				pygame.quit()
