#
#   parts.py
#

import pygame
from pygame.locals import *
import pygame.mixer
import sys
import time
import random
#import pyautogui as pag    # スクリーンショット用
#import pygetwindow as gw   # スクリーンショット用
import math

# 定数定義
WIDTH = 640         # 画面横幅の設定
HIGHT = 480         # 画面高さの設定

#🔰ゲーム時間を変える場合はこの数字を変える
TIME_OUT = 10       #ゲームのプレイ時間[秒]

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

MOVE_MAX_X = 430
MOVE_MIN_X = 130
MOVE_MAX_Y = 370
MOVE_MIN_Y = -60

INIT_RED_X = 120
INIT_RED_Y = 30
INIT_BLUE_X = 430
INIT_BLUE_Y = 300

#グローバル変数の初期化
class g:
    MODE_TITLE = 0
    MODE_SELECT_ITEM = 1
    MODE_PLAY = 2
    MODE_JUDGE = 3
    MODE_END = 4
    red_x = INIT_RED_X
    red_y = INIT_RED_Y
    blue_x = INIT_BLUE_X
    blue_y = INIT_BLUE_Y
    red_speed = 5 
    blue_speed = 5
    selected_item_red = 1
    selected_item_blue = 1
    red_dir = 90
    blue_dir = 270
    tick = 0
    ink_stamp_records = []  # インクスタンプの位置とタイプを記録するリスト
    costume_change_time_red = 0
    costume_red = 0
    costume_change_time_blue = 0
    costume_blue = 0
    red_facing_right = True
    blue_facing_right = False
    red_point = 0
    blue_point = 0



#
# 初期化処理
#
def parts_init():
    pygame.init()
    
    g.mode = g.MODE_TITLE
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
    pygame.display.set_icon(g.red)
    pygame.display.set_caption('PAINT TO WIN GAME')


# 画像のサイズ設定処理
# （画像をロードし、サイズを取得後、サイズ変更する）
# load_and_scale_image(画像パス, 変更倍率):
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)

# スプライトズ設定処理
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
    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.title = pygame.image.load("img/タイトル.png").convert()
    g.title = pygame.transform.scale(g.title, (WIDTH, HIGHT))
    g.item_haikei = pygame.image.load("img/アイテム選択背景.png").convert()
    g.item_haikei = pygame.transform.scale(g.item_haikei, (WIDTH, HIGHT))
    g.haikei = pygame.image.load("img/はいけい.png").convert()
    g.haikei = pygame.transform.scale(g.haikei, (WIDTH, HIGHT))

    # 吹き出し
    g.hukidasi = load_and_scale_image("img/吹き出し.png", 1)
    # 赤ブルーム画像読み込み
    g.item_red = load_and_scale_image("img/赤ブルーム1.png", 2/3)
    g.red = load_and_scale_image("img/赤ブルーム1.png", 1/4)
    g.red1 = load_and_scale_image("img/赤ブルーム2.png", 1/4)

    # ✅プログラミングチャレンジ5 
    g.title_red = load_and_scale_image("img/赤ブルーム1.png", 1/6)


    # 青ブルーム画像読み込み
    g.title_blue = load_and_scale_image("img/青ブルーム1.png", 1)
    g.blue = load_and_scale_image("img/青ブルーム1.png", 1/4)
    g.blue1 = load_and_scale_image("img/青ブルーム2.png", 1/4)
    # えのぐ
    g.red_ink = load_and_scale_image("img/えのぐ赤.png", 1/4)
    g.red_ink_big = load_and_scale_image("img/えのぐ赤.png", 1/3)
    g.blue_ink = load_and_scale_image("img/えのぐ青.png", 1/4)
    g.blue_ink_big = load_and_scale_image("img/えのぐ青.png", 1/3)
    # アイテム
    g.item_shoes = prepare_sprite("img/アイテムスピードアップ.png", 1/3, (200, 180))
    g.item_shoes_big = prepare_sprite("img/アイテムスピードアップ.png", 1/2, (200, 180))
    g.item_ink = prepare_sprite("img/アイテムえのぐ.png", 1/3, (450, 180))
    g.item_ink_big = prepare_sprite("img/アイテムえのぐ.png", 1/2, (450, 180))
    g.select_item_ink_red = load_and_scale_image("img/アイテムえのぐ赤.png", 1/5)
    g.select_item_ink_blue = load_and_scale_image("img/アイテムえのぐ青.png", 1/5)
    g.select_item_speedup_red = load_and_scale_image("img/アイテムスピードアップ赤.png", 1/5)
    g.select_item_speedup_blue = load_and_scale_image("img/アイテムスピードアップ青.png", 1/5)
    # スタンプ
    g.ink_stamp_images = {    # スタンプ画像
        'stamp1': g.red_ink,
        'stamp2': g.blue_ink,
        'stamp3': g.red_ink_big,
        'stamp4': g.blue_ink_big
    }
    # その他
    g.point_sikaku = load_and_scale_image("img/得点操作.png", 1/2)

#
# 音準備
#
def prepare_sound():
   if g.sound_ok:
      g.bgm = pygame.mixer.Sound("sound/bgm.mp3")
      g.decide_s = pygame.mixer.Sound("sound/決定音.mp3")
      g.select_s = pygame.mixer.Sound("sound/選択音.mp3")

#
# BGM再生
#
def play_bgm_sound():
   if g.sound_ok:
      g.bgm.set_volume(0.5)
      g.bgm.play(-1)

#
# 決定音再生
#
def play_decide_sound():
   if g.sound_ok:
      g.decide_s.play()

#
# 選択音再生
#
def play_select_sound():
   if g.sound_ok:
      g.select_s.play()

#
# BGM終了
#
def stop_bgm():
   if g.sound_ok:
       g.bgm.fadeout(100)


#
# 指定された時間待つ(時間経過後のイベントチェックもする)
#
def wait_time(times):
    StartTime = pygame.time.get_ticks()
    while True:
        pygame.time.delay(10)
        pygame.display.update()

        if g.mode == g.MODE_SELECT_ITEM:
            return
        if (pygame.time.get_ticks() - StartTime) > times * 1000:
            return

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_event(event)
            if event.type == KEYDOWN:
                if g.mode == g.MODE_TITLE:
                    if event.key == pygame.K_SPACE:
                        g.mode = g.MODE_SELECT_ITEM
                        return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
#
# 背景を描く
#
def draw_haikei():
    g.screen.blit(g.haikei, (0,0))

#
# 赤ブルームを描く
#
def draw_red():
    g.screen.blit(g.red, (g.red_x, g.red_y))

#
# 青ブルームを描く
#
def draw_blue():
    g.screen.blit(g.blue, (g.blue_x, g.blue_y))

#
# 赤ブルームの得点の判定
#
def judge_red_point(x, y):
    red, green, blue, _ = g.screen.get_at((x, y))
    if red == 255 and green == 0 and blue == 0:
        return True
    else:
        return False

#
# 青ブルームの得点の判定
#
def judge_blue_point(x, y):
    red, green, blue, _ = g.screen.get_at((x, y))
    if red == 0 and green == 38 and blue == 255:
        return True
    else:
        return False

#
# すべてのスタンプ位置にえのぐを描画
#
def draw_ink_stamp():
    for pos, dir, stamp_type in g.ink_stamp_records:
        g.screen.blit(pygame.transform.rotate(g.ink_stamp_images[stamp_type], dir - 90), pos)

#
# タイトル画面に赤ブルームを描く
#
def red_stamp():
    g.screen.blit(g.title_red, (g.red_x, g.red_y))

#
# 試合開始前の初期化
#
def init_mode_play():
    g.mode = g.MODE_PLAY
    g.red_x = INIT_RED_X
    g.red_y = INIT_RED_Y
    g.blue_x = INIT_BLUE_X
    g.blue_y = INIT_BLUE_Y
    g.tick_start = pygame.time.get_ticks()
    g.selected_item_blue = random.randint(1, 2)
    if g.selected_item_blue == 2:
        g.blue_speed = 8
    play_bgm_sound()

#
# マウスイベント処理
#
def mouse_event(event):
    if g.mode == g.MODE_SELECT_ITEM:
        if g.item_ink_big.rect.collidepoint(event.pos):
            g.selected_item_red = 1
            play_decide_sound()
            init_mode_play()

        if g.item_shoes_big.rect.collidepoint(event.pos):
            g.selected_item_red = 2
            g.red_speed = 8
            play_decide_sound()
            init_mode_play()

#
# ボックスを描く
#
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
# アイテム選択中の処理
#
def select_item():
    while g.mode == g.MODE_SELECT_ITEM:
        g.screen.blit(g.item_haikei, (0,0))
        g.screen.blit(g.item_red, (20, 280))
        g.screen.blit(g.hukidasi, (150, 280))
        text = g.font.render("使うアイテムをクリックしよう！", True, (0,0,0))
        g.screen.blit(text, [175, 303])

        mouse_pos = pygame.mouse.get_pos()
        g.screen.blit(g.item_ink.image, g.item_ink.rect)
        g.screen.blit(g.item_shoes.image, g.item_shoes.rect)
        if g.item_ink.rect.collidepoint(mouse_pos):
            g.screen.blit(g.item_ink_big.image, g.item_ink_big.rect)
            if g.selected_item_red != 1:
                g.selected_item_red = 1
                play_select_sound()
        elif g.item_shoes.rect.collidepoint(mouse_pos):
            g.screen.blit(g.item_shoes_big.image, g.item_shoes_big.rect)
            if g.selected_item_red != 2:
                g.selected_item_red = 2
                play_select_sound()
        else:
            g.selected_item_red = 0
        update_and_eventchk()

#
# 選択されたアイテムを描く
#
def draw_selected_item():
    item_pos_red = (20, 50)
    item_pos_blue = (530, 50)
    if g.selected_item_red == 1:
        g.screen.blit(g.select_item_ink_red, item_pos_red)
    elif g.selected_item_red == 2:
        g.screen.blit(g.select_item_speedup_red, item_pos_red)
    if g.selected_item_blue == 1:
        g.screen.blit(g.select_item_ink_blue, item_pos_blue)
    elif g.selected_item_blue == 2:
        g.screen.blit(g.select_item_speedup_blue, item_pos_blue)

#
# ゲーム実行中の処理
#
def play_game():
    
    while g.mode == g.MODE_PLAY:
        draw_haikei()
        draw_selected_item()
        draw_ink_stamp()
        move_blue()
        move_red()

        g.tick = pygame.time.get_ticks() - g.tick_start
        draw_box(10, 440, 55, 30, str(int(TIME_OUT - g.tick / 1000)))
        if (g.tick > TIME_OUT * 1000):
            g.mode = g.MODE_JUDGE

        if g.costume_red == 0:
            if g.red_facing_right:
                red = g.red
            else:
                red = pygame.transform.flip(g.red, True, False)
        else:
            if g.red_facing_right:
                red = g.red1
            else:
                red = pygame.transform.flip(g.red1, True, False)
        g.screen.blit(red, (g.red_x, g.red_y))

        if g.costume_blue == 0:
            if g.blue_facing_right:
                blue = g.blue
            else:
                blue = pygame.transform.flip(g.blue, True, False)
        else:
            if g.blue_facing_right:
                blue = g.blue1
            else:
                blue = pygame.transform.flip(g.blue1, True, False)

        g.screen.blit(blue, (g.blue_x, g.blue_y))
        update_and_eventchk()

#
# 赤ブルームのコスチュームを変える
#
def change_costume_red():
    current_time = pygame.time.get_ticks()
    if current_time - g.costume_change_time_red > 100:
        g.costume_change_time_red = current_time
        if g.costume_red == 0:
            g.costume_red = 1
        else:
            g.costume_red = 0

#
# 青ブルームのコスチュームを変える
#
def change_costume_blue():
    current_time = pygame.time.get_ticks()
    if current_time - g.costume_change_time_blue > 100:
        g.costume_change_time_blue = current_time
        if g.costume_blue == 0:
            g.costume_blue = 1
        else:
            g.costume_blue = 0

#
# 赤ブルームを動かす
#
def move_red():
    pressed_keys = pygame.key.get_pressed()
    if (pressed_keys[K_RIGHT] or pressed_keys[K_LEFT] or
        pressed_keys[K_UP] or pressed_keys[K_DOWN]):
        change_costume_red()

    if pressed_keys[K_RIGHT]:
        g.red_facing_right = True
        g.red_dir = 90
        if g.red_x < MOVE_MAX_X:
            g.red_x += g.red_speed
            put_red_ink_stamp()
    if pressed_keys[K_LEFT]:
        g.red_dir = 270
        g.red_facing_right = False
        if g.red_x > MOVE_MIN_X:
            g.red_x -= g.red_speed
            put_red_ink_stamp()
    if pressed_keys[K_UP]:
        g.red_dir = 0
        if g.red_y > MOVE_MIN_Y:
            g.red_y -= g.red_speed
            put_red_ink_stamp()
    if pressed_keys[K_DOWN]:
        g.red_dir = 180
        if g.red_y < MOVE_MAX_Y:
            g.red_y += g.red_speed
            put_red_ink_stamp()

#
# 青ブルームを動かす
#
def move_blue():
    change_costume_blue()
    g.blue_x += g.blue_speed * math.sin(math.radians(g.blue_dir))
    g.blue_y += g.blue_speed * math.cos(math.radians(g.blue_dir))
    put_blue_ink_stamp()
    if (g.blue_x < MOVE_MIN_X):
        g.blue_dir = random.randint(0, 180)
    if (g.blue_x > MOVE_MAX_X):
        g.blue_dir = random.randint(180, 360)
    if (g.blue_y < MOVE_MIN_Y):
        g.blue_dir = random.randint(-90, 90)
    if (g.blue_y > MOVE_MAX_Y):
        g.blue_dir = random.randint(90, 270)
    if g.blue_dir >= 0 and g.blue_dir < 180:
        g.blue_facing_right = True
    else:
        g.blue_facing_right = False

#
# スタンプ情報を記録（位置とタイプと方向）
#
def put_ink_stamp(stamp, x, y, dir):
    if stamp == 'stamp1' or stamp == 'stamp3':
        if g.red_facing_right:
            position = (x, y + 75)
        else:
            position = (x + 40, y + 75)
    else:
        if g.blue_facing_right:
            position = (x, y + 75)
        else:
            position = (x + 40, y + 75)
    g.ink_stamp_records.append((position, dir, stamp))

#
# 赤ブルームのインクスタンプを記録する
#
def put_red_ink_stamp():
    if g.selected_item_red == 1:
        put_ink_stamp('stamp3', g.red_x, g.red_y, g.red_dir)
    else:
        put_ink_stamp('stamp1', g.red_x, g.red_y, g.red_dir)

#
# 青ブルームのインクスタンプを記録する
#
def put_blue_ink_stamp():
    if g.selected_item_blue == 1:
        put_ink_stamp('stamp4', g.blue_x, g.blue_y, g.blue_dir)
    else:
        put_ink_stamp('stamp2', g.blue_x, g.blue_y, g.blue_dir)


#
# 画面更新とユーザー操作を監視
#

def update_and_eventchk():
    pygame.display.update()
    g.clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


#ポイントを表示する
def draw_point():
    draw_box(250-100, 440-5, 55 + 105, 30 + 10, "赤色　　　　", GRAY, GRAY, DARKGRAY)
    draw_box(250,     440,   55,       30,      str(g.red_point))
    draw_box(430-100, 440-5, 55 + 105, 30 + 10, "青色　　　　", GRAY, GRAY, DARKGRAY)
    draw_box(430,     440,   55,       30,      str(g.blue_point))
    

#色判定
def judge_point(x,y):
    if judge_red_point(x, y):
        g.red_point = g.red_point + 1
    if judge_blue_point(x, y):
        g.blue_point = g.blue_point + 1
#ポイントリセット
def reset_point():
    g.red_point = 0
    g.blue_point = 0