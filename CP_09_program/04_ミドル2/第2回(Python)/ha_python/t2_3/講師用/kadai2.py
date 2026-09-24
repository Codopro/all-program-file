def print2(str):
    print(str)
    print(str)

print2("こんにちは")

# プログラミングチャレンジ２
# 文字の長さを表示する
def str_len(str):
    return len(str)

print(str_len("こんにちは"))

# 文字をゆっくりと表示する
import time

def slow_print(str):
    for char in str:
        print(char, end='', flush=True)
        time.sleep(1)
    print()

slow_print("こんにちは")