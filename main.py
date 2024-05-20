import pygame
import random
import math

# INITIALIZE PYGAME
pygame.init()
screen = pygame.display.set_mode((448, 512))

pygame.display.set_caption("Space Invaders")

icon = pygame.image.load('Invader.png')
pygame.display.set_icon(icon)
#SCORE
scores = [30, 20, 20, 10, 10]
score = 0
font = pygame.font.Font('space_invaders.ttf', 16)

textX = 20
textY = 20

def show_score(x, y):
    score_names = font.render("SCORE< 1 >                HI-SCORE                SCORE< 2 >", True, (255, 255, 255))
    score_player_one = font.render(f"{score:04d}", True, (255, 255, 255))
    score_high = font.render(f"{score:04d}", True, (255, 255, 255))
    screen.blit(score_names, (x, y))
    screen.blit(score_player_one, (x + 24, y + 32))
    screen.blit(score_player_one, (x + 168, y + 32))

clock = pygame.time.Clock()

# Player
playerX = 207
playerY = 420
player_Xdelta = 0

class Cannon:
    def __init__(self, sprite, positionX, positionY):
        self.sprite = sprite
        self.positionX = positionX
        self.positionY = positionY

    def draw(self):
        screen.blit(self.sprite, (self.positionX, self.positionY))

laser_cannon = Cannon(pygame.image.load('LaserCannon.png'), playerX, playerY)

# Bullet 
bulletImg = pygame.image.load('Bullet.png')
bulletX = 0
bulletY = 420
bullet_Ydelta = 8
bullet_state = "ready"

# Invader
invaders = []

positionX_invader = 32
positionY_invader = 128
invader_Xdelta = 4
invader_Ydelta = 8
invaders_num_column = 11
sprite_value = 1

change_direction = False
move_down = False

invaders_per_row = [pygame.image.load('Invader2.png'), pygame.image.load('Invader1.png'), pygame.image.load('Invader1.png'), pygame.image.load('Invader3.png'), pygame.image.load('Invader3.png')]
invaders_per_row_second = [pygame.image.load('Invader2-2.png'), pygame.image.load('Invader1-2.png'), pygame.image.load('Invader1-2.png'), pygame.image.load('Invader3-2.png'), pygame.image.load('Invader3-2.png')]

class Invader:
    def __init__(self, sprites, sprite_value, positionX, positionY, score):
        self.sprites = sprites
        self.positionX = positionX
        self.positionY = positionY
        self.sprite_value = sprite_value
        self.score = score
    
    def draw(self):
        screen.blit(self.sprites[self.sprite_value], (self.positionX, self.positionY))

#FILL THE INVADERS ARRAY--------------------------------------------------
for i in range(len(invaders_per_row)):
    invaders_row = []
    #CREATE A ROW OF INVADERS GIVING THEIR SPRITES AND POSITIONS IN X AND Y
    for _ in range(invaders_num_column):
        invaders_row.append(Invader((invaders_per_row[i], invaders_per_row_second[i]), 0, positionX_invader, positionY_invader, scores[i]))
        positionX_invader += 32
    #ADD ROW TO LIST OF INVADERS
    invaders.append(invaders_row)

    positionX_invader = 32
    positionY_invader += 32

index_invaders_rows = len(invaders) - 1
time_at = 0
#-------------------------------------------------------------------------
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))

def isColliding(enemyX, enemyY, bulletX, bulletY):
    # sum by 8 because the center of the bullet in x and y is in 8 and the center of the enemy is at 16 so 16 - 8 = 8
    distance = math.sqrt(((enemyX - bulletX + 8)**2) + ((enemyY - bulletY + 8)**2))
    if distance < 15:
        return True
    else:
        return False

# LOOP
running = True
while running:

    clock.tick(60)
    actual_time = pygame.time.get_ticks()

    #RGB 0 - 255
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_Xdelta = -2
            if event.key == pygame.K_d:
                player_Xdelta = 2
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = laser_cannon.positionX + 8
                bulletY = laser_cannon.positionY - 10
                fire_bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player_Xdelta = 0

    # PLAYER MOVEMENT
    laser_cannon.positionX += player_Xdelta

    if laser_cannon.positionX <= -5:
        laser_cannon.positionX = -5
    elif laser_cannon.positionX >= 421:
        laser_cannon.positionX = 421

    # BULLET MOVEMENT AND DRAW
    if bullet_state == "fire" and bulletY >= 0:
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_Ydelta
    else:
        bullet_state = "ready"
    #----------------------------------------------------------------------
    # MOVE INVADERS PER ROW
    invaders_row = []
    if ((actual_time - time_at) > 100) and (len(invaders) != 0):
        # index_invaders_rows initialize as the number of rows - 1, get the last row
        invaders_row = invaders[index_invaders_rows]
        
        # MOVE INVADERS
        for invader in invaders_row:
            invader.positionX += invader_Xdelta
            invader.sprite_value = sprite_value
        
        # MOVE INVADERS DOWN
        if move_down:
            for invader in invaders_row:
                invader.positionY += invader_Ydelta
        
        # CHECK IF INVADER COLLIDES WITH A WALL
        if invaders_row[0].positionX <= -4:
            change_direction = True
        elif invaders_row[-1].positionX >= 420:
            change_direction = True

        time_at = pygame.time.get_ticks()
        
        index_invaders_rows -= 1
        if index_invaders_rows == -1:
            move_down = False
            # CHANGE THE DIRECTION OF THE INVADERS
            if change_direction:
                invader_Xdelta = -1 * invader_Xdelta
                move_down = True
                change_direction = False
            # CHANGE SPRITE VALUE
            if sprite_value == 1:
                sprite_value = 0
            else:
                sprite_value = 1
            # RETURN TO THE FINAL ROW OF INVADERS
            index_invaders_rows = len(invaders) - 1
    #--------------------------------------------------------------
    # CHECK COLLISION BULLET WITH INVADERS
    eliminate_invader = (-1, 0)
    for i in range(len(invaders)):
        for j in range(len(invaders[i])):
            collision = isColliding(invaders[i][j].positionX, invaders[i][j].positionY, bulletX, bulletY)
            if collision:
                bulletY = -0.5
                eliminate_invader = (i,j)
                score += invaders[i][j].score
    
    # CHECK IF AN INVADER NEEDS TO BE ELIMINATED
    if eliminate_invader[0] != -1:
        invaders[eliminate_invader[0]].pop(eliminate_invader[1])
        #IF THE ROW IS EMPTY ELIMINATE IT
        if len(invaders[eliminate_invader[0]]) == 0:
            invaders.pop(eliminate_invader[0])
            if eliminate_invader[0] == index_invaders_rows:
                index_invaders_rows = index_invaders_rows - 1
    #----------------------------------------------------------------
    #DRAW PLAYER
    laser_cannon.draw()
    show_score(textX, textY)
    #Draw Invaders
    for invaders_rows in invaders:
        for invader in invaders_rows:
            invader.draw()
    
    pygame.display.update() 