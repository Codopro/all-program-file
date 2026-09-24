from parts import *

#
# アプリランチャー
# 授業用フォルダを更新すると、アイコンが増えます
#
def launcher():
    clock = pygame.time.Clock()
    white = pygame.Color('white')

    while True:
        g.screen.fill(white)
        g.screen.blit(g.smartphone, (200,10))
        for i in range(5):
            for j in range(3):
                if not (i == 4 and j != 0):
                    g.screen.blit(g.icon[j + i * 3], (ICON_BASE_X + j * ICON_DIFF_X, ICON_BASE_Y + i * ICON_DIFF_Y))
                    if i == 0 or i == 1:
                        text = g.font.render(str(4 + j + i * 3) + "月", True, white)
                        g.screen.blit(text, [ICON_BASE_X + 14 + j * ICON_DIFF_X, ICON_BASE_Y + TEXT_OFFSET_Y + i * ICON_DIFF_Y])
                    elif i == 2:
                        text = g.font.render(str(4 + j + i * 3) + "月", True, white)
                        g.screen.blit(text, [ICON_BASE_X + 9 + j * ICON_DIFF_X, ICON_BASE_Y + TEXT_OFFSET_Y + i * ICON_DIFF_Y])
                    elif i == 3:
                        text = g.font.render(str(j + 1) + "月", True, white)
                        g.screen.blit(text, [ICON_BASE_X + 14 + j * ICON_DIFF_X, ICON_BASE_Y + TEXT_OFFSET_Y + i * ICON_DIFF_Y])
                    elif i == 4:
                        text = g.font.render("スタートアップ", True, white)
                        g.screen.blit(text, [ICON_BASE_X - 10 + j * ICON_DIFF_X, ICON_BASE_Y + TEXT_OFFSET_Y + i * ICON_DIFF_Y])

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#
# メイン
#
def main():
    parts_init()
    launcher()

if __name__ == '__main__':
    main()
