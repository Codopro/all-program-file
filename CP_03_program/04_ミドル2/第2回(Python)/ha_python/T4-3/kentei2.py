# 数あてゲーム
import random
secret = random.randint(1, 10)  # 1から10の間の秘密の数字を決定
while True:
    guess = int(input("1から10の数字を当ててください: "))
    if guess == secret:
        print("正解！おめでとう！")
        ?????
    print("違います！もう一度！")
