#
# <ミドル２コース Python課題 9月号 積ん読ゲーム>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# 新しい本を作る
#
def make_new_book():
    play_new_book_snd()
    book_init_pos =  (WIDTH / 2, 100)
    sprite = prepare_book_sprite("img/book.png", 1/6, book_init_pos)
    sprite.rect.centerx = random.randint(0 + 200, WIDTH-200)
    g.books.append(sprite)
    g.book_group.add(sprite)

#
# 画面更新とイベント監視
#
def update_and_eventchk():
    pygame.display.update()
    g.clock.tick(30)
    for event in pygame.event.get():
        if event.type == g.NEW_BOOK_EVENT:
            print("新しい本が落ちてくる")
            #✅プログラミングチャレンジ2
            # 新しい本を作る
            make_new_book()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

#
# 台を動かす
#
def move_dai(speed):
    keys = pygame.key.get_pressed()
    #✅プログラミングチャレンジ3
    if keys[pygame.K_RIGHT] == True:
        if g.dai.rect.centerx < 640:
            g.dai.rect.centerx += speed
    if keys[pygame.K_LEFT] == True:
        if g.dai.rect.centerx > 0:
            g.dai.rect.centerx -= speed

#
# 本が落ちてくる
#
def drop_book():
    pygame.time.set_timer(g.NEW_BOOK_EVENT, 3000)
    while g.mode == g.MODE_DROP_BOOK:
        # draw_basic_sprite()
        # 背景を白色で塗りつぶす
    #    g.screen.fill(WHITE)
        draw_haikei()
        draw_memori()
        draw_dai()
        draw_hari()
        draw_books()
        g.book_group.update()

        #✅プログラミングチャレンジ4
        # 10冊積めたらゲームクリアーにする
        if len(g.book_group) > 10:
            draw_hukidashi("10冊積んだぞ！")
            g.mode = g.MODE_END
            break

        draw_last_book()
        move_dai(5)

        if abs(g.total_zure) > 60:
            g.mode = g.MODE_BREAK_DOWN_BOOK

        update_and_eventchk()

#
# 本が崩れる
#
def break_down_book():
    pygame.time.set_timer(g.NEW_BOOK_EVENT, 0)
    while g.mode == g.MODE_BREAK_DOWN_BOOK:
        for sprite in g.book_group:
            sprite.stage = 3
        g.screen.fill(WHITE)
        draw_memori()
        draw_dai()
        draw_hari()
        g.book_group.update()
        draw_books()
        draw_last_book()
        draw_hukidashi(str(len(g.book_group)) + "冊でくずれた...")
        play_game_over_snd()
        g.mode = g.MODE_END

        update_and_eventchk()

#
# ゲーム終了
#
def game_end():
    while g.mode == g.MODE_END:
        update_and_eventchk()

#
# 開始
#
def start():
    #初期化（しょきか）
    parts_init()

    #本が落ちてくる
    drop_book()

    #本が崩れる
    break_down_book()

    #ゲーム終了
    game_end()

#
# 🔰ここからメインプログラムを開始しています
#
start()

