#
#   parts.py
#

import pygame
from pygame.locals import *
import pygame.mixer
import random
import sys
import time

# 定数定義（じょうすう／ていすう　ていぎ）
WIDTH = 640          # 画面横幅の設定
HIGHT = 480          # 画面高さの設定

RED = (255, 0, 0)               # 赤
GREEN = (0, 255, 0)             # 緑
BLUE = (0, 0, 255)              # 青
YELLOW = (255, 255, 0)          # 黄
CYAN = (0, 255, 255)            # シアン
MAGENTA = (255, 0, 255)         # マゼンタ
WHITE = (255, 255, 255)         # 白
BLACK = (0, 0, 0)               # 黒
GRAY = (230, 240, 255)          # 灰色
DARKGRAY = (87, 94, 117)        # 黒灰色
ORANGE = (255, 140, 26)         # オレンジ
MILK_CHOCO = (210, 105, 30)     # ミルクチョコレート色
DARK_CHOCO = (139, 69, 19)      # ダークチョコレート色
GOLD = (255, 215, 0)            # ゴールド
SILVER = (192, 192, 192)        # シルバー
PINK = (255, 105, 180)          # ピンク
LIGHT_BLUE = (0, 191, 255)      # 明るい青
PASTEL_GREEN = (152, 251, 152)  # パステルグリーン

ICHIGO = 0
LEMON = 1
MELON = 2
BLUE_HAWAII = 3

#グローバル変数の初期化
class g:
    MODE_DROP_ICE = 0
    MODE_BODY = 1
    MODE_POUR_SYRUP = 2
    MODE_TOPPING = 3
    MODE_COMPLETE = 4
    syrup_machine_num = 0
    stop_syrup = False
    syrup_sprites = []
    syrup_flavors = []
    ichigo_num = 0
    lemon_num = 0
    melon_num = 0
    blue_hawaii_num = 0
    total_syrup_num = 0
    topping_num = 0
    topping_pushed = False
    chocolates = []
    chocolates_moving = []
    watermelon_moving = 0
    watermelon_rot = 0
    cookie_moving = 0
    cookie_rot = 0
    prev_time = -1
#
# 初期化処理
#
def parts_init():
    pygame.init()

    g.mode = g.MODE_DROP_ICE
    g.clock = pygame.time.Clock()

    try:
        pygame.mixer.init()
        g.sound_ok = True
    except Exception as e:
        print(f"サウンド初期化エラーが発生しました: {e}")
        g.sound_ok = False

    g.screen = pygame.display.set_mode((WIDTH, HIGHT))
    g.font = pygame.font.SysFont("meiryo", 20)

    # 画像の準備
    prepare_image()

    # サウンドの準備
    prepare_sound()

    # ウインドウタイトルを設定
    pygame.display.set_icon(g.cup.image) ####
    pygame.display.set_caption('かき氷シミュレーター')

# 画像のサイズ設定処理
# （画像をロードし、サイズを取得後、サイズ変更する）
# load_and_scale_image(画像パス, 変更倍率):
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)

# スプライト設定処理
# （画像をロードし、サイズ、位置を設定する）
def prepare_sprite(image, scale, init_pos):
    sprite = pygame.sprite.Sprite()
    sprite.image = load_and_scale_image(image, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = init_pos
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite

#
# 画像準備
#
def prepare_image():
    init_pos = (WIDTH / 2, HIGHT / 2)
    cup_init_pos = (WIDTH / 2, HIGHT / 2 + 80)
    syrup_machine_init_pos = (WIDTH / 2, HIGHT / 2 - 230)
    right_arrow_init_pos = (WIDTH / 2 + 260, HIGHT / 2 - 200)
    left_arrow_init_pos = (WIDTH / 2 - 260, HIGHT / 2 - 200)
    right_triangle_init_pos = (WIDTH / 2 - 177, HIGHT / 2 - 180)
    left_triangle_init_pos = (WIDTH / 2 - 303, HIGHT / 2 - 180)
    topping_init_pos = (WIDTH / 2 - 240, HIGHT / 2 - 180)
    watermelon_init_pos = (WIDTH / 2, HIGHT / 2 - 180)
    cookie_init_pos = (WIDTH / 2, HIGHT / 2 - 180)
    to_next_init_pos = (WIDTH / 2 + 240, HIGHT / 2 + 200)

    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei = pygame.image.load("img/背景.png").convert()
    g.haikei = pygame.transform.scale(g.haikei, (WIDTH, HIGHT))

    g.right_arrow = prepare_sprite("img/arrow.png", 1/2, right_arrow_init_pos)
    g.left_arrow = prepare_sprite("img/arrow.png", 1/2, left_arrow_init_pos)
    g.left_arrow.image = pygame.transform.flip(g.left_arrow.image, True, False)
    g.to_next = prepare_sprite("img/次へ.png", 1/2, to_next_init_pos)
    g.cup = prepare_sprite("img/cup05.png", 1/3, cup_init_pos)
    g.cups = []
    for i in range(1, 6):
        g.cups.append(load_and_scale_image(f"img/cup0{i}.png", 1/3))
    for i in range(1, 3):
        g.syrup_machine = prepare_sprite("img/シロップマシン_イチゴ.png", 1/2, syrup_machine_init_pos)
    g.syrup_machines = []
    g.syrup_machines.append(load_and_scale_image("img/シロップマシン_イチゴ.png", 1/2))
    g.syrup_machines.append(load_and_scale_image("img/シロップマシン_レモン.png", 1/2))
    g.syrup_machines.append(load_and_scale_image("img/シロップマシン_メロン.png", 1/2))
    g.syrup_machines.append(load_and_scale_image("img/シロップマシン_ブルーハワイ.png", 1/2))
    g.syrup = prepare_sprite("img/シロップ_イチゴ.png", 1/2, init_pos)
    g.syrups = []
    g.syrups.append(load_and_scale_image("img/シロップ_イチゴ.png", 1/2))
    g.syrups.append(load_and_scale_image("img/シロップ_レモン.png", 1/2))
    g.syrups.append(load_and_scale_image("img/シロップ_メロン.png", 1/2))
    g.syrups.append(load_and_scale_image("img/シロップ_ブルーハワイ.png", 1/2))

    g.right_triangle = prepare_sprite("img/triangle.png", 1/8, right_triangle_init_pos)
    g.left_triangle = prepare_sprite("img/triangle.png", 1/8, left_triangle_init_pos)
    g.left_triangle.image = pygame.transform.flip(g.left_triangle.image, True, False)
    g.topping = prepare_sprite("img/トッピングカラフルチョコ.png", 1/2, topping_init_pos)
    g.toppings = []
    g.toppings.append(load_and_scale_image("img/トッピングカラフルチョコ.png", 1/2))
    g.toppings.append(load_and_scale_image("img/トッピングスイカ.png", 1/2))
    g.toppings.append(load_and_scale_image("img/トッピングクッキー.png", 1/2))

    g.chocolate = prepare_sprite("img/チョコ.png", 1/4, init_pos)
    g.watermelon = prepare_sprite("img/watermelon.png", 1/2, watermelon_init_pos)
    g.cookie = prepare_sprite("img/cookie.png", 1/3, cookie_init_pos)
    g.sliced_ice = prepare_sprite("img/氷片.png", 1/3, init_pos)

    image_center = g.watermelon.rect.center  # 元の画像の中心座標
    g.watermelon_rot_rect = g.watermelon.image.get_rect(center=image_center)

    image_center = g.cookie.rect.center  # 元の画像の中心座標
    g.cookie_rot_rect = g.cookie.image.get_rect(center=image_center)

#
# 音準備
#
def prepare_sound():
    if g.sound_ok:
        pass

def draw_haikei():
    g.screen.blit(g.haikei, (0,0))

def draw_cup(cup):
    g.screen.blit(cup.image, cup.rect)

def draw_sliced_ice(sliced_ice):
    g.screen.blit(sliced_ice.image, sliced_ice.rect)

def draw_right_triangle():
    g.screen.blit(g.right_triangle.image, g.right_triangle.rect)

def draw_left_triangle():
    g.screen.blit(g.left_triangle.image, g.left_triangle.rect)

def draw_to_next():
    g.screen.blit(g.to_next.image, g.to_next.rect)

def draw_topping():
    g.topping.image = g.toppings[g.topping_num]
    g.screen.blit(g.topping.image, g.topping.rect)

def draw_syrup_machine():
    g.syrup_machine.image = g.syrup_machines[g.syrup_machine_num]
    g.screen.blit(g.syrup_machine.image, g.syrup_machine.rect)

def draw_right_arrow():
    g.screen.blit(g.right_arrow.image, g.right_arrow.rect)

def draw_left_arrow():
    g.screen.blit(g.left_arrow.image, g.left_arrow.rect)

def draw_to_next():
    g.screen.blit(g.to_next.image, g.to_next.rect)

def draw_chocolates(i):
    g.screen.blit(g.chocolates[i].image, g.chocolates[i].rect)

def draw_syrup(i):
    g.screen.blit(g.syrup_sprites[i].image, g.syrup_sprites[i].rect)

def draw_watermelon():
    g.screen.blit(g.watermelon.image, g.watermelon.rect)

def draw_cookie():
    g.screen.blit(g.cookie.image, g.cookie.rect)

def draw_syrup_num():
    (in_x, in_y, in_width, in_hight) = (110, 230, 55, 30)
    (out_x, out_y, out_width, out_hight) = (in_x - 100, in_y - 5, in_width + 105, in_hight + 10)
    draw_box(out_x, out_y, out_width, out_hight, "イチゴ　　　　", GRAY, GRAY, DARKGRAY)
    draw_box(in_x, in_y, in_width, in_hight, str(g.ichigo_num))

    (in_x, in_y, in_width, in_hight) = (110, 280, 55, 30)
    (out_x, out_y, out_width, out_hight) = (in_x - 100, in_y - 5, in_width + 105, in_hight + 10)
    draw_box(out_x, out_y, out_width, out_hight, "レモン　　　　", GRAY, GRAY, DARKGRAY)
    draw_box(in_x, in_y, in_width, in_hight, str(g.lemon_num))

    (in_x, in_y, in_width, in_hight) = (110, 330, 55, 30)
    (out_x, out_y, out_width, out_hight) = (in_x - 100, in_y - 5, in_width + 105, in_hight + 10)
    draw_box(out_x, out_y, out_width, out_hight, "メロン　　　　", GRAY, GRAY, DARKGRAY)
    draw_box(in_x, in_y, in_width, in_hight, str(g.melon_num))

    (in_x, in_y, in_width, in_hight) = (150, 380, 55, 30)
    (out_x, out_y, out_width, out_hight) = (in_x - 140, in_y - 5, in_width + 145, in_hight + 10)
    draw_box(out_x, out_y, out_width, out_hight, "ブルーハワイ　　　", GRAY, GRAY, DARKGRAY)
    draw_box(in_x, in_y, in_width, in_hight, str(g.blue_hawaii_num))

    (in_x, in_y, in_width, in_hight) = (110, 430, 55, 30)
    (out_x, out_y, out_width, out_hight) = (in_x - 100, in_y - 5, in_width + 105, in_hight + 10)
    draw_box(out_x, out_y, out_width, out_hight, "合計　　　　　", GRAY, GRAY, DARKGRAY)
    draw_box(in_x, in_y, in_width, in_hight, str(g.total_syrup_num))

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



    
def wait_time(times):
    StartTime = pygame.time.get_ticks()
    while True:
        pygame.time.delay(10)
        pygame.display.update()

        if (pygame.time.get_ticks() - StartTime) > times * 1000:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


#
# マウスイベント処理
#
def mouse_event(event):
    if g.mode == g.MODE_POUR_SYRUP:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # 右矢印がクリックされた判定
            if g.right_arrow.rect.collidepoint(pos):
                if g.syrup_machine_num == 3:
                    g.syrup_machine_num = 0
                else:
                    g.syrup_machine_num+=1

            # 左矢印がクリックされた判定
            if g.left_arrow.rect.collidepoint(pos):
                if g.syrup_machine_num == 0:
                    g.syrup_machine_num = 3
                else:
                    g.syrup_machine_num-=1

            # つぎへがクリックされた判定
            if g.to_next.rect.collidepoint(pos):
                g.mode = g.MODE_TOPPING
    elif g.mode == g.MODE_TOPPING:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # 右矢印がクリックされた判定
            if g.right_triangle.rect.collidepoint(pos):
                if g.topping_num == 2:
                    g.topping_num = 0
                else:
                    g.topping_num+=1

            # 左矢印がクリックされた判定
            if g.left_triangle.rect.collidepoint(pos):
                if g.topping_num == 0:
                    g.topping_num = 2
                else:
                    g.topping_num-=1

            # トッピングがクリックされた判定
            if g.topping.rect.collidepoint(pos):
                g.topping_pushed = True

            # つぎへがクリックされた判定
            if g.to_next.rect.collidepoint(pos):
                    g.mode = g.MODE_COMPLETE

#
# 画面更新とユーザー操作を監視
#
def update_and_eventchk():
    pygame.display.update()
    g.clock.tick(60)
    for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN
            or event.type == pygame.MOUSEBUTTONUP
            or event.type == pygame.MOUSEMOTION):
            mouse_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
