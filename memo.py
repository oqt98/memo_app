from colorama import init, Fore, Style
init(autoreset=True)

import json
import os
from datetime import datetime

MEMO_FILE = "memo.json"

# ファイルがなければ初期化
if not os.path.exists(MEMO_FILE):
    with open(MEMO_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

# メモを読み込む
def load_memos():
    with open(MEMO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# メモを保存する
def save_memos(memos):
    with open(MEMO_FILE, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)

# メモを追加する
def add_memo():
    memos = load_memos()

    # 既存カテゴリを一覧表示
    categories = sorted(set(m["category"] for m in memos))
    print("\n📚 既存カテゴリ一覧：")
    for i, cat in enumerate(categories, 1):
        print(f"{i}: {cat}")
    print(f"{len(categories)+1}: 新しいカテゴリを作成")
    print("b: 戻る")

    choice = input("カテゴリを選んでください（番号）：")
    if choice.lower() == "b":
        print("↩️ メニューに戻ります。")
        return

    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(categories):
            category = categories[idx - 1]
        elif idx == len(categories) + 1:
            category = input("🆕 新しいカテゴリ名を入力してください：")
        else:
            print("❌ 無効な選択です。")
            return
    else:
        print("❌ 数字で選んでください。")
        return

    content = input("📝 メモ内容を入力：")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_id = memos[-1]["id"] + 1 if memos else 1

    memo = {
        "id": new_id,
        "category": category,
        "content": content,
        "created_at": created_at
    }

    memos.append(memo)
    save_memos(memos)
    print("✅ メモを追加しました！")

    
# メモを表示する（←この関数が抜けてる！）
def show_memos():
    memos = load_memos()
    if not memos:
        print(Fore.YELLOW + "📭 メモがありません。")
        return

    print(Fore.CYAN + Style.BRIGHT + "📖 登録されたメモ一覧：\n")

    for memo in memos:
        print(Fore.GREEN + f"📝 [{memo['id']}] {memo['category']}（{memo['created_at']}）")
        print(Fore.WHITE + Style.BRIGHT + memo["content"])
        print(Fore.MAGENTA + "-" * 40)



def delete_memo():
    memos = load_memos()
    if not memos:
        print(Fore.YELLOW + "📭 メモがありません。削除できません。")
        return

    show_memos()
    try:
        delete_id = int(input("🗑 削除したいメモのIDを入力してください："))
    except ValueError:
        print(Fore.RED + "❌ 数字で入力してください。")
        return

    updated_memos = [memo for memo in memos if memo["id"] != delete_id]

    if len(updated_memos) == len(memos):
        print(Fore.RED + f"❌ ID {delete_id} のメモは見つかりませんでした。")
        return

    save_memos(updated_memos)
    print(Fore.GREEN + f"🗑 ID {delete_id} のメモを削除しました！")


def filter_by_category():
    memos = load_memos()
    if not memos:
        print(Fore.YELLOW + "📭 メモがありません。")
        return

    category = input("🔍 表示したいカテゴリを入力してください：")

    filtered = [memo for memo in memos if memo["category"] == category]

    if not filtered:
        print(Fore.RED + f"🔍「{category}」に該当するメモはありません。")
        return

    print(Fore.CYAN + f"\n📂 カテゴリ「{category}」のメモ一覧：\n")
    for memo in filtered:
        print(Fore.GREEN + Style.BRIGHT + f"📝 [{memo['id']}]（{memo['created_at']}）")
        print(Fore.WHITE + memo["content"])
        print(Fore.MAGENTA + "-" * 40)

def list_categories():
    memos = load_memos()
    categories = sorted(set(memo["category"] for memo in memos))
    return categories

def filter_by_category_with_choice():
    memos = load_memos()
    if not memos:
        print("📭 メモがありません。")
        return

    # カテゴリ一覧を取得
    categories = sorted(set(memo["category"] for memo in memos))
    print("\n📂 表示カテゴリを選んでください：")
    for i, cat in enumerate(categories, 1):
        print(f"{i}: {cat}")
    print("b: 戻る")  # ← 追加！

    choice = input("番号を選んでください：")
    if choice.lower() == "b":
        print("↩️ メニューに戻ります。")
        return

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(categories):
        print("❌ 無効な選択です。")
        return

    selected_category = categories[int(choice) - 1]
    filtered = [memo for memo in memos if memo["category"] == selected_category]

    print(f"\n📂 カテゴリ「{selected_category}」のメモ一覧：\n")
    for memo in filtered:
        print(f"📝 [{memo['id']}]（{memo['created_at']}）")
        print(memo["content"])
        print("-" * 40)


def sort_memos():
    memos = load_memos()
    if not memos:
        print("📭 メモがありません。")
        return

    print("\n📊 並び替えの方法を選んでください：")
    print("1: 日時（新しい順）")
    print("2: 日時（古い順）")
    print("3: カテゴリ順（A→Z）")
    print("4: ID順（昇順）")
    print("5: ID順（降順）")
    print("0: メニューに戻る")

    choice = input("番号を入力：")

    if choice == "1":
        sorted_memos = sorted(memos, key=lambda x: x["created_at"], reverse=True)
    elif choice == "2":
        sorted_memos = sorted(memos, key=lambda x: x["created_at"])
    elif choice == "3":
        sorted_memos = sorted(memos, key=lambda x: x["category"])
    elif choice == "4":
        sorted_memos = sorted(memos, key=lambda x: x["id"])
    elif choice == "5":
        sorted_memos = sorted(memos, key=lambda x: x["id"], reverse=True)
    elif choice == "0":
        return
    else:
        print("❌ 無効な入力です。0〜5を選んでください。")
        return

    # 表示処理（show_memosをコピーして再利用）
    print(Fore.CYAN + Style.BRIGHT + "\n📖 並び替え後のメモ一覧：\n")
    for memo in sorted_memos:
        print(Fore.GREEN + f"📝 [{memo['id']}] {memo['category']}（{memo['created_at']}）")
        print(Fore.WHITE + Style.BRIGHT + memo["content"])
        print(Fore.MAGENTA + "-" * 40)





# ↓↓↓↓↓↓ 必ずこの下に main（メニュー）を書く！ ↓↓↓↓↓↓

if __name__ == "__main__":
    while True:
        print(Fore.BLUE + Style.BRIGHT + "\n==== メモ帳アプリ ====")
        print(Fore.CYAN + "1: メモを追加")
        print("2: メモを表示")
        print("3: メモを削除")
        print("4: カテゴリで表示（手入力）")
        print("5: カテゴリで表示（選択）")  # ← 追加
        print("6: 並び替えて表示")  # メニュー表示に追加
        print("7: 終了")

        choice = input("番号を選んでください：")

        if choice == "1":
            add_memo()
        elif choice == "2":
            show_memos()
        elif choice == "3":
            delete_memo()
        elif choice == "4":
            filter_by_category()
        elif choice == "5":
            filter_by_category_with_choice()
        elif choice == "6":
            sort_memos()
        elif choice == "7":
            print(Fore.BLUE + "👋 またね！")
            break
        else:
            print(Fore.RED + "❌ 無効な入力です。1〜7を選んでください。")




