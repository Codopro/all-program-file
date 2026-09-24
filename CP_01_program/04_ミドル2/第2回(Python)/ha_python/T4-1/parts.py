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
KASA_COLOR = (0x65, 0x38, 0x00) # かさの色

#グローバル変数の初期化
class g:
    NEW_RAIN_EVENT = pygame.USEREVENT + 1
    THUNDER_EVENT = pygame.USEREVENT + 2
    WIND_LEVEL_EVENT = pygame.USEREVENT + 3
    MODE_SUNNY = 0
    MODE_RAIN_START = 1
    MODE_GAME_START = 2
    MODE_GAME_OVER = 3
    mode = MODE_SUNNY
    neko_costume_num = 0
    neko_costume = []
    kasa_remain_time = 0
    kasa_exist = False
    kasa_angle = 0
    rain_group = pygame.sprite.Group()
    rain_level = 0
    FINE = 0
    RAIN_START = 1
    HEAVY_RAIN = 2
    THUNDER = 3
    weather = FINE
    WIND_STRENGTH = 3
    wind_level = 0
    wind_level_start = False
    title_text = []
#
# 雨のスプライトクラス
#
class RainSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, scale):
        super().__init__()
        self.stage = 1

    def update(self):
        # 落ちる
        if self.stage == 1:
            if self.rect.centery > HIGHT - 50 or check_collision_with_color(self, KASA_COLOR):
                self.stage = 2
            elif pygame.sprite.collide_mask(self, g.neko):
                 g.mode = g.MODE_GAME_OVER
            else:
                self.rect.y += 10
                # 傾ける処理
                angle_rad = math.atan(g.wind_level / 10)
                angle_deg = math.degrees(angle_rad)
                self.image = pygame.transform.rotate(g.rain01_image, angle_deg)
                if g.weather == g.HEAVY_RAIN or g.weather == g.THUNDER:
                    self.rect.x += g.wind_level
        # 落ちた
        elif self.stage == 2:
            play_picha_snd()
            self.image = g.rain02_image
            self.stage4_start_time = pygame.time.get_ticks()
            self.stage = 3
        # １秒待ってから消える
        elif self.stage == 3:
            current_time = pygame.time.get_ticks()
            if current_time > self.stage4_start_time + 1000:
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
    pygame.display.set_icon(g.neko.image)
    pygame.display.set_caption('あめよけゲーム') ####

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

# 雨スプライト設定処理
# （画像をロードし、サイズ、位置を設定する）
def prepare_rain_sprite(image, scale, init_pos):
    sprite  = RainSprite(image, scale)
    sprite.image = load_and_scale_image(image, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = init_pos
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite


#
# 画像準備
#
def prepare_image():
    neko_init_pos =  (WIDTH / 2, HIGHT / 2 + 175)
    kasa_init_pos =  (WIDTH / 2, HIGHT / 2)

    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei_fine = pygame.image.load("img/晴れ.png").convert()
    g.haikei_fine = pygame.transform.scale(g.haikei_fine, (WIDTH, HIGHT))
    g.haikei_rain_start = pygame.image.load("img/降り始め.png").convert()
    g.haikei_rain_start = pygame.transform.scale(g.haikei_rain_start, (WIDTH, HIGHT))
    g.haikei_heavy_rain = pygame.image.load("img/大雨.png").convert()
    g.haikei_heavy_rain = pygame.transform.scale(g.haikei_heavy_rain, (WIDTH, HIGHT))
    g.haikei_thunder = pygame.image.load("img/雷.png").convert()
    g.haikei_thunder = pygame.transform.scale(g.haikei_thunder, (WIDTH, HIGHT))

    g.neko_costume.append(load_and_scale_image("img/run01.png", 1/8))
    g.neko_costume.append(load_and_scale_image("img/run02.png", 1/8))
    g.neko_costume.append(load_and_scale_image("img/run03.png", 1/8))
    g.neko_costume.append(load_and_scale_image("img/run04.png", 1/8))
    g.neko_costume.append(load_and_scale_image("img/run05.png", 1/8))
    g.neko_costume.append(load_and_scale_image("img/run06.png", 1/8))
    g.neko_costume.append(load_and_scale_image("img/run07.png", 1/8))
    g.neko_costume.append(load_and_scale_image("img/run08.png", 1/8))
    g.neko = prepare_sprite("img/run01.png", 1/8, neko_init_pos)

    g.kasa = prepare_sprite("img/かさ.png", 1/2, kasa_init_pos)
    g.kasa_image = load_and_scale_image("img/かさ.png", 1/2)

    g.rain01_image = load_and_scale_image("img/雨粒01.png", 1/15)
    g.rain02_image = load_and_scale_image("img/雨粒02.png", 1/15)

    g.hukidashi = load_and_scale_image("img/吹き出し.png", 2/3)
    g.inv_hukidashi = pygame.transform.flip(g.hukidashi, True, False)
    g.big_hukidashi = load_and_scale_image("img/吹き出し.png", 4/5)
    g.big_inv_hukidashi = pygame.transform.flip(g.big_hukidashi, True, False)

    g.title_text.append(load_and_scale_image("img/あ.png", 1))
    g.title_text.append(load_and_scale_image("img/め.png", 1))
    g.title_text.append(load_and_scale_image("img/よ.png", 1))
    g.title_text.append(load_and_scale_image("img/け.png", 1))
    g.title_text.append(load_and_scale_image("img/ゲ.png", 1))
    g.title_text.append(load_and_scale_image("img/ー.png", 1))
    g.title_text.append(load_and_scale_image("img/ム.png", 1))

#
# 雨を作る
#
def make_new_rain():
    if len(g.rain_group) < 50: # 最大数を制限
        rain_init_pos =  (WIDTH / 2, 0)
        sprite = prepare_rain_sprite("img/雨粒01.png", 1/15, rain_init_pos)
        sprite.rect.centerx = random.randint(0+20, 640-20)
        g.rain_group.add(sprite)

#
# 風の確認
#
def check_wind_level():
    if g.rain_level > 20 and g.wind_level_start == False:
        g.wind_level_start = True
        pygame.time.set_timer(g.WIND_LEVEL_EVENT, random.randint(500, 1500))

#
# 天気の確認
#
def check_tenki():
    if g.rain_level > 20:
        if g.weather != g.THUNDER:
            g.weather = g.HEAVY_RAIN
        if g.rain_level > 50:
            # １秒待つ
            if check_timer(1000) == False:
                return
            if random.randint(1, 5) == 1:
                g.weather = g.THUNDER
                pygame.time.set_timer(g.THUNDER_EVENT, 1000)

#
# 雨を描く
#
def draw_rain():
    g.rain_group.draw(g.screen)

#
# 背景の描画
#
def draw_haikei():
    if g.weather == g.FINE:
        g.screen.blit(g.haikei_fine, (0,0))
    elif g.weather == g.RAIN_START:
        g.screen.blit(g.haikei_rain_start, (0,0))
    elif g.weather == g.HEAVY_RAIN:
        g.screen.blit(g.haikei_heavy_rain, (0,0))
    elif g.weather == g.THUNDER:
        g.screen.blit(g.haikei_thunder, (0,0))

#
# ねこの描画
#
def draw_neko():
    g.screen.blit(g.neko.image, g.neko.rect)

#
# ねこの移動
#
def move_neko():
    neko_speed = 6
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        play_ashioto()
        change_neko_costume(True)
        if g.neko.rect.centerx < WIDTH:
            g.neko.rect.x += neko_speed
    if keys[pygame.K_LEFT]:
        play_ashioto()
        change_neko_costume(False)
        if g.neko.rect.centerx > 0:
            g.neko.rect.x -= neko_speed

#
# ねこのコスチュームを変える
#
def change_neko_costume(right):
    g.neko_costume_num += 1
    if g.neko_costume_num >= len(g.neko_costume):
        g.neko_costume_num = 0
    g.neko.image = g.neko_costume[g.neko_costume_num]
    if not right:
        g.neko.image = pygame.transform.flip(g.neko.image, True, False)

#
# ねこのコスチュームを暗くする
#
def change_neko_dark():
    g.neko.image = adjust_brightness(g.neko.image.convert_alpha(), -1)

#
# かさの描画
#
def draw_kasa():
    if g.kasa_exist:
        g.screen.blit(g.kasa.image, g.kasa.rect)

#
# かさの処理
#
def kasa_transaction():
    kasa_x_offset = -25
    kasa_y_offset = -60
    keys = pygame.key.get_pressed()

    if g.kasa_exist == True:
        if g.kasa_remain_time > 0:
            g.kasa.rect.x = g.neko.rect.x + kasa_x_offset
            g.kasa.rect.y = g.neko.rect.y + kasa_y_offset
            g.kasa_remain_time -= 1
        else:
            if g.kasa_remain_time == 0:
                play_hyuun_snd()
            g.kasa_remain_time -= 1
            g.kasa.rect.x += 20
            g.kasa.rect.y -= 20
            g.kasa_angle += 10
            g.kasa.image = pygame.transform.rotate(g.kasa_image, g.kasa_angle)
            if g.kasa.rect.x > 640:
                g.kasa_exist = False
                g.kasa_angle = 0
                g.kasa.image = g.kasa_image
                pygame.transform.rotate(g.kasa.image, g.kasa_angle)
    else:
        if keys[pygame.K_SPACE]:
            play_open_kasa_snd()
            g.kasa_remain_time = 50
            g.kasa_exist = True
            g.kasa.rect.x = g.neko.rect.x + kasa_x_offset
            g.kasa.rect.y = g.neko.rect.y + kasa_y_offset

#
# 音声ファイルの読み出しとボリューム設定
#
def load_sound_and_set_volume(audio_file, volume):
    sound = pygame.mixer.Sound(audio_file)
    sound.set_volume(volume)
    return sound

#
# BGMファイルの読み出しとボリューム設定
#
def load_music_and_set_volume(audio_file, volume):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.set_volume(volume)

#
# 音準備
#
def prepare_sound():
    g.ashioto_channel = 0xff
    g.doronuma_channel = 0xff
    if g.sound_ok:
        g.pasha_snd = load_sound_and_set_volume("sound/バシャッ.mp3", 0.5)
        g.picha_snd = load_sound_and_set_volume("sound/ピチャッ.wav", 0.5)
        g.hyuun_snd = load_sound_and_set_volume("sound/ヒューン.mp3", 0.5)
        g.potapota_snd = load_sound_and_set_volume("sound/ポタポタ.mp3", 0.5)
        g.open_kasa_snd = load_sound_and_set_volume("sound/傘開く.mp3", 0.5)
        g.ashioto_snd = load_sound_and_set_volume("sound/足音.wav", 0.5)
        g.doronuma_snd = load_sound_and_set_volume("sound/泥沼.mp3", 0.5)
        g.run_snd = load_sound_and_set_volume("sound/雨で濡れた道路を走る.mp3", 0.5)
        g.heiwa_snd = load_sound_and_set_volume("sound/平和なBGM.wav", 0.5)

#
# 天気によって足音を変える
#
def play_ashioto():
    if g.weather != g.FINE:
        play_ashioto_snd()

    if g.weather == g.HEAVY_RAIN or g.weather == g.THUNDER:
        play_doronuma_snd()

#
# パシャ音再生
#
def play_pasha_snd():
    if g.sound_ok:
        g.pasha_snd.play()

#
# ピチャッ音再生
#
def play_picha_snd():
    if g.sound_ok:
        g.picha_snd.play()

#
# ヒューン音再生
#
def play_hyuun_snd():
    if g.sound_ok:
        g.hyuun_snd.play()

#
# ポタポタ音再生
#
def play_potapota_snd():
    if g.sound_ok:
        g.potapota_snd.play()

#
# 傘開く音再生
#
def play_open_kasa_snd():
    if g.sound_ok:
        g.open_kasa_snd.play()

#
# 泥沼音再生
#
def play_doronuma_snd():
    if g.sound_ok:
        if g.doronuma_channel == 0xff  or not g.doronuma_channel.get_busy():
            g.doronuma_channel = g.doronuma_snd.play()

#
# 足音再生
#
def play_ashioto_snd():
    if g.sound_ok:
        if g.ashioto_channel == 0xff  or not g.ashioto_channel.get_busy():
            g.ashioto_channel = g.ashioto_snd.play()

#
# 雨で濡れた道路を走る音再生
#
def play_run_snd():
    if g.sound_ok:
        g.run_snd.play()

#
# 風音再生
#
def play_wind_snd():
    if g.sound_ok:
        load_music_and_set_volume("sound/風.mp3", 0.5)
        pygame.mixer.music.play()

#
# つよい雨音再生
#
def play_havy_rain_snd():
    if g.sound_ok:
        load_music_and_set_volume("sound/つよい雨.mp3", 0.5)
        pygame.mixer.music.play()

#
# 雷雨音再生
#
def play_thunder_rain_snd():
    if g.sound_ok:
        load_music_and_set_volume("sound/雷雨.mp3", 0.5)
        pygame.mixer.music.play()

#
# 平和なBGM再生
#
def play_heiwa_snd():
    if g.sound_ok:
        g.heiwa_snd.play()

#
# 全ての音を止める
#
def stop_all_snd():
    if g.sound_ok:
        pygame.mixer.stop()

#
# 音を再生中？
#
def is_playing_snd():
    return pygame.mixer.get_busy()

#
# 音楽再生中？
#
def is_playing_music():
    return pygame.mixer.music.get_busy()

#
# BGM再生
#
def play_bgm():
    if not is_playing_music():
        if g.weather == g.RAIN_START:
            play_wind_snd()
        if g.rain_level > 20 and g.rain_level < 50:
            play_havy_rain_snd()
        if g.rain_level > 49:
            play_thunder_rain_snd()

#
# 指定した時間間隔が経過したかを判定する関数
#
def check_timer(interval):
    if not hasattr(check_timer, "last_time"):
        check_timer.last_time = pygame.time.get_ticks()  # 初期化

    current_time = pygame.time.get_ticks()
    if current_time - check_timer.last_time > interval:
        check_timer.last_time = current_time  # タイマーリセット
        return True
    return False

#
# 明るさを調整する関数
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
# 色の衝突を検出する関数
#
def check_collision_with_color(sprite, color):
    sprite_mask = pygame.mask.from_surface(sprite.image)
    offset = (sprite.rect.left, sprite.rect.top)
    for x in range(sprite.rect.width):
        for y in range(sprite.rect.height):
            if sprite_mask.get_at((x, y)):
                chk_x = offset[0] + x
                chk_y = offset[1] + y
                if chk_x >= 0 and chk_x < WIDTH and chk_y >= 0 and chk_y < HIGHT:
                    if g.screen.get_at((chk_x, chk_y))[:3] == color:
                        return True
    return False

#
# 吹き出しにテキストを描く
#  左右反転対応
#
def draw_hukidashi(x, y, text_char):
    text = g.font.render(text_char, True, BLACK)
    if x > WIDTH / 2:
        g.screen.blit(g.inv_hukidashi, (x - 140, y))
        text_rect = text.get_rect(topleft=(x - 140 + 10, y + 5))
    else:
        g.screen.blit(g.hukidashi, (x, y))
        text_rect = text.get_rect(topleft=(x + 10, y + 5))
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
# 画面更新とイベント、ユーザー操作を監視
#
def update_and_eventchk():
    pygame.display.update()
    g.clock.tick(30)
    for event in pygame.event.get():
        if event.type == g.THUNDER_EVENT:
            g.weather = g.HEAVY_RAIN
        if event.type == g.WIND_LEVEL_EVENT:
            g.wind_level = random.randint(g.WIND_STRENGTH * -1, g.WIND_STRENGTH)
            pygame.time.set_timer(g.WIND_LEVEL_EVENT, random.randint(500, 1500))
        if event.type == g.NEW_RAIN_EVENT:
            make_new_rain()
            pygame.time.set_timer(g.NEW_RAIN_EVENT, int(30 * 1000 / (10 + g.rain_level / 3)))
            if g.rain_level < 5000: ####
                g.rain_level += 10
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
