import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init
pygame.font.init()
pygame.mixer.init()
# Set window size to 800 width and 600 height
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('media/background/background.png')


# Game Over Text
over_font = pygame.font.Font('FreeSansBold.ttf',64)


# Background Music
mixer.music.load('media/audio/Game_Start.mp3')
mixer.music.play()

# Score
score = 0
font = pygame.font.Font('FreeSansBold.ttf',32)
textX=10
textY=10

def show_score(x,y):
    score_value = font.render("Score :" + str(score),True,(255,255,255))
    screen.blit(score_value, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text, (200,250))

# Title and Icon
pygame.display.set_caption("Niazi Invader")
icon = pygame.image.load('media/icons/niazi_invader.png')
pygame.display.set_icon(icon)


# Ship
shipImg = pygame.image.load('media/icons/ship.png')

# Position the ship on the window relative to window size, values can vary.
shipX = 370
shipY = 480
shipMoveX =0

# Enemies
niaziImg =[]
niaziX = []
niaziY = []
niaziMoveX = []
niaziMoveY = []
num_niazi = 5

for i in range (num_niazi):
    niaziImg.append(pygame.image.load('media/icons/niazi_invader.png'))
    niaziX.append(random.randint(0,660))
    niaziY.append(random.randint(50,150))
    niaziMoveX.append(1)
    niaziMoveY.append(40)

# Bullet
bulletImg = pygame.image.load('media/icons/bullet.png')

# Ready state means you can't see the bullet on the screen
# Fire - The bullet starts moving
bulletX = 0
bulletY = 480
bulletMoveX = 0
bulletMoveY = 5
bulletState = "ready"

def ship(x,y):

    # Draws ship on the screen
    screen.blit(shipImg, (x, y))

def niazi(x,y,i):

    # Draws the enemy on the screen
    screen.blit(niaziImg[i], (x, y))


def fire_bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16,y + 10))

def isCollison(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance <30:
        return True
    else:
        return False


running = True

# Game running
while running:

    # Background color for screen set by R,G,B values
    screen.fill((0,0,0))
    
    # Background image
    screen.blit(background,(0,0))

    # Close game on when you click X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # Check for keystroke (left or right)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shipMoveX = -2
            if event.key == pygame.K_RIGHT:
                shipMoveX = 2

            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bullet_sound = mixer.Sound('media/audio/laser.mp3')
                    bullet_sound.play()
                    bulletX = shipX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                shipMoveX = 0


    # Ship movement
    shipX+=shipMoveX
    if shipX <= 0:
        shipX = 0;
    
    elif shipX >= 736:
        shipX = 736



    # Enemy movement
    for i in range(num_niazi):

        #Game Over
        if niaziY[i] >340:
            for j in range (num_niazi):
                niaziY[j] = 1000;
            game_over_text()
            game_over_sound = mixer.Sound('media/audio/Game_Over.mp3')
            game_over_sound.play()
            break        
        niaziX[i] += niaziMoveX[i]
        if niaziX[i] <= 0:
            niaziMoveX[i] = 1;
            niaziY[i] += niaziMoveY[i]
        
        elif niaziX[i] >= 670:
            niaziMoveX[i] = -1
            niaziY[i] += niaziMoveY[i]

        # Collison
        collison = isCollison(niaziX[i], niaziY[i], bulletX, bulletY)
        if collison:
            explosion_sound = mixer.Sound('media/audio/explosion.mp3')
            explosion_sound.play()
            bullet_state = "ready"
            bulletY = 480
            score+=1
            print(score)

            niaziX[i] = random.randint(0,670)
            niaziY[i] = random.randint(50,150)
        
        # Display enemy
        niazi(niaziX[i],niaziY[i],i)

    # Bullet movement
    if bulletY <=0:
        bulletY =480
        bulletState = "ready"


    if (bulletState is "fire"):
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletMoveY 

    
    show_score(textX,textY)
    # Displaying the ship
    ship(shipX,shipY)

    # Updating display (MUST)
    pygame.display.update()