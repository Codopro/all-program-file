import random

mondai = 0
while True:
    mondai += 1
    if mondai > 10:
        print("10問正解！がんばったね。")
        break
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    answer = input(str(num1) + " x " + str(num2) + " = ")
    answer = int(answer)
    
    if answer == num1 * num2:
        print("正解です！")
    else:
        print("ざんねん。。。")
        break
