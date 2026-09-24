# 指定された数だけ★を表示する
def print_stars(kosuu):
    for i in range(kosuu):
        print('★ ', end='')
    print()  # 改行

print("今日はともだちとゲームをしてあそんだ！")
print_stars(10)