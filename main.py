import pygame
import random
from math import sqrt
from math import pow

pygame.init() #initialize
#window initialization
window = pygame.display.set_mode((800,600)) #game window
bg = pygame.image.load('images/bg.jpg')
pygame.display.set_caption('Space Invaders')
game_icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(game_icon)
#player variable
player_icon = pygame.image.load('images/player_icon.png')
player_Xcord = 370
player_Ycord = 530
player_Xcord_change = 0
#target variables
target_icon = []
target_Xcord = []
target_Ycord = []
target_Xcord_change = []
target_Ycord_change = []
target_num = 5
for i in range(target_num):
    target_icon.append(pygame.image.load('images/target_icon.png'))
    target_Xcord.append(random.randint(0,736))
    target_Ycord.append(0)
    target_Xcord_change.append(0.7)
    target_Ycord_change.append(40)
#bullet variables
bullet_icon = pygame.image.load('images/bullet_icon.png')
bullet_Xcord = 0
bullet_Ycord = 530
bullet_Ycord_change = 2
bullet_sb_state = True 
#score and game over text
score_value = 0
font = pygame.font.SysFont('Imapct',32)
score_x = 10
score_y = 10
game_over_text = pygame.font.SysFont('Impact',64)

def score_display(x,y):
    score = font.render('Score:'+str(score_value), True, (255,255,0))
    window.blit(score, (x, y))

def game_over():
    go = game_over_text.render('GAME OVER!',True,(255,255,0))
    window.blit(go, (230,250))

def player(xcord, ycord):
    window.blit(player_icon,(xcord ,ycord))

def target(xcord, ycord, i):
    window.blit(target_icon[i],(xcord ,ycord))

def bullet(xcord, ycord):
    global bullet_sb_state
    bullet_sb_state = False
    window.blit(bullet_icon,(xcord+16,ycord+10))

def collision(x1,y1,x2,y2):
    p = sqrt(pow(x2-x1 , 2)+pow(y2-y1 , 2))                 #distance formula
    if p < 27:
        return True
    else:
        return False

game_time = True
while game_time:
    window.blit(bg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_time = False               #close the game instance if the quit button is pressed

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xcord_change = -1
            if event.key == pygame.K_RIGHT:
                player_Xcord_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_sb_state:
                    bullet_Xcord = player_Xcord
                    bullet(bullet_Xcord,bullet_Ycord)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_Xcord_change = 0
    
    player_Xcord +=player_Xcord_change
    if player_Xcord <= 0:
        player_Xcord = 0
    elif player_Xcord >= 736:
        player_Xcord = 736

    for i in range(target_num):
        if target_Ycord[i] > 490:
            for j in range(target_num):
                target_Ycord[j] = 2000
            game_over()
            break

        target_Xcord[i] +=target_Xcord_change[i]
        if target_Xcord[i] <= 0:
            target_Xcord_change[i] = 0.7
            target_Ycord[i] += target_Ycord_change[i]
        elif target_Xcord[i] >= 736:
            target_Xcord_change[i] = -0.7
            target_Ycord[i] += target_Ycord_change[i]

        col = collision(target_Xcord[i], target_Ycord[i], bullet_Xcord, bullet_Ycord)
        if col:
            bullet_Ycord = 530
            bullet_sb_state = True
            score_value +=1
            #print (score_value)
            target_Xcord[i] = random.randint(0,736)
            target_Ycord[i] = 0

        target(target_Xcord[i], target_Ycord[i], i)

    if bullet_Ycord <= 0 :
        bullet_Ycord = 530
        bullet_sb_state = True
        
    if not bullet_sb_state:
        bullet(bullet_Xcord,bullet_Ycord)
        bullet_Ycord -= bullet_Ycord_change
    player(player_Xcord, player_Ycord)
    score_display(score_x, score_y)
    
    pygame.display.update() #updating the frame
