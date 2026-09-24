import pygame

# Pygameの初期化
pygame.init()

# 画面のサイズ設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 画像とテキストの読み込み
background_image = pygame.image.load("img/prog_city.png")
character_image = pygame.image.load("img/hakase.png")
font = pygame.font.SysFont("meiryo", 55)

# タイトル・アイコン設定
pygame.display.set_caption("インデント課題")
icon_image = pygame.image.load("img/hakase.png")  # アイコン画像をロード
pygame.display.set_icon(icon_image)  # ウィンドウのアイコンとして設定

# キャラクターの位置設定
character_rect = character_image.get_rect()
character_rect.bottom = screen_height

# ✅課題３用の関数
def kadai3(text):
    # 背景とキャラクターの描画
    screen.blit(background_image, (0, 0))
    screen.blit(character_image, character_rect)

    # テキストの描画
        screen.blit(font.render(text, True, (255, 255, 255)), (280, 50))

    # 画面の更新
pygame.display.flip()
    
    # 3秒待機して終了
　　pygame.time.wait(3000) #3000ミリ秒=3秒  
    pygame.quit()
    
#
# 🚩ここからメインプログラムを開始します
#
kadai3("チャレンジ大成功！")