# パスワードを3回間違えたらロックされる
password = "1234"
attempts = 0
while True:
    pin = input("暗証番号を入力してください: ")
    if pin == password:
        print("認証成功！")
        break
    attempts += 1
    if attempts >= 3:
        ????? ????:
            print("ロックされました！")
