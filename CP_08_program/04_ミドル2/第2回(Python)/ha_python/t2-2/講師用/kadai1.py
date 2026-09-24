import pygame
import math

def kyori_hantei(kyori):
    stop = 0
    #✅課題1　この下からプログラムを作ります
    if kyori < 100:
        stop = 1
    return stop

# Pygameの初期化
pygame.init()

# 画面の設定
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# 色の設定
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
light_blue = (173, 216, 230)
pink = (255, 192, 203)
gold = (255, 215, 0)

# 方眼紙の設定
grid_size = 50  # 方眼紙のマスの大きさ

# 物体の初期位置
object1_pos = [width // 2, height // 2]
object2_pos = [0, 0]

# 方眼紙の描画関数
def draw_grid():
    for x in range(0, width, grid_size):
        pygame.draw.line(screen, pink if x % (grid_size * 5) == 0 else light_blue, (x, 0), (x, height))
    for y in range(0, height, grid_size):
        pygame.draw.line(screen, pink if y % (grid_size * 5) == 0 else light_blue, (0, y), (width, y))

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

def update_and_eventchk():
    clock = pygame.time.Clock()
    pygame.display.update()
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

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

    distance = ((object1_pos[0] - object2_pos[0])**2 + (object1_pos[1] - object2_pos[1])**2)**0.5
    stop = kyori_hantei(distance)
    if stop == 1:
        color = red
    else:
        color = blue

    # 物体の描画
    draw_star(screen, gold, object2_pos, 30, 15, 5)
    pygame.draw.circle(screen, color, object1_pos, 20)

    # 画面を更新
    pygame.display.flip()

    # 物体2の移動
    if color == blue:
        object2_pos[0] += 1
        if object2_pos[0] > 640:
            object2_pos[0] = 0
        object2_pos[1] += 1
        if object2_pos[1] > 480:
            object2_pos[1] = 0
    update_and_eventchk()

