import pygame
import sys
import random
import math

# 初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# キャラクターの初期設定
character_color = (0, 128, 255)
character_radius = 30

#グローバル変数の初期化
class g:
    character_x = random.randint(character_radius, WIDTH - character_radius)
    character_y = random.randint(character_radius, HEIGHT - character_radius)
    speed_x = 5
    speed_y = 3

def kyori():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    distance = ((g.character_x - mouse_x) ** 2 + (g.character_y - mouse_y) ** 2) ** 0.5
    return distance

def wait_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def move_ball():
    g.character_x += g.speed_x
    g.character_y += g.speed_y

    # 壁に当たったときの反射
    if g.character_x - character_radius <= 0 or g.character_x + character_radius >= WIDTH:
        g.speed_x *= -1
    if g.character_y - character_radius <= 0 or g.character_y + character_radius >= HEIGHT:
        g.speed_y *= -1

    #✅プログラミングチャレンジ1






    # 背景を描画
    screen.fill(WHITE)

    pygame.draw.circle(screen, character_color, (g.character_x, g.character_y), character_radius)

    pygame.display.flip()
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
