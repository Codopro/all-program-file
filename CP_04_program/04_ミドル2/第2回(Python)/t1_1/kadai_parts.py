import pygame
import random
import math

# グローバル変数の定義
WIDTH, HEIGHT = 640, 480
screen = None
box_image = None
coin_image = None
coins = []

# 画像のリサイズ関数（縦横比を保持）
def resize_image(image, target_width):
    original_width, original_height = image.get_size()
    scale_factor = target_width / original_width
    new_height = int(original_height * scale_factor)
    return pygame.transform.scale(image, (target_width, new_height))

# 初期化関数
def init():
    global screen, box_image, box2_image, coin_image,bloom_image, bloom2_image, font
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("課題1")
    

    # 宝箱画像の読み込み、リサイズ、反転
    box_image = pygame.image.load("img/box1.png")
    box_image = resize_image(box_image, 100)  
    box_image = pygame.transform.flip(box_image, True, False)
    box2_image = pygame.image.load("img/box2.png")
    box2_image = resize_image(box2_image, 100) 
    box2_image = pygame.transform.flip(box2_image, True, False)

    # コイン画像の読み込み、リサイズ
    coin_image = pygame.image.load("img/コイン.png")
    coin_image = resize_image(coin_image, 30) 

    pygame.display.set_icon(coin_image)

    #　赤ブルーム画像の読み込み、リサイズ、反転
    bloom_image = pygame.image.load("img/赤ブルーム.png")
    bloom_image = resize_image(bloom_image, 100)  
    bloom_image = pygame.transform.flip(bloom_image, True, False)
    bloom2_image = pygame.image.load("img/赤ブルーム立ち.png")
    bloom2_image = resize_image(bloom2_image, 50)  
    
    # 左上のコインの数の初期化とフォントオブジェクトの作成
    pygame.font.init()  # フォントモジュールの初期化
    font = pygame.font.Font(None, 72)  # デフォルトフォントでサイズ36のフォントオブジェクトを作成



# コインのクラス
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = coin_image.get_width()
        self.angle = random.uniform(0, math.pi / 8)
        self.speed = random.uniform(2.5, 4.5)
        self.gravity = 0.2
        self.x_speed = math.cos(self.angle) * self.speed
        self.y_speed = math.sin(self.angle) * self.speed * 8  # 初速度の縦方向成分

    def move(self):
        self.x += self.x_speed
        self.y_speed -= self.gravity
        self.y -= self.y_speed*0.8

        if self.y > HEIGHT - self.size:
            self.y = HEIGHT - self.size
            self.x_speed = 0
            self.y_speed = 0

    def draw(self):
        screen.blit(coin_image, (self.x, self.y))

# コインを生成してアニメーションを行う関数
def coin(count):
    init()
    clock = pygame.time.Clock()
    global box_image
    box_rect = box_image.get_rect(bottomleft=(WIDTH / 4, HEIGHT))  # 宝箱を画面の下部に配置
    bloom_rect = bloom_image.get_rect(bottomleft=( (WIDTH / 4) -155, HEIGHT-15))  # 宝箱を画面の下部に配置
    bloom2_rect = bloom2_image.get_rect(bottomleft=( (WIDTH / 4) -105, HEIGHT-15))  # 宝箱を画面の下部に配置

    screen.fill((0, 0, 0))  # 背景を黒に設定
    screen.blit(box_image, box_rect.topleft)
    screen.blit(bloom2_image, bloom2_rect.topleft)

    coin_count_text = font.render(f"coin: {len(coins)}", True, (255, 255, 255))  # 白色でコインの数を描画
    screen.blit(coin_count_text, (10, 10))  # 画面の左上にテキストを描画

    pygame.display.flip()

    pygame.time.delay(1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))  # 背景を黒に設定
        screen.blit(box2_image, box_rect.topleft)
        screen.blit(bloom_image, bloom_rect.topleft)
        
        if len(coins) < count:  # コインを生成
            coins.append(Coin(box_rect.centerx, box_rect.top+30))

        all_coins_landed = True
        for coin in coins:
            coin.move()
            coin.draw()
            if coin.y_speed != 0:  # まだ落下中のコインがあるかチェック
                all_coins_landed = False

        # コインの数を表示
        coin_count_text = font.render(f"coin: {len(coins)}", True, (255, 255, 255))  # 白色でコインの数を描画
        screen.blit(coin_count_text, (10, 10))  # 画面の左上にテキストを描画

        pygame.display.flip()
        clock.tick(60)

        if all_coins_landed:  # 全てのコインが地面に落ちたら1秒待って終了
            pygame.time.delay(1000)
            break

    pygame.quit()



