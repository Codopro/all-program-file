#
# <ミドル２コース Python課題 10号 ハロウィン>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# お菓子を集める
#
def get_candy():
    start_time = pygame.time.get_ticks()
    play_bgm1_sound()
    while g.mode == g.MODE_START:
        nokori_time = 80 - int((pygame.time.get_ticks() - start_time) / 1000)
        if nokori_time == 30:
            change_bgm()
        if nokori_time == 0:
            g.mode = g.MODE_TIMEUP
        move_obake()
        update_candy()
        original_challenge()
        draw_haikei_house()
        move_dose()
        draw_dose()
        draw_obake()
        disp_nokori_time(nokori_time)
        disp_candy_num()
        disp_trick_or_treat()
        get_candy_hantei()
        update_and_eventchk()

#
# オリジナルチャレンジ
# ドースとおばけが触れたら、ドースのお菓子がおばけに取られる！
#
def original_challenge():
    if calculate_distance(g.dose, g.obake) < 40:
        g.obake_candy += g.dose_candy
        g.dose_candy = 0
    return

#
# ゲーム終了
#
def timeup():
    dose_pos = (20, 180)
    obake_pos = (450, 180)
    stop_bgm()
    play_timeup_sound()
    while g.mode == g.MODE_TIMEUP:
        draw_haikei_house()
        draw_big_dose(dose_pos)
        draw_big_obake(obake_pos)
        draw_hukidashi(dose_pos[0] + 100, dose_pos[1] - 50, str(g.dose_candy) + "コ集めた！")
        draw_hukidashi(obake_pos[0] - 100, obake_pos[1] - 50, str(g.obake_candy) + "コ集めました..")
        update_and_eventchk()

#
# オープニングのセリフを話す
#
def say_opening_serihu(dose_serihu, obake_serihu):
    dose_pos = (20, 180)
    obake_pos = (450, 180)
    if g.serihu_order % 2 == 0:
        try:
            draw_hukidashi(dose_pos[0] + 100, dose_pos[1] - 50, dose_serihu[0], True)
        except IndexError as e:
            g.mode = g.MODE_START
    else:
        try:
            draw_hukidashi(obake_pos[0] - 100, obake_pos[1] - 50, obake_serihu[0], True)
        except IndexError as e:
            g.mode = g.MODE_START

    if pygame.time.get_ticks() - g.serihu_time > 2000:
        g.serihu_time = pygame.time.get_ticks()
        try:
            if g.serihu_order % 2 == 0:
                dose_serihu.pop(0)
            else:
                obake_serihu.pop(0)
        except IndexError as e:
            g.mode = g.MODE_START
        g.serihu_order += 1

#
# オープニング処理
#
def opening():
    dose_serihu = []
    obake_serihu = []
    dose_pos = (20, 180)
    obake_pos = (450, 180)
    g.serihu_time = pygame.time.get_ticks()

    #✅プログラミングチャレンジ3
    # ドースとお化けの会話をリストに設定する
    dose_serihu.append("ハロー、おばけさん！")
    obake_serihu.append("こんにちは、ドースさん")
    dose_serihu.append("おかしをいっぱいあつめよう！")
    obake_serihu.append("私も負けませんよ")

    g.serihu_time = pygame.time.get_ticks()

    while g.mode == g.MODE_OPENING:
        draw_haikei_house()
        draw_big_dose(dose_pos)
        draw_big_obake(obake_pos)
        say_opening_serihu(dose_serihu, obake_serihu)
        update_and_eventchk()

#
# お菓子の数を増やす（増やす個数は１から５までのランダムな数）
#
def increase_candy():
    #✅プログラミングチャレンジ2
    # お菓子の数を増やす
    g.candy_num[0] += random.randint(1,5)
    g.candy_num[1] += random.randint(1,5)
    g.candy_num[2] += random.randint(1,5)
    g.candy_num[3] += random.randint(1,5)
    return

#
# 一定時間ごとにお家のお菓子の数を更新
#
def update_candy():
    current_time = pygame.time.get_ticks()
    if  current_time > g.candy_time:
        increase_candy()
        g.candy_time = current_time + random.randint(1,3) * 1000

#
# 開始
#
def start():
    #初期化（しょきか）
    parts_init()

    #オープニング
    opening()

    #お菓子を集める
    get_candy()

    #ゲーム終了
    timeup()


#
# 🔰ここからメインプログラムを開始しています
#
start()
