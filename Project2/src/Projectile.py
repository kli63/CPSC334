import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, app):
        pygame.sprite.Sprite.__init__(self)
        self.app = app
        self.speed = 10
        self.image = self.app.projectile_asset
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, player, world):
        self.rect.x += (self.direction * self.speed) + self.app.screen_scroll

        if self.rect.right < 0 or self.rect.left > self.app.screen_width:
            self.kill()

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(player, self.app.projectile_group, False):
            if player.alive:
                player.health -= 5
                self.kill()

        for enemy in self.app.enemy_group:
            if pygame.sprite.spritecollide(enemy, self.app.projectile_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()
