#
# <ミドル２コース Python課題 ４月号 PAINT TO WIN GAME>
#

# partsファイル(パーツファイル)をインポート
from parts import *

#
# ✅タイトル画面処理
#
def draw_title():
    #タイトル背景を表示
    g.screen.blit(g.title, (0,0))
    
    # 🔰オープニング処理開始
    while g.mode == g.MODE_TITLE:    
    
        # 赤ブルームを最初に位置にする
        g.red_x = 100
        g.red_y = 300

        # ✅プログラミングチャレンジ2
        # タイトル画面で４回、赤ブルームが表示されるようにする
        
        kaisuu = 1
        while kaisuu < 9:
            red_stamp()
            g.red_x = g.red_x + 50
            wait_time(1)
            kaisuu = kaisuu + 1
        
        # 赤ブルームを消して１秒待つ動き
        g.screen.blit(g.title, (0,0)) # 赤ブルームの表示を消す
        update_and_eventchk() # 画面更新&キー操作チェック
        wait_time(1) # 1秒待つ（時間経過後のイベントチェックもあり)
    


#   
# 勝敗判定中の処理
#
def judge_winner():
    #音楽停止
    stop_bgm()

    #勝敗の判定
    while g.mode == g.MODE_JUDGE:
        reset_point() #ポイント初期化
        update_and_eventchk() # 画面更新&キー操作チェック

        # ✅プログラミングチャレンジ4
        # 勝敗判定を行う(y方向の繰り返し)
        y = 20

        while y < 480:
            # ✅プログラミングチャレンジ3
            # 勝敗判定を行う(x方向の繰り返し)
            x = 140
            while x < 490:
                judge_point(x, y)
                x = x + 20
            y = y + 20
        # ポイントを表示する
        draw_point()



#
# start関数（スタートかんすう）
#
def start():
    #初期化
    parts_init()

    # タイトル表示
    draw_title()
    
    # アイテム選択画面
    select_item()
    
    # ゲーム中
    play_game()
    
    # 勝敗判定
    judge_winner()


#
# 🚩ここからメインプログラムを開始しています
#
start()