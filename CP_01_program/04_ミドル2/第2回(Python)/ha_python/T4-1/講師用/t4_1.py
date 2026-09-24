#
# <ミドル２コース Python課題 １月号 あめよけゲーム>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# 晴れ
#
def process_sunny():
    x, y = 30, 100
    g.weather = g.FINE
    start_time = pygame.time.get_ticks()
    play_heiwa_snd()
    draw_haikei()
    draw_neko()
    #✅プログラミングチャレンジ2
    for i in range(7):
        g.screen.blit(g.title_text[i], (x, y))
        x += 80
        wait_time(1)
    while g.mode == g.MODE_SUNNY:
        if (pygame.time.get_ticks() - start_time) >= 5000:
            g.mode = g.MODE_RAIN_START

        draw_haikei()
        draw_kasa()
        kasa_transaction()
        move_neko()
        draw_neko()

        update_and_eventchk()

#
# 降り始め
#
def process_rain_start():
    g.weather = g.RAIN_START
    start_time = pygame.time.get_ticks()
    stop_all_snd()
    while g.mode == g.MODE_RAIN_START:
        play_bgm()
        if (pygame.time.get_ticks() - start_time) >= 2000:
            g.mode = g.MODE_GAME_START

        draw_haikei()
        draw_kasa()
        kasa_transaction()
        move_neko()
        draw_neko()

        update_and_eventchk()

#
# ゲームスタート
#
def game_start():
    pygame.time.set_timer(g.NEW_RAIN_EVENT, int(30 * 1000 / (10 + g.rain_level)))
    while g.mode == g.MODE_GAME_START:
        play_bgm()
        draw_haikei()
        draw_kasa()
        check_tenki()
        check_wind_level()
        move_neko()
        kasa_transaction()
        g.rain_group.update()

        draw_neko()
        draw_rain()

        update_and_eventchk()

#
# ゲームオーバー
#
def game_over():
    play_pasha_snd()
    play_potapota_snd()
    #✅プログラミングチャレンジ3
    for i in range(100):
        change_neko_dark()
        draw_neko()
        wait_time(0.01)
    draw_hukidashi(g.neko.rect.centerx, g.neko.rect.y - 60, "ずぶぬれだ...")
    wait_time(2)
    draw_hukidashi(g.neko.rect.centerx, g.neko.rect.y - 60, "こまったぞ...")
    wait_time(2)
    draw_hukidashi(g.neko.rect.centerx, g.neko.rect.y - 60, "家に帰らないと")

    while g.mode == g.MODE_GAME_OVER:
        play_bgm()
        update_and_eventchk()

#
# 開始
#
def start():
    #初期化（しょきか）
    parts_init()

    #晴れ
    process_sunny()

    #降り始め
    process_rain_start()

    #ゲームスタート
    game_start()

    #ゲームオーバー
    game_over()


#
# 🔰ここからメインプログラムを開始しています
#
start()
