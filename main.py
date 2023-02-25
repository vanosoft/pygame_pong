import os, sys


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"


from pygame import *
from parallel import thread


DEBUG = 0

DIFFICULT = 2

DIFFICULT_FORMULA_COEFFICIENT = 0.125
ACCELERATION_COEFFICIENT = 1.001
SPLASH_TIME = 2
TARGET_FPS = 60
SPLASH_FONT_SIZE = 118
TITLE_FONT_SIZE = 72
PARAGRAPH_FONT_SIZE = 32
FPS_FONT_SIZE = 18
INITIAL_BALL_SPEED = 5.0

ENEMY_CONSTANT = DIFFICULT_FORMULA_COEFFICIENT*\
 DIFFICULT


init()
font.init()
display.init()
mixer.init()

clock = time.Clock()
clock.tick(TARGET_FPS)

run = 1
paddle_score = 0
enemy_score = 0

sc = display.set_mode\
 ((0, 0), DOUBLEBUF|FULLSCREEN)

clock.tick(TARGET_FPS)

spl_font = font.Font('caviar-dreams.ttf',\
 SPLASH_FONT_SIZE)

txt = spl_font.render('Talisman', 1,\
 (255, 255, 255))

tm = transform.smoothscale(\
 image.load('author.png'), (100, 100))

ticks = 0

loading_completed = 0

@thread
def load():
    global \
        bg,\
        ball,\
        ball_rect,\
        ball_speed,\
        ball_acceleration,\
        ball_velocity,\
        paddle,\
        paddle_rect,\
        enemy,\
        enemy_rect,\
        fps_font,\
        par_font,\
        tit_font,\
        loading_completed

    bg = transform.smoothscale(\
     image.load('bg.png'),\
     sc.get_size()).convert()

    ball = image.load('ball.png').convert_alpha()
    ball_rect = Rect(sc.get_width()/2-32,\
     sc.get_height()/2-32, 64, 64)
    ball_speed = INITIAL_BALL_SPEED
    ball_acceleration = ACCELERATION_COEFFICIENT
    ball_velocity = Vector2(5, 5)
    ball_velocity.scale_to_length(ball_speed)

    paddle = image.load('paddle.png').\
    convert_alpha()
    paddle_rect = Rect(sc.get_width()/2-60,\
     sc.get_height()-(sc.get_height()//3.65),
     120, 32)

    enemy = transform.flip(paddle, 0, 1)
    enemy_rect = Rect(sc.get_width()/2-60,\
     sc.get_height()//3.85, 120, 32)

    fps_font = font.Font('caviar-dreams.ttf',\
     FPS_FONT_SIZE)
    par_font = font.Font('caviar-dreams.ttf',\
     PARAGRAPH_FONT_SIZE)
    tit_font = font.Font('caviar-dreams.ttf',\
     TITLE_FONT_SIZE)
    
    loading_completed = 1

load()

while run:
    clock.tick(TARGET_FPS)
    fps = clock.get_fps()+1
    dt = 1
    for e in event.get():
        if e.type == QUIT:
            run = 0
    sc.blit(tm,\
     ((sc.get_width()-tm.get_width())/2,\
     (sc.get_height()-tm.get_height())/2-100))
    sc.blit(txt,\
     ((sc.get_width()-txt.get_width())/2,\
     (sc.get_height()-tm.get_height())/2))
    ticks += 1
    display.flip()
    if ticks >= SPLASH_TIME*TARGET_FPS and\
     loading_completed:
        break

while run:
    clock.tick(TARGET_FPS)
    fps = clock.get_fps()+1
    dt = 1#/fps
    for e in event.get():
        if e.type == QUIT:
            run = 0
        if e.type == MOUSEMOTION:
            paddle_rect.x =\
             mouse.get_pos()[0] - 60
    sc.blit(bg, (0, 0))
    sc.blit(ball, (ball_rect.x, ball_rect.y))
    sc.blit(paddle,\
     (paddle_rect.x, paddle_rect.y))
    sc.blit(enemy,\
     (enemy_rect.x, enemy_rect.y))
    sc.blit(tit_font.render\
     (f'YOU: {paddle_score}', 1,
     (0, 255, 255)), (16, 16))
    sc.blit(tit_font.render\
     (f'CPU: {enemy_score}', 1,
     (0, 255, 255)),\
     (16, 16+tit_font.get_height()))
    if DEBUG:
        draw.rect(sc, (255, 0, 0), paddle_rect, 1)
        draw.rect(sc, (255, 0, 0), ball_rect, 1)
        draw.rect(sc, (255, 0, 0), enemy_rect, 1)
        sc.blit(fps_font.render\
     (f'FPS: {int(fps)}', 1, (255, 0, 170)),
     (10, 0))
    display.flip()
    enemy_rect.x +=\
     ENEMY_CONSTANT*(ball_rect.x-\
      enemy_rect.x-60+32)
    ball_rect.move_ip(dt*ball_velocity)
    if paddle_rect.colliderect(ball_rect) or\
     enemy_rect.colliderect(ball_rect):
        ball_velocity.y *= -1
    ball_speed *= ball_acceleration
    ball_velocity.scale_to_length(ball_speed)
    if not 0 < ball_rect.x < sc.get_width()-64:
        ball_velocity.x *= -1
    if not enemy_rect.y-2 < ball_rect.y <\
     paddle_rect.y+2:
        if enemy_rect.y-2 >= ball_rect.y:
            paddle_score += 1
        else:
            enemy_score += 1
        ball_rect = Rect(sc.get_width()/2-32,\
         sc.get_height()/2-32, 64, 64)
        ball_speed = INITIAL_BALL_SPEED
        ball_velocity = Vector2(5, 5)
        ball_velocity.scale_to_length(ball_speed)
        

display.quit()
