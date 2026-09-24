#
#   parts.py
#

import pygame
from pygame.locals import *
import pygame.mixer
import sys
import time
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

TRAINING_COLOR = (0xae, 0x62, 0x04)
BENKYO_COLOR  = (0x46, 0xaa, 0x00)
FASSION_COLOR = (0x00, 0x86, 0xc4)
ODEKAKE_COLOR = (0x7c, 0x30, 0xc2)
OYASUMI_COLOR = (0xdb, 0x00, 0x2c)

TILE_X = 30
TILE_Y = 380
TILE_DIFF_X = 120
TRAINING_TOP_LEFT = (TILE_X + TILE_DIFF_X * 0, TILE_Y)
BENKYO_TOP_LEFT   = (TILE_X + TILE_DIFF_X * 1, TILE_Y)
FASSION_TOP_LEFT  = (TILE_X + TILE_DIFF_X * 2, TILE_Y)
ODEKAKE_TOP_LEFT  = (TILE_X + TILE_DIFF_X * 3, TILE_Y)
OYASUMI_TOP_LEFT  = (TILE_X + TILE_DIFF_X * 4, TILE_Y)

#グローバル変数の初期化
class g:
    status_name = ["ちからづよさ", "かしこさ", "うつくしさ", "あかるさ", "たいりょく"]
    MODE_SELECT_MENU = 0
    MODE_MENU_SELECTED = 1
    MODE_STATUS_CHANGE = 2
    mode = MODE_SELECT_MENU
    HAIKEI_NONE = 0
    HAIKEI_TRAINING = 1
    HAIKEI_BENKYO = 2
    HAIKEI_FASSION = 3
    HAIKEI_ODEKAKE = 4
    HAIKEI_OYASUMI = 5
    haikei = HAIKEI_NONE
    training_sts = 0
    benkyo_sts = 0
    fassion_sts = 0
    odekake_sts = 0
    oyasumi_sts = 0
    target_training_sts = 0
    target_benkyo_sts = 0
    target_fassion_sts = 0
    target_odekake_sts = 0
    target_oyasumi_sts = 100
    angle = 0
    TRAINING = 1
    BENKYO = 2
    FASSION = 3
    ODEKAKE = 4
    OYASUMI = 5
    select_menu = 0
    move_cnt = 0
    alpha = 255
    menu_image = None
    menu_rect = 0
    arrow = []
    arrow_x = [0] * 5
    arrow_y = [0] * 5
    arrow_alpha = [255] * 5

#
# 初期化処理
#
def parts_init():
    pygame.init()

    g.clock = pygame.time.Clock()

    try:
        pygame.mixer.init()
        g.sound_ok = True
    except Exception as e:
        print(f"サウンド初期化エラーが発生しました: {e}")
        g.sound_ok = False

    g.screen = pygame.display.set_mode((WIDTH, HIGHT))
    g.font = pygame.font.SysFont("meiryo", 20)
    g.status_font = pygame.font.SysFont("meiryo", 50, bold=True)

    # 画像の準備
    prepare_image()

    # サウンドの準備
    prepare_sound()

    # ウインドウタイトルを設定
    pygame.display.set_icon(g.neko) ####
    pygame.display.set_caption('育成ゲーム') ####

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
    g.haikei_bedroom = pygame.image.load("img/Bedroom 1.png").convert()
    g.haikei_oyasumi = pygame.transform.scale(g.haikei_bedroom, (WIDTH, HIGHT))
    g.haikei_city = pygame.image.load("img/Colorful City.png").convert()
    g.haikei_odekake = pygame.transform.scale(g.haikei_city, (WIDTH, HIGHT))
    g.haikei_playground = pygame.image.load("img/Playground.png").convert()
    g.haikei_training = pygame.transform.scale(g.haikei_playground, (WIDTH, HIGHT))
    g.haikei_room = pygame.image.load("img/Room 1.png").convert()
    g.haikei_benkyo = pygame.transform.scale(g.haikei_room, (WIDTH, HIGHT))
    g.haikei_slopes = pygame.image.load("img/Slopes.png").convert()
    g.haikei_fassion = pygame.transform.scale(g.haikei_slopes, (WIDTH, HIGHT))

    g.neko = load_and_scale_image("img/cat-a.png", 2/3)
    g.training = load_and_scale_image("img/01_training.png", 1/4)
    g.benkyo = load_and_scale_image("img/02_benkyo.png", 1/4)
    g.fassion = load_and_scale_image("img/03_fassion.png", 1/4)
    g.odekake = load_and_scale_image("img/04_odekake.png", 1/4)
    g.oyasumi = load_and_scale_image("img/05_oyasumi.png", 1/4)
    g.big_training = load_and_scale_image("img/01_training.png", 1/4 * 1.25)
    g.big_benkyo = load_and_scale_image("img/02_benkyo.png", 1/4 * 1.25)
    g.big_fassion = load_and_scale_image("img/03_fassion.png", 1/4 * 1.25)
    g.big_odekake = load_and_scale_image("img/04_odekake.png", 1/4 * 1.25)
    g.big_oyasumi = load_and_scale_image("img/05_oyasumi.png", 1/4 * 1.25)
    g.arrow.append(load_and_scale_image("img/arrow_training.png", 1/2))
    g.arrow.append(load_and_scale_image("img/arrow_benkyo.png", 1/2))
    g.arrow.append(load_and_scale_image("img/arrow_fassion.png", 1/2))
    g.arrow.append(load_and_scale_image("img/arrow_odekake.png", 1/2))
    g.status = load_and_scale_image("img/ステータス一覧.png", 1)
    g.hukidashi = load_and_scale_image("img/吹き出し_middle.png", 3/4)


    
def draw_selected_panel():
    if g.move_cnt == 0:
        match g.select_menu:
            case g.TRAINING:
                g.menu_image = g.training
                g.menu_rect = g.menu_image.get_rect(topleft=TRAINING_TOP_LEFT)
                g.menu_rect = g.big_training.get_rect(center=g.menu_rect.center)
                g.menu_image = g.big_training
            case g.BENKYO:
                g.menu_image = g.benkyo
                g.menu_rect = g.menu_image.get_rect(topleft=BENKYO_TOP_LEFT)
                g.menu_rect = g.big_benkyo.get_rect(center=g.menu_rect.center)
                g.menu_image = g.big_benkyo
            case g.FASSION:
                g.menu_image = g.fassion
                g.menu_rect = g.menu_image.get_rect(topleft=FASSION_TOP_LEFT)
                g.menu_rect = g.big_fassion.get_rect(center=g.menu_rect.center)
                g.menu_image = g.big_fassion
            case g.ODEKAKE:
                g.menu_image = g.odekake
                g.menu_rect = g.menu_image.get_rect(topleft=ODEKAKE_TOP_LEFT)
                g.menu_rect = g.big_odekake.get_rect(center=g.menu_rect.center)
                g.menu_image = g.big_odekake
            case g.OYASUMI:
                g.menu_image = g.oyasumi
                g.menu_rect = g.menu_image.get_rect(topleft=OYASUMI_TOP_LEFT)
                g.menu_rect = g.big_oyasumi.get_rect(center=g.menu_rect.center)
                g.menu_image = g.big_oyasumi
        g.move_cnt += 1
    elif g.move_cnt <= 5:
        g.menu_rect.y -= 5
        g.screen.blit(g.menu_image, g.menu_rect)
        g.move_cnt += 1
    elif g.move_cnt <= 15:
        g.alpha -= 25
        g.menu_image.set_alpha(g.alpha)
        g.screen.blit(g.menu_image, g.menu_rect)
        g.move_cnt += 1
    else:
        g.move_cnt = 0
        g.alpha = 255
        g.menu_image.set_alpha(g.alpha)
        g.mode = g.MODE_STATUS_CHANGE


def draw_panel(image, big_image, pos, haikei):
    rect = image.get_rect(topleft=pos)
    mouse_pos = pygame.mouse.get_pos()
    is_mouse_over = rect.collidepoint(mouse_pos)
    if is_mouse_over:
        g.haikei = haikei
        g.angle += 30
        angle_radians = math.radians(g.angle)
        big_rect = big_image.get_rect(center=rect.center)
        g.screen.blit(adjust_brightness(big_image, math.sin(angle_radians) * 20 + 20), big_rect)
    else:
        g.screen.blit(image, rect)
    return is_mouse_over
    
def draw_training():
    return draw_panel(g.training, g.big_training, TRAINING_TOP_LEFT, g.HAIKEI_TRAINING)
    
def draw_benkyo():
    return draw_panel(g.benkyo, g.big_benkyo, BENKYO_TOP_LEFT, g.HAIKEI_BENKYO)
    
def draw_fassion():
    return draw_panel(g.fassion, g.big_fassion, FASSION_TOP_LEFT, g.HAIKEI_FASSION)
    
def draw_odekake():
    return draw_panel(g.odekake, g.big_odekake, ODEKAKE_TOP_LEFT, g.HAIKEI_ODEKAKE)
    
def draw_oyasumi():
    return draw_panel(g.oyasumi, g.big_oyasumi, OYASUMI_TOP_LEFT, g.HAIKEI_OYASUMI)
    
def draw_status_panel():
    g.screen.blit(g.status, (10,10))
    
def draw_arrow(arrow_num):
    image = g.arrow[g.select_menu - 1]
    for i in range(arrow_num):
        g.arrow_y[i] -= 5
        #幽霊効果
        g.arrow_alpha[i] -= 25
        image.set_alpha(g.arrow_alpha[i])
        g.screen.blit(image, (g.arrow_x[i], g.arrow_y[i]))

#
# 背景を描く
#
def draw_haikei():
    match g.haikei:
        case g.HAIKEI_NONE:
            g.screen.fill(WHITE)
        case g.HAIKEI_TRAINING:
            g.screen.blit(g.haikei_training, (0,0))
        case g.HAIKEI_BENKYO:
            g.screen.blit(g.haikei_benkyo, (0,0))
        case g.HAIKEI_FASSION:
            g.screen.blit(g.haikei_fassion, (0,0))
        case g.HAIKEI_ODEKAKE:
            g.screen.blit(g.haikei_odekake, (0,0))
        case g.HAIKEI_OYASUMI:
            g.screen.blit(g.haikei_oyasumi, (0,0))

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
        g.status_up_snd = load_sound_and_set_volume("sound/ステータス上昇.mp3", 0.5)
        g.mouse_over_snd = load_sound_and_set_volume("sound/マウスオーバー.mp3", 0.5)
        g.hp_minus_snd = load_sound_and_set_volume("sound/体力減少.mp3", 0.5)
        g.decide_snd = load_sound_and_set_volume("sound/決定.mp3", 0.5)
        g.tired_snd = load_sound_and_set_volume("sound/疲れた.mp3", 0.5)
        g.kaihuku_snd = load_sound_and_set_volume("sound/回復.mp3", 0.5)

def play_status_up_snd():
    if g.sound_ok:
        g.status_up_snd.play()

def play_mouse_over_snd():
    if g.sound_ok:
        g.mouse_over_snd.play()

def play_hp_minus_snd():
    if g.sound_ok:
        g.hp_minus_snd.play()

def play_decide_snd():
    if g.sound_ok:
        g.decide_snd.play()

def play_tired_snd():
    if g.sound_ok:
        g.tired_snd.play()

def play_kaihuku_snd():
    if g.sound_ok:
        g.kaihuku_snd.play()

def draw_training_status():
    if  g.training_sts < g.target_training_sts:
        g.training_sts += 1
    draw_status(140, 10, f"{g.training_sts % 100:02}", TRAINING_COLOR)
    
def draw_benkyo_status():
    if  g.benkyo_sts < g.target_benkyo_sts:
        g.benkyo_sts += 1
    draw_status(140, 10 + 60 * 1, f"{g.benkyo_sts % 100:02}", BENKYO_COLOR)
    
def draw_fassion_status():
    if  g.fassion_sts < g.target_fassion_sts:
        g.fassion_sts += 1
    draw_status(140, 10 + 60 * 2, f"{g.fassion_sts % 100:02}", FASSION_COLOR)
    
def draw_odekake_status():
    if  g.odekake_sts < g.target_odekake_sts:
        g.odekake_sts += 1
    draw_status(140, 10 + 60 * 3, f"{g.odekake_sts % 100:02}", ODEKAKE_COLOR)
    
def draw_oyasumi_status():
    if  g.oyasumi_sts < g.target_oyasumi_sts:
        g.oyasumi_sts += 4
    elif g.oyasumi_sts > g.target_oyasumi_sts:
        g.oyasumi_sts -= 1
    draw_status(140 - 30, 10 + 60 * 4, f"{g.oyasumi_sts:03}", OYASUMI_COLOR)
    
#
# ステータスを描く
#
def draw_status(x, y, text_char, color):
    text = g.status_font.render(text_char, True, color)
    g.screen.blit(text, (x, y))
    
#
# 吹き出しにテキストを描く
#
def draw_hukidashi(x, y, text_char):
    text = g.font.render(text_char, True, BLACK)
    g.screen.blit(g.hukidashi, (x, y))
    text_rect = text.get_rect(topleft=(x + 15, y + 8))
    g.screen.blit(text, text_rect)

#
# 明るさを調整する
#
def adjust_brightness(surface, brightness):
    adjusted_surface = surface.copy()

    if brightness > 0:
        # 明るくする: 白をブレンド
        overlay = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((brightness, brightness, brightness, 0))
        adjusted_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    elif brightness < 0:
        # 暗くする: 黒をブレンド
        overlay = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((-brightness, -brightness, -brightness, 0))
        adjusted_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

    return adjusted_surface

#
# マウスイベント処理
#
def mouse_event(event):
    if g.mode == g.MODE_SELECT_MENU:
        # マウスボタンが押されたとき
        if event.type == pygame.MOUSEBUTTONDOWN:
            if g.training.get_rect(topleft=TRAINING_TOP_LEFT).collidepoint(event.pos):
                play_decide_snd()
                g.select_menu = g.TRAINING
            elif g.benkyo.get_rect(topleft=BENKYO_TOP_LEFT).collidepoint(event.pos):
                play_decide_snd()
                g.select_menu = g.BENKYO
            elif g.fassion.get_rect(topleft=FASSION_TOP_LEFT).collidepoint(event.pos):
                play_decide_snd()
                g.select_menu = g.FASSION
            elif g.odekake.get_rect(topleft=ODEKAKE_TOP_LEFT).collidepoint(event.pos):
                play_decide_snd()
                g.select_menu = g.ODEKAKE
            elif g.oyasumi.get_rect(topleft=OYASUMI_TOP_LEFT).collidepoint(event.pos):
                play_decide_snd()
                g.select_menu = g.OYASUMI
            else:
                g.select_menu = 0

        # マウスボタンが離されたとき
        if event.type == pygame.MOUSEBUTTONUP:
            if g.select_menu != 0:
                g.mode = g.MODE_MENU_SELECTED

#
# 画面更新とユーザー操作を監視
#
def update_and_eventchk():
    pygame.display.update()
    g.clock.tick(30)
    for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN
            or event.type == pygame.MOUSEBUTTONUP
            or event.type == pygame.MOUSEMOTION):
            mouse_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
