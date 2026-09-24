import pygame
import sys
from pygame.locals import *

#グローバル変数の初期化
class g:
    sw_blue = 0 #OFF
    sw_red = 0 #OFF
    sound_ok = False

#
# ゲームの初期化
#
def init_game():
    pygame.init()
    global screen, clock
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()


    g.little_person = prepare_sprite('img/横.png', 1/3, (100, 315))
    g.little_person_happy = prepare_sprite('img/喜ぶ.png', 1/3, (100, 315))
    g.treasure_chest = prepare_sprite('img/宝箱.png', 1/3, (-100, 0))  # 初期位置は画面外
    g.switch_blue = prepare_sprite('img/off_青.png', 1/3, (470, 400))
    g.switch_red = prepare_sprite('img/off_赤.png', 1/3, (350, 400))
    g.switch_blue_on = prepare_sprite('img/on_青.png', 1/3, (470, 405))
    g.switch_red_on = prepare_sprite('img/on_赤.png', 1/3, (350, 405))

    # ウインドウタイトルを設定
    icon_image = pygame.image.load("img/off_赤.png").convert_alpha()
    pygame.display.set_icon(icon_image)
    pygame.display.set_caption('課題1：条件分岐その1')


    try:
        pygame.mixer.init()
        g.sound_ok = True
    except Exception as e:
        print(f"サウンド初期化エラーが発生しました: {e}")
        g.sound_ok = False

    if g.sound_ok:
        g.falling_sound = pygame.mixer.Sound('sound/落ちる.mp3')
        g.get_sound = pygame.mixer.Sound('sound/当たり.mp3')



#
# 画像の読み込みとスケール調整
#
def load_and_scale_image(image_path, scale):
    image = pygame.image.load(image_path)
    if scale != 1:
        size = round(image.get_width() * scale), round(image.get_height() * scale)
        image = pygame.transform.scale(image, size)
    return image

#
# スプライトの準備
#
def prepare_sprite(image, scale, init_pos):
    sprite = pygame.sprite.Sprite()
    sprite.image = load_and_scale_image(image, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = init_pos
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite
 
#
# ゲームのメインループ
#
def game_loop():
    g.sw_blue = 0 #OFF
    g.sw_red = 0 #OFF
    click_flag = False

    while not click_flag:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, 425, 640, 15))  # 緑色部分
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(0, 440, 640, 30))  # 茶色部分
 
        screen.blit(g.little_person.image, g.little_person.rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if g.switch_blue.rect.collidepoint(event.pos) and not g.sw_blue == 1:
                    g.sw_blue = 1 #ON
                    click_flag = True
                    
                elif g.switch_red.rect.collidepoint(event.pos) and not g.sw_red == 1:
                    g.sw_red = 1 #ON
                    click_flag = True                  
        if g.sw_blue == 0:       
            screen.blit(g.switch_blue.image, g.switch_blue.rect)
        else:
            screen.blit(g.switch_blue_on.image, g.switch_blue_on.rect)
        if g.sw_red == 0:      
            screen.blit(g.switch_red.image, g.switch_red.rect)
        else:
            screen.blit(g.switch_red_on.image, g.switch_red_on.rect)
        pygame.display.update()
        clock.tick(30)  # FPSを30に設定

def wait_click():
    init_game()
    game_loop()

def fall_kobito():

    end_flag = False

    if g.sound_ok:
        g.falling_sound.play()


    while not end_flag:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, 425, 25, 15))  # 緑色部分(左)
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(0, 440, 25, 30))  # 茶色部分(左)

        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(175, 425, 465, 15))  # 緑色部分(右)
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(175, 440, 465, 30))  # 茶色部分(右)


        if g.sw_blue == 0:       
            screen.blit(g.switch_blue.image, g.switch_blue.rect)
        else:
            screen.blit(g.switch_blue_on.image, g.switch_blue_on.rect)
        if g.sw_red == 0:      
            screen.blit(g.switch_red.image, g.switch_red.rect)
        else:
            screen.blit(g.switch_red_on.image, g.switch_red_on.rect)

        if g.little_person.rect.y < 600:  # 小人を落下させる
            g.little_person.rect.y += 10
            screen.blit(g.little_person.image, g.little_person.rect)

            if  g.little_person.rect.y > 600:
                end_flag = True


        if end_flag:
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(30)  # FPSを30に設定

def get_chest():

    if g.sound_ok:
        g.get_sound.play()

    g.treasure_chest.rect.center = (220, 0)  # 宝箱の落下開始位置

    end_flag = False

    while not end_flag:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, 425, 640, 15))  # 緑色部分
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(0, 440, 640, 30))  # 茶色部分

        if g.sw_blue == 0:       
            screen.blit(g.switch_blue.image, g.switch_blue.rect)
        else:
            screen.blit(g.switch_blue_on.image, g.switch_blue_on.rect)
        if g.sw_red == 0:      
            screen.blit(g.switch_red.image, g.switch_red.rect)
        else:
            screen.blit(g.switch_red_on.image, g.switch_red_on.rect)
    


        if g.treasure_chest.rect.y < 340:
            g.treasure_chest.rect.y += 30  # 宝箱を落下させる
            screen.blit(g.treasure_chest.image, g.treasure_chest.rect)
            screen.blit(g.little_person_happy.image, g.little_person_happy.rect)
            
            if g.treasure_chest.rect.y > 340:
                end_flag = True


        if end_flag:
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()
        clock.tick(30)  # FPSを30に設定


def test():
    while True:
        screen.fill((0, 0, 0))        
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, 425, 640, 15))  # 緑色部分
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(0, 440, 640, 30))  # 茶色部分

        screen.blit(g.little_person.image, g.little_person.rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                if g.switch_blue.rect.collidepoint(event.pos) and not g.sw_blue == 1:
                    g.sw_blue = 1 #ON
                    g.sw_red = 0  #OFF
                    
                elif g.switch_red.rect.collidepoint(event.pos) and not g.sw_red == 1:
                    g.sw_blue = 0 #OFF
                    g.sw_red = 1 #ON

        if g.sw_blue == 0:       
            screen.blit(g.switch_blue.image, g.switch_blue.rect)
        else:
            screen.blit(g.switch_blue_on.image, g.switch_blue_on.rect)
        if g.sw_red == 0:      
            screen.blit(g.switch_red.image, g.switch_red.rect)
        else:
            screen.blit(g.switch_red_on.image, g.switch_red_on.rect)

        pygame.display.update()
        clock.tick(30)  # FPSを30に設定
