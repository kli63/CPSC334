import pygame

class GameApplication:
	def __init__(self):
		self.init_game_state()
		self.load_assets()

	def init_game_state(self):
		self.screen_width = 800
		self.screen_height = int(self.screen_width * 0.8)
		self.fps = 60

		self.gravity = 0.7
		self.scroll_thresh = 200
		self.rows = 16
		self.cols = 150
		self.tile_size = self.screen_height // self.rows
		self.tile_types = 17
		self.max_levels = 3

		self.red = (255, 0, 0)
		self.white = (255, 255, 255)
		self.green = (0, 255, 0)
		self.black = (0, 0, 0)
		self.pink = (235, 65, 54)

		self.screen_scroll = 0
		self.bg_scroll = 0
		self.level = 1
		self.start_game = False
		self.start_intro = False
		self.moving_left = False
		self.moving_right = False
		self.shoot = False
		self.bomb = False
		self.bomb_thrown = False
		self.crouched = False

		self.enemy_group = pygame.sprite.Group()
		self.projectile_group = pygame.sprite.Group()
		self.bomb_group = pygame.sprite.Group()
		self.explosion_group = pygame.sprite.Group()
		self.pickup_group = pygame.sprite.Group()
		self.environment_object_group = pygame.sprite.Group()
		self.lava_group = pygame.sprite.Group()
		self.exit_group = pygame.sprite.Group()
  
	def load_assets(self):
		pygame.init()
		pygame.mixer.init()
		pygame.font.init()

		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		pygame.display.set_caption('Adventures of Foxy')
		self.clock = pygame.time.Clock()

		self.start_asset = pygame.image.load('../assets/buttons/start.png').convert_alpha()
		self.exit_asset = pygame.image.load('../assets/buttons/exit.png').convert_alpha()
		self.restart_asset = pygame.image.load('../assets/buttons/restart.png').convert_alpha()

		self.bg_back_asset = pygame.image.load('../assets/environment/back.png').convert_alpha()
		self.bg_lava_asset = pygame.image.load('../assets/environment/lava.png').convert_alpha()
		self.bg_rock_asset = pygame.image.load('../assets/environment/middle-rock.png').convert_alpha()

		self.asset_list = []
		for x in range(self.tile_types):
			asset = pygame.image.load(f'../assets/world/{x}.png')
			asset = pygame.transform.scale(asset, (self.tile_size, self.tile_size))
			self.asset_list.append(asset)

		self.projectile_asset = pygame.image.load('../assets/icons/projectile.png').convert_alpha()
		self.bomb_asset = pygame.image.load('../assets/icons/bomb.png').convert_alpha()
		self.health_potion_asset = pygame.image.load('../assets/icons/health_potion.png').convert_alpha()
		self.mana_potion_asset = pygame.image.load('../assets/icons/mana_potion.png').convert_alpha()

		self.pickup_types = {
			'Health': self.health_potion_asset,
			'Mana': self.mana_potion_asset,
			'Bomb': self.bomb_asset
		}

		self.font = pygame.font.SysFont('Futura', 30)
		
	def draw_bg(self):
		self.screen.fill(self.black)
		back_width = self.bg_back_asset.get_width()
		lava_width = self.bg_lava_asset.get_width()
		rock_width = self.bg_rock_asset.get_width()

		for x in range(10):
			self.screen.blit(self.bg_back_asset, ((x * back_width) - self.bg_scroll * 0.6, 0))
			self.screen.blit(self.bg_rock_asset, ((x * back_width) + (back_width // 2) - (rock_width // 2) - (self.bg_scroll * 0.65), self.screen_height - self.bg_rock_asset.get_height() - 50))

		lava_start = int(-(self.bg_scroll * 0.7 % lava_width))
		for lava_x in range(lava_start, self.screen_width, lava_width):
			self.screen.blit(self.bg_lava_asset, (lava_x, self.screen_height - self.bg_lava_asset.get_height()))

	def draw_mana_bar(self, x, y, current_mana, max_mana, overcharge_mana):
		bar_width = 150
		bar_height = 5
		filled_width = (current_mana / max_mana) * bar_width

		pygame.draw.rect(self.screen, self.black, (x - 2, y - 2, bar_width + 4, bar_height + 4)) 
		pygame.draw.rect(self.screen, (0, 0, 255), (x, y, filled_width, bar_height)) 



	def draw_text(self, text, text_col, x, y):
		asset = self.font.render(text, True, text_col)
		self.screen.blit(asset, (x, y))



	def reset_level(self):
		self.enemy_group.empty()
		self.projectile_group.empty()
		self.bomb_group.empty()
		self.explosion_group.empty()
		self.pickup_group.empty()
		self.environment_object_group.empty()
		self.lava_group.empty()
		self.exit_group.empty()

		data = []
		for row in range(self.rows):
			r = [-1] * self.cols
			data.append(r)

		return data