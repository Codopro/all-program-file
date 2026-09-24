#
# おにぎりの具材に応じたメッセージを表示する
#
def get_onigiri_message(guzai):
    message = ""

    #✅課題1　この下からプログラムを作ります
    if guzai == "しゃけ":
        message = "おいしい！"

    #✅プログラミングチャレンジ1
    # さけ、うめ、ツナマヨに対応する
    match guzai:
        case "しゃけ":
            message = "おいしい！"
        case "うめ":
            message = "すっぱーい！"
        case "ツナマヨ":
            message = "まろやか～"

    return message


if __name__ == "__main__":
    import kadai_parts
    kadai_parts.run_game()
