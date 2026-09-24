#
# <ミドル２コース Python課題 １２月 ろうそく吹き消しゲーム>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# ろうそくの火をだんだん消していく処理
#
def chg_rosoku_hp():
    #✅プログラミングチャレンジ2


    return

#
# 机のダメージをチェックする
#
def check_desk_damage():
    #✅プログラミングチャレンジ3






    return

#
# ろうそくの火が復活していく処理
#
def rosoku_hukkatu():
    #✅プログラミングチャレンジ4



    return

#
# ゲームのメイン処理
#
def main_start():
    while g.mode == MODE_MAIN:
        chg_bress_mode()
        chg_cake_costume()
        chg_rosoku_hp()
        rosoku_hukkatu()
        check_desk_damage()
        boy_eat_cake()
        make_wind()
        move_cake()
        yurasu_desk()
        destroy_desk()
        g.wind_group.update()
        g.bress_group.update()

        draw_haikei()
        draw_wind()
        draw_desk()
        draw_hibi()
        draw_boy()
        draw_cake()
        draw_bress()
        draw_white_mask()
        draw_boy_hukidashi()

        play_sound()
        update_and_eventchk()

#
# ゲーム終了時の処理
#
def game_end():
    while g.mode == MODE_END:
        draw_haikei()
        draw_boy()
        update_and_eventchk()
#
# 開始
#
def start():
    #初期化（しょきか）
    parts_init()

    #本体
    main_start()

    #ゲーム終了
    game_end()

#
# 🔰ここからメインプログラムを開始しています
#
start()
