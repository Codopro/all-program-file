#===============================================
#スタートアップ課題2 Pythonコードを読み方を学ぶ
#===============================================

import pygame
import os

# 初期化
pygame.init()

# 画面サイズ設定
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# タイトル設定
pygame.display.set_caption("ジャンプアニメーション")

# アイコンを設定
icon_image = pygame.image.load('img/robo2-a.png')  # アイコン画像をロード
pygame.display.set_icon(icon_image)  # ウィンドウのアイコンとして設定

# ロードする画像とサイズ変更
image_path = 'img/robo2-a.png'
original_image = pygame.image.load(image_path)
image_size = (100, 100)  # 画像サイズ（幅、高さピクセル）
robot_image = pygame.transform.scale(original_image, image_size)
robot_pos = [220, 280] #ロボットの位置（左上から右に250ピクセル、下に280ピクセルずらす)


# ✅セリフ関数
def serifu(text):
    
    screen.fill((0, 0, 0))  # 画面を黒で塗りつぶし（RBG)

    font = pygame.font.SysFont("meiryo", 55)
    text_surface = font.render(text, True, (255, 255, 255)) #テキストの色は白(RGB)
    #セリフの位置設定(左上から右に150ピクセル、下に150ピクセルずらす)
    screen.blit(text_surface, (150, 150))
    pygame.display.flip()  # 画面更新
    
# ✅ジャンプ関数
def jump(height):
    
    duration = int(round(height/3,0))
    
    screen.blit(robot_image, robot_pos)  # 画像表示
    pygame.display.flip()  # 画面更新
    pygame.time.wait(2000)
    
    original_y = robot_pos[1]
    
      #🔰「ジャンプする距離/3」した回数にわけて移動させている(「~回繰り返す」と同じ)
    for step in range(duration):
        t = step / duration  # 時間の進行を表す変数
        robot_pos[1] = original_y - height * 4 * t * (1 - t) #なめらかにジャンプさせる式
        screen.fill((0, 0, 0))  # 画面を黒で塗りつぶし
        screen.blit(robot_image, robot_pos)  # 画像表示
        pygame.display.flip()  # 画面更新
        pygame.time.delay(20)  #20ミリ秒間隔
        
    robot_pos[1] = original_y #元の位置にもどす
    screen.fill((0, 0, 0))  # 画面を黒で塗りつぶし
    screen.blit(robot_image, robot_pos)  # 画像表示
    pygame.display.flip()  # 画面更新
    
    pygame.time.wait(2000)  # 2秒待機
    pygame.quit()
    
#
# 🚩ここからメインプログラムを開始します
#
serifu("おはよう") 
jump(50)  # 数値のピクセルだけジャンプ