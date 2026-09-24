#
# <ミドル２コース Python課題 ７月号 かき氷シミュレーター>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# 50個の氷片をふらせる(100 回移動させる。y 座標が大きくなったら上から)
#
def move_sliced_ice(sliced_ice, cup):
    for j in range(100):
        draw_haikei()
        draw_cup(cup)
        for i in range(50):
            sliced_ice[i].rect.y += 5
            if sliced_ice[i].rect.centery > 360:
                sliced_ice[i].rect.centery = 0
            draw_sliced_ice(sliced_ice[i])
        draw_syrup_num()
        update_and_eventchk()

#
# 氷片を50個作る
#
def make_sliced_ice(sliced_ice):
    for i in range(50):
        sprite =  pygame.sprite.Sprite()
        sprite.image = g.sliced_ice.image.copy()
        sprite.image = pygame.transform.rotozoom(sprite.image, random.randint(-90, 90), 1)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = (320 + random.randint(-130, 130), random.randint(0, 360))
        sliced_ice.append(sprite)

#
# かき氷を作る
#
def drop_shaved_ice():
    sliced_ice = []
    make_sliced_ice(sliced_ice)

    for i in range(5):
        g.cup.image = g.cups[i]
        move_sliced_ice(sliced_ice, g.cup)

    g.mode = g.MODE_POUR_SYRUP


#
#✅シロップの数を数える
#
def count_syrup_num(syrup_flavor):
    if syrup_flavor == ICHIGO:
        g.ichigo_num = g.ichigo_num + 1
    elif syrup_flavor == LEMON:
        g.lemon_num = g.lemon_num + 1
    elif syrup_flavor == MELON:
        g.melon_num = g.melon_num + 1
    elif syrup_flavor == BLUE_HAWAII:
        g.blue_hawaii_num = g.blue_hawaii_num + 1

    # ✅プログラミングチャレンジ2
    # シロップの合計を計算してかけすぎないようにする
    g.total_syrup_num = g.ichigo_num + g.lemon_num + g.melon_num + g.blue_hawaii_num

    # シロップの合計が 100 以上ならばシロップをストップする
    if g.total_syrup_num >= 100:
        g.stop_syrup = True

#
# カップに触れるまでシロップを落とす
#
def drop_syrup():
    i = 0
    while i < len(g.syrup_sprites):
        draw_syrup(i)
        if pygame.sprite.collide_mask(g.syrup_sprites[i], g.cup):
            if g.syrup_flavors[i] != -1:
                g.syrup_sprites[i].image.set_alpha(128)
                rect_y = g.syrup_sprites[i].rect.y
                g.syrup_sprites[i].rect.y = random.randint(rect_y + 30, 380)
                g.syrup_flavors[i] = -1
        else:
            g.syrup_sprites[i].rect.y += 5
        i += 1

#
# シロップをかける処理
#
def pour_syrup():
    while g.mode == g.MODE_POUR_SYRUP:
        draw_haikei()
        draw_cup(g.cup)
        draw_syrup_machine()
        draw_right_arrow()
        draw_left_arrow()
        draw_to_next()
        drop_syrup()
        draw_syrup_num()

        # キー入力処理
        keys = pygame.key.get_pressed()
        # 右矢印キー
        if keys[pygame.K_RIGHT]:
            if g.syrup_machine.rect.centerx < WIDTH / 2 + 140:
                g.syrup_machine.rect.x += 2
        # 左矢印キー
        if keys[pygame.K_LEFT]:
            if g.syrup_machine.rect.centerx >  WIDTH / 2 - 140:
                g.syrup_machine.rect.x -= 2
        # スペースキー
        if keys[pygame.K_SPACE]:
            if not g.stop_syrup:
                time = pygame.time.get_ticks()
                if (time - g.prev_time) > 100:
                    sprite =  pygame.sprite.Sprite()
                    g.syrup.image = g.syrups[g.syrup_machine_num]
                    sprite.image = g.syrup.image.copy()
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.center = g.syrup_machine.rect.center
                    sprite.rect.y += 70
                    g.syrup_sprites.append(sprite)
                    g.syrup_flavors.append(g.syrup_machine_num)
                    count_syrup_num(g.syrup_flavors[-1])
                    g.prev_time = pygame.time.get_ticks()

        update_and_eventchk()

#
# スイカの処理
#
def move_watermelon():
    if g.watermelon_moving == 1:
        watermelon_rot_image = pygame.transform.rotozoom(g.watermelon.image,
                                                         g.watermelon_rot, 1)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if g.watermelon_rot_rect.centerx < 450:
                g.watermelon_rot_rect.x += 2
        if keys[pygame.K_LEFT]:
            if g.watermelon_rot_rect.centerx > 190:
                g.watermelon_rot_rect.x -= 2
        if keys[pygame.K_a]:
            g.watermelon_rot += 1
        if keys[pygame.K_d]:
            g.watermelon_rot -= 1
        if keys[pygame.K_SPACE]:
            g.watermelon_moving = 2
            g.watermelon.image = watermelon_rot_image
            g.watermelon.rect = g.watermelon_rot_rect
        g.screen.blit(watermelon_rot_image, g.watermelon_rot_rect)
    elif g.watermelon_moving == 2:
        if pygame.sprite.collide_mask(g.watermelon, g.cup):
            g.watermelon.rect.y += 130
            g.watermelon_moving = 3
        else:
            g.watermelon.rect.y += 5
        draw_watermelon()
    elif g.watermelon_moving == 3:
        draw_watermelon()

#
# クッキーの処理
#
def move_cookie():
    if g.cookie_moving == 1:
        cookie_rot_image = pygame.transform.rotozoom(g.cookie.image,
                                                     g.cookie_rot, 1)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if g.cookie_rot_rect.centerx < 450:
                g.cookie_rot_rect.x += 2
        if keys[pygame.K_LEFT]:
            if g.cookie_rot_rect.centerx > 190:
                g.cookie_rot_rect.x -= 2
        if keys[pygame.K_a]:
            g.cookie_rot += 1
        if keys[pygame.K_d]:
            g.cookie_rot -= 1
        if keys[pygame.K_SPACE]:
            g.cookie_moving = 2
            g.cookie.image = cookie_rot_image
            g.cookie.rect = g.cookie_rot_rect
        g.screen.blit(cookie_rot_image, g.cookie_rot_rect)
    elif g.cookie_moving == 2:
        if pygame.sprite.collide_mask(g.cookie, g.cup):
            g.cookie.rect.y += 130
            g.cookie_moving = 3
        else:
            g.cookie.rect.y += 5
        draw_cookie()
    elif g.cookie_moving == 3:
        draw_cookie()

#
#  色を選択する処理
#
def select_color():
    iro = 0
    #✅プログラミングチャレンジ3
    iro = random.randint(0, 6)
    if iro == 0:
        (r, g, b) = DARK_CHOCO
    elif iro == 1:
        (r, g, b) = PINK
    elif iro == 2:
        (r, g, b) = PASTEL_GREEN
    elif iro == 3:
        (r, g, b) = GOLD
    elif iro == 4:
        (r, g, b) = SILVER
    elif iro == 5:
        (r, g, b) = LIGHT_BLUE
    else:
        (r, g, b) = MILK_CHOCO

    return (r, g, b)

#
# 色を赤/青/緑の３つのランダムな色にする
#
def change_color(image):
    (r, g, b) = select_color()
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            image.set_at((x, y), (r, g, b, 200))


#
# トッピングの処理
#
def put_topping():
    while g.mode == g.MODE_TOPPING:
        draw_haikei()
        draw_right_triangle()
        draw_left_triangle()
        draw_to_next()
        draw_topping()
        move_watermelon()
        move_cookie()
        draw_cup(g.cup)
        draw_syrup_num()
        i = 0
        while i < len(g.syrup_sprites):
            draw_syrup(i)
            i+=1
        i = 0
        while i < len(g.chocolates):
            draw_chocolates(i)
            if pygame.sprite.collide_mask(g.chocolates[i], g.cup):
                if g.chocolates_moving[i]:
                    rect_y = g.chocolates[i].rect.y
                    g.chocolates[i].rect.y = random.randint(rect_y + 5, 370)
                    g.chocolates_moving[i] = False
            else:
                g.chocolates[i].rect.y += 5
            i += 1

        if g.topping_pushed:
            # スプレーチョコ
            if g.topping_num == 0:
                for i in range(10):
                    sprite =  pygame.sprite.Sprite()
                    sprite.image = g.chocolate.image.copy()
                    change_color(sprite.image)
                    sprite.image = pygame.transform.rotozoom(sprite.image,
                                                             random.randint(-90, 90),
                                                             1)
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.center = (320 + random.randint(-130, 130),
                                          random.randint(0, 160))
                    g.chocolates.append(sprite)
                    g.chocolates_moving.append(True)

            # すいか
            elif g.topping_num == 1:
                if g.watermelon_moving != 3:
                    g.watermelon_moving = 1
            # クッキー
            elif g.topping_num == 2:
                if g.cookie_moving != 3:
                    g.cookie_moving = 1
            g.topping_pushed = False
        update_and_eventchk()
#
# 完成
#
def complete():
    while True:
        update_and_eventchk()

#
# 開始
#
def start():
    # 初期化（しょきか）
    parts_init()

    # 氷片をふらせる
    drop_shaved_ice()

    # シロップをかける
    pour_syrup()

    # トッピングをのせる
    put_topping()

    # 完成
    complete()
#
# 🔰ここからメインプログラムを開始しています
#
start()
