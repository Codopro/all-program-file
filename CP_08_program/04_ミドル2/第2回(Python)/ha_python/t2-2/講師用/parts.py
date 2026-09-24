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
import colorsys

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
    NEW_FIREWORK_EVENT = pygame.USEREVENT + 1
    MODE_CENTER_PHONE = 0
    MODE_SETUMEI = 1
    MODE_TITLE = 2
    MODE_FIREWORK = 3
    MODE_KEKKA = 4
    MODE_BODY = 10
    mode = MODE_CENTER_PHONE
    mouse_pushed = False
    fireworks = []
    fever_mode = False
    hanabi1_images = []
    hanabi2_images = []
    firework_group = pygame.sprite.Group()
    point = 0
    point_img = []

def fever_mode():
    if g.fever_mode == False:
        g.fever_mode = True
        pygame.time.set_timer(g.NEW_FIREWORK_EVENT, 0)
        pygame.time.set_timer(g.NEW_FIREWORK_EVENT, 200)

#
# 花火
#
class FireworkSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, scale):
        super().__init__()
        self.stage = 1
        self.bomb_y = random.randint(50, 300)
        self.bomb_time = 0
        self.size_change_cnt = 0
        self.size_change_cnt_max = random.randint(5, 10)
        self.color = random.randint(0, 9)
        self.toumei = 255

    def update(self):
        # 準備
        if self.stage == 1:
            self.image = g.hanabi1_images[self.color]
            self.toumei = 255
            self.image.set_alpha(self.toumei)
            self.stage = 2
            play_uchiage_snd()
        # 打ち上げ
        if self.stage == 2:
            if self.rect.centery < self.bomb_y:
                self.stage = 3
            else:
                self.rect.y -= 5
        # 一旦、消える
        elif self.stage == 3:
            if self.toumei > 0:
                self.toumei -= 255 / 10
                self.image.set_alpha(self.toumei)
            else:
                self.stage4_start_time = pygame.time.get_ticks()
                self.stage = 4
        # 0.5 秒待つ
        elif self.stage == 4:
            current_time = pygame.time.get_ticks()
            if current_time > self.stage4_start_time + 500:
                self.image = g.hanabi2_images[self.color]
                self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
                self.toumei = 255
                self.image.set_alpha(self.toumei)
                self.image_rect_center = self.rect.center
                self.stage = 5
        # 爆発
        elif self.stage == 5:
            if self.size_change_cnt < self.size_change_cnt_max:
                self.image = pygame.transform.rotozoom(self.image, 0, 1.2)
                self.rect = self.image.get_rect()
                self.rect.center = self.image_rect_center
                self.size_change_cnt += 1
                # スマートフォンと花火の距離を求めて変数 kyori に代入
                kyori = calculate_distance(self, g.phone)
                #✅プログラミングチャレンジ2
                # 距離が 200 より小さいと時に得点の音を鳴らし、ポイントを増やす
                if  kyori < 200:
                    play_point_snd()
                    g.point += 1
                #✅プログラミングチャレンジ3
                # 距離が 50 以下の時に「いいね！」を表示し、ボーナス点５点を与える
                if  kyori <= 50:
                    draw_iine()
                    g.point += 5
                #✅プログラミングチャレンジ4
                # 距離が 0 の時にフィーバーモードに突入
                if  kyori == 0:
                    fever_mode()
            else:
                self.stage = 6
        # 幽霊効果 & 削除
        elif self.stage == 6:
            if self.toumei > 0:
                self.toumei -= 255 / 10
                self.image.set_alpha(self.toumei)
            else:
                play_bomb_snd()
                self.kill()

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

    # 画像の準備
    prepare_image()

    # サウンドの準備
    prepare_sound()

    # ウインドウタイトルを設定
    pygame.display.set_icon(g.hanabi2)
    pygame.display.set_caption('花火大会撮影')

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

# 花火スプライト設定処理
# （画像をロードし、サイズ、位置を設定する）
def prepare_firework_sprite(image, scale, init_pos):
    sprite = FireworkSprite(image, scale)
    sprite.image = load_and_scale_image(image, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = init_pos
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite

#
# 画像準備
#
def prepare_image():
    phone_init_pos =  (WIDTH / 2, HIGHT)
    kaishi_init_pos =  (WIDTH / 2, HIGHT / 2)

    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei = pygame.image.load("img/Stars.png").convert()
    g.haikei = pygame.transform.scale(g.haikei, (WIDTH, HIGHT))

    g.hanabi1 = load_and_scale_image("img/花火1.png", 1/2)
    g.hanabi2 = load_and_scale_image("img/花火2.png", 1/2)
    g.setumei = load_and_scale_image("img/説明.png", 1/2)
    g.title01 = load_and_scale_image("img/タイトル01.png", 1/2)
    g.title02 = load_and_scale_image("img/タイトル02.png", 1/2)
    g.sokomade = load_and_scale_image("img/そこまで.png", 2/3)
    g.sokomade02 = load_and_scale_image("img/そこまで02.png", 1/3)
    g.iine = load_and_scale_image("img/いいね！.png", 1)
    g.fever = load_and_scale_image("img/フィーバー.png", 1)

    g.phone = prepare_sprite("img/スマホ.png", 1/4, phone_init_pos)
    g.kaishi = prepare_sprite("img/タイトル03.png", 1/2, kaishi_init_pos)
    g.kaishi2 = prepare_sprite("img/タイトル03.png", 1/2, kaishi_init_pos)

    make_firework_images()
    for i in range(10):
        g.point_img.append(load_and_scale_image(f'img/{i}.png', 1/3))

#
# 花火の画像作成
#
def make_firework_images():
    for i in range(10):
        color = random.randint(0, 100)
        g.hanabi1_images.append(change_hue(g.hanabi1, color))
        g.hanabi2_images.append(change_hue(g.hanabi2, color))

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
# 得点画像を描く
#
def draw_point_img(num, pos):
    g.screen.blit(g.point_img[num], pos)

#
# そこまでを描く
#
def draw_sokomade():
    image_rect = g.sokomade.get_rect(center=(320, 240))
    g.screen.blit(g.sokomade, image_rect)

#
# そこまで2を描く
#
def draw_sokomade02():
    g.screen.blit(g.sokomade02, (200, 200))

#
# スマートフォンを描く
#
def draw_phone():
    g.screen.blit(g.phone.image, g.phone.rect)

#
# 説明画像を描く
#
def draw_setumei():
    g.screen.blit(g.setumei, (50, 50))

#
# タイトル01画像を描く
#
def draw_title01():
    g.screen.blit(g.title01, (520, 30))

#
# タイトル02画像を描く
#
def draw_title02():
    g.screen.blit(g.title02, (420, 80))

#
# 
#
def draw_iine():
    g.screen.blit(g.iine, (380, 80))

#
# 
#
def draw_fever():
    if g.fever_mode == True:
        g.screen.blit(g.fever, (15, 140))

#
# 開始画像を描く
#
def draw_kaishi(size):
    g.kaishi2.image = pygame.transform.rotozoom(g.kaishi.image, 0, size)
    g.kaishi2.rect = g.kaishi2.image.get_rect()
    g.kaishi2.rect.center = (320, 240)
    g.screen.blit(g.kaishi2.image, g.kaishi2.rect)

#
# 花火を描く
#
def draw_firework():
    g.firework_group.draw(g.screen)

#
# 背景を描く
#
def draw_haikei():
    g.screen.blit(g.haikei, (0,0))

#
# 1000の桁を描く
#
def draw_point_1000():
    point1000 = int(g.point / 1000)
    draw_point_img(point1000, (130, 220))

#
# 100の桁を描く
#
def draw_point_100():
    point100 = int(g.point % 1000 / 100)
    draw_point_img(point100, (130, 260))

#
# 10の桁を描く
#
def draw_point_10():
    point10 = int(g.point % 100 / 10)
    draw_point_img(point10, (130, 300))

#
# 1の桁を描く
#
def draw_point_1():
    point1 = int(g.point % 10)
    draw_point_img(point1, (130, 340))

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
        g.point_snd = load_sound_and_set_volume("sound/カーソル移動6.mp3", 0.5)
        g.jidai_snd = load_sound_and_set_volume("sound/時代劇演出1.mp3", 0.5)
        g.kozutumi_snd = load_sound_and_set_volume("sound/小鼓（こつづみ）.mp3", 0.5)
        g.uchiage_snd = load_sound_and_set_volume("sound/打ち上げ花火1.mp3", 0.5)
        g.bomb_snd = load_sound_and_set_volume("sound/打ち上げ花火2.mp3", 0.5)
        g.wood1_snd = load_sound_and_set_volume("sound/拍子木1.mp3", 0.5)
        g.wood2_snd = load_sound_and_set_volume("sound/拍子木2.mp3", 0.5)
        g.dodon_snd = load_sound_and_set_volume("sound/和太鼓でドドン.mp3", 0.5)

#
# 得点音再生
#
def play_point_snd():
    if g.sound_ok:
        g.point_snd.play()

#
# 時代劇音再生
#
def play_jidai_snd():
    if g.sound_ok:
        g.jidai_snd.play()

#
# 小鼓音再生
#
def play_kozutumi_snd():
    if g.sound_ok:
        g.kozutumi_snd.play()

#
# 打ち上げ音再生
#
def play_uchiage_snd():
    if g.sound_ok:
        g.uchiage_snd.play()

#
# 爆発音再生
#
def play_bomb_snd():
    if g.sound_ok:
        g.bomb_snd.play()

#
# 拍子木1音再生
#
def play_wood1_snd():
    if g.sound_ok:
        g.wood1_snd.play()

#
# 拍子木2音再生
#
def play_wood2_snd():
    if g.sound_ok:
        g.wood2_snd.play()

#
# 和太鼓音再生
#
def play_dodon_snd():
    if g.sound_ok:
        g.dodon_snd.play()

#
# スマートフォンの移動
#
def move_phone():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if g.phone.rect.centerx < 640:
            g.phone.rect.x += 4
            if keys[pygame.K_SPACE]:
                g.phone.rect.x += 8
    if keys[pygame.K_LEFT]:
        if g.phone.rect.centerx > 0:
            g.phone.rect.x -= 4
            if keys[pygame.K_SPACE]:
                g.phone.rect.x -= 8
    if keys[pygame.K_UP]:
        if g.phone.rect.centery > 0:
            g.phone.rect.y -= 4
            if keys[pygame.K_SPACE]:
                g.phone.rect.y -= 8
    if keys[pygame.K_DOWN]:
        if g.phone.rect.centery < 480:
            g.phone.rect.y += 4
            if keys[pygame.K_SPACE]:
                g.phone.rect.y += 8


#
# 花火を作る
#
def make_new_firework():
    firework_init_pos =  (WIDTH / 2, HIGHT)
    sprite = prepare_firework_sprite("img/花火1.png", 1/2, firework_init_pos)
    sprite.rect.centerx = random.randint(0, 640)
    g.fireworks.append(sprite)
    g.firework_group.add(sprite)

#
# 色を変える
#
def change_hue(image, hue_change):
    # 新しいSurfaceを作成
    new_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            # 元のピクセルの色を取得
            color = image.get_at((x, y))
            r, g, b, a = color.r / 255.0, color.g / 255.0, color.b / 255.0, color.a
            # RGBからHSVへ変換
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            # 色相を変更
            h = (h + hue_change / 360.0) % 1.0
            # HSVからRGBへ変換
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            new_color = pygame.Color(int(r * 255), int(g * 255), int(b * 255), a)
            # 新しい色を設定
            new_image.set_at((x, y), new_color)
    return new_image

def draw_point():
    (in_x, in_y, in_width, in_hight) = (110, 30, 55, 30)
    (out_x, out_y, out_width, out_hight) = (in_x - 100, in_y - 5, in_width + 105, in_hight + 10)
    draw_box(out_x, out_y, out_width, out_hight, "得点　　　　", GRAY, GRAY, DARKGRAY)
    draw_box(in_x, in_y, in_width, in_hight, str(g.point))


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
# 指定された時間(秒)待つ
#
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
    if g.mode == g.MODE_SETUMEI:
        if event.type == pygame.MOUSEBUTTONDOWN:
            g.mouse_pushed = True

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
        if event.type == g.NEW_FIREWORK_EVENT:
            make_new_firework()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
