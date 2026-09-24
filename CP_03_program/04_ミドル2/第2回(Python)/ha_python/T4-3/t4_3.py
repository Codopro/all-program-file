#
# <ミドル２コース Python課題 3月号 育成ゲーム>
#

# partsファイル(パーツファイル)をインポート
from parts import *
import random

#
# ねこを描く
#
def draw_neko():
    if not hasattr(draw_neko, "x"):
        draw_neko.x, draw_neko.y = 270, 200
        draw_neko.velocity_y = 0
        draw_neko.gravity = 1

    #✅プログラミングチャレンジ4















    g.screen.blit(g.neko, (draw_neko.x, draw_neko.y))


#
# メニュー選択
#
def select_menu():
    mouse_over = False
    sound_played = False
    while g.mode == g.MODE_SELECT_MENU:

        draw_haikei()
        draw_neko()

        g.haikei = g.HAIKEI_NONE
        a = draw_training()
        b = draw_benkyo()
        c = draw_fassion()
        d = draw_odekake()
        e = draw_oyasumi()
        if a == True or b == True or c == True or d == True or e == True:
            if sound_played == False:
                play_mouse_over_snd()
                sound_played = True
        else:
            sound_played = False

        draw_status_panel()

        draw_training_status()
        draw_benkyo_status()
        draw_fassion_status()
        draw_odekake_status()
        draw_oyasumi_status()

        update_and_eventchk()

#
# メニューが選択された
#
def menu_selected():
    while g.mode == g.MODE_MENU_SELECTED:
        draw_haikei()
        draw_neko()
        draw_status_panel()

        draw_training_status()
        draw_benkyo_status()
        draw_fassion_status()
        draw_odekake_status()
        draw_oyasumi_status()

        draw_selected_panel()
        update_and_eventchk()

def draw_status_change_iroiro():
        draw_haikei()
        draw_neko()
        draw_status_panel()
        draw_training_status()
        draw_benkyo_status()
        draw_fassion_status()
        draw_odekake_status()
        draw_oyasumi_status()
        update_and_eventchk()

#
# ステータス変更
#
def status_change():
    status_change_start_time = pygame.time.get_ticks()
    status_change_stage = 0
    muri = False
    if g.select_menu == g.OYASUMI:
        g.target_oyasumi_sts += 50
        if g.target_oyasumi_sts > 100:
            g.target_oyasumi_sts = 100
        # 課題対応前は一度に変わる
        g.oyasumi_sts = g.target_oyasumi_sts
        #✅プログラミングチャレンジ3





    else:
        up_status_val = random.randint(5, 10)
        down_hp_val = random.randint(20, 30)
        if down_hp_val > g.oyasumi_sts:
            muri = True
        else:
            match g.select_menu:
                case g.TRAINING:
                    g.target_training_sts += up_status_val
                case g.BENKYO:
                    g.target_benkyo_sts += up_status_val
                case g.FASSION:
                    g.target_fassion_sts += up_status_val
                case g.ODEKAKE:
                    g.target_odekake_sts += up_status_val

    while g.mode == g.MODE_STATUS_CHANGE:
        current_time = pygame.time.get_ticks()
        draw_haikei()
        draw_neko()

        draw_status_panel()

        draw_training_status()
        draw_benkyo_status()
        draw_fassion_status()
        draw_odekake_status()
        draw_oyasumi_status()

        if g.select_menu == g.OYASUMI:
            if status_change_stage == 0:
                play_kaihuku_snd()
                status_change_stage = 1
            if status_change_stage == 1:
                draw_hukidashi(330, 150, "たいりょくがかいふく！")
                if current_time > status_change_start_time + 2000:
                    g.mode = g.MODE_SELECT_MENU
        else:
            if muri:
                if status_change_stage == 0:
                    play_tired_snd()
                    status_change_stage = 1
                if status_change_stage == 1:
                    draw_hukidashi(330, 150, "つかれちゃったからムリ！")
                    if current_time > status_change_start_time + 2000:
                        g.mode = g.MODE_SELECT_MENU
            else:
                if status_change_stage == 0:
                    play_status_up_snd()
                    for i in range(5):
                        g.arrow_x[i] = 280 + random.randint(0, 100)
                        g.arrow_y[i] = 200 + random.randint(0, 100)
                        g.arrow_alpha[i] = 255
                    status_change_stage = 1
                if status_change_stage == 1:
                    serihu = g.status_name[g.select_menu - 1] + "が" + str(up_status_val) + "アップ！"
                    draw_hukidashi(330, 150, serihu)
                    if current_time > status_change_start_time + 1000:
                        g.target_oyasumi_sts -= down_hp_val;
                        status_change_stage = 2
                        play_hp_minus_snd()
                if status_change_stage == 2:
                    serihu = "体力が" + str(down_hp_val) + "ダウン..."
                    draw_hukidashi(330, 150, serihu)
                    if current_time > status_change_start_time + 3000:
                        g.mode = g.MODE_SELECT_MENU
                if current_time > status_change_start_time + 500:
                    arrow_num = 5
                elif current_time > status_change_start_time + 400:
                    arrow_num = 4
                elif current_time > status_change_start_time + 300:
                    arrow_num = 3
                elif current_time > status_change_start_time + 200:
                    arrow_num = 2
                else:
                    arrow_num = 1
                draw_arrow(arrow_num)

        update_and_eventchk()

#
# 開始
#
def start():
    #初期化（しょきか）
    parts_init()

    #✅プログラミングチャレンジ2

    #メニュー選択
    # select_menu()

    #メニューが選択された
    menu_selected()

    #ステータス変更
    status_change()

#
# 🔰ここからメインプログラムを開始しています
#
start()
