import pygame
import random

# 初期設定
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("課題3")
# グローバル変数の宣言
kosuu = 0

# フォントの設定
font = pygame.font.SysFont(None, 72)  # システムのデフォルトフォントを72ポイントで使用

# 画像のリサイズ関数（縦横比を保持）
def resize_image(image, target_width):
    original_width, original_height = image.get_size()
    scale_factor = target_width / original_width
    new_height = int(original_height * scale_factor)
    return pygame.transform.scale(image, (target_width, new_height))


# 画像の読み込み
red_bloom_img = pygame.image.load('img/赤ブルーム立ち.png')
red_bloom_img = resize_image(red_bloom_img, 50) 
mushroom_images = [
    pygame.image.load('img/キノコ1.png'),
    pygame.image.load('img/キノコ2.png'),
    pygame.image.load('img/キノコ3.png')
]
icon_img = pygame.image.load('img/キノコ1.png')
icon_img = resize_image(icon_img, 50) 
pygame.display.set_icon(icon_img)



# 赤ブルームの初期位置
red_bloom_rect = red_bloom_img.get_rect(bottomleft=(100, HEIGHT))

# キノコオブジェクトのリスト
mushrooms = []

def kinoko_draw():
    image = random.choice(mushroom_images)
    rect = image.get_rect(midbottom=(random.randint(0, WIDTH), 0))
    stopped = False  # キノコが停止しているかのフラグを追加
    mushrooms.append((image, rect, stopped))  # stopped フラグを追加

def update_mushrooms():
    for i, mushroom in enumerate(mushrooms):
        image, rect, stopped = mushroom
        if not stopped:  # キノコがまだ停止していない場合
            rect.y += 8  # キノコの落下速度

            # 当たり判定用の矩形を作成（元の矩形のサイズを半分にする）
            hit_rect = pygame.Rect(rect.x + rect.width // 4, rect.y + rect.height // 4, rect.width // 2, rect.height // 2)

            # 他のキノコに接触した場合の処理
            for other_mushroom in mushrooms:
                other_image, other_rect, other_stopped = other_mushroom
                if rect == other_rect:
                    continue  # 同じキノコは無視
                other_hit_rect = pygame.Rect(other_rect.x + other_rect.width // 4, other_rect.y + other_rect.height // 4, other_rect.width // 2, other_rect.height // 2)
                if hit_rect.colliderect(other_hit_rect) and hit_rect.bottom <= other_hit_rect.bottom:
                    rect.bottom = other_rect.top + other_rect.height // 4  # 当たり判定を考慮してキノコの上に乗せる
                    stopped = True  # キノコの移動を停止

            # 画面底に達したら停止
            if hit_rect.bottom >= HEIGHT:
                rect.y = HEIGHT - rect.height + (rect.height - hit_rect.height) // 2 # 当たり判定を考慮して位置調整
                stopped = True  # キノコの移動を停止

        # 更新されたキノコ情報をリストに戻す
        mushrooms[i] = (image, rect, stopped)

# kinoko関数の定義
def kinoko():
    global kosuu  # グローバル変数を関数内で使用する宣言
    kosuu += 1  # キノコのカウントを増やす
    kinoko_draw()  # キノコを一つ追加

    all_stopped = False
    while not all_stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        update_mushrooms()  # キノコの位置を更新

        screen.fill((0, 0, 0))  # 背景を塗りつぶし
        screen.blit(red_bloom_img, red_bloom_rect)  # 赤ブルームを描画

        # キノコの数を画面左上に表示
        count_text = font.render(f'Kinoko: {kosuu}', True, (255, 255, 255))
        screen.blit(count_text, (10, 10))

        # キノコを描画
        all_stopped = True
        for mushroom in mushrooms:
            image, rect, stopped = mushroom
            if not stopped:
                all_stopped = False
            screen.blit(image, rect)

        pygame.display.flip()
        clock.tick(60)