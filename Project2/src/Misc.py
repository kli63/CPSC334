import pygame

class HealthBar():
    def __init__(self, x, y, health, max_health, app):
        self.app = app
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(self.app.screen, self.app.black, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(self.app.screen, self.app.red, (self.x, self.y, 150, 20))
        pygame.draw.rect(self.app.screen, self.app.green, (self.x, self.y, 150 * ratio, 20))


class ScreenFade():
    def __init__(self, direction, colour, speed, app):
        self.app = app
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        screen = self.app.screen

        if self.direction == 1:
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, self.app.screen_width // 2, self.app.screen_height))
            pygame.draw.rect(screen, self.colour, (self.app.screen_width // 2 + self.fade_counter, 0, self.app.screen_width, self.app.screen_height))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, self.app.screen_width, self.app.screen_height // 2))
            pygame.draw.rect(screen, self.colour, (0, self.app.screen_height // 2 + self.fade_counter, self.app.screen_width, self.app.screen_height))
        if self.direction == 2:
            pygame.draw.rect(screen, self.colour, (0, 0, self.app.screen_width, 0 + self.fade_counter))
        
        if self.fade_counter >= self.app.screen_width:
            fade_complete = True

        return fade_complete
