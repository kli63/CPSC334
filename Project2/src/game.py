import pygame
import csv
import serial  # For joystick serial communication
import RPi.GPIO as GPIO
import time

from GameApplication import GameApplication
from Button import *
from Projectile import *
from Bomb import *
from Misc import *
from Character import *
from World import *

# GPIO setup for buttons
GPIO.setmode(GPIO.BCM)
START_BUTTON_PIN = 2
SHOOT_BUTTON_PIN = 2
BOMB_BUTTON_PIN = 3
CROUCH_SWITCH_PIN = 4

GPIO.setup(START_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SHOOT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOMB_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize serial communication for joystick with ESP32
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Adjust port as necessary

app = GameApplication()

intro_fade = ScreenFade(1, app.black, 4, app)
death_fade = ScreenFade(2, app.black, 4, app)

start_button = Button(app.screen_width // 2 - 130, app.screen_height // 2 - 150, app.start_asset, 1)
exit_button = Button(app.screen_width // 2 - 110, app.screen_height // 2 + 50, app.exit_asset, 1)
restart_button = Button(app.screen_width // 2 - 100, app.screen_height // 2 - 50, app.restart_asset, 2)

# Read joystick data from ESP32
def read_joystick():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("X:"):
            try:
                x_val, y_val = line.split(',')
                x_val = int(x_val.split(':')[1])
                y_val = int(y_val.split(':')[1])
                return x_val, y_val
            except (IndexError, ValueError):
                return None, None
    return None, None

# Load level data
def load_level(level):
    world_data = app.reset_level()
    with open(f'../assets/level_data/level{level}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    world = World(app)
    player, health_bar = world.process_data(world_data)

    return world, player, health_bar

world, player, health_bar = load_level(app.level)

# Define joystick dead zones and thresholds for movement
JOYSTICK_DEADZONE_X = 2780  # Dead center for X
JOYSTICK_DEADZONE_Y = 2850  # Dead center for Y
THRESHOLD = 200  # Range for dead zone (adjustable)

# Handle input from GPIO and joystick
def input():
    global run
    
    # Check GPIO for start, shoot, and bomb buttons
    if GPIO.input(START_BUTTON_PIN) == GPIO.LOW and not app.start_game:
        app.start_game = True
        app.start_intro = True

    app.shoot = GPIO.input(SHOOT_BUTTON_PIN) == GPIO.LOW

    if GPIO.input(BOMB_BUTTON_PIN) == GPIO.LOW:
        app.bomb = True
    else:
        app.bomb = False
        app.bomb_thrown = False

    # Read joystick data
    x_val, y_val = read_joystick()

    # Manage crouching
    keys = pygame.key.get_pressed()
    if app.crouched:  # If already crouched, keep player crouched and stop movement
        player.update_action(3)
        app.moving_left = False
        app.moving_right = False
        player.jump = False
    else:
        # Joystick movement and jump
        if x_val is not None and y_val is not None:
            if x_val < JOYSTICK_DEADZONE_X - THRESHOLD:
                app.moving_left = True
                app.moving_right = False
            elif x_val > JOYSTICK_DEADZONE_X + THRESHOLD:
                app.moving_right = True
                app.moving_left = False
            else:
                if not keys[pygame.K_a]:  # Only set to False if 'a' is not pressed
                    app.moving_left = False
                if not keys[pygame.K_d]:  # Only set to False if 'd' is not pressed
                    app.moving_right = False

            if y_val < JOYSTICK_DEADZONE_Y - THRESHOLD and player.alive:
                player.jump = True
            else:
                player.jump = False

    # Handle key inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                app.moving_left = True
            if event.key == pygame.K_d:
                app.moving_right = True
            if event.key == pygame.K_SPACE:
                app.shoot = True
            if event.key == pygame.K_q:
                app.bomb = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_s and player.alive:
                app.crouched = True
                player.update_action(3)  # Lock player in crouching
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                app.moving_left = False
            if event.key == pygame.K_d:
                app.moving_right = False
            if event.key == pygame.K_SPACE:
                app.shoot = False
            if event.key == pygame.K_q:
                app.bomb_thrown = False
            if event.key == pygame.K_s:
                app.crouched = False  # Unlock crouch when 's' is released

def render():
    global run, player, world, health_bar
    if not app.start_game:
        app.screen.fill(app.black)
        if start_button.draw(app.screen) or GPIO.input(START_BUTTON_PIN) == GPIO.LOW:  # Start on button press
            app.start_game = True
            app.start_intro = True
        if exit_button.draw(app.screen):
            run = False
    else:
        app.draw_bg()
        world.draw()
        health_bar.draw(player.health)
        app.draw_text('AMMO: ', app.white, 10, 35)
        for x in range(player.mana):
            app.screen.blit(app.projectile_asset, (90 + (x * 10), 40))
        app.draw_text('BOMBS: ', app.white, 10, 60)
        for x in range(player.bombs):
            app.screen.blit(app.bomb_asset, (135 + (x * 15), 60))

        player.draw()
        app.enemy_group.draw(app.screen)
        app.projectile_group.draw(app.screen)
        app.bomb_group.draw(app.screen)
        app.explosion_group.draw(app.screen)
        app.item_box_group.draw(app.screen)
        app.environment_object_group.draw(app.screen)
        app.lava_group.draw(app.screen)
        app.exit_group.draw(app.screen)

        if not player.alive:
            if death_fade.fade():
                if restart_button.draw(app.screen) or GPIO.input(START_BUTTON_PIN) == GPIO.LOW:
                    death_fade.fade_counter = 0
                    app.start_intro = True
                    app.bg_scroll = 0
                    world, player, health_bar = load_level(app.level)


def update():
    global run, player, world, health_bar

    player.update()
    for enemy in app.enemy_group:
        enemy.ai(player, world)
        enemy.update()

    app.projectile_group.update(player, world)
    app.bomb_group.update(player, world)
    app.explosion_group.update()
    app.item_box_group.update(player)
    app.environment_object_group.update()
    app.lava_group.update()
    app.exit_group.update()

    if app.start_intro:
        if intro_fade.fade():
            app.start_intro = False
            intro_fade.fade_counter = 0

    if player.alive:
        if app.shoot:
            player.shoot()
        if app.bomb and not app.bomb_thrown and player.bombs > 0:
            bomb = Bomb(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                        player.rect.top, player.direction, app)
            app.bomb_group.add(bomb)
            player.bombs -= 1
            app.bomb_thrown = True

        if player.in_air:
            player.update_action(2)  # Jump
        elif app.moving_left or app.moving_right:
            player.update_action(1)  # Run
        else:
            player.update_action(0)  # Idle

        app.screen_scroll, level_complete = player.move(world)
        app.bg_scroll -= app.screen_scroll

        if level_complete:
            app.level += 1
            if app.level <= app.max_levels:
                app.bg_scroll = 0
                world, player, health_bar = load_level(app.level)
            else:
                pass

    else:
        app.screen_scroll = 0

run = True
while run:
    app.clock.tick(app.fps)
    input()
    update()
    render()
    pygame.display.update()

pygame.quit()
GPIO.cleanup()
