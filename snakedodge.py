import math
import random
import pygame
from pygame import mixer

# Starts pygame
pygame.init()


# Creates window for game
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
# music bg
mixer.music.load('back ground music.mp3')
mixer.music.play(-1)
# Title and logo
pygame.display.set_caption("Snake Dodge")
icon = pygame.image.load('snek.png')
pygame.display.set_icon(icon)

game_win = pygame.image.load('winner.jpg')
go_screen = pygame.image.load("GAAME OVER.jpg")


# skins

# Player
playerImg = pygame.image.load('snakey player.png')
playerImg = pygame.transform.scale(playerImg, (40, 40))
playerX = 170
playerY = 125
playerX_change = 0
playerY_change = 0

# Enemies

Enemy1Img = (pygame.image.load('ENEMEy.png'))
Enemy1X = (random.randint(20, 400))
Enemy1Y = (random.randint(400, 550))
Enemy1X_change = (random.randint(1, 2))
Enemy1Y_change = 0

# bullets

Bullet1Img = pygame.image.load('wepunee.png')
Bullet1Img = pygame.transform.scale(Bullet1Img, (40, 40))
Bullet1X = 0
Bullet1Y = Enemy1Y
Bullet1Y_change = 0.5
bullet_state = "ready"

Bullet2Img = pygame.image.load('DROPY.png')
Bullet2Img = pygame.transform.scale(Bullet2Img, (40, 40))
Bullet2X = playerX
Bullet2Y = playerY
Bullet2Y_change = 0.4
Bullet2X_change = 0
bullet2_state = "GO"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 189
textY = 30

game_over = pygame.font.Font('freesansbold.ttf', 100)


def s_score(x, y):
    score = font.render(str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_player(x, y):
    global bullet2_state
    bullet2_state = "SHOOT"
    screen.blit(Bullet2Img, (x + 1, y + 0))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(Bullet1Img, (x + 11, y + 0))


def enemy(x, y):
    screen.blit(Enemy1Img, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def game_o(Bullet1X, Bullet1Y, playerX, playerY):
    distance = math.sqrt((math.pow(Bullet1X - playerX, 2)) + (math.pow(Bullet1Y - playerY, 2)))
    if distance < 25:
        return True
    else:
        return False


def bullet_collision(Bullet1X, Bullet1Y, Bullet2X, Bullet2Y):
    distance = math.sqrt((math.pow(Bullet1X - Bullet2X, 2)) + (math.pow(Bullet1Y - Bullet2Y, 2)))
    if distance < 25:
        return True
    else:
        return False


def player_hit_enemy_col(Enemy1X, Enemy1Y, Bullet2X, Bullet2Y):
    distance = math.sqrt((math.pow(Enemy1X - Bullet2X, 2)) + (math.pow(Enemy1Y - Bullet2Y, 2)))
    if distance < 30:
        return True
    else:
        return False

# Game loop


running = True

while running:

    screen.fill((174, 198, 207))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Move snake

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_UP:
                playerY_change = -0.3
            if event.key == pygame.K_DOWN:
                playerY_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet2_state == "GO":
                    bullet_sound = mixer.Sound('HS.mp3')
                    bullet_sound.play()
                    Bullet2X = playerX
                    fire_player(playerX, Bullet2Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('HS.mp3')
                    bullet_sound.play()
                    Bullet1X = Enemy1X
                    fire_bullet(Enemy1X, Bullet1Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerY_change = 0

    # Player movement
    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 236:
        playerY = 236
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 336:
        playerX = 336

    # Enemy movement
    Enemy1X += Enemy1X_change
    if Enemy1X <= 0:
        Enemy1X_change = 0.2
    elif Enemy1X >= 336:
        Enemy1X_change = -0.2

    # Bullet movement

    if Bullet1Y <= 10:
        Bullet1Y = Enemy1Y
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(Bullet1X, Bullet1Y)
        Bullet1Y -= Bullet1Y_change

    # friendly bullet movement

    if Bullet2Y >= 600:
        Bullet2Y = playerY
        bullet2_state = "GO"

    if bullet2_state == "SHOOT":
        fire_player(Bullet2X, Bullet2Y)
        Bullet2Y += Bullet2Y_change

    B_collision = bullet_collision(Bullet1X, Bullet1Y, Bullet2X, Bullet2Y)
    if B_collision:
        EXP = mixer.Sound('HS.mp3')
        EXP.play()
        Bullet2Y = playerY
        Bullet1Y = Enemy1Y
        bullet_state = "ready"
        bullet2_state = "GO"
        score_value += 0.5

    player_hit_enemy = player_hit_enemy_col(Enemy1X, Enemy1Y, Bullet2X, Bullet2Y)
    if player_hit_enemy:
        PXE = mixer.Sound('HS.mp3')
        PXE.play()
        Bullet2Y = playerY
        Enemy1X = random.randint(20, 400)
        bullet2_state = "GO"
        score_value += 5

    s_score(textX, textY)
    enemy(Enemy1X, Enemy1Y)
    player(playerX, playerY)

    game_oo = game_o(Bullet1X, Bullet1Y, playerX, playerY)
    if game_oo == True:
        clock.tick(60000)
        screen.blit(go_screen, (0, 0))
        score_value -= score_value

    if score_value == 200:
        screen.blit(game_win, (0, 0))
        score_value -= score_value

    clock.tick(600000000000000000000)
    pygame.display.update()
