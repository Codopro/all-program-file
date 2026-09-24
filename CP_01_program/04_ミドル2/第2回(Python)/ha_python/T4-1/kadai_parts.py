import pygame
import sys
from kadai1 import *

width, height = 640, 480
BACKGROUND_COLOR = (145, 226, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((width, height))

# 画像のサイズ設定処理
# （画像をロードし、サイズを取得後、サイズ変更する）
# load_and_scale_image(画像パス, 変更倍率):
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)

def draw_neko():
    neko = load_and_scale_image("img/run01.png", 1/5)
    x = random.randint(0, 640 - 200)  # 幅内にランダム配置
    y = random.randint(50, 480 - 120)  # 高さ内にランダム配置
    screen.blit(neko, (x, y))  # 画像を描画
    return x, y

#
# 吹き出しにテキストを描く
#  左右反転対応
#
def draw_hukidashi(x, y, text_char):
    x += 40
    y -= 40
    font = pygame.font.SysFont("meiryo", 20)
    hukidashi = load_and_scale_image("img/吹き出し.png", 2/3)
    text = font.render(str(text_char), True, BLACK)
    screen.blit(hukidashi, (x, y))
    text_rect = text.get_rect(topleft=(x + 10, y + 5))
    screen.blit(text, text_rect)

def run_game(pygame):
    # 画面サイズの設定
    pygame.display.set_caption("課題")


    screen.fill(BACKGROUND_COLOR)
    kadai1(draw_neko, draw_hukidashi)

    # メインループ
    while True:

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

