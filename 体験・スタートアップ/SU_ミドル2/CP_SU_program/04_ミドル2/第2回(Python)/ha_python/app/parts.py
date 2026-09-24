import pygame
import subprocess
import time
import os

# 定数定義
WIDTH = 640
HIGHT = 480
ICON_BASE_X = 229
ICON_BASE_Y = 65
ICON_DIFF_X = 74
ICON_DIFF_Y = 79
TEXT_OFFSET_Y = 49

# グローバル変数クラス
class global_values:
    icon = []
    icon_exist = []

# 設定したグローバル変数クラスをプログラム中で使えるようにする（インスタンス化）
g = global_values()

#
# 各種初期化
#
def parts_init():
    pygame.init()
    pygame.mixer.init()

    g.screen = pygame.display.set_mode((WIDTH, HIGHT))
    g.font = pygame.font.SysFont("meiryo", 10)

    # タイトルを設定
    g.blank_icon = pygame.image.load("img/smartphone.png").convert_alpha()
    pygame.display.set_icon(g.blank_icon)
    pygame.display.set_caption('ランチャー')

    # サウンドの準備

    # 画像の準備
    g.smartphone = pygame.image.load("img/smartphone.png").convert()
    g.smartphone = pygame.transform.rotozoom(g.smartphone, 0, 1/3.5)
    for i in range(5):
        for j in range(3):
            if i == 4:
                file_path = '../startup/startup_icon.png'
            else:
                file_path = f'../t{i + 1}_{j + 1}/t{i + 1}_{j + 1}_icon.png'

            if os.path.exists(file_path):
                g.icon_exist.append(True)
                g.icon.append(pygame.image.load(file_path).convert_alpha())
                
            else:
                g.icon_exist.append(False)
                g.icon.append(pygame.image.load(f'img/ブランクアイコン.png').convert_alpha())
            g.icon[i * 3 + j] = pygame.transform.rotozoom(g.icon[i * 3 + j], 0, 1/2.05)

#
# マウスクリック判定
#
def check_mouse_push(x, y):
    for i in range(5):
        for j in range(3):
            icon_no = i * 3 + j
            icon_x = ICON_BASE_X + j * ICON_DIFF_X
            icon_y = ICON_BASE_Y + i * ICON_DIFF_Y
            icon_size = 43

            if (icon_x < x and x < icon_x + icon_size and icon_y < y and y < icon_y + icon_size):
                if g.icon_exist[icon_no]:
                    if icon_no < 12:
                        cp = subprocess.run(['python', f't{i + 1}_{j + 1}.py'], cwd=f'../t{i + 1}_{j + 1}')
                    elif icon_no == 12:
                        cp = subprocess.run(['python',  'startup.py'], cwd=f'../startup')

#
# マウスイベント処理
#
def mouse_event(event):
    mouse_presses = pygame.mouse.get_pressed()
    if mouse_presses[0]:
        x, y = event.pos
        check_mouse_push(x, y)
