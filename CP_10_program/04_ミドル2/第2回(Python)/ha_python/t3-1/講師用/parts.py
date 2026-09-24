#
#   parts.py
#

import pygame
from pygame.locals import *
import pygame.mixer
import sys
import time
import random
import math

# 定数定義（じょうすう／ていすう　ていぎ）
WIDTH = 640          # 画面横幅の設定
HIGHT = 480          # 画面高さの設定

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

#グローバル変数の初期化
class g:
    MODE_OPENING = 0
    MODE_START = 1
    MODE_TIMEUP = 2
    MODE_END = 3
    mode = 0
    candy_num = [0] * 4
    candy_time = 0
    dose_candy = 0
    obake_candy = 0
    kakudo = 0
    obake_yure = 0
    house = []
    bgm2_play = False
    obake_facing_right = False
    dose_facing_right = True
    obake_get_time = 0
    dose_get_time = 0
    opening_serihu = 0
    serihu_order = 0

#
# 初期化処理
#
def parts_init():
    pygame.init()

    g.mode = g.MODE_OPENING
    g.clock = pygame.time.Clock()

    try:
        pygame.mixer.init()
        g.sound_ok = True
    except Exception as e:
        print(f"サウンド初期化エラーが発生しました: {e}")
        g.sound_ok = False

    g.screen = pygame.display.set_mode((WIDTH, HIGHT))
    g.font = pygame.font.SysFont("meiryo", 18)

    # 画像の準備
    prepare_image()

    # サウンドの準備
    prepare_sound()

    # ウインドウタイトルを設定
    pygame.display.set_icon(g.obake.image) ####
    pygame.display.set_caption('Halloween') ####

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
    dose_init_pos =  (WIDTH / 2, HIGHT / 2)
    obake_init_pos =  (WIDTH / 2, HIGHT / 2)
    house_a_init_pos =  (WIDTH / 2 - 275, HIGHT / 2 - 150)
    house_b_init_pos =  (WIDTH / 2 + 275, HIGHT / 2 - 150)
    house_c_init_pos =  (WIDTH / 2 - 275, HIGHT / 2 + 180)
    house_d_init_pos =  (WIDTH / 2 + 275, HIGHT / 2 + 180)

    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei = pygame.image.load("img/背景.png").convert()
    g.haikei = pygame.transform.scale(g.haikei, (WIDTH, HIGHT))
    g.hukidashi = load_and_scale_image("img/吹き出し.png", 2/3)
    g.inv_hukidashi = pygame.transform.flip(g.hukidashi, True, False)
    g.big_hukidashi = load_and_scale_image("img/吹き出し.png", 4/5)
    g.big_inv_hukidashi = pygame.transform.flip(g.big_hukidashi, True, False)
    g.big_dose = load_and_scale_image("img/ドース.png", 1/3)
    g.big_obake = load_and_scale_image("img/obake.png", 1/5)
    g.dose = prepare_sprite("img/歩く.png", 1/6, dose_init_pos)
    g.obake = prepare_sprite("img/obake.png", 1/14, obake_init_pos)
    g.house.append(prepare_sprite("img/house.png", 1/14, house_a_init_pos))
    g.house.append(prepare_sprite("img/house.png", 1/14, house_b_init_pos))
    g.house.append(prepare_sprite("img/house.png", 1/14, house_c_init_pos))
    g.house.append(prepare_sprite("img/house.png", 1/14, house_d_init_pos))
    g.num = []
    for i in range(0, 10):
        g.num.append(load_and_scale_image(f'img/{i}.png', 1/3))

#
# 音声ファイルの読み出しとボリューム設定
#
def load_sound_and_set_volume(audio_file, volume):
    sound = pygame.mixer.Sound(audio_file)
    sound.set_volume(volume)
    return sound

#
# 音準備
#
def prepare_sound():
    if g.sound_ok:
        g.obake_get_snd = load_sound_and_set_volume("sound/おばけお菓子ゲット.mp3", 0.5)
        g.timeup_snd = load_sound_and_set_volume("sound/タイムアップ.mp3", 0.5)
        g.dose_get_snd = load_sound_and_set_volume("sound/ドースお菓子ゲット.mp3", 0.5)
        g.bgm1 = load_sound_and_set_volume("sound/前半BGM.mp3", 0.2)
        g.bgm2 = load_sound_and_set_volume("sound/後半BGM.mp3", 0.2)

#
# ドースのお菓子ゲット音再生
#
def play_dose_get_sound():
    if g.sound_ok == True:
        g.dose_get_snd.play()

#
# おばけのお菓子ゲット音再生
#
def play_obake_get_sound():
    if g.sound_ok == True:
        g.obake_get_snd.play()

#
# タイムアップ音再生
#
def play_timeup_sound():
    if g.sound_ok == True:
        g.timeup_snd.play()

#
# BGM 再生
#
def play_bgm1_sound():
    if g.sound_ok == True:
        g.bgm1.play(-1)

#
# BGM 変更
#
def change_bgm():
    if g.sound_ok == True:
        if g.bgm2_play == False:
            g.bgm1.stop()
            g.bgm2.play(-1)
            g.bgm2_play = True

#
# BGM を止める
#
def stop_bgm():
    if g.sound_ok == True:
        g.bgm1.stop()
        g.bgm2.stop()

#
# 背景と家の描画
#
def draw_haikei_house():
    g.screen.blit(g.haikei, (0,0))
    g.screen.blit(g.house[0].image, g.house[0].rect)
    g.screen.blit(g.house[1].image, g.house[1].rect)
    g.screen.blit(g.house[2].image, g.house[2].rect)
    g.screen.blit(g.house[3].image, g.house[3].rect)

#
# ドースの描画
#
def draw_dose():
    g.screen.blit(g.dose.image, g.dose.rect)

#
# おばけの描画
#
def draw_obake():
    g.screen.blit(g.obake.image, g.obake.rect)

#
# 大きいドースの描画
#
def draw_big_dose(dose_pos):
    g.screen.blit(g.big_dose, dose_pos)

#
# 大きいおばけの描画
#
def draw_big_obake(pos):
    g.screen.blit(g.big_obake, pos)

#
# 残り時間の描画
#
def disp_nokori_time(nokori_time):
    ten_digit = int(nokori_time / 10)
    g.screen.blit(g.num[ten_digit], (WIDTH / 2 - 22 - 30, HIGHT / 2 - 240))
    one_digit = nokori_time % 10
    g.screen.blit(g.num[one_digit], (WIDTH / 2 + 22 - 30, HIGHT / 2 - 240))


#
# お菓子の数の描画
#
def disp_candy_num():
    (out_x, out_y, out_width, out_hight) = (WIDTH / 2 - 310, HIGHT / 2 - 230, 130, 40)
    draw_box(out_x, out_y, out_width, out_hight, "お菓子" + str(g.candy_num[0]) + "個", GRAY, GRAY, DARKGRAY)
    (out_x, out_y, out_width, out_hight) = (WIDTH / 2 + 180, HIGHT / 2 - 230, 130, 40)
    draw_box(out_x, out_y, out_width, out_hight, "お菓子" + str(g.candy_num[1]) + "個", GRAY, GRAY, DARKGRAY)
    (out_x, out_y, out_width, out_hight) = (WIDTH / 2 - 310, HIGHT / 2 + 100, 130, 40)
    draw_box(out_x, out_y, out_width, out_hight, "お菓子" + str(g.candy_num[2]) + "個", GRAY, GRAY, DARKGRAY)
    (out_x, out_y, out_width, out_hight) = (WIDTH / 2 + 180, HIGHT / 2 + 100, 130, 40)
    draw_box(out_x, out_y, out_width, out_hight, "お菓子" + str(g.candy_num[3]) + "個", GRAY, GRAY, DARKGRAY)

#
# 四角とその中に文字の描画
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
# ドースの移動
#
def move_dose():
    keys = pygame.key.get_pressed()
    dose_speed = 3
    if check_collision_with_color(g.dose, (102, 68, 152)): #c78d50
        # print("道を外れた")
        dose_speed = 1

    if keys[pygame.K_RIGHT]:
        if g.dose.rect.centerx < WIDTH:
            g.dose.rect.x += dose_speed
            facing_dose(True)
    if keys[pygame.K_LEFT]:
        if g.dose.rect.centerx > 0:
            g.dose.rect.x -= dose_speed
            facing_dose(False)
    if keys[pygame.K_UP]:
        if g.dose.rect.centery > 0:
            g.dose.rect.y -= dose_speed
    if keys[pygame.K_DOWN]:
        if g.dose.rect.centery < HIGHT:
            g.dose.rect.y += dose_speed

#
# おばけの移動
#
def move_obake():
    # 縦に揺れる動き
    angle_radians = math.radians(g.kakudo)
    g.obake.rect.y += math.cos(angle_radians) + 0.5
    g.kakudo += 8

    max_candy = g.candy_num[0]
    max_house = 0
    for i in range(1,4):
        if g.candy_num[i] > max_candy:
            max_candy = g.candy_num[i]
            max_house = i
    x_zure = g.house[max_house].rect.x - g.obake.rect.x
    facing_obake(x_zure > 0)
    if x_zure != 0:
        g.obake.rect.x += (x_zure / abs(x_zure))
    y_zure = g.house[max_house].rect.y - g.obake.rect.y
    if y_zure != 0:
        g.obake.rect.y += (y_zure / abs(y_zure))

#
# おばけの向きを変える
#
def facing_obake(right):
    if right:
        if not g.obake_facing_right:
            g.obake_facing_right = True
            g.obake.image = pygame.transform.flip(g.obake.image, True, False)
    else:
        if g.obake_facing_right:
            g.obake_facing_right = False
            g.obake.image = pygame.transform.flip(g.obake.image, True, False)

#
# ドースの向きを変える
#
def facing_dose(right):
    if right:
        if not g.dose_facing_right:
            g.dose_facing_right = True
            g.dose.image = pygame.transform.flip(g.dose.image, True, False)
    else:
        if g.dose_facing_right:
            g.dose_facing_right = False
            g.dose.image = pygame.transform.flip(g.dose.image, True, False)

#
# Trick or Treat と言う
#
def disp_trick_or_treat():
    if pygame.time.get_ticks() - g.obake_get_time < 1000:
        draw_hukidashi(g.obake.rect.x, g.obake.rect.y - 50, "Trick or Treat..")
    if pygame.time.get_ticks() - g.dose_get_time < 1000:
        draw_hukidashi(g.dose.rect.x, g.dose.rect.y - 50, "Trick or Treat!")

#
# お菓子をとれたか判定
#
def get_candy_hantei():
    for i in range(4):
        if calculate_distance(g.dose, g.house[i]) < 40 and g.candy_num[i] != 0:
            play_dose_get_sound()
            g.dose_get_time = pygame.time.get_ticks()
            g.dose_candy += g.candy_num[i]
            g.candy_num[i] = 0
        if calculate_distance(g.obake, g.house[i]) < 40 and g.candy_num[i] != 0:
            play_obake_get_sound()
            g.obake_get_time = pygame.time.get_ticks()
            g.obake_candy += g.candy_num[i]
            g.candy_num[i] = 0

#
# 吹き出しにテキストを描く
#  左右反転対応
#
def draw_hukidashi(x, y, text_char, big = False):
    if x > WIDTH / 2:
        if big:
            g.screen.blit(g.big_inv_hukidashi, (x, y))
        else:
            g.screen.blit(g.inv_hukidashi, (x, y))
    else:
        if big:
            g.screen.blit(g.big_hukidashi, (x, y))
        else:
            g.screen.blit(g.hukidashi, (x, y))
    text = g.font.render(text_char, True, BLACK)
    # テキストの描画
    text_rect = text.get_rect(topleft=(x + 10, y + 5))
    g.screen.blit(text, text_rect)

#
# 2つのスプライトの距離を測る
#
def calculate_distance(sprite1, sprite2):
    # スプライトの中心座標を取得
    x1, y1 = sprite1.rect.center
    x2, y2 = sprite2.rect.center
    # ユークリッド距離の計算
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

#
# 色の衝突を検出する
#
def check_collision_with_color(sprite, color):
    sprite_mask = pygame.mask.from_surface(sprite.image)
    offset = (sprite.rect.left, sprite.rect.top)
    for x in range(sprite.rect.width):
        for y in range(sprite.rect.height):
            if sprite_mask.get_at((x, y)):
                if 0 <= offset[0] + x < WIDTH and 0 <=offset[1] + y < HIGHT:
                    if g.screen.get_at((offset[0] + x, offset[1] + y))[:3] == color:
                        return True
    return False

#
# 画面更新とユーザー操作を監視
#
def update_and_eventchk():
    pygame.display.update()
    g.clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
