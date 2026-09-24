from kadai_parts import *

print("こんにちは！")

#✅課題1　この下からプログラムを作ります
def print_red(str):
    print(f"{RED}{str}{RESET}")
    print(f"{BLUE}{str}{RESET}")
    print(f"{GREEN}{str}{RESET}")

print_red("はい、こんにちは！")
