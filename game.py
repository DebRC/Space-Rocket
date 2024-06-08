# importing modules
import pygame
import sys
import random
from pygame import mixer
from pygame.locals import *

# initializing pygame
pygame.init()

# resolution of the screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# caption and icon
pygame.display.set_caption("Space Rocket")
icon = pygame.image.load("Images\\icon.png")
pygame.display.set_icon(icon)

# player
player_image = pygame.image.load("Images\\rocket.png")
player_size = 30
player_pos = [int(WIDTH/2), int(HEIGHT-3*player_size)]

# enemy
enemy_image = pygame.image.load("Images\\asteroid.png")
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), random.randint(0, HEIGHT)]
enemy_list = [enemy_pos]
enemy_speed = 0

# laser
laser_image = pygame.image.load("Images\\laser.png")
laser_size = 10
laser_speed = 15
laser_list = []

# background image
background = pygame.image.load("Images\\background.png")

# background sound
mixer.music.load("Sounds\\background.ogg")
mixer.music.play(-1)

# basic
score = 0
game_over = False
clock = pygame.time.Clock()

# fonts
myFont = pygame.font.SysFont("calibri", 35, bold=True, italic=True)
game_over_font = pygame.font.Font("Fonts\\font.otf", 60, italic=True)

def speed(score, enemy_speed):
    if score < 10:
        enemy_speed = 5
    elif score < 20:
        enemy_speed = 6
    elif score < 30:
        enemy_speed = 9
    elif score < 50:
        enemy_speed = 13
    elif score < 65:
        enemy_speed = 16
    else:
        enemy_speed = 20
    return enemy_speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 8 and delay < 0.06:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))

def new_enemy_pos(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def multiple_collision(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if collision(player_pos, enemy_pos):
            return True
    return False

def collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    if (e_x >= p_x and e_x < (p_x+player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y+player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            explosion = mixer.Sound("Sounds\\explosion.wav")
            mixer.music.stop()
            explosion.play()
            return True
    return False

def draw_lasers(laser_list):
    for laser_pos in laser_list:
        screen.blit(laser_image, (laser_pos[0], laser_pos[1]))

def move_lasers(laser_list):
    for idx, laser_pos in enumerate(laser_list):
        if laser_pos[1] <= 0:
            laser_list.pop(idx)
        else:
            laser_pos[1] -= laser_speed

def laser_collision(laser_list, enemy_list, score):
    for laser_pos in laser_list:
        for enemy_pos in enemy_list:
            if collision(laser_pos, enemy_pos):
                explosion = mixer.Sound("Sounds\\explosion.wav")
                explosion.play()
                laser_list.remove(laser_pos)
                enemy_list.remove(enemy_pos)
                score += 1
                break
    return score

def gameover(game_over, score):
    screen.blit(background, (0, 0))
    text = " Game Over !"
    label = game_over_font.render(text, 1, (255, 153, 102))
    screen.blit(label, (int(WIDTH/2)-200, int(HEIGHT/2)-50))
    text = "Your Score: "+str(score)
    label = game_over_font.render(text, 1, (255, 153, 102))
    screen.blit(label, (int(WIDTH/2)-200, int(HEIGHT/2)))

running = True
while running:
    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                x = player_pos[0]
                y = player_pos[1]
                if event.key == pygame.K_LEFT:
                    if x > 0:
                        x -= player_size+10
                elif event.key == pygame.K_RIGHT:
                    if x < 700:
                        x += player_size+10
                elif event.key == pygame.K_UP:
                    if y > 30:
                        y -= player_size+10
                elif event.key == pygame.K_DOWN:
                    if y < 500:
                        y += player_size+10
                elif event.key == pygame.K_SPACE:
                    laser_pos = [x + (player_size//2 - laser_size//2) + 4, y]
                    laser_list.append(laser_pos)
                player_pos = [x, y]

        screen.blit(background, (0, 0))
        game_over = collision(player_pos, enemy_pos)
        drop_enemies(enemy_list)
        score = new_enemy_pos(enemy_list, score)
        enemy_speed = speed(score, enemy_speed)
        text = "Your Score: "+str(score)
        label = myFont.render(text, 1, (204, 255, 51))
        screen.blit(label, (int(WIDTH-250), 0))
        game_over = multiple_collision(enemy_list, player_pos)
        draw_enemies(enemy_list)
        draw_lasers(laser_list)
        move_lasers(laser_list)
        score = laser_collision(laser_list, enemy_list, score)
        screen.blit(player_image, (player_pos[0], player_pos[1]))
        clock.tick(30)
        pygame.display.update()
    else:
        gameover(game_over, score)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()

    pygame.display.update()
