import pygame

# pygameの初期化
pygame.init()

def move_sprite(keys, x, y, speed):
    #✅課題1　この下からプログラムを作ります
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= speed

    #✅プログラミングチャレンジ1
    if keys[pygame.K_w] and keys[pygame.K_a] and keys[pygame.K_s] and keys[pygame.K_d]:
        x = 400
        y = 300

    return x, y

if __name__ == "__main__":
    import kadai_parts
    kadai_parts.run_game(pygame)
