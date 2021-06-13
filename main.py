import pygame
pygame.font.init()
pygame.mixer.init()
import os
import random as r
import time
GAME_FONT = pygame.font.SysFont('comicsans', 40)
WIN_FONT = pygame.font.SysFont('comicsans', 100)
HEIGHT, WIDTH = 700, 1200
VEL = 15
FPS = 60

P1_HIT = pygame.USEREVENT + 1
P2_HIT = pygame.USEREVENT + 2
TOP_HIT = pygame.USEREVENT + 3
BOT_HIT = pygame.USEREVENT + 4
P1_MISS = pygame.USEREVENT + 5
P2_MISS = pygame.USEREVENT + 6
P1_WIN = pygame.USEREVENT + 7
P2_WIN = pygame.USEREVENT + 8


#----------------------------------------------------------------------------------------------------------

BALL_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'cirkle2.png')), (50, 50))
#BALL_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'cirkle.png')), (50, 50))

#-----------------------------------------------------------------------------------------------------------




BG_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bg.jpg')), (WIDTH, HEIGHT))
PLAYER_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'rectangle1.png')), (50, HEIGHT//3))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_win(ball, player_1, player_2, balls, p1_score, p2_score):
    WIN.blit(BG_SPRITE, (0, 0))
    
    p1_score_text = GAME_FONT.render("PLAYER1 SCORE: " + str(p1_score), 1, (255, 255, 255))
    p2_score_text = GAME_FONT.render("PLAYER2 SCORE: " + str(p2_score), 1, (255, 255, 255))

    WIN.blit(p1_score_text, (10, 10))
    WIN.blit(p2_score_text, (WIDTH - p2_score_text.get_width() - 5, 10))

    for ball in balls:
        pygame.draw.rect(WIN, (0, 0, 0, 255), ball)
    WIN.blit(BALL_SPRITE, (ball.x, ball.y))
    WIN.blit(PLAYER_SPRITE, (player_1.x, player_1.y))
    WIN.blit(PLAYER_SPRITE, (player_2.x, player_2.y))
    pygame.display.update()
    

def player_1_movement(player_1, keys_pressed):
    if keys_pressed[pygame.K_w] and player_1.y - VEL > - VEL*3:
        player_1.y -= VEL
    if keys_pressed[pygame.K_s] and player_1.y + VEL < HEIGHT - PLAYER_SPRITE.get_height() + VEL*3:
        player_1.y += VEL

def player_2_movement(player_2, keys_pressed):
    if keys_pressed[pygame.K_i] and player_2.y - VEL > - VEL*3:
        player_2.y -= VEL
    if keys_pressed[pygame.K_k] and player_2.y + VEL < HEIGHT - PLAYER_SPRITE.get_height() + VEL*3:
        player_2.y += VEL

def handle_ball(ball, player_1, player_2, balls, BALL_VEL_X, BALL_VEL_Y):
    ball.x -= BALL_VEL_X
    ball.y -= BALL_VEL_Y
    for ball in balls:   
        if player_1.colliderect(ball):
                pygame.event.post(pygame.event.Event(P1_HIT))
        if player_2.colliderect(ball):
                pygame.event.post(pygame.event.Event(P2_HIT))
        if ball.y <= 0:
            pygame.event.post(pygame.event.Event(TOP_HIT))
        if ball.y >= HEIGHT - 50:
            pygame.event.post(pygame.event.Event(BOT_HIT))
        if ball.x < 0:
            balls.remove(ball)
            pygame.event.post(pygame.event.Event(P1_MISS))
        if ball.x > WIDTH :
            balls.remove(ball)
            pygame.event.post(pygame.event.Event(P2_MISS))
        
def reset_ball(balls, ball, BALL_VEL_X):
    pygame.time.delay(2000)
    ball.y = 350
    ball.x = 600
    balls.append(ball)

def main():
    player_1 = pygame.Rect(10, HEIGHT//2 - PLAYER_SPRITE.get_height()//2, PLAYER_SPRITE.get_width(), PLAYER_SPRITE.get_height())
    player_2 = pygame.Rect(WIDTH - 10 - PLAYER_SPRITE.get_width(), HEIGHT//2 - PLAYER_SPRITE.get_height()//2, PLAYER_SPRITE.get_width(), PLAYER_SPRITE.get_height())
    ball = pygame.Rect(WIDTH//2 - BALL_SPRITE.get_width()//2, HEIGHT//2 - BALL_SPRITE.get_height()//2, 50, 50)
    balls = [ball]
    BALL_VEL_X = 10
    BALL_VEL_Y = r.randint(1, 10)

    p1_score = 0
    p2_score = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys_pressed = pygame.key.get_pressed()
            if event.type == P1_WIN:
                win_text = WIN_FONT.render("PLAYER1 WON!", 1, (255, 255, 255))
                WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2 , HEIGHT/2 - win_text.get_height()/2 - 80))
                pygame.display.update()
                p1_score = 0
                p2_score = 0
                pygame.time.delay(5000)
            if event.type == P2_WIN:    
                win_text = WIN_FONT.render("PLAYER2 WON!", 1, (255, 255, 255))
                WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2 , HEIGHT/2 - win_text.get_height()/2 - 80))
                pygame.display.update()
                p1_score = 0
                p2_score = 0
                pygame.time.delay(5000)
            if event.type == P1_HIT:
                NEW_VEL_X = BALL_VEL_X - BALL_VEL_X*2
                BALL_VEL_X = NEW_VEL_X
                BALL_VEL_X -= 2
            if event.type == P2_HIT:
                NEW_VEL_X = BALL_VEL_X - BALL_VEL_X - BALL_VEL_X
                BALL_VEL_X = NEW_VEL_X
                BALL_VEL_X += 2
            if event.type == TOP_HIT:
                NEW_VEL_Y = BALL_VEL_Y - BALL_VEL_Y*2
                BALL_VEL_Y = NEW_VEL_Y
            if event.type == BOT_HIT:
                NEW_VEL_Y = BALL_VEL_Y - BALL_VEL_Y - BALL_VEL_Y
                BALL_VEL_Y = NEW_VEL_Y
            if event.type == P1_MISS:
                p2_score += 1
                BALL_VEL_X = 10
                if p2_score == 10:
                    pygame.event.post(pygame.event.Event(P2_WIN))
                print("p1: " + str(p1_score), "p2: " + str(p2_score))
            if event.type == P2_MISS:
                p1_score += 1
                BALL_VEL_X = -10
                if p1_score == 10:
                    pygame.event.post(pygame.event.Event(P1_WIN))
                print("p1: " + str(p1_score), "p2: " + str(p2_score))  

        if len(balls) == 0:
            reset_ball(balls, ball, BALL_VEL_X)
        handle_ball(ball, player_1, player_2, balls, BALL_VEL_X, BALL_VEL_Y)  
        player_1_movement(player_1, keys_pressed)
        player_2_movement(player_2, keys_pressed)
        draw_win(ball, player_1, player_2, balls, p1_score, p2_score)

main()