import pygame
import sys
from kadai1 import *


# 画像のサイズ設定処理
# （画像をロードし、サイズを取得後、サイズ変更する）
# load_and_scale_image(画像パス, 変更倍率):
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)


def run_game(pygame):
    # 画面サイズの設定
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("動かす")

    # フォント設定
    font = pygame.font.SysFont("meiryo", 24)

    # 初期値
    x, y = 400, 300
    radius = 30
    color = (0, 0, 255)  # 青
    point = 0

    # 移動速度
    speed = 5

    # 各おにぎりの画像読み込み
    cake = load_and_scale_image("img/0.png", 2/3)
    dosu = load_and_scale_image("img/食べる1.png", 2/3)

    # メインループ
    while True:
        screen.fill((255, 255, 255))  # 画面を白で塗りつぶす

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # キーが押されているかどうかを確認
        keys = pygame.key.get_pressed()
        x, y = move_sprite(keys, x, y, speed)

        if x < 170 and x > 110 and y < 280 and y > 220:
            x, y = 400, 300
            point += 1

        screen.blit(dosu, (30, 200))
        screen.blit(cake, (x, y))
        text = font.render("得点：" + str(point) + "点", True, (0, 0, 0))
        screen.blit(text, (400, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)
