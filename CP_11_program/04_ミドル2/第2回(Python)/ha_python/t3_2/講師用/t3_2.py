#
# <ミドル２コース Python課題 11月号 焼き芋>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# いもの状態管理
#
def manage_imo_state():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        pass
        #✅プログラミングチャレンジ2
        # スペースキーが押されたときの処理
        match g.imo_status:
            case g.IMO_START:
                g.imo_status = g.IMO_MOVING
            case g.IMO_ROASTING:
                g.imo_status = g.IMO_ROASTED
                g.mode = g.MODE_ROASTED

#
# やきあがりの処理
#
def yakiagari():
    pass
    #✅プログラミングチャレンジ3
    # 焼き上がった時のドースのコメントとコスチュームを決定する
    match g.imo:
        case g.imo_nama:
            g.eval_comment = "まだ生だよ！"
            g.dose = g.dose_syonbori
        case g.imo_namayake:
            g.eval_comment = "焼き足りないなあ…"
            g.dose = g.dose_syonbori
        case g.imo_tyoudoii:
            g.eval_comment = "う～ん、絶妙！"
            g.dose = g.dose_perori
        case _:
            g.eval_comment = "ちょっと苦いな"
            g.dose = g.dose_standing

#
# いもを焼いているときにドースがセリフを言う
#
def dose_say_serihu():
    serihu = ""
    # オリジナルチャレンジ
    match g.imo:
        case g.imo_nama:
            serihu = "おなかすいた…"
        case g.imo_namayake:
            serihu = "いいにおいがしてきた！"
        case g.imo_tyoudoii:
            serihu = "もうがまんできない！"
        case g.imo_kogeta:
            serihu = "なかはだいじょうぶ！"

    if serihu != "" and g.imo_status != g.IMO_START:
        draw_hukidashi(100, 140, serihu)


#
# いもを焼く処理
#
def imo_roasting():
    while g.mode == g.MODE_ROASTING:
        draw_haikei()
        draw_dose()
        draw_wood_dark()
        if g.imo_status != g.IMO_START:
            draw_imo()
        draw_fire()
        manage_imo_state()
        move_imo()
        chg_roasting_imo()
        dose_say_serihu()

        update_and_eventchk()

#
# いもが焼きあがった時に動く処理
#
def imo_roasted():
    roasted_time = pygame.time.get_ticks()
    stop_fire_snd()
    yakiagari()
    decide_bairitu()
    g.imo_pos = [150, 220]
    g.imo = pygame.transform.rotate(g.imo, -30)
    while g.mode == g.MODE_ROASTED:
        draw_haikei()
        draw_wood_dark()
        draw_roasted_state_imo_dose(roasted_time)

        update_and_eventchk()

#
# 開始
#
def start():
    #初期化（しょきか）
    parts_init()

    #焼き芋を焼く
    imo_roasting()

    #焼き芋出来上がり
    imo_roasted()

#
# 🔰ここからメインプログラムを開始しています
#
start()
