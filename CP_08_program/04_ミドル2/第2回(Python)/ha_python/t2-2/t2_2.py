#
# <ミドル２コース Python課題 8月号 花火大会撮影>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# スマートフォンを真ん中に動かす
#
def center_phone():
    while g.mode == g.MODE_CENTER_PHONE:
        for i in range(10):
            g.phone.rect.y -= 480 / 2 / 10
            draw_haikei()
            draw_phone()
            update_and_eventchk()
        wait_time(1)
        g.mode = g.MODE_SETUMEI

#
# 説明表示
#
def disp_setumei():
    toumei = 0
    while g.mode == g.MODE_SETUMEI:
        g.setumei.set_alpha(toumei)
        for i in range(10):
            toumei = toumei + 255 / 10
            draw_haikei()
            draw_phone()
            g.setumei.set_alpha(toumei)
            draw_setumei()
            update_and_eventchk()

        # マウスが押されるまで待つ
        g.mouse_pushed = False
        while g.mouse_pushed == False:
            update_and_eventchk()

        for i in range(10):
            toumei = toumei + 255 / 10
            draw_haikei()
            draw_phone()
            g.setumei.set_alpha(toumei)
            draw_setumei()
            update_and_eventchk()
        g.mode = g.MODE_TITLE

#
# タイトル表示
#
def disp_title():
    while g.mode == g.MODE_TITLE:
        # 納涼
        toumei = 0
        wait_time(1)
        play_wood1_snd()
        for i in range(10):
            toumei = toumei + 255 / 10
            draw_haikei()
            draw_phone()
            g.title01.set_alpha(toumei)
            draw_title01()
            update_and_eventchk()

        # 花火大会
        toumei = 0
        wait_time(1.5)
        play_wood1_snd()
        for i in range(10):
            toumei = toumei + 255 / 10
            draw_haikei()
            draw_phone()
            draw_title01()
            g.title02.set_alpha(toumei)
            draw_title02()
            update_and_eventchk()

        # 開始
        toumei = 0
        size = 4
        wait_time(1.5)
        for i in range(10):
            toumei = toumei + 255 / 10
            size = size - 2.7 / 10
            draw_haikei()
            draw_phone()
            draw_title01()
            draw_title02()
            g.kaishi.image.set_alpha(toumei)
            draw_kaishi(size)
            update_and_eventchk()

        play_dodon_snd()
        wait_time(1.5)
        g.mode = g.MODE_FIREWORK


#
# 花火打ち上げ
#
def firework():
    firework_start_time = pygame.time.get_ticks()
    pygame.time.set_timer(g.NEW_FIREWORK_EVENT, 1000)
    while g.mode == g.MODE_FIREWORK:
        current_time = pygame.time.get_ticks()
        if current_time > firework_start_time + 30000:
            g.mode = g.MODE_KEKKA
            # イベントを停止
            pygame.time.set_timer(g.NEW_FIREWORK_EVENT, 0)
        else:
            draw_haikei()
            draw_fever()
            g.firework_group.update()
            draw_firework()
            move_phone()
            draw_phone()
            draw_point()

        if g.point > 300:
            fever_mode()

        update_and_eventchk()

#
# 結果発表
#
def kekka():
    kekka_start_time = pygame.time.get_ticks()
    kekka_stage = 0
    while g.mode == g.MODE_KEKKA:
        current_time = pygame.time.get_ticks()
        if kekka_stage == 0:
            play_wood1_snd()
            draw_sokomade()
            kekka_stage = 1
        if kekka_stage == 1 and current_time > kekka_start_time + 1500:
            play_wood2_snd()
            draw_sokomade02()
            kekka_stage = 2
        if kekka_stage == 2 and current_time > kekka_start_time + 3000:
            play_kozutumi_snd()
            draw_point_1000()
            kekka_stage = 3
        if kekka_stage == 3 and current_time > kekka_start_time + 4000:
            play_kozutumi_snd()
            draw_point_100()
            kekka_stage = 4
        if kekka_stage == 4 and current_time > kekka_start_time + 5000:
            play_kozutumi_snd()
            draw_point_10()
            kekka_stage = 5
        if kekka_stage == 5 and current_time > kekka_start_time + 6000:
            play_jidai_snd()
            draw_point_1()
            kekka_stage = 6

        update_and_eventchk()

#
# start関数（スタートかんすう）
#
def start():
    #初期化（しょきか）
    parts_init()

    # スマートフォンの移動
    center_phone()

    # 説明の表示
    disp_setumei()

    # タイトルの表示
    disp_title()

    # 花火打ち上げ
    firework()

    # 結果発表
    kekka()

#
# 🔰ここからメインプログラムを開始しています
#
start()
