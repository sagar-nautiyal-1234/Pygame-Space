import pygame
import random
import math
from pygame import mixer

# Initialize Pygame and mixer
pygame.init()
mixer.init()

win = pygame.display.set_mode((900, 600))

# Background
bg = pygame.image.load('Images/bg.jpg')
mixer.music.load('Music/background.wav')
mixer.music.play(-1)

# Player setup
player_img = pygame.image.load('Images/spaceship.png')
playerX = 200
playerY = 350
py_change = 0

# Enemy setup
enemy_img = pygame.image.load('Images/alien.png')
enemyX = 755
enemyY = random.randint(0, 550)
ex_change = 0.1

# Game window setup
pygame.display.set_caption("Space")
icon = pygame.image.load('Images/logo.png')
pygame.display.set_icon(icon)

# Projectile setup
pro_img = pygame.image.load('Images/laser.png')
proX = 0
proY = 350
prox_change = 0.5
proy_change = 0
pro_state = "ready"

# SCORE BOARD
score = 0
font = pygame.font.Font('Font/pricedown bl.ttf', 32)
scoreX = 0
scoreY = 0

# Game Over setup
game_over_font = pygame.font.Font('Font/pricedown bl.ttf', 64)

# Load sound effects
laser_sound = mixer.Sound('Music/shoot.wav')
col_sound = mixer.Sound('Music/explosion.wav')

# FUNCTIONS
def player(x, y):
    win.blit(player_img, (x, y))


def enemy(x, y):
    win.blit(enemy_img, (x, y))


def projectile(x, y):
    global pro_state
    pro_state = "fire"
    win.blit(pro_img, (x + 16, y + 10))


def scoreboard(x, y):
    score_display = font.render("Score: " + str(score), True, (240, 248, 255))
    win.blit(score_display, (x, y))


def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(win.get_width() / 2, win.get_height() / 2))
    win.blit(game_over_text, text_rect.topleft)


def is_collision(enemyX, enemyY, proX, proY):
    distance = math.sqrt((math.pow(enemyX - proX, 2)) + (math.pow(enemyY - proY, 2)))
    return distance < 27


# MAIN GAME LOOP
running = True
game_over = False
while running:
    win.fill((255, 255, 255))
    win.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP:
                    py_change = -0.3
                if event.key == pygame.K_DOWN:
                    py_change = 0.3
                if event.key == pygame.K_SPACE:
                    if pro_state == "ready":
                        proX = playerX
                        proY = playerY
                        laser_sound.play()  # Play the laser sound effect
                        projectile(proX, proY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                py_change = 0

    if not game_over:
        playerY += py_change
        if playerY <= 0:
            playerY = 0
        if playerY >= 550:
            playerY = 550

        # Move the enemy
        enemyX -= ex_change
        if enemyX < playerX:
            game_over = True

        enemy(enemyX, enemyY)

        # Move the projectile
        if pro_state == "fire":
            projectile(proX, proY)
            proX += prox_change
            if proX >= 850:
                pro_state = "ready"

        # Check for collision
        if is_collision(enemyX, enemyY, proX, proY):
            col_sound.play()  # Play collision sound effect
            pro_state = "ready"
            score += 1
            enemyX = 875
            enemyY = random.randint(0, 575)

        scoreboard(scoreX, scoreY)
        player(playerX, playerY)
    else:
        show_game_over()

    pygame.display.update()
