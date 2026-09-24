#
# <ミドル２コース スタートアップ課題　ストーリー作成に挑戦する>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# ✅キャラクター用の関数（かんすう）
#
def draw_character():
    #🔰STEP3の課題はここから下のコードを変更します
    draw_robo1(5,30)
    draw_robo2(0,30)
    draw_robo3(12,30)

#
# ✅セリフ用の関数（かんすう）
# 
def draw_serifu():
    #🔰STEP3の課題はここから下のコードを変更します
    draw_moji("私の名前はサポタです！", 0, 2)
    draw_moji("他のコースの友達に会いに行きます。", 2, 4)
    draw_moji("こちらのロボットは「けいさんできるんジャー」です。", 6,9)
    draw_moji("最後に、「たんさクン」です。", 13, 14)
    draw_moji("歩いているのでゆっくりです。", 14, 16)
    draw_moji("これからの私とハカセのこと、よろしくお願いします！", 18,30)

#
# start関数（スタートかんすう）
#
def start():
    #初期化（しょきか）
    parts_init()

    #カウント・BGM開始
    g.tick_start = pygame.time.get_ticks()
    play_bgm_sound()

    while True:
        # 背景を出す
        draw_haikei()

        # セリフを出す
        draw_serifu()

        #キャラクターを出す
        draw_character()
         
        #経過時間を計算する
        g.tick=pygame.time.get_ticks() - g.tick_start #ミリ秒で取得
        g.tick= round(g.tick/1000,1) #秒に変換し、小数点第一まで表示

        # 時間を表示する
        text = g.font.render(str(g.tick)+"秒", True, (0,0,0))
        g.screen.blit(text, [10, 10])
            
        #画面更新処理
        pygame.time.delay(1)
        pygame.display.update()

        #終わりのタイミング(30秒経過)
        if (g.tick > 30):
            #1秒音楽フェードアウト
            g.bgm.fadeout(1000)
            pygame.time.wait(1000)
            #プログラム終了
            pygame.quit()
            sys.exit()
            
        #ユーザー操作をチェック
        for event in pygame.event.get():
            #プログラム終了させた時（ウィンドウの×ボタン）
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
#
# 🚩ここからメインプログラムを開始しています
#
start()
