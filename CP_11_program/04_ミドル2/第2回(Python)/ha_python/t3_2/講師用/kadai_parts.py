import pygame
import sys
from kadai1 import get_onigiri_message  # onigiri_message.py から関数をインポート

# 画像のサイズ設定処理
# （画像をロードし、サイズを取得後、サイズ変更する）
# load_and_scale_image(画像パス, 変更倍率):
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)

def run_game():
    # Pygameの初期化
    pygame.init()

    # 画面サイズ設定
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("おにぎりの具")

    # フォント設定
    font = pygame.font.SysFont("meiryo", 20)

    # 色の設定
    WHITE = (255, 255, 255)
    GLAY  = (0xe6, 0xf0, 0xff)
    BLACK = (0, 0, 0)

    # 各おにぎりの画像読み込み
    onigiri_sake = load_and_scale_image("img\onigiri_sake.png", 2/3)
    onigiri_ume = load_and_scale_image("img\onigiri_ume.png", 2/3)
    onigiri_tunamayo = load_and_scale_image("img\onigiri_tunamayo.png", 2/3)

    # 画像の位置
    onigiri_sake_rect = onigiri_sake.get_rect(topleft=(20, 200))
    onigiri_ume_rect = onigiri_ume.get_rect(topleft=(200, 20))
    onigiri_tunamayo_rect = onigiri_tunamayo.get_rect(topleft=(360, 200))

    # メッセージの初期化
    message = ""
    bubble_visible = False

    def draw_bubble(text, pos):
        """吹き出しを描画する関数"""
        bubble_rect = pygame.Rect(pos[0] - 10, pos[1] - 40, 200, 50)
        pygame.draw.rect(screen, WHITE, bubble_rect)
        pygame.draw.rect(screen, BLACK, bubble_rect, 2)  # 吹き出しの枠
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (pos[0], pos[1] - 30))

    # メインループ
    running = True
    while running:
        # イベントの確認
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # 鮭おにぎりがクリックされた場合
                if onigiri_sake_rect.collidepoint(mouse_pos):
                    message = get_onigiri_message("しゃけ")  # メッセージ取得
                    bubble_visible = True
                    bubble_pos = mouse_pos

                # 梅干しおにぎりがクリックされた場合
                elif onigiri_ume_rect.collidepoint(mouse_pos):
                    message = get_onigiri_message("うめ")  # メッセージ取得
                    bubble_visible = True
                    bubble_pos = mouse_pos

                # ツナマヨおにぎりがクリックされた場合
                elif onigiri_tunamayo_rect.collidepoint(mouse_pos):
                    message = get_onigiri_message("ツナマヨ")  # メッセージ取得
                    bubble_visible = True
                    bubble_pos = mouse_pos

        # 画面を灰色で塗りつぶす
        screen.fill(GLAY)

        # おにぎりを描画
        screen.blit(onigiri_sake, onigiri_sake_rect)
        screen.blit(onigiri_ume, onigiri_ume_rect)
        screen.blit(onigiri_tunamayo, onigiri_tunamayo_rect)

        # 吹き出しを表示
        if bubble_visible:
            draw_bubble(message, bubble_pos)

        # 画面更新
        pygame.display.flip()

    # Pygameの終了
    pygame.quit()
    sys.exit()
