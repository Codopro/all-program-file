#
# <ミドル２コース Python課題 5月号 自動販売機シミュレーター>
# partsファイル

import pygame
from pygame.locals import *
import pygame.mixer
import sys
import time
import random

#
# 商品を購入
# 🔰タッチ部分にドンペイカードが触れた時動く関数
def buy_products():
    pygame.display.update()
    # ✅プログラミングチャレンジ2
    # 残高が十分にあれば商品を購入する
    # 価格をチェックして残高以下ならば、残高を引く


#
# 商品を購入
# 🔰ブルームをクリックしてチャージする動き
def donpay_charge():
    kotae = abs(int(g.input_text))

    # ✅プログラミングチャレンジ3
    # 残高を増やす（99より大きいときはエラーとする）



# 定数定義
WIDTH = 640           # 画面横幅の設定
HIGHT = 480           # 画面高さの設定

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
    MODE_KUJI = 0
    MODE_PLAY = 1
    dragging = False
    offset_x = 0
    offset_y = 0
    zandaka = 0
    potato_price = 10
    chicken_price = 30
    doll_price = 80
    price = 0
    goods_number = 1
    broom_clicked = False
    input_text = ''
    donpay_move_home = False
    donpay_home_pos = (540, 365)
    kuji_pos = (50, 250)
    got_products= []
    product_move = False
    product_move_target_x = 0
    product_move_target_y = 0
    over_charge_start_ticks = -1
    short_money_start_ticks = -1
    kotae = 0
    click_count = 0
    provide_product_count = 0

#
# 初期化処理
#
def parts_init():
    pygame.init()

    g.mode = g.MODE_PLAY
    g.clock = pygame.time.Clock()

    #販売価格を更新
    price_update()

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
    icon_image = pygame.image.load("img/アイコン.png").convert_alpha()
    pygame.display.set_icon(icon_image)
    pygame.display.set_caption('自動販売機シミュレーター')


#
# 販売価格の更新
#
def price_update():
    #販売価格を更新
    if g.goods_number == 1:
        g.price = g.potato_price
    elif g.goods_number == 2:
        g.price = g.chicken_price
    elif g.goods_number == 3:
        g.price = g.doll_price

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
    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.haikei = pygame.image.load("img/説明あり.png").convert_alpha()
    g.haikei = pygame.transform.scale(g.haikei, (WIDTH, HIGHT))
    # ブルーム画像読み込み
    g.broom_right = prepare_sprite("img/横.png", 2/5, (380, 320))
    g.broom_left = g.broom_right
    g.broom_left.image = pygame.transform.flip(g.broom_left.image, True, False)
    # DonPAY
    g.donpay = prepare_sprite("img/DonPAY.png", 1/2, g.donpay_home_pos)
    # 入れ替えボタン
    g.irekae = prepare_sprite("img/入れ替え.png", 2/3, (90, 290))
    # タッチ部分
    g.touch = prepare_sprite("img/タッチ部分.png", 2/3, (180, 290))
    # 人形
    g.doll = prepare_sprite("img/人形.png", 1/2, (150, 140))
    # チキン
    g.chicken = prepare_sprite("img/チキン.png", 1/2, (150, 140))
    # ポテチ
    g.potato = prepare_sprite("img/ポテチ.png", 1/2, (150, 140))
    # 吹き出し
    g.hukidashi = load_and_scale_image("img/吹き出し.png", 3/4)
    g.hukidashi = pygame.transform.flip(g.hukidashi, True, False)
    # ギフトカード
    g.kuji = load_and_scale_image("img/開ける前.png", 1)
    g.kuji_open1 = load_and_scale_image("img/開ける前2.png", 1)
    g.kuji_open2 = load_and_scale_image("img/開ける前3.png", 1)
    g.kuji_atari = load_and_scale_image("img/あたり.png", 1)
    g.kuji_hazure = load_and_scale_image("img/はずれ.png", 1)
    # 残高表示
    g.number = []
    for i in range(0,10):
        g.number.append(load_and_scale_image(f'img/{i}.png', 1/2.7))

#
# 音準備
#
def prepare_sound():
    if g.sound_ok:
        g.error_sound = pygame.mixer.Sound("sound/エラー音.wav")
        g.buy_sound = pygame.mixer.Sound("sound/購入音.wav")
        g.products_out_sound = pygame.mixer.Sound("sound/出てくる音.wav")
        g.kuji_open_sound = pygame.mixer.Sound("sound/開封音.mp3")
        g.kuji_hasami_sound = pygame.mixer.Sound("sound/はさみ.wav")
        g.kuji_atari_sound = pygame.mixer.Sound("sound/Magic Spell.wav")
        g.kuji_hazure_sound = pygame.mixer.Sound("sound/Disconnect.wav")

#
# エラー音再生
#
def play_error_sound():
    if g.sound_ok:
        g.error_sound.play()

#
# 購買音再生
#
def play_buy_sound():
    if g.sound_ok:
        g.buy_sound.play()

#
# 商品が出てくる音再生
#
def play_get_sound():
    if g.sound_ok:
        g.products_out_sound.play()

#
# ギフトカードをあける音再生
#
def play_kuji_open_sound():
    if g.sound_ok:
        g.kuji_open_sound.play()

#
# はさみ音再生
#
def play_kuji_hasami_sound():
    if g.sound_ok:
        g.kuji_hasami_sound.play()

#
# ギフトカードあたり音再生
#
def play_kuji_atari_sound():
    if g.sound_ok:
        g.kuji_atari_sound.play()

#
# ギフトカードはずれ音再生
#
def play_kuji_hazure_sound():
    if g.sound_ok:
        g.kuji_hazure_sound.play()


#
# ギフトカード開封演出
#
def open_gift() :
    # ギフトカード開封前
    draw_haikei()
    g.screen.blit(g.kuji, g.kuji_pos)
    wait_time(1) #1秒待つ

    # ギフトカードリボン開封
    draw_haikei()
    g.screen.blit(g.kuji_open1, (g.kuji_pos[0] - 50, g.kuji_pos[1] - 50))
    play_kuji_open_sound()
    wait_time(1) #1秒待つ

    # ギフトカードハサミ開封
    draw_haikei()
    g.screen.blit(g.kuji_open2, g.kuji_pos)
    play_kuji_hasami_sound()
    wait_time(2) #2秒待つ

    draw_haikei()

#
# テキストボックスを描く
#
def draw_box(rect_x, rect_y, rect_width, rect_height, text, inner_color=ORANGE, outer_color=WHITE, text_color=WHITE, radius=3, border=2):
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

    # テキストの描画
    text = g.font.render(text, True, text_color)
    text_rect = text.get_rect(center=(rect_x + rect_width / 2, rect_y + rect_height / 2))
    g.screen.blit(text, text_rect)


#
# 背景画面の描画
#
def draw_haikei():
    g.screen.blit(g.haikei, (0, 0))

#
# あたりの描画
#
def draw_atari():
    g.screen.blit(g.kuji_atari, g.kuji_pos)
    play_kuji_atari_sound() #音は組み込み

#
# はずれの描画
#
def draw_hazure():
    g.screen.blit(g.kuji_hazure, g.kuji_pos)
    play_kuji_hazure_sound() #音は組み込み

#
# ブルームを描く
#
def draw_broom():
    g.screen.blit(g.broom_left.image, g.broom_left.rect)

#
# DonPAYを描く
#
def draw_donpay():
    g.screen.blit(g.donpay.image, g.donpay.rect)

#
# 吹き出しにテキストを描く
#
def draw_hukidashi(text):
    (x, y) = (150,150)
    g.screen.blit(g.hukidashi, (x, y))
    # テキストの描画
    for line in text.split('\n'):  # 改行記号でテキストを分割
        text_surface = g.font.render(line, True, pygame.Color('black'))
        g.screen.blit(text_surface, (x + 10, y + 5))
        y += 18  # 次の行のためにy座標を更新

#
# ディスプレイ商品を描く
#
def draw_disp_products():
    if g.goods_number == 1:
        draw_potato()
    elif g.goods_number == 2:
        draw_chicken()
    elif g.goods_number == 3:
        draw_doll()

#
# 購入済商品を描く
#
def draw_got_products():
    for sprite in g.got_products:
        g.screen.blit(sprite.image, sprite.rect)

#
# 購入済商品を動かす
#
def move_buy_products():
    if g.product_move:
        diff_x = g.got_products[-1].rect.centerx - g.product_move_target_x
        diff_y = g.got_products[-1].rect.centery - g.product_move_target_y
        if diff_x > 3:
            g.got_products[-1].rect.centerx-=3
        elif diff_x < -3:
            g.got_products[-1].rect.centerx+=3
        else:
            g.got_products[-1].rect.centerx-=diff_x
        if diff_y > 3:
            g.got_products[-1].rect.centery-=3
        elif diff_y < -3:
            g.got_products[-1].rect.centery+=3
        else:
            g.got_products[-1].rect.centery-=diff_y

        if diff_x == 0 and diff_y == 0:
            g.product_move = False

#
# ポテチを描く
#
def draw_potato():
    g.screen.blit(g.potato.image, g.potato.rect)
    draw_box(110, 190, 55, 30, str(g.potato_price))

#
# チキンを描く
#
def draw_chicken():
    g.screen.blit(g.chicken.image, g.chicken.rect)
    draw_box(110, 190, 55, 30, str(g.chicken_price))

#
# 人形を描く
#
def draw_doll():
    g.screen.blit(g.doll.image, g.doll.rect)
    draw_box(110, 190, 55, 30, str(g.doll_price))

#
# 入れ替えボタンを描く
#
def draw_irekae():
    g.screen.blit(g.irekae.image, g.irekae.rect)

#
# タッチ部分を描く
#
def draw_touch():
    g.screen.blit(g.touch.image, g.touch.rect)

#
# 残高を描く
#
def draw_zandaka():
    tens_place = int(g.zandaka / 10)
    ones_place = g.zandaka % 10
    g.screen.blit(g.number[tens_place], (530,410))
    g.screen.blit(g.number[ones_place], (566,410))

#
# 入力ボックスを描く
#
def draw_input_box():
    draw_box(50, 380, 500, 64, g.input_text, pygame.Color('white'), pygame.Color('lightskyblue3'), pygame.Color('black'), 10, 6)

#
# チャージエラー処理
#
def charge_error():
    g.over_charge_start_ticks = pygame.time.get_ticks()



#
# 「どんぐりが足りないみたい」というセリフの出力
#
def say_donpay_busoku():
     g.short_money_start_ticks = pygame.time.get_ticks()


#
# 商品のクローン処理
#
def products_clone():
    sprite =  pygame.sprite.Sprite()

    if g.goods_number == 1:
        sprite.image = g.potato.image.copy()
    elif g.goods_number == 2:
        sprite.image = g.chicken.image.copy()
    elif g.goods_number == 3:
        sprite.image = g.doll.image.copy()

    sprite.image = pygame.transform.rotozoom(sprite.image, random.randint(-45, 45), 0.5)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = (145, 370)
    g.product_move = True
    g.product_move_target_x = 145 + random.randint(-80, 80)
    g.product_move_target_y = 370 + 40 + random.randint(0, 20)

    g.got_products.append(sprite)


#
# donpay を初期位置に戻す
#
def move_donpay_home():
    if g.donpay_move_home == True:
        diff_x = g.donpay.rect.centerx - g.donpay_home_pos[0]
        diff_y = g.donpay.rect.centery - g.donpay_home_pos[1]

        if diff_x > 10:
            g.donpay.rect.x -= 20
        elif diff_x < -10:
            g.donpay.rect.x += 20
        else:
            g.donpay.rect.x -= diff_x

        if diff_y > 10:
            g.donpay.rect.y -= 20
        elif diff_y < -10:
            g.donpay.rect.y += 20
        else:
            g.donpay.rect.y -= diff_y

        if diff_x == 0 and diff_y == 0:
            g.donpay_move_home = False

#
# 指定された時間（秒）待つ
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
    if g.mode == g.MODE_PLAY:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # ブルームがクリックされた判定
            pos = pygame.mouse.get_pos()
            if g.broom_left.rect.collidepoint(pos):
                g.broom_clicked = True

            # 入れ替えがクリックされた判定
            if g.irekae.rect.collidepoint(pos):
                if g.goods_number == 3:
                    g.goods_number = 1
                else:
                    g.goods_number +=1

                #販売価格を更新
                price_update()

            # どんペイがクリックされた判定
            if g.donpay.rect.collidepoint(pos) and not g.donpay_move_home:
                g.dragging = True
                g.offset_x = g.donpay.rect.x - event.pos[0]
                g.offset_y = g.donpay.rect.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            g.dragging = False
            g.donpay_move_home = True
            # タッチ部分とカードが触れたかの判定
            if pygame.sprite.collide_rect(g.donpay, g.touch):
                buy_products()

                

        elif event.type == pygame.MOUSEMOTION:
            if g.dragging:
                # マウスの位置に基づいてスプライトの位置を更新
                g.donpay.rect.x = event.pos[0] + g.offset_x
                g.donpay.rect.y = event.pos[1] + g.offset_y

#
# キーボードイベント処理
#
def key_event(event):
    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        g.broom_clicked = False
        try:
            donpay_charge()
        except:
            pass
        g.input_text = ''  # テキストをリセット
    elif event.key == pygame.K_BACKSPACE:
        g.input_text = g.input_text[:-1]
    else:
        g.input_text += event.unicode


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
        if event.type == pygame.KEYDOWN:
            key_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def add_zandaka(ans):
    g.zandaka = g.zandaka + ans


