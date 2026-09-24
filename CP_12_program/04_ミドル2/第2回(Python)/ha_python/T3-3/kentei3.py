# 商品は貰える？
import random

dice1 = random.randint(1, 6)
dice2 = random.randint(1, 6)
print(dice1, dice2)
if dice1 ?? dice2 ?? dice1+dice2 ?? 8:
    print("賞品をゲット！")
else:
    print("賞品はもらえません。")