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
    MODE_DROP_BOOK = 0
    MODE_BREAK_DOWN_BOOK = 1
    MODE_END = 2
    mode = MODE_DROP_BOOK
    NEW_BOOK_EVENT = pygame.USEREVENT + 1
    books = []
    book_group = pygame.sprite.Group()
    total_zure = 0

#
# 本のスプライトクラス
#
class BookSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, scale):
        super().__init__()
        self.stage = 1
        self.zure = 0

    def update(self):
        # 落ちる
        if self.stage == 1:
            if self.rect.centery > HIGHT - 50:
                self.kill()
            elif check_collision_with_color(self, (0x00, 0xe9, 0xff)) or \
                 check_collision_with_color(self, (0xd8, 0x3f, 0x44)):
                play_close_book_snd()
                self.image = g.book2
                self.rect.y += 5
                self.zure = self.rect.centerx - g.dai.rect.centerx
                g.total_zure += self.zure
                # print(self.zure)
                # print(g.total_zure)
                self.stage = 2
            else:
                self.rect.y += 10
        # 台と一緒に横に動く
        elif self.stage == 2:
            self.rect.centerx = g.dai.rect.centerx + self.zure
        # 崩れる
        elif self.stage == 3:
            if g.total_zure > 0:
                self.rect.x += random.randint(10*1.5, 50*1.5)
                self.image = pygame.transform.rotate(self.image, random.randint(-20*1.5, 0))
            else:
                self.rect.x += random.randint(-50*1.5, -10*1.5)
                self.image = pygame.transform.rotate(self.image, random.randint(0, 20*1.5))

#
# 初期化処理
#
def parts_init():
    pygame.init()

    g.mode = g.MODE_DROP_BOOK
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
    pygame.display.set_icon(g.book2)
    pygame.display.set_caption('積ん読ゲーム')

#
# 画像のサイズ設定処理
# （画像をロードし、サイズを取得後、サイズ変更する）
#
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)

#
# スプライト設定処理
# （画像をロードし、サイズ、位置を設定する）
#
def prepare_sprite(image, scale, init_pos):
    sprite = pygame.sprite.Sprite()
    sprite.image = load_and_scale_image(image, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = init_pos
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite

#
# 本のスプライト設定処理
# （画像をロードし、サイズ、位置を設定する）
#
def prepare_book_sprite(image, scale, init_pos):
    sprite = BookSprite(image, scale)
    sprite.image = load_and_scale_image(image, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = init_pos
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite

#
# 画像準備
#
def prepare_image():
    book_init_pos = (WIDTH / 2, 50)
    dai_init_pos = (WIDTH / 2, HIGHT - 50)
    hari_init_pos = (100, 100)
    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei = pygame.image.load("img/背景.png").convert()
    g.haikei = pygame.transform.scale(g.haikei, (WIDTH, HIGHT))
    g.book = prepare_sprite("img/book.png", 1/4, book_init_pos)
    g.dai = prepare_sprite("img/dai.png", 1/4, dai_init_pos)
    g.hari = prepare_sprite("img/hari2.png", 1/4, hari_init_pos)
    g.hari_rect = g.hari.image.get_rect(center=hari_init_pos)  # 画像の中心を設定
    g.hari_rotated_image = pygame.transform.rotate(g.hari.image, 90)
    g.hari_rotated_rect = g.hari_rotated_image.get_rect(center=g.hari_rect.center)  # 中心を調整

    g.memori = load_and_scale_image("img/memori.png", 1/4)
    g.book2 = load_and_scale_image("img/book2.png", 1/6)
    g.hukidashi = load_and_scale_image("img/吹き出し.png", 2/3)

#
#背景画面の描画
#
def draw_haikei():
    g.screen.blit(g.haikei, (0, 0))

#
# 台を描く
#
def draw_dai():
    g.screen.blit(g.dai.image, g.dai.rect)

#
# 目盛りを描く
#
def draw_memori():
    g.screen.blit(g.memori, (0, 0))

#
# 針を描く
#
def draw_hari():
    g.hari_rotated_image = pygame.transform.rotate(g.hari.image, 90 - g.total_zure)
    g.hari_rotated_rect = g.hari_rotated_image.get_rect(center=g.hari_rect.center)  # 中心を調整
    g.screen.blit(g.hari_rotated_image, g.hari_rotated_rect.topleft)

#
# 最後の本以外を描く
#
def draw_books():
    sprite_list = list(g.book_group)
    for sprite in sprite_list[:-1]:
        g.screen.blit(sprite.image, sprite.rect)

#
# 最後の本（落下中）を描く
#
def draw_last_book():
    sprite_list = list(g.book_group)
    if sprite_list:
        sprite = sprite_list[-1]
        g.screen.blit(sprite.image, sprite.rect)

#
# 吹き出しにテキストを描く
#
def draw_hukidashi(text_char):
    g.screen.blit(g.hukidashi, (350,50))
    text = g.font.render(text_char, True, BLACK)
    # テキストの描画
    text_rect = text.get_rect(topleft=(350+15, 50+6))
    g.screen.blit(text, text_rect)

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
        g.new_book_snd = load_sound_and_set_volume("sound/ページをめくる1.mp3", 0.5)
        g.close_book_snd = load_sound_and_set_volume("sound/布団に倒れ込む.mp3", 0.5)
        g.game_over_snd = load_sound_and_set_volume("sound/本を閉じる2.mp3", 0.5)
        pass

#
# 本が作成される音再生
#
def play_new_book_snd():
    if g.sound_ok:
        g.new_book_snd.play()

#
# 本が落ちる音再生
#
def play_close_book_snd():
    if g.sound_ok:
        g.close_book_snd.play()

#
# ゲームオーバー音再生
#
def play_game_over_snd():
    if g.sound_ok:
        g.game_over_snd.play()

#
# 色の衝突を検出する関数
#
def check_collision_with_color(sprite, color):
    sprite_mask = pygame.mask.from_surface(sprite.image)
    offset = (sprite.rect.left, sprite.rect.top)
    for x in range(sprite.rect.width):
        for y in range(sprite.rect.height):
            if sprite_mask.get_at((x, y)):
                if g.screen.get_at((offset[0] + x, offset[1] + y))[:3] == color:
                    return True
    return False

