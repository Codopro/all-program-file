#
# <ミドル２コース Python課題 7月号 スクロールゲーム>
#   parts.py
#

import pygame
from pygame.locals import *
import pygame.mixer
import sys
import time
import random

#グローバル変数の初期化
class g:
    player_x = 0
    course_a_x = 320
    course_b_x = 320 + 640
    player_facing_right = True
    coins = []
    coins_pos = []
    make_coin_num = 0
    coin_num = 0
    goal_time = 100000


# 定数定義（じょうすう／ていすう　ていぎ）
WIDTH = 640          # 画面横幅の設定
HIGHT = 480          # 画面高さの設定
TOTAL_COIN_NUM = 50

RED = (255, 0, 0)            # 赤
GREEN = (0, 255, 0)          # 緑
BLUE = (0, 0, 255)           # 青
YELLOW = (255, 255, 0)       # 黄
CYAN = (0, 255, 255)         # シアン
MAGENTA = (255, 0, 255)      # マゼンタ
WHITE = (255, 255, 255)      # 白
BLACK = (0, 0, 0)            # 黒
GRAY = (0xe6, 0xf0, 0xff)    # 灰色
DARKGRAY = (0x57, 0x5e, 0x75) # 黒灰色
ORANGE = (255, 0x8c, 0x1a)   # 橙色

# 画像のサイズ設定処理G
# （画像をロードし、サイズを取得後、サイズ変更する）
# load_and_scale_image(画像パス, 変更倍率):
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)

def prepare_sprite(image, scale, init_pos):
    sprite = pygame.sprite.Sprite()
    sprite.image = load_and_scale_image(image, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = init_pos
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite

def prepare_picture():
    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei = pygame.image.load("img/背景.png").convert()
    g.haikei = pygame.transform.scale(g.haikei, (640, 480))
    g.hukidashi = load_and_scale_image("img/吹き出し.png", 1/2)

    # キャラクターは倍率を指定を使用してロード
    g.goal = prepare_sprite("img/ゴール.png", 1/4, (3400, 310))
    g.goal_centerx = 3400
    g.player = prepare_sprite("img/主人公.png", 1/7, (100, 250))
    g.player_speed_y = 0
    g.course_a = prepare_sprite("img/コースA.png", 640/887/1.1, (g.course_a_x, 400))
    g.course_b = prepare_sprite("img/コースB.png", 640/944/1.1, (g.course_b_x, 400))
    g.coin = prepare_sprite("img/コイン.png", 1/4, (0, 0))


def prepare_sound():
    g.bgm = pygame.mixer.Sound("sound/Drum Funky.wav")
    g.coin_sound = pygame.mixer.Sound("sound/Coin.wav")

def parts_init():
    pygame.init()

    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"サウンド初期化エラーが発生しました: {e}")

    g.screen = pygame.display.set_mode((WIDTH, HIGHT))
    g.font = pygame.font.SysFont("meiryo", 16)
    g.title_font = pygame.font.SysFont("meiryo", 55)
    g.count_font = pygame.font.SysFont("meiryo", 150)
    g.mode = 0

    # 画像の準備
    prepare_picture()

    # サウンドの準備
    prepare_sound()

    # タイトルを設定
    pygame.display.set_icon(g.player.image)
    pygame.display.set_caption('スクロールゲーム')

#
# BGM 再生
#
def play_bgm_sound():
    g.bgm.set_volume(0.2)
    g.bgm.play(-1)

def draw_box(rect_x, rect_y, rect_width, rect_height, text_char, inner_color=ORANGE, outer_color=WHITE, text_color=WHITE):
    # 丸角矩形のパラメータ
    radius = 3
    border = 2  # 枠線の太さ

    # 外側の丸角矩形
    pygame.draw.rect(g.screen, outer_color, (rect_x, rect_y + radius, rect_width, rect_height - 2*radius))
    pygame.draw.rect(g.screen, outer_color, (rect_x + radius, rect_y, rect_width - 2*radius, rect_height))
    pygame.draw.circle(g.screen, outer_color, (rect_x + radius, rect_y + radius), radius)
    pygame.draw.circle(g.screen, outer_color, (rect_x + rect_width - radius, rect_y + radius), radius)
    pygame.draw.circle(g.screen, outer_color, (rect_x + radius, rect_y + rect_height - radius), radius)
    pygame.draw.circle(g.screen, outer_color, (rect_x + rect_width - radius, rect_y + rect_height - radius), radius)

    # 内側の丸角矩形
    inner_rect_x = rect_x + border
    inner_rect_y = rect_y + border
    inner_rect_width = rect_width - 2 * border
    inner_rect_height = rect_height - 2 * border
    inner_radius = radius - border

    pygame.draw.rect(g.screen, inner_color, (inner_rect_x, inner_rect_y + inner_radius, inner_rect_width, inner_rect_height - 2*inner_radius))
    pygame.draw.rect(g.screen, inner_color, (inner_rect_x + inner_radius, inner_rect_y, inner_rect_width - 2*inner_radius, inner_rect_height))
    pygame.draw.circle(g.screen, inner_color, (inner_rect_x + inner_radius, inner_rect_y + inner_radius), inner_radius)
    pygame.draw.circle(g.screen, inner_color, (inner_rect_x + inner_rect_width - inner_radius, inner_rect_y + inner_radius), inner_radius)
    pygame.draw.circle(g.screen, inner_color, (inner_rect_x + inner_radius, inner_rect_y + inner_rect_height - inner_radius), inner_radius)
    pygame.draw.circle(g.screen, inner_color, (inner_rect_x + inner_rect_width - inner_radius, inner_rect_y + inner_rect_height - inner_radius), inner_radius)

    text = g.font.render(text_char, True, text_color)
    # テキストの描画
    text_rect = text.get_rect(center=(rect_x + rect_width / 2, rect_y + rect_height / 2))
    g.screen.blit(text, text_rect)

#
# 吹き出しにテキストを描く
#
def draw_hukidashi(text_char):
    g.screen.blit(g.hukidashi, (450,250))
    text = g.font.render(text_char, True, BLACK)
    # テキストの描画
    text_rect = text.get_rect(topleft=(450+5, 250+10))
    g.screen.blit(text, text_rect)


# 色の衝突を検出する関数
def detect_color_collision(sprite1, sprite2):
    if pygame.sprite.collide_rect(sprite1, sprite2):
        # 衝突領域のピクセルを確認
        for x in range(max(sprite1.rect.left, sprite2.rect.left), min(sprite1.rect.right, sprite2.rect.right)):
            for y in range(max(sprite1.rect.top, sprite2.rect.top), min(sprite1.rect.bottom, sprite2.rect.bottom)):
                if sprite1.image.get_at((x - sprite1.rect.left, y - sprite1.rect.top)) == (0xE8, 0x32, 0x20) and \
                   sprite2.image.get_at((x - sprite2.rect.left, y - sprite2.rect.top)) == (0, 0x57, 0x57):
                    return True
    return False

def change_course_x(x):
    if (x - g.player_x) < -320:
        x += 1280
    elif (x - g.player_x) > (640 + 320):
        x -= 1280
    return x

def move_course():
    g.course_a.rect.centerx = g.course_a_x - g.player_x
    g.course_a_x = change_course_x(g.course_a_x)
    g.course_b.rect.centerx = g.course_b_x - g.player_x
    g.course_b_x = change_course_x(g.course_b_x)

def down_player():
    g.player.rect.centery += g.player_speed_y
    g.player_speed_y += 0.8
    if (detect_color_collision(g.player, g.course_a) or \
        detect_color_collision(g.player, g.course_b)) and \
        g.player_speed_y > 0: # 落下中
        g.player_speed_y = 0

def jump():
    if detect_color_collision(g.player, g.course_a) or \
       detect_color_collision(g.player, g.course_b):
        g.player_speed_y = -12

def right():
    if g.player.rect.centerx > 400:
        g.player_x += 7
    else:
        g.player.rect.centerx += 7
    if not g.player_facing_right:
        g.player_facing_right = True
        g.player.image = pygame.transform.flip(g.player.image, True, False)

def left():
    if g.player.rect.centerx < 250:
        g.player_x -= 7
    else:
        g.player.rect.centerx -= 7
    if g.player_facing_right:
        g.player_facing_right = False
        g.player.image = pygame.transform.flip(g.player.image, True, False)

def key_check():
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
        right()
    if keys[K_LEFT]:
        left()
    if keys[K_UP]:
        jump()

def draw_coin():
    n = 0
    for sprite in g.coins:
        sprite.rect.centerx = g.coins_pos[n][0] - g.player_x
        sprite.rect.centery = g.coins_pos[n][1]
        if sprite.rect.centerx > 0 and sprite.rect.centerx < 640:
            g.screen.blit(sprite.image, sprite.rect)
        n = n + 1

def draw_goal():
    g.goal.rect.centerx = g.goal_centerx - g.player_x
    if g.goal.rect.centerx > 0 and g.goal.rect.centerx < 640:
        g.screen.blit(g.goal.image, g.goal.rect)

def make_coin():
    if pygame.time.get_ticks() > g.coin_time:
        g.make_coin_num+=1
        if g.make_coin_num <= TOTAL_COIN_NUM:
            sprite = g.coin
            g.coins.append(sprite)
            g.coins_pos.append((random.randint(0, 3400), random.randint(100, 300)))
            g.coin_time += random.randint(100, 1000)

def goal_check():
    if pygame.sprite.collide_rect(g.goal, g.player): # 衝突判定
        g.goal_time = pygame.time.get_ticks()
        g.mode = 2

def draw_coin_num():
    draw_box(550-100, 30-5, 55 + 105, 30 + 10, "コインの数　　　　", GRAY, GRAY, DARKGRAY)
    draw_box(550, 30, 55, 30, str(g.coin_num))


def draw_tc(count):
    g.screen.blit(g.haikei, (0,0))
    text = g.count_font.render(str(count), True, CYAN)
    g.screen.blit(text, [300, 150])
    pygame.display.update()
    pygame.time.wait(1000)

