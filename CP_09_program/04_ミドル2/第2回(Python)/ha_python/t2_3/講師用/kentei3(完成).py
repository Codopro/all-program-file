# さいころをふって、出た数を表示する
import random

def roll_dice():
    return random.randint(1, 6)

# 使用例
result = roll_dice()
print("サイコロの目は:", result)