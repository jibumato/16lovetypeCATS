#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成した恋愛トリセツPDFを自動検査する。

ENFJ版の点検で見つかった不具合が他タイプで再発しないよう、
これまで手で見つけた欠陥をすべて機械チェックに落としてある。
"""
import os
import re
import sys

import pymupdf

SP = "/tmp/claude-0/-home-user-16lovetypeCATS/ca9b5b1a-5375-5908-aa61-ec0aeb6a5928/scratchpad/"

# 丁寧語から外れる語尾（本文で使ってはいけないもの）
# 「〜ないように」等に誤爆しないよう、後続文字まで見て判定する
CASUAL = [r'だよ。', r'だよ<', r'なんだ。', r'ないよ(?![うに])', r'じゃん', r'してね。', r'しよう。',
          r'するよ。', r'あるよ。', r'くるよ。', r'なるよ。', r'いくよ。', r'見てるよ',
          r'らしい。', r'んだって', r'てるから', r'てるのに', r'じゃなくて', r'教えるよ',
          r'答えるよ', r'育ててね', r'見られるよ', r'ズレてると', r'されてるモデル']

# セリフ・文例は口語で当然なので、判定対象から外す
QUOTED = re.compile(r'[「『][^」』]{0,80}[」』]')


def strip_quotes(text):
    """会話例やテンプレ文（「」で囲まれた部分）を伏せ字にして本文だけ残す。"""
    return QUOTED.sub(lambda m: "〓" * len(m.group(0)), text)


# 展開されずに残ったテンプレート変数
TEMPLATE = r'\{[a-zA-Z_][\w\+\-\.\[\]\'\"]*\}|\{\{|\}\}'


def check(path):
    name = os.path.basename(path)
    d = pymupdf.open(path)
    PW, PH = d[0].rect.width, d[0].rect.height
    issues = []

    if d.page_count != 32:
        issues.append(f"ページ数が{d.page_count}（32であるべき）")
    if abs(PW - 595) > 2 or abs(PH - 842) > 2:
        issues.append(f"判型が{PW:.0f}x{PH:.0f}pt（A4であるべき）")

    text_all = []
    for i in range(d.page_count):
        pg = d[i]
        t = pg.get_text()
        text_all.append(t)

        # 1) 用紙外へのはみ出し
        out = [b for b in pg.get_text("blocks")
               if b[3] > PH - 6 or b[2] > PW - 6 or b[0] < 6 or b[1] < 2]
        if out:
            issues.append(f"p{i+1}: 用紙外の要素 {len(out)}件（例: {out[0][4][:20].strip()!r}）")

    joined = "".join(text_all)

    # 2) 丁寧語の崩れ
    for pat in CASUAL:
        for i, t in enumerate(text_all):
            m = re.search(pat, strip_quotes(t.replace("\n", "")))
            if m:
                ctx = t.replace("\n", "")[max(0, m.start() - 20):m.end() + 2]
                issues.append(f"p{i+1}: 丁寧語の崩れ …{ctx}")
                break

    # 3) 未展開のテンプレート変数
    for i, t in enumerate(text_all):
        for m in re.finditer(TEMPLATE, t):
            issues.append(f"p{i+1}: 未展開のテンプレート {m.group(0)!r}")
            break

    # 4) 同じ語の連続重複（「心理学者心理学者」のような事故）
    for i, t in enumerate(text_all):
        flat = t.replace("\n", "")
        for m in re.finditer(r'([一-龥ァ-ヶー]{3,6})\1', flat):
            issues.append(f"p{i+1}: 語の重複 {m.group(1)!r}")
            break

    # 5) 犬版の名残
    for w in ("わんこ", "ゴールデン", "16lovetypedogs", "犬"):
        if w in joined:
            issues.append(f"犬版の名残 {w!r}")

    # 6) 丸ゴシックが埋め込まれているか
    fonts = {f[3] for i in range(d.page_count) for f in d[i].get_fonts()}
    if not any("Rounded" in f for f in fonts):
        issues.append("丸ゴシック(M PLUS Rounded 1c)が埋め込まれていない")

    d.close()
    return name, issues


def main():
    targets = sys.argv[1:] or sorted(
        os.path.join(SP, f) for f in os.listdir(SP) if f.endswith("_love_guide_cat.pdf"))
    ng = 0
    for path in targets:
        name, issues = check(path)
        if issues:
            ng += 1
            print(f"❌ {name}")
            for x in issues[:12]:
                print("     ", x)
            if len(issues) > 12:
                print(f"      … ほか{len(issues)-12}件")
        else:
            print(f"✔ {name}  問題なし")
    print(f"\n検査 {len(targets)}件 / 問題あり {ng}件")
    return 1 if ng else 0


if __name__ == "__main__":
    sys.exit(main())
