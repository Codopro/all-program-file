#
#   parts.py
#
import pygame
from pygame.locals import *
import pygame.mixer
import sys
import time
import random

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
    MODE_ROASTING = 0
    MODE_ROASTED = 1
    mode = MODE_ROASTING

    IMO_START = 0
    IMO_MOVING = 1
    IMO_ROASTING = 2
    IMO_ROASTED = 3
    imo_status = IMO_START

    imo_move_count = 0
    imo_pos = [150, 220]
    imo_kasoku = -10
    yakiguai = 0
    point_bairitu = 0
    fire_power = 0
    amasa = 0
    point = 0
    eval_comment = ""
    roasted_stage = 0

#
# 初期化処理
#
def parts_init():
    pygame.init()

    g.mode = g.MODE_ROASTING
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
    pygame.display.set_icon(g.imo_nama) ####
    pygame.display.set_caption('Sweet potato') ####


# 画像のサイズ設定処理
# （画像をロードし、サイズを取得後、サイズ変更する）
# load_and_scale_image(画像パス, 変更倍率):
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)

#
# 画像準備
#
def prepare_image():
    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei = pygame.image.load("img/背景.png").convert()
    g.haikei = pygame.transform.scale(g.haikei, (WIDTH, HIGHT))

    g.hukidashi = load_and_scale_image("img/吹き出し.png", 2/3)
    g.inv_hukidashi = pygame.transform.flip(g.hukidashi, True, False)

    g.imo_kogeta = load_and_scale_image("img/こげた.png", 1/5)
    g.imo_tyoudoii = load_and_scale_image("img/ちょうどいい.png", 1/5)
    g.imo_nama = load_and_scale_image("img/生.png", 1/5)
    g.imo_namayake = load_and_scale_image("img/生焼け.png", 1/5)
    g.imo = g.imo_nama

    g.fire1 = load_and_scale_image("img/火1.png", 1/2)
    g.fire2 = load_and_scale_image("img/火2.png", 1/2)
    g.fire3 = load_and_scale_image("img/火3.png", 1/2)
    g.fire1.set_alpha(256 * 70 / 100)
    g.fire2.set_alpha(256 * 70 / 100)
    g.fire3.set_alpha(256 * 70 / 100)
    g.fire = g.fire1

    g.wood_dark = load_and_scale_image("img/火が消えている.png", 1/4)
    g.wood_light = load_and_scale_image("img/火がついている.png", 1/4)

    g.dose_standing = load_and_scale_image("img/立つ.png", 1/3)
    g.dose_syonbori = load_and_scale_image("img/しょんぼり.png", 1/3)
    g.dose_perori = load_and_scale_image("img/ペロリ.png", 1/3)
    g.dose_eating1 = load_and_scale_image("img/食べる1.png", 1/3)
    g.dose_eating2 = load_and_scale_image("img/食べる2.png", 1/3)
    g.dose = g.dose_standing

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
        g.fire_snd = load_sound_and_set_volume("sound/焚き火の音.mp3", 0.5)

#
# 背景の描画
#
def draw_haikei():
    g.screen.blit(g.haikei, (0,0))

#
# ドースの描画
#
def draw_dose():
    g.screen.blit(g.dose, (50,200))

#
# ドースの描画(立っている)
#
def draw_dose_standing():
    g.screen.blit(g.dose_standing, (50,200))

#
# ドースの描画(食べている1)
#
def draw_dose_eating1():
    g.screen.blit(g.dose_eating1, (50,200))

#
# ドースの描画(食べている2)
#
def draw_dose_eating2():
    g.screen.blit(g.dose_eating2, (50,200))

#
# 木の描画
#
def draw_wood_dark():
    g.screen.blit(g.wood_dark, (400,350))

#
# いもの描画
#
def draw_imo():
    g.screen.blit(g.imo, g.imo_pos)

#
# たき火の描画
#
def draw_fire():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if g.fire_power < 100:
            g.fire_power += 1
    else:
        if g.fire_power > 1:
            g.fire_power -= 1

    # 20%の確率でランダムに変更
    if random.random() < 0.2:
        g.fire = random.choice([g.fire1, g.fire2, g.fire3])

    scale_factor = (g.fire_power / 4 + 20) / 100
    original_width, original_height = g.fire.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    fire = pygame.transform.scale(g.fire, new_size)

    if g.fire_power > 5:
        play_fire_snd()
        g.screen.blit(fire, (475 - scale_factor * 100, 330 - scale_factor * 120))

#
# たき火の音再生
#
def play_fire_snd():
    if g.sound_ok:
        if random.random() < 0.2:
            g.fire_snd.play()

#
# たき火の音を止める
#
def stop_fire_snd():
    if g.sound_ok:
        g.fire_snd.stop()

#
# いもの状態を変更する
#
def chg_roasting_imo():
    if g.imo_status == g.IMO_ROASTING:
        g.yakiguai += g.fire_power / 500
        g.amasa += (140 * g.fire_power - g.fire_power * g.fire_power) / 10000
        if round(g.yakiguai) < 40:
            g.imo = g.imo_nama
            draw_hukidashi(321, 250, "まだ生だよ…")
        elif round(g.yakiguai) < 80:
            g.imo = g.imo_namayake
            draw_hukidashi(321, 250, "もうちょっと焼こう")
        elif round(g.yakiguai) < 90:
            g.imo = g.imo_tyoudoii
            draw_hukidashi(321, 250, "今が食べどき！")
        else:
            g.imo = g.imo_kogeta
            draw_hukidashi(321, 250, "こげちゃった…")

#
# いもを動かす
#
def move_imo():
    if g.imo_status == g.IMO_MOVING:
        g.imo_pos[0] += 23
        g.imo_pos[1] += 7 + g.imo_kasoku
        g.imo_kasoku += 2
        g.imo_move_count += 1
        if g.imo_move_count > 10:
            g.imo_status = g.IMO_ROASTING

#
# ポイント倍率を決定する
#
def decide_bairitu():
    match g.imo:
        case g.imo_nama:
            g.point_bairitu = 0.1
        case g.imo_namayake:
            g.point_bairitu = 0.3
        case g.imo_tyoudoii:
            g.point_bairitu = 1
        case _:
            g.point_bairitu = 0.5

#
# 焼き上がり状態の時に芋とドースを描く
#
def draw_roasted_state_imo_dose(roasted_time):
    current_time = pygame.time.get_ticks()
    if g.roasted_stage == 0:
        draw_imo()
        draw_dose_eating1()
        if current_time > roasted_time + 1000:
            g.roasted_stage = 1
    elif g.roasted_stage == 1:
        draw_imo()
        draw_dose_eating2()
        if current_time > roasted_time + 2000:
            g.roasted_stage = 2
    elif g.roasted_stage == 2:
        draw_imo()
        draw_dose()
        draw_hukidashi(100, 140, g.eval_comment)
        if current_time > roasted_time + 4000:
            g.roasted_stage = 3
    elif g.roasted_stage == 3:
        draw_imo()
        draw_dose()
        draw_hukidashi(100, 140, str(round(g.amasa * g.point_bairitu)) + "ポイント！")
        if current_time > roasted_time + 6000:
            g.roasted_stage = 4
    else:
        draw_dose_standing()

#
# 吹き出しにテキストを描く
#  左右反転対応
#
def draw_hukidashi(x, y, text_char, big = False):
    if x > WIDTH / 2:
        g.screen.blit(g.inv_hukidashi, (x, y))
    else:
        g.screen.blit(g.hukidashi, (x, y))
    text = g.font.render(text_char, True, BLACK)
    # テキストの描画
    text_rect = text.get_rect(topleft=(x + 10, y + 5))
    g.screen.blit(text, text_rect)


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
