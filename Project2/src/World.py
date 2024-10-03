import pygame
from Misc import *
from Character import *

class EnvironmentObject(pygame.sprite.Sprite):
	def __init__(self, asset, x, y, app):
		pygame.sprite.Sprite.__init__(self)
		self.app = app
		self.image = asset
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + self.app.tile_size // 2, y + (self.image.get_height() - self.app.tile_size))

	def update(self):
		self.rect.x += self.app.screen_scroll


class Lava(pygame.sprite.Sprite):
	def __init__(self, asset, x, y, app):
		pygame.sprite.Sprite.__init__(self)
		self.app = app
		self.image = asset
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + self.app.tile_size // 2, y + (self.image.get_height() - self.app.tile_size))

	def update(self):
		self.rect.x += self.app.screen_scroll


class Exit(pygame.sprite.Sprite):
	def __init__(self, asset, x, y, app):
		pygame.sprite.Sprite.__init__(self)
		self.app = app
		self.image = asset
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + self.app.tile_size // 2, y + (self.image.get_height() - self.app.tile_size))

	def update(self):
		self.rect.x += self.app.screen_scroll


class Pickup(pygame.sprite.Sprite):
	def __init__(self, pickup_types, pickup_type, x, y, app):
		pygame.sprite.Sprite.__init__(self)
		self.app = app
		self.pickup_type = pickup_type
		self.image = pickup_types[self.pickup_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + self.app.tile_size // 2, y + (self.image.get_height() - self.app.tile_size))

	def update(self, player):
		self.rect.x += self.app.screen_scroll
		if pygame.sprite.collide_rect(self, player):
			if self.pickup_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.pickup_type == 'Mana':
				player.mana += 8
			elif self.pickup_type == 'Bomb':
				player.bombs += 3
			self.kill()


class World():
	def __init__(self, app):
		self.obstacle_list = []
		self.app = app

	def process_data(self, data):
		self.level_length = len(data[0])
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					asset = self.app.asset_list[tile]
					asset_rect = asset.get_rect()
					asset_rect.x = x * self.app.tile_size
					asset_rect.y = y * self.app.tile_size
					tile_data = (asset, asset_rect)
					if tile >= 0 and tile <= 4:
						self.obstacle_list.append(tile_data)
					elif tile >= 5 and tile <= 6:
						lava = Lava(asset, x * self.app.tile_size, y * self.app.tile_size, self.app)
						self.app.lava_group.add(lava)
					elif tile >= 7 and tile <= 10:
						environment_object = EnvironmentObject(asset, x * self.app.tile_size, y * self.app.tile_size, self.app)
						self.app.environment_object_group.add(environment_object)
					elif tile == 11:
						player = Player(['Idle', 'Run', 'Jump', 'Crouch', 'Death'], x * self.app.tile_size, y * self.app.tile_size, 
						 1.65, 5, 8, 5, self.app)
						health_bar = HealthBar(100, 42, player.health, player.health, self.app)
					elif tile == 12:
						enemy = Enemy(['Idle', 'Flying', 'Death'], x * self.app.tile_size, y * self.app.tile_size, 
						1.65, 1, 100000, 0, self.app)
						self.app.enemy_group.add(enemy)
					elif tile == 13:
						item_box = Pickup(self.app.pickup_types, 'Mana', x * self.app.tile_size, y * self.app.tile_size, self.app)
						self.app.item_box_group.add(item_box)
					elif tile == 14:
						item_box = Pickup(self.app.pickup_types, 'Bomb', x * self.app.tile_size, y * self.app.tile_size, self.app)
						self.app.item_box_group.add(item_box)
					elif tile == 15:
						item_box = Pickup(self.app.pickup_types, 'Health', x * self.app.tile_size, y * self.app.tile_size, self.app)
						self.app.item_box_group.add(item_box)
					elif tile == 16:
						exit = Exit(asset, x * self.app.tile_size, y * self.app.tile_size, self.app)
						self.app.exit_group.add(exit)

		return player, health_bar


	def draw(self):
		for tile in self.obstacle_list:
			tile[1][0] += self.app.screen_scroll
			self.app.screen.blit(tile[0], tile[1])