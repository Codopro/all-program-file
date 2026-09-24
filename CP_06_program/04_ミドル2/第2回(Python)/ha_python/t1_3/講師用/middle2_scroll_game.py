#
# <ミドル２コース ７月号 スクロールゲーム>
#

# partsファイル(パーツファイル)をインポート
from parts import *
from middle2_scroll_game_kadai import *

def get_coin():
    for i in range(len(g.coins) -1, -1, -1):    # リストから削除するので後ろから繰り返す
        sprite = g.coins[i]
        sprite.rect.centerx = g.coins_pos[i][0] - g.player_x
        sprite.rect.centery = g.coins_pos[i][1]
        if pygame.sprite.collide_rect(sprite, g.player): # 衝突判定
            kadai4()
            g.coin_sound.play()
            del g.coins[i]
            del g.coins_pos[i]

def draw_goal_serifu():
    current_ticks = pygame.time.get_ticks()
    if current_ticks - g.goal_time < 2000:
        kadai5()
#
# 開始
#
def start():
    #初期化（しょきか）
    parts_init()

    clock = pygame.time.Clock()

    while True:
        g.screen.blit(g.haikei, (0,0))

        # タイトル画面
        if g.mode == 0:
            kadai2()
            play_bgm_sound()
            g.coin_time = pygame.time.get_ticks()
            g.mode = 1

        # ゲーム画面
        elif g.mode == 1:
            draw_coin_num()
            key_check()
            down_player()
            move_course()
            make_coin()
            draw_coin()
            draw_goal()
            get_coin()
            goal_check()

            g.screen.blit(g.course_a.image, g.course_a.rect)
            g.screen.blit(g.course_b.image, g.course_b.rect)
            g.screen.blit(g.player.image, g.player.rect)

        # ゲーム終了
        elif g.mode == 2:
            draw_coin_num()
            draw_coin()
            draw_goal()
            draw_goal_serifu()
            if pygame.time.get_ticks() - g.goal_time > 2000:
                g.bgm.stop()

            g.screen.blit(g.course_a.image, g.course_a.rect)
            g.screen.blit(g.course_b.image, g.course_b.rect)
            g.screen.blit(g.player.image, g.player.rect)

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                pass
                #if g.mode == 0:
                #    if event.key == K_SPACE:
                #        play_bgm_sound()
                #        g.coin_time = pygame.time.get_ticks()
                #        g.mode = 1
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#
# 🔰ここからメインプログラムを開始しています
#
start()
g
