# 恋愛攻略書（有料PDF）ビルダー

犬版「16わんこ恋愛診断」の恋愛攻略書（全32ページ）と同一構成・同一デザインで、
猫版のプレミアムPDFを生成します。

## 使い方
```bash
pip install pillow playwright pymupdf
python3 build_guide.py ENFJ      # → guide_enfj.html
python3 topdf.py enfj            # → enfj_love_guide_cat.pdf
```

## 構成（全32ページ・7部構成）
- P1 表紙／P2 この本の使い方／P3 もくじ
- PART I 基礎編（P4-12）：恋愛人格・5段階・3つの罠・全16相性マップ・TOP5・要注意タイプ・LINE攻略・ケンカ倦怠期・結婚観
- P13 PART II 扉
- PART II 理論編（P14-21）：愛着スタイル・相手別接し方・愛の言語・あるある30・落とし穴・三角理論・ビッグファイブ・認知機能
- WORK（P22-24）：理論で自己分析・理想と現実の棚卸し・本音を伝える練習
- APPENDIX（P25-31）：仲直りフローチャート・復縁という選択／見極め／テクニック／タイプ別／SNS／SNS実践
- P32 裏表紙

## データ整合
- 相性スコアは index.html の `compatScore()` をそのまま実装（サイト表示と完全一致）
- 恋愛ステータス（★）は index.html の `PARAM` と一致
- 猫種名・性格文は `LOC.json`（index.html の LOC から抽出）

## 他タイプへの展開
`build_guide.py` 内の `C = {...}` がタイプ固有の原稿。ここを差し替えれば他15タイプを生成できる。
`guide-drafts/_datasheet.md` と `compat-matrix.md` が正データ。
