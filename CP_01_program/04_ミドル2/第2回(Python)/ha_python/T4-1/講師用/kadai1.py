import pygame
import random

# pygameの初期化
pygame.init()

def kadai1(draw_neko, draw_hukidashi):
    #✅課題1　この下からプログラムを作ります
    for i in range(10):
        x, y = draw_neko()

        #✅プログラミングチャレンジ1
        draw_hukidashi(x, y, i)

if __name__ == "__main__":
    import kadai_parts
    kadai_parts.run_game(pygame)
