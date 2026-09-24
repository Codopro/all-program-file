#
# parts.py
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

MODE_MAIN = 0
MODE_END = 1

BRESS_MODE_NONE = 0
BRESS_MODE_BACK = 1
BRESS_MODE_FORWARD = 2

#グローバル変数の初期化
class g:
    mode = MODE_MAIN
    wind_group = pygame.sprite.Group()
    bress_mode = BRESS_MODE_NONE
    speed_gain = 0
    bress_group = pygame.sprite.Group()
    desk_damage = 0
    yure_stage = 0
    yure_count = 0
    hibi_stage = 0
    destroy_desk_stage = 0
    leg1_direction = random.randint(45, 80)
    leg2_direction = random.randint(45, 80)
    leg3_direction = random.randint(45, 80)
    leg4_direction = random.randint(45, 80)
    desk1_direction = random.randint(45, 80)
    desk2_direction = random.randint(45, 80)
    desk3_direction = random.randint(45, 80)
    desk4_direction = random.randint(45, 80)
    cake_speed_x = 0
    cake_speed_y = 0
    cake_rect_centerx = 0
    cake_rect_centery = 0
    angle = 0
    rosoku_hp = 100
    white_wall_alpha = 0
    alpha_step = 0
    boy_eat_status = 0
    boy_eat_status_chg_time = 0

#
# 初期化処理
#
def parts_init():
    pygame.init()

    g.mode = MODE_MAIN
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
    pygame.display.set_icon(g.cake.image)
    pygame.display.set_caption('ろうそく吹き消しゲーム')

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
    return sprite

#
# 画像準備
#
def prepare_image():
    desk_init_pos = (400, 400)
    boy_init_pos = (50, 450)
    cake_init_pos = (400, 280)
    init_pos = (320, 240)
    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei = pygame.image.load("img/背景.png").convert()
    g.haikei = pygame.transform.scale(g.haikei, (WIDTH, HIGHT))

    g.white_wall = pygame.transform.scale(g.haikei, (WIDTH, HIGHT))
    g.white_wall = g.white_wall.convert_alpha()

    g.bress = prepare_sprite("img/息.png", 1/2, init_pos)
    g.wind = prepare_sprite("img/風.png", 2/3, init_pos)

    g.desk_left = prepare_sprite("img/1a.png", 2/3, desk_init_pos)
    g.desk_left_broken =  load_and_scale_image("img/1b.png", 2/3)
    g.desk_front = prepare_sprite("img/2a.png", 2/3, desk_init_pos)
    g.desk_front_broken =  load_and_scale_image("img/2b.png", 2/3)
    g.desk_right = prepare_sprite("img/3a.png", 2/3, desk_init_pos)
    g.desk_right_broken =  load_and_scale_image("img/3b.png", 2/3)
    g.desk_back = prepare_sprite("img/4a.png", 2/3, desk_init_pos)
    g.desk_back_broken =  load_and_scale_image("img/4b.png", 2/3)

    g.leg_right_back = prepare_sprite("img/脚（右後）.png", 2/3, desk_init_pos)
    g.leg_right_front = prepare_sprite("img/脚（右前）.png", 2/3, desk_init_pos)
    g.leg_left_back = prepare_sprite("img/脚（左後）.png", 2/3, desk_init_pos)
    g.leg_left_front = prepare_sprite("img/脚（左前）.png", 2/3, desk_init_pos)

    g.hibi = prepare_sprite("img/ひび1.png", 2/3, desk_init_pos)
    g.hibi2 =  load_and_scale_image("img/ひび2.png", 2/3)
    g.hibi3 =  load_and_scale_image("img/ひび3.png", 2/3)

    g.cake = prepare_sprite("img/5.png", 3/4, cake_init_pos)
    g.cake0 = load_and_scale_image("img/0.png", 4/5)
    g.cake1 = load_and_scale_image("img/1.png", 4/5)
    g.cake2 = load_and_scale_image("img/2.png", 4/5)
    g.cake3 = load_and_scale_image("img/3.png", 4/5)
    g.cake4 = load_and_scale_image("img/4.png", 4/5)
    g.cake5 = load_and_scale_image("img/5.png", 4/5)
    g.cake_rect_centerx = g.cake.rect.centerx
    g.cake_rect_centery = g.cake.rect.centery

    g.boy = prepare_sprite("img/立つ.png", 4/5, boy_init_pos)
    g.boy_standing = load_and_scale_image("img/立つ.png", 4/5)
    g.boy_eat1 = load_and_scale_image("img/食べる1.png", 4/5)
    g.boy_eat2 = load_and_scale_image("img/食べる2.png", 4/5)
    g.boy_eat3 = load_and_scale_image("img/食べる3.png", 4/5)
    g.boy_syonbori = load_and_scale_image("img/しょんぼり.png", 4/5)

    g.hukidashi = load_and_scale_image("img/吹き出し.png", 2/3)

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
        g.destroy_wall_snd = load_sound_and_set_volume("sound/パンチで壁を破壊.mp3", 0.5)
        g.hubuki_snd = load_sound_and_set_volume("sound/吹く.mp3", 0.2)
        g.wind_snd = load_sound_and_set_volume("sound/吸う.mp3", 0.2)
        g.break_wood_snd = load_sound_and_set_volume("sound/机にヒビ.mp3", 0.5)
        g.uresii_snd = load_sound_and_set_volume("sound/うれしい.mp3", 0.5)
        g.jyuu_snd = load_sound_and_set_volume("sound/ジューッ.mp3", 0.5)
        g.taberu_snd = load_sound_and_set_volume("sound/食べる.mp3", 0.5)
        g.manuke_snd = load_sound_and_set_volume("sound/間抜け4.mp3", 0.5)

#
# 風クラス
#
class WindSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, scale):
        super().__init__()
        self.image = load_and_scale_image(image_path, scale)
        self.speed = 0
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

        if g.bress_mode == BRESS_MODE_FORWARD:
            self.rect.centerx = 0
            g.speed_gain = 1
        else:
            self.rect.centerx = 640
            g.speed_gain = -1
        self.rect.centery = random.randint(0, 480)

    def update(self):
        self.speed += g.speed_gain * 5
        self.rect.centerx += self.speed
        if self.rect.centerx > 720:
            self.kill()
        if self.rect.centerx < 0:
            self.kill()

#
# 風スプライト設定処理
# （画像をロードし、サイズ、位置を設定する）
def prepare_wind_sprite(image, scale, init_pos):
    sprite = WindSprite(image, scale)
    return sprite

#
# 風を作る
#
def make_wind():
    if g.bress_mode == BRESS_MODE_BACK or g.bress_mode == BRESS_MODE_FORWARD: ### or and の課題
        if g.boy_eat_status == 0:
            wind_init_pos =  (WIDTH / 2, HIGHT)
            sprite = prepare_wind_sprite("img/風.png", 1/2, wind_init_pos)
            sprite.rect.centery = random.randint(0, 480) ####
            g.wind_group.add(sprite)

#
# 風を描く
#
def draw_wind():
    g.wind_group.draw(g.screen)

#
# 息クラス
#
class BressSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, scale):
        super().__init__()
        self.image = load_and_scale_image(image_path, scale)
        self.speed = 50
        self.direction = random.randint(70, 110)
        self.rect = self.image.get_rect()
        self.rect.center = (70, 300)
        g.desk_damage += 1

    def update(self):
        angle_radians = math.radians(self.direction)
        self.rect.centerx += self.speed * math.sin(angle_radians)
        self.rect.centery += -self.speed * math.cos(angle_radians)
        if self.rect.centerx > 680:
            self.kill()

#
# 息スプライト設定処理
# （画像をロードし、サイズ、位置を設定する）
def prepare_bress_sprite(image, scale, init_pos):
    sprite = BressSprite(image, scale)
    return sprite

#
# 息を作る
#
def make_new_bress():
    if g.boy_eat_status == 0:
        bress_init_pos =  (WIDTH / 2, HIGHT)
        sprite = prepare_bress_sprite("img/息.png", 1/2, bress_init_pos)
        g.bress_group.add(sprite)

#
# 息を描く
#
def draw_bress():
    g.bress_group.draw(g.screen)

#
# 息とドースのキー入力処理
#
def chg_bress_mode():
    if g.boy_eat_status == 0:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            g.bress_mode = BRESS_MODE_FORWARD
            g.boy.image = g.boy_eat3
            make_new_bress()
        else:
            if keys[pygame.K_SPACE]:
                g.bress_mode = BRESS_MODE_BACK
                g.boy.image = g.boy_eat1
            else:
                g.bress_mode = BRESS_MODE_NONE
                g.boy.image = g.boy_standing

#
# ケーキのコスチュームを変える
#
def chg_cake_costume():
    if g.rosoku_hp < 15:
        g.cake.image = g.cake0
    elif g.rosoku_hp < 30:
        g.cake.image = g.cake1
    elif g.rosoku_hp < 45:
        g.cake.image = g.cake2
    elif g.rosoku_hp < 60:
        g.cake.image = g.cake3
    elif g.rosoku_hp < 80:
        g.cake.image = g.cake4
    else:
        g.cake.image = g.cake5

#
# 吹き出しを描く
#
def draw_boy_hukidashi():
    if g.boy_eat_status == 3 or g.boy_eat_status == 4:
        if g.cake.image != g.cake0:
            draw_hukidashi(100, 150, "あつっ！")
        else:
            draw_hukidashi(100, 150, "うまーい！")

#
# ドースがケーキを食べる処理
#
def boy_eat_cake():
    if g.boy_eat_status == 1:
        stop_all_sound()
        play_taberu_sound()
        g.bress_mode = BRESS_MODE_NONE
        g.boy.image = g.boy_eat2
        g.boy_eat_status = 2
        g.boy_eat_status_chg_time = pygame.time.get_ticks()
    elif g.boy_eat_status == 2:
        current_time = pygame.time.get_ticks()
        if current_time > g.boy_eat_status_chg_time + 500:
            if g.cake.image != g.cake0:
                g.boy.image = g.boy_syonbori
                play_jyuu_sound()
                g.boy_eat_status = 3
                g.boy_eat_status_chg_time = pygame.time.get_ticks()
            else:
                play_uresii_sound()
                g.boy_eat_status = 4
                g.boy_eat_status_chg_time = pygame.time.get_ticks()
    elif g.boy_eat_status == 3:
        current_time = pygame.time.get_ticks()
        if current_time > g.boy_eat_status_chg_time + 1000:
            g.boy_eat_status = 4
            g.boy_eat_status_chg_time = pygame.time.get_ticks()
    elif g.boy_eat_status == 4:
        current_time = pygame.time.get_ticks()
        if current_time > g.boy_eat_status_chg_time + 1000:
            g.cake_rect_centerx = g.cake.rect.centerx = 400
            g.cake_rect_centery = g.cake.rect.centery = 280
            g.cake_speed_x = 0
            g.cake_speed_y = 0
            g.rosoku_hp = 100
            g.cake.image = g.cake5
            g.boy_eat_status = 0

#
# ケーキを動かす
#
def move_cake():
    if g.boy_eat_status == 0:
        if g.bress_mode == BRESS_MODE_BACK:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_b]:
                g.cake_speed_x = 0
                g.cake_speed_y = 0
            else:
                g.cake_speed_x -= 0.2
                g.cake_speed_y = (300 - g.cake.rect.centery) / 100

            g.cake_rect_centerx += g.cake_speed_x
            g.cake_rect_centery += g.cake_speed_y
            g.cake.rect.centerx = g.cake_rect_centerx
            g.cake.rect.centery = g.cake_rect_centery

            if g.cake.rect.centerx < 200:
                g.boy_eat_status = 1
        else:
            g.cake_speed_x = 0
            g.cake_speed_y = 0

#
# 机を動かす
#
def move_desk(speed):
    g.leg_right_back.rect.x+=speed
    g.leg_left_back.rect.x+=speed
    g.leg_right_front.rect.x+=speed
    g.leg_left_front.rect.x+=speed
    g.desk_left.rect.x+=speed
    g.desk_right.rect.x+=speed
    g.desk_front.rect.x+=speed
    g.desk_back.rect.x+=speed
    g.hibi.rect.x+=speed
    g.leg_right_back.rect.y+=speed
    g.leg_left_back.rect.y+=speed
    g.leg_right_front.rect.y+=speed
    g.leg_left_front.rect.y+=speed
    g.desk_left.rect.y+=speed
    g.desk_right.rect.y+=speed
    g.desk_front.rect.y+=speed
    g.desk_back.rect.y+=speed
    g.hibi.rect.y+=speed

#
# 机を揺らす
#
def yurasu_desk():
    speed = 10
    if g.yure_stage == 1:
        move_desk(-speed)
        g.yure_count+=1
        if g.yure_count >= 3:
            g.yure_count = 0
            g.yure_stage = 2
    elif g.yure_stage == 2:
        move_desk(speed)
        g.yure_count+=1
        if g.yure_count >= 6:
            g.yure_count = 0
            g.yure_stage = 3
    elif g.yure_stage == 3:
        move_desk(-speed)
        g.yure_count+=1
        if g.yure_count >= 3:
            g.yure_count = 0
            g.yure_stage = 4

#
# 机を破壊する
#
def destroy_desk():
    if g.destroy_desk_stage == 1:
        g.white_wall_alpha = 255
        g.alpha_step = 12
        stop_all_sound()
        play_destroy_wall_sound()
        g.destroy_desk_stage = 2
    if g.destroy_desk_stage == 2:
        destroy_desk_parts(g.leg_right_back, g.leg1_direction)
        destroy_desk_parts(g.leg_right_front, g.leg2_direction)
        destroy_desk_parts(g.leg_left_back, g.leg3_direction)
        destroy_desk_parts(g.leg_left_front, g.leg4_direction)
        g.desk_right.image = g.desk_right_broken
        g.desk_left.image = g.desk_left_broken
        g.desk_front.image = g.desk_front_broken
        g.desk_back.image = g.desk_back_broken
        destroy_desk_parts(g.desk_right, g.desk1_direction)
        destroy_desk_parts(g.desk_left, g.desk2_direction)
        destroy_desk_parts(g.desk_front, g.desk3_direction)
        destroy_desk_parts(g.desk_back, g.desk4_direction)
        g.cake.rect.x += 10
        rotated_image = pygame.transform.rotate(g.cake.image, g.angle)
        g.cake.image = rotated_image
        g.angle += 10
        if g.angle >= 360:
            g.angle = 0
    elif g.destroy_desk_stage == 3:
        g.boy.image = g.boy_syonbori
        play_manuke_sound()
        g.mode = MODE_END

#
# 机の部品を破壊する
#
def destroy_desk_parts(desk_parts, direction):
    speed = 20
    angle_radians = math.radians(direction)
    desk_parts.rect.centerx += speed * math.sin(angle_radians)
    desk_parts.rect.centery += -speed * math.cos(angle_radians)
    if desk_parts.rect.centerx > 1680:
        desk_parts.kill()
        g.destroy_desk_stage = 3


#
# 白マスクを描く
#
def draw_white_mask():
    if g.white_wall_alpha != 0:
        g.white_wall_alpha -= g.alpha_step
        if g.white_wall_alpha < 0:
            g.white_wall_alpha = 0
    g.white_wall.set_alpha(g.white_wall_alpha)
    g.screen.blit(g.white_wall, (0, 0))

#
# ひびを描く
#
def draw_hibi():
    if g.destroy_desk_stage != 0:
        return
    if g.desk_damage == 200 and g.hibi_stage > 0:
        play_break_wood_sound()
        g.white_wall_alpha = 255
        g.alpha_step = 25
        g.hibi.image = g.hibi3
    elif g.desk_damage == 125 and g.hibi_stage > 0:
        play_break_wood_sound()
        g.white_wall_alpha = 255
        g.alpha_step = 25
        g.hibi.image = g.hibi2
    elif g.desk_damage == 50 and g.hibi_stage > 0:
        play_break_wood_sound()
        g.white_wall_alpha = 255
        g.alpha_step = 25

    if g.desk_damage > 50 and g.hibi_stage > 0:
        g.screen.blit(g.hibi.image, g.hibi.rect)

#
# 机を描く
#
def draw_desk():
    g.screen.blit(g.leg_right_back.image, g.leg_right_back.rect)
    g.screen.blit(g.leg_left_back.image, g.leg_left_back.rect)
    g.screen.blit(g.leg_right_front.image, g.leg_right_front.rect)
    g.screen.blit(g.leg_left_front.image, g.leg_left_front.rect)
    g.screen.blit(g.desk_back.image, g.desk_back.rect)
    g.screen.blit(g.desk_left.image, g.desk_left.rect)
    g.screen.blit(g.desk_right.image, g.desk_right.rect)
    g.screen.blit(g.desk_front.image, g.desk_front.rect)

#
# ケーキを描く
#
def draw_cake():
    if g.boy_eat_status == 0:
        g.screen.blit(g.cake.image, g.cake.rect)

#
# 背景を描く
#
def draw_haikei():
    g.screen.blit(g.haikei, (0,0))

#
# ドースを描く
#
def draw_boy():
    g.screen.blit(g.boy.image, g.boy.rect)

#
# うれしい音の再生
#
def play_uresii_sound():
    if g.sound_ok:
        g.uresii_snd.play()

#
# ジュ―音の再生
#
def play_jyuu_sound():
    if g.sound_ok:
        g.jyuu_snd.play()

#
# 食べる音の再生
#
def play_taberu_sound():
    if g.sound_ok:
        g.taberu_snd.play()

#
# まぬけ音の再生
#
def play_manuke_sound():
    if g.sound_ok:
        g.manuke_snd.play()

#
# 壁破壊音の再生
#
def play_destroy_wall_sound():
    if g.sound_ok:
        g.destroy_wall_snd.play()

#
# 吹雪音の再生
#
def play_hubuki_sound():
    if g.sound_ok:
        if pygame.mixer.get_busy():
            pass
        else:
            g.hubuki_snd.play()

#
# 風音の再生
#
def play_wind_sound():
    if g.sound_ok:
        if pygame.mixer.get_busy():
            pass
        else:
            g.wind_snd.play()

#
# 木が割れる音の再生
#
def play_break_wood_sound():
    if g.sound_ok:
        g.break_wood_snd.play()

#
# 全ての音を止める
#
def stop_all_sound():
    if g.sound_ok:
        pygame.mixer.stop()

#
# 吹雪と風の音を再税
#
def play_sound():
    if g.destroy_desk_stage == 1 or g.destroy_desk_stage == 2 or g.destroy_desk_stage == 3:
        return

    if g.bress_mode == BRESS_MODE_NONE:
        if g.boy_eat_status == 0:
            stop_all_sound()
    elif g.bress_mode == BRESS_MODE_FORWARD:
        play_hubuki_sound()
    elif g.bress_mode == BRESS_MODE_BACK:
        play_wind_sound()

#
# 吹き出しにテキストを描く
#
def draw_hukidashi(x, y, text_char):
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
