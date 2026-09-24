import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面設定
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Star Display")

# 色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# フォント設定
font = pygame.font.SysFont("meiryo", 32)
star_font = pygame.font.SysFont("meiryo", 24)  # 星を描画するためのフォント

def display_calculation_and_stars(expression):
    # 式の計算
    result = eval(expression)

    # 星の数を計算結果に基づいて決定（最大100）
    num_stars = min(int(result), 100)

    # 星のテキストを生成（10個ごとに改行）
    stars_text_str = ''
    for i in range(num_stars):
        stars_text_str += '★'
        if (i + 1) % 10 == 0:  # 10個ごとに改行を挿入
            stars_text_str += '\n'
    
    # 計算結果をテキストに変換
    text = font.render(expression + " = " + str(result), True, WHITE)
    
    # 星のテキストをレンダリング
    stars_text = star_font.render(stars_text_str, True, GOLD, BLACK)  # 背景色を指定する場合はここに追加

    # 画面をクリア
    screen.fill(BLACK)
    
    # テキストを画面に描画
    screen.blit(text, (50, 20))
    
    if result < 1 or result > 100:
        stars_text = star_font.render("1より小さいか、100より大きい数です！", True, WHITE)  # 背景色を指定する場合はここに追加
        screen.blit(stars_text, (100, 80))
    else:
        # 星を画面に描画（複数行にわたるため、位置調整が必要になるかもしれません）
        y_offset = 0
        for line in stars_text_str.split('\n'):
            line_text = star_font.render(line, True, GOLD)
            screen.blit(line_text, (160, 60 + y_offset))
            y_offset += star_font.get_linesize()  # 次の行のためにオフセットを増やす
    
    # 画面を更新
    pygame.display.flip()

def keisan(expression):
    # メインループ
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 計算式と結果、および星を表示
        display_calculation_and_stars(expression)  # ここで計算式を変更可能

        # イベントループの外で無限ループしないようにする
        # pygame.time.wait(5000)  # デモのため5秒後にウィンドウを閉じる
        # running = False

    # Pygameの終了
    pygame.quit()
    sys.exit()
