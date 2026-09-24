import pygame
import random

import math
import sys


# 画面サイズの設定
WIDTH = 640
HEIGHT = 480

# 色の設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 天気のランダム選択（3秒経過後に一度だけ実行）
start_time = pygame.time.get_ticks()
weather_selected = False
weather = None


# 最後に移動した時間
last_move_time = start_time

# 半円の中心点と半径の設定
center_x, center_y = 300, 100  # 雲の中心付近に設定
radius = 80  # 半円の半径
start_angle = math.pi  # 半円の開始角度（ラジアン単位）、ここでは左側の端から開始

# 「ゴ」の初期位置（半円の左端）
go_x, go_y = center_x - radius, center_y

# 移動させる回数と現在の回数
total_moves = 4
current_move = 0

# 移動間隔を計算（3秒間でtotal_moves回移動）
move_interval = 1500 / total_moves  # ミリ秒単位

# 最後に移動した時間
last_move_time = start_time


# pygameの初期化
pygame.init()

# 画面の設定
screen = pygame.display.set_mode((WIDTH, HEIGHT))



# 画像の読み込みと画面サイズへの調整
def load_background_image(image_path):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))  # 画面サイズに合わせてスケーリング
    return image

# スプライトの準備
def prepare_sprite(image, scale, init_pos):
    sprite = pygame.sprite.Sprite()
    sprite.image = load_and_scale_image(image, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = init_pos
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite

# 画像の読み込みとスケール調整
def load_and_scale_image(image_path, scale):
    image = pygame.image.load(image_path)
    if scale != 1:
        size = round(image.get_width() * scale), round(image.get_height() * scale)
        image = pygame.transform.scale(image, size)
    return image

# 背景画像の準備
background_images = {
    'sunny': load_background_image('img/晴れ.png'),
    'rain': load_background_image('img/雨.png')
}



# スプライトの準備
g = {}
g['little_person'] = prepare_sprite('img/横.png', 1/3, (100, 315))
g['little_person_happy'] = prepare_sprite('img/喜ぶ.png', 1/3, (100, 315))
g['cloud'] = prepare_sprite('img/雲.png', 1, (400, 150))

# ウインドウタイトルを設定

pygame.display.set_caption('課題2・3：条件分岐その2')
icon_image = pygame.image.load("img/雲.png").convert_alpha()
pygame.display.set_icon(icon_image)

# テキストを表示する関数
def draw_text(text, position, size=30):
    font = pygame.font.SysFont("meiryo", size)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, position)


def start():


    global last_move_time,go_x,go_y,current_move
    running = True
    while running:
        screen.fill(BLACK)  # 黒で画面をクリア

        current_time = pygame.time.get_ticks()

        # 最初の2秒間の処理
        if current_time - start_time < 2000:
            screen.blit(g['little_person'].image, g['little_person'].rect)
            screen.blit(g['cloud'].image, g['cloud'].rect)
            draw_text('明日の天気は・・・', (20, HEIGHT - 50))
            # 「ゴ」の移動処理
            if current_time - last_move_time >= move_interval and current_move < total_moves:
                # 角度の計算（左から右へ半円を描く）
                angle = start_angle + (math.pi / total_moves) * current_move
                # 新しい位置の計算
                go_x = center_x + radius * math.cos(angle) + (current_move * 20)  # 右にシフトする効果を追加
                go_y = center_y + radius * math.sin(angle) - (current_move * 10)  # 上にシフトする効果を追加
                # 移動回数と最後に移動した時間を更新
                current_move += 1
                last_move_time = current_time

            # 「ゴ」を描画
            draw_text('ゴゴゴ', (go_x, go_y))
        else:
            pygame.time.wait(500)
            running = False


        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

        # FPSの制御
        pygame.time.Clock().tick(60)

def hare():
    screen.blit(background_images['sunny'], (0, 0))
    screen.blit(g['little_person_happy'].image, g['little_person_happy'].rect)
    draw_text('晴れ！', (20, HEIGHT - 50))
    pygame.display.flip()

    pygame.time.wait(1500)
    pygame.quit()
    sys.exit()

def ame():
    screen.blit(background_images['rain'], (0, 0))
    screen.blit(g['little_person'].image, g['little_person'].rect)
    draw_text('雨。', (20, HEIGHT - 50))    
    pygame.display.flip()

    pygame.time.wait(1500)
    pygame.quit()
    sys.exit()
