#
# <ミドル２コース Python課題 5月号 自動販売機シミュレーター>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# ギフトカードをひく
#
def giftcard():

    #ギフトカード開封演出（未開封→開封途中→はさみをいれるまで）
    open_gift()
    
    # 
    # ✅プログラミングチャレンジ1：
    # ギフトカードの抽選処理


    wait_time(1) #1秒待つ
    g.mode = g.MODE_PLAY #シミュレータ動作開始

#
# 自販機シミュレータ動作中の処理
#
def sim_start():
    game_start_ticks = pygame.time.get_ticks()
    while g.mode == g.MODE_PLAY:
        move_donpay_home()
        draw_haikei()
        draw_broom()
        draw_irekae()
        draw_touch()
        draw_zandaka()
        draw_disp_products()
        move_buy_products()
        draw_got_products()
        draw_donpay()

        if g.broom_clicked:
            draw_hukidashi("いくらチャージする？\n(エンターキーで決定)")
            draw_input_box()

        current_ticks = pygame.time.get_ticks()
        if current_ticks - game_start_ticks < 2000:
            draw_hukidashi("チャージするには\nぼくをクリックしてね。")
        if current_ticks - g.over_charge_start_ticks < 2000:
            draw_hukidashi("チャージ上限は99だよ")
        if current_ticks - g.short_money_start_ticks < 2000:
            draw_hukidashi("どんぐりが足りないみたい")
        update_and_eventchk()


#
# start関数（スタートかんすう）
#
def start():
    #初期化
    parts_init()

    # くじ画面
    giftcard()

    # 自販機シミュレータ動作中
    sim_start()

#
# 🚩ここからメインプログラムを開始しています
#
start()
