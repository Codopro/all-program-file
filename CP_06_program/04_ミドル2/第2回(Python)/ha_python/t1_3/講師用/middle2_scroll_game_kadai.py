#
# <ミドル２コース ７月号 スクロールゲーム>
# 課題ファイル
#

# partsファイル(パーツファイル)をインポート
from parts import *


def kadai2():
    pass
    # 解答
    count = 3
    draw_tc(count)
    count = count - 1
    draw_tc(count)
    count = count - 1
    draw_tc(count)

def kadai4():
    pass
    # 解答
    g.coin_num += 1

def kadai5():
    pass
    # 解答
    draw_hukidashi("コインを"+str(g.coin_num)+"枚とったよ！")
