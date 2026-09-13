# 埋め込みフォント

`M PLUS Rounded 1c`（SIL Open Font License 1.1）を、本文で使う文字だけにサブセット化した woff2。

- 生成元：`https://fonts.gstatic.com/s/mplusrounded1c/` の各ウェイト TTF（400 / 700 / 800）
- サブセット：`fonttools` で `guide_*.html` の使用文字（約1,000字）に限定
- サイズ：3.4MB → 約150KB ／ ウェイト

## なぜ埋め込むのか
PDF生成に使う Playwright の Chromium はこの環境のプロキシを経由しないため、
`@import` での Google Fonts 取得が `ERR_CONNECTION_RESET` で失敗し、
IPAPGothic 等のシステムフォントで描画されてしまう。
data URI で埋め込むことでネットワークに依存せず、意図した丸ゴシックで出力される。

## 文字を追加したとき
他タイプで新しい文字が出る場合はサブセットを作り直す：

    python3 -c "import re;h=open('guide_xxxx.html',encoding='utf-8').read();b=re.sub(r'<style.*?</style>','',h,flags=re.S);b=re.sub(r'<[^>]+>',' ',b);open('subset_chars.txt','w',encoding='utf-8').write(''.join(sorted(set(c for c in b if c.strip() and ord(c)>31))))"
    python3 -c "
    from fontTools import subset
    t=open('subset_chars.txt',encoding='utf-8').read()
    for w in (400,700,800):
        subset.main([f'mpr-{w}.ttf',f'--text={t}','--flavor=woff2',f'--output-file=mpr-{w}.woff2','--no-hinting'])"
