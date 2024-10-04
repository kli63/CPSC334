import pygame
import os
import random
from Projectile import Projectile

class Character(pygame.sprite.Sprite):
	def __init__(self, char_type, animation_types, x, y, scale, speed, mana, bombs, app):
		pygame.sprite.Sprite.__init__(self)
		self.app = app
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		self.mana = mana
		self.start_mana = mana
		self.shoot_cooldown = 0
		self.bombs = bombs
		self.health = 100
		self.max_health = self.health
		self.direction = 1
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		self.move_counter = 0
		self.vision = pygame.Rect(0, 0, 150, 20)
		self.idling = False
		self.idling_counter = 0
		self.animation_types = animation_types
		self.load_animations(animation_types, x, y, scale)

	def load_animations(self, animation_types, x, y, scale):
		for animation in animation_types:
			temp_list = []
			num_of_frames = len(os.listdir(f'../assets/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				asset = pygame.image.load(f'../assets/{self.char_type}/{animation}/{i}.png').convert_alpha()
				asset = pygame.transform.scale(asset, (int(asset.get_width() * scale), int(asset.get_height() * scale)))
				temp_list.append(asset)
			self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()

	def update(self):
		self.update_animation()
		self.check_alive()
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1

	def move(self, world):
		screen_scroll = 0
		dx = 0
		dy = 0

		if self.app.moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if self.app.moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		if self.jump == True and self.in_air == False:
			self.vel_y = -11
			self.jump = False
			self.in_air = True


		self.vel_y += self.app.gravity
		if self.vel_y > 10:
			self.vel_y = 10
		dy += self.vel_y

		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
				if self.char_type == 'enemy':
					self.direction *= -1
					self.move_counter = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if self.vel_y < 0: 
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				elif self.vel_y >= 0: 
					self.vel_y = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom
		
		if pygame.sprite.spritecollide(self, self.app.lava_group, False):
			self.health = 0

		level_complete = False
		if pygame.sprite.spritecollide(self, self.app.exit_group, False):
			level_complete = True

		if self.rect.bottom > self.app.screen_height:
			self.health = 0

		if self.char_type == 'player':
			if self.rect.left + dx < 0 or self.rect.right + dx > self.app.screen_width:
				dx = 0

		self.rect.x += dx
		self.rect.y += dy

		if self.rect.right > self.app.screen_width - self.app.scroll_thresh or self.rect.left < self.app.scroll_thresh:
			self.rect.x -= dx 
			screen_scroll = -dx  

		return screen_scroll, level_complete

	def shoot(self):
		if self.shoot_cooldown == 0 and self.mana > 0:
			self.shoot_cooldown = 20
			projectile = Projectile(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), 
									self.rect.centery, self.direction, self.app)
			self.app.projectile_group.add(projectile)
			self.mana -= 1

	def update_animation(self):
		ANIMATION_COOLDOWN = 100
		self.image = self.animation_list[self.action][self.frame_index]
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == len(self.animation_types) - 1:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0

	def update_action(self, new_action):
		if new_action != self.action:
			self.action = new_action
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(len(self.animation_types) - 1)

	def draw(self):
		self.app.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Player(Character):
	def __init__(self, animation_types, x, y, scale, speed, mana, bombs, app):
		super().__init__('player', animation_types, x, y, scale, speed, mana, bombs, app)


class Enemy(Character):
	def __init__(self, animation_types, x, y, scale, speed, mana, bombs, app):
		super().__init__('enemy', animation_types, x, y, scale, speed, mana, bombs, app)
	
	def ai(self, player, world):
		if self.alive and player.alive:
			if self.idling == False and random.randint(1, 200) == 1:
				self.update_action(0)
				self.idling = True
				self.idling_counter = 50
			if self.vision.colliderect(player.rect):
				self.update_action(0)
				self.shoot()
			else:
				if self.idling == False:
					if self.direction == 1:
						ai_moving_right = True
					else:
						ai_moving_right = False
					ai_moving_left = not ai_moving_right
					self.move(world)
					self.update_action(1)
					self.move_counter += 1
					self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

					if self.move_counter > self.app.tile_size:
						self.direction *= -1
						self.move_counter *= -1
				else:
					self.idling_counter -= 1
					if self.idling_counter <= 0:
						self.idling = False
		self.rect.x += self.app.screen_scroll