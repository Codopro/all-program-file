import pygame
import sys

title = "☆～★～☆～★～☆～"
text = "はかせのぼうけん！"  # 表示したい文字列
display_text = ""

# pygameの初期化
pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("文字を１つずつ表示する")
font = pygame.font.SysFont("meiryo", 60)
text_index = 0
clock = pygame.time.Clock()

CHAR_INTERVAL = 500
next_char_time = pygame.time.get_ticks() + CHAR_INTERVAL
now = pygame.time.get_ticks()
running = True

while running:
    if text_index < len(text) and now >= next_char_time:
        #✅課題1　この下からプログラムを作ります
        display_text = text[text_index]
        text_index += 1
        #✅プログラミングチャレンジ1
#        display_text += text[text_index]
#        text_index += 1
        next_char_time = now + CHAR_INTERVAL

    screen.fill((0, 0, 0))

    text_surface = font.render(title, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2-100))
    screen.blit(text_surface, text_rect)

    text_surface = font.render(display_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text_surface, text_rect)

    text_surface = font.render(title, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2+100))
    screen.blit(text_surface, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
