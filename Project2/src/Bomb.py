import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, app):
        pygame.sprite.Sprite.__init__(self)
        self.app = app
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = app.bomb_asset

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self, player, world):
        self.vel_y += self.app.gravity
        dx = self.direction * self.speed
        dy = self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx + self.app.screen_scroll
        self.rect.y += dy

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 0.5, self.app)
            self.app.explosion_group.add(explosion)

            if abs(self.rect.centerx - player.rect.centerx) < self.app.tile_size * 2 and \
                    abs(self.rect.centery - player.rect.centery) < self.app.tile_size * 2:
                player.health -= 50
            for enemy in self.app.enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < self.app.tile_size * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < self.app.tile_size * 2:
                    enemy.health -= 50


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, app):
        pygame.sprite.Sprite.__init__(self)
        self.app = app
        self.images = []
        for num in range(1, 6):
            asset = pygame.image.load(f'../assets/explosion/exp{num}.png').convert_alpha()
            asset = pygame.transform.scale(asset, (int(asset.get_width() * scale), int(asset.get_height() * scale)))
            self.images.append(asset)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += self.app.screen_scroll

        EXPLOSION_SPEED = 4
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
