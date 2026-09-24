import pygame
import sys
import random
import math

def kyori_hantei1(kyori):
    gameover = 0
    #✅プログラミングチャレンジ1-1　この下からプログラムを作ります
    # 距離（kyori）が40より小さい時にgameoverを1にする


    return gameover

def kyori_hantei2(kyori):
    hantai = 0
    #✅プログラミングチャレンジ1-2　この下からプログラムを作ります
    # 距離（kyori）が100以下の時にhantaiを1にする


    return hantai

def kyori_hantei3(kyori):
    gameclear = 0
    #✅oプログラミングチャレンジ1-3　この下からプログラムを作ります
     # 距離（kyori）が30より小さい時にgameclearを1にする


    return gameclear

# Pygameの初期化
pygame.init()

# 画面の設定
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont("meiryo", 64)
font2 = pygame.font.SysFont("meiryo", 28)

# 色の設定
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
light_blue = (173, 216, 230)
pink = (255, 192, 203)
black = (0, 0, 0)
gold = (255, 215, 0)

# 進む方向
to_right = True
to_down = True

# 方眼紙の設定
grid_size = 50  # 方眼紙のマスの大きさ

# 物体の初期位置
object1_pos = [width // 2, height // 2]
object2_pos = [50, 50]
#object2_pos = [random.randint(0, width), random.randint(0, height)]


# 方眼紙の描画関数
def draw_grid():
    for x in range(0, width, grid_size):
        pygame.draw.line(screen, pink if x % (grid_size * 5) == 0 else light_blue, (x, 0), (x, height))
    for y in range(0, height, grid_size):
        pygame.draw.line(screen, pink if y % (grid_size * 5) == 0 else light_blue, (0, y), (width, y))


def update_and_eventchk():
    clock = pygame.time.Clock()
    pygame.display.update()
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# 星を描く
def draw_star(surface, color, center, outer_radius, inner_radius, points):
    angle = math.pi / points
    point_list = []
    for i in range(points * 2):
        r = outer_radius if i % 2 == 0 else inner_radius
        x = center[0] + int(math.cos(i * angle) * r)
        y = center[1] + int(math.sin(i * angle) * r)
        point_list.append((x, y))
    pygame.draw.polygon(surface, color, point_list)

# ゲームオーバー
def game_over():
    while True:
        text = font.render("GAME OVER!", True, black)
        # テキストの描画
        text_rect = text.get_rect(center=(width / 2, height / 2))
        screen.blit(text, text_rect)

        update_and_eventchk()

# ゲームクリアー
def game_clear():
    while True:
        text = font.render("GAME CLEAR!", True, red)
        # テキストの描画
        text_rect = text.get_rect(center=(width / 2, height / 2))
        screen.blit(text, text_rect)

        update_and_eventchk()


# ゴールを描く
def draw_goal():
    # 四角形を描く
    pygame.draw.rect(screen, black, [500, 50, 100, 100], 2)  # 外枠の四角形
    # テキストを描く
    text = font2.render("ゴール", True, red)
    text_rect = text.get_rect(center=(550, 100))
    screen.blit(text, text_rect)

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 物体1をキー操作で移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        object1_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        object1_pos[0] += 5
    if keys[pygame.K_UP]:
        object1_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        object1_pos[1] += 5

    # 方眼紙を背景として描画
    screen.fill(white)
    draw_grid()
    draw_goal()
    # 物体の描画
    pygame.draw.circle(screen, blue, object1_pos, 20)
    draw_star(screen, gold, object2_pos, 30, 15, 5)

    distance = ((object1_pos[0] - object2_pos[0])**2 + (object1_pos[1] - object2_pos[1])**2)**0.5
    over = kyori_hantei1(distance)
    if over == 1:
        game_over()
    hantai = kyori_hantei2(distance)
    if hantai == 1:
        if object1_pos[0] > object2_pos[0]:
            to_right = False
        else:
            to_right = True
        if object1_pos[1] > object2_pos[1]:
            to_down = False
        else:
            to_down = True
    kyori = ((550 - object2_pos[0])**2 + (100 - object2_pos[1])**2)**0.5
    clear = kyori_hantei3(kyori)
    if clear == 1:
        game_clear()

    # 画面を更新
    pygame.display.flip()

    # 物体2の移動
    if to_right:
        object2_pos[0] += 1
        if object2_pos[0] > 620:
            game_over()
    else:
        object2_pos[0] -= 1
        if object2_pos[0] < 20:
            game_over()
    if to_down:
        object2_pos[1] += 1
        if object2_pos[1] > 460:
            game_over()
    else:
        object2_pos[1] -= 1
        if object2_pos[1] < 20:
            game_over()
    update_and_eventchk()

