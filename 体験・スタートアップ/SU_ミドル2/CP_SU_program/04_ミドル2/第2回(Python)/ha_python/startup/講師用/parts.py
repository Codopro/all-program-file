import pygame
from pygame.locals import *
import pygame.mixer
import sys
import time

#グローバル変数の初期化
class global_values:
   bgx = 0
   tick = 0
   robo3_x = 450  #✅ロボ3のｘ座標の初期位置


# 定数定義（じょうすう／ていすう　ていぎ）
WIDTH = 640                  # 画面横幅の設定
HIGHT = 480                  # 画面高さの設定

RED = (255, 0, 0)            # 赤
GREEN = (0, 255, 0)          # 緑
BLUE = (0, 0, 255)           # 青
YELLOW = (255, 255, 0)       # 黄
CYAN = (0, 255, 255)         # シアン
MAGENTA = (255, 0, 255)      # マゼンタ
WHITE = (255, 255, 255)      # 白
BLACK = (0, 0, 0)            # 黒
GRAY = (128, 128, 128)       # 灰色

#設定したグローバル変数をプログラム中で使えるようにする（インスタンス化）
g = global_values()

# 画像のサイズ設定処理
# （画像をロードし、サイズを取得後、サイズ変更する）
# load_and_scale_image(画像パス, 変更倍率):
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)

def prepare_picture():
    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei = pygame.image.load("img/prog_city.png").convert()
    g.haikei = pygame.transform.scale(g.haikei, (640, 480))

    # キャラクターは倍率を指定を使用してロード
    g.robo1a = load_and_scale_image("img/robo1-a.png", 1/4)
    g.robo1b = load_and_scale_image("img/robo1-b.png", 1/4)
    g.robo2a = load_and_scale_image("img/robo2-a.png", 1/6)
    g.robo2b = load_and_scale_image("img/robo2-b.png", 1/6)
    g.robo3a = load_and_scale_image("img/robo3-a.png", 1/7)
    g.robo3b = load_and_scale_image("img/robo3-b.png", 1/7)

def prepare_sound():
    g.bgm = pygame.mixer.Sound("sound/bgm.mp3")

def parts_init():
    # pygame モジュールの初期化,設定
    pygame.init()
    pygame.mixer.init()

    g.screen = pygame.display.set_mode((WIDTH, HIGHT))
    g.font = pygame.font.SysFont("meiryo", 20)
    g.title_font = pygame.font.SysFont("meiryo", 55)

    # 画像の準備
    prepare_picture()

    # サウンドの準備
    prepare_sound()

    # タイトルを設定
    pygame.display.set_icon(g.robo1a)
    pygame.display.set_caption('スタートアップ')

#
# BGM 再生
#
def play_bgm_sound():
    g.bgm.set_volume(0.2)
    g.bgm.play(-1)

def draw_haikei():
    # 背景画像を2枚描画する
    g.bgx = (g.bgx - 0.5) % WIDTH
    g.screen.blit(g.haikei, (g.bgx, 0))
    g.screen.blit(g.haikei, (g.bgx - WIDTH, 0))

def draw_robo1(start_time = 0, end_time = 100000):
    if (start_time < g.tick and g.tick < end_time):
        robo1_x = 100 #✅ここを変えるとキャラクターの位置（座標）を変えることができます
        robo1_y = 300 #✅ここを変えるとキャラクターの位置（座標）を変えることができます
        if ((g.tick//0.3) % 2 == 0):
            g.screen.blit(g.robo1a, (robo1_x, robo1_y))
        else:
            g.screen.blit(g.robo1b, (robo1_x, robo1_y))

def draw_robo2(start_time = 0, end_time = 100000):
    if (start_time < g.tick and g.tick < end_time):
        robo2_x = 400 #✅ここを変えるとキャラクターの位置（座標）を変えることができます
        robo2_y = 50  #✅ここを変えるとキャラクターの位置（座標）を変えることができます
        if ((g.tick//0.3) % 2 == 0):
            g.screen.blit(g.robo2a, (robo2_x, robo2_y))
        else:
            g.screen.blit(g.robo2b, (robo2_x, robo2_y-10))

def draw_robo3(start_time = 0, end_time = 100000):
    if (start_time < g.tick and g.tick < end_time):
        robo3_y = 370 #✅ここを変えるとキャラクターの位置（座標）を変えることができます
        g.robo3_x = g.robo3_x - 0.02 #✅少しずつ下がる仕組み。行12の数値を変えると初期位置を変えれます。
        if ((g.tick//0.3) % 2 == 0):
            g.screen.blit(g.robo3a, (g.robo3_x-20, robo3_y))
        else:
            g.screen.blit(g.robo3b, (g.robo3_x-20, robo3_y))


#セリフの画面描画関数
#文字数が多い場合は改行。画面外に出る場合は文字切れする
def draw_moji(moji="文字が未設定です", start_time=0, end_time=100000000):
    if start_time <= g.tick and g.tick <= end_time:
        g.screen.fill(CYAN) #✅変えるとセリフの背景の色が変わります。19行~27行の定数(REDなど)か、(0,0,0)の形式でRGB設定でも可能

        # フォントサイズの設定
        font_size = 35  #✅左の数字を変えると、セリフの文字サイズ変更できます
        font = pygame.font.SysFont("meiryo", font_size)

        # テキストを行に分割
        lines = []
        current_line = ""
        for char in moji:
            # 現在の行に次の文字を追加してテスト
            test_line = current_line + char
            test_render = font.render(test_line, True, WHITE)
            if test_render.get_width() > g.screen.get_width():
                # 現在の行をlinesに追加し、新しい行を始める
                lines.append(current_line)
                current_line = char
            else:
                current_line += char
        lines.append(current_line)  # 最後の行を追加

        # 行ごとに描画
        y = g.screen.get_height() / 2 - len(lines) * font_size / 2 - font_size
        for line in lines:
            text_render = font.render(line, True, WHITE)
            g.screen.blit(text_render, (20, y))
            y += text_render.get_height()  # 次の行の位置
