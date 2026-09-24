from kadai2_parts import *

# ✅課題3 下のプログラムのxxxを変更して動かせるようにしよう！
kosuu = 1
while kosuu < 11:
    kinoko()  # キノコを一つ降らせる
    kosuu = kosuu + 1

# 🔰プログラムを終了する前に2秒間(2000ミリ秒)待機させる
pygame.time.wait(2000)