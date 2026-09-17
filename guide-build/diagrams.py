# -*- coding: utf-8 -*-
"""恋愛トリセツPDF用 図解パーツ（印刷安全なインラインSVG）"""
import math

W, L, K, Y, G = "#e0559a", "#c9a0f0", "#2c1b3d", "#ffe27a", "#f0e6f6"
SUB = "#7d6f86"


def _poly(cx, cy, r, n, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + i * 360 / n)),
             cy + r * math.sin(math.radians(rot + i * 360 / n))) for i in range(n)]


def svg_radar(labels, vals, maxv=5, size=158):
    """5角形レーダーチャート（恋愛ステータス）"""
    cx = cy = size / 2
    R = size * 0.30
    n = len(labels)
    out = []
    for f in (0.25, 0.5, 0.75, 1.0):
        pts = " ".join("%.1f,%.1f" % p for p in _poly(cx, cy, R * f, n))
        out.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="1"/>' % (pts, G))
    for x, y in _poly(cx, cy, R, n):
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
                   % (cx, cy, x, y, G))
    dp = []
    for i, v in enumerate(vals):
        a = math.radians(-90 + i * 360 / n)
        dp.append((cx + R * (v / maxv) * math.cos(a), cy + R * (v / maxv) * math.sin(a)))
    out.append('<polygon points="%s" fill="%s" fill-opacity=".26" stroke="%s" stroke-width="2"/>'
               % (" ".join("%.1f,%.1f" % p for p in dp), W, W))
    for x, y in dp:
        out.append('<circle cx="%.1f" cy="%.1f" r="2.7" fill="%s" stroke="%s" stroke-width="1"/>' % (x, y, W, K))
    for i, (lb, v) in enumerate(zip(labels, vals)):
        a = math.radians(-90 + i * 360 / n)
        lx, ly = cx + (R + 19) * math.cos(a), cy + (R + 19) * math.sin(a)
        anc = "middle" if abs(math.cos(a)) < .4 else ("start" if math.cos(a) > 0 else "end")
        out.append('<text x="%.1f" y="%.1f" font-size="7.4" font-weight="700" fill="%s" text-anchor="%s">%s</text>'
                   % (lx, ly, K, anc, lb))
        out.append('<text x="%.1f" y="%.1f" font-size="8.2" font-weight="800" fill="%s" text-anchor="%s">%s</text>'
                   % (lx, ly + 9, W, anc, "★" * v))
    PAD = 40
    return ('<svg viewBox="%d %d %d %d" style="width:100%%;height:auto">%s</svg>'
            % (-PAD, -10, size + PAD * 2, size + 24, "".join(out)))


def svg_hbars(rows, maxv=100, h=14, unit=""):
    """横棒グラフ rows=[(ラベル, 値)] / [(ラベル, 値, 補足)]"""
    H = len(rows) * h + 4
    out = []
    for i, r in enumerate(rows):
        lb, v = r[0], r[1]
        sub = r[2] if len(r) > 2 else ""
        y = i * h + 3
        bw = 112 * (v / maxv)
        out.append('<text x="0" y="%.1f" font-size="7.2" font-weight="700" fill="%s">%s</text>' % (y + 7, K, lb))
        out.append('<rect x="58" y="%.1f" width="112" height="8" rx="4" fill="%s" stroke="%s" stroke-width=".8"/>'
                   % (y + 1.5, G, K))
        out.append('<rect x="58" y="%.1f" width="%.1f" height="8" rx="4" fill="%s"/>' % (y + 1.5, bw, W))
        out.append('<text x="175" y="%.1f" font-size="7.8" font-weight="800" fill="%s">%s%s</text>'
                   % (y + 7.4, W, v, unit))
        if sub:
            out.append('<text x="196" y="%.1f" font-size="6.3" fill="%s">%s</text>' % (y + 7.2, SUB, sub))
    return '<svg viewBox="0 0 260 %d" style="width:100%%;height:auto">%s</svg>' % (H, "".join(out))


def svg_quad(x, y, xlab, ylab, quads, you="YOU"):
    """2軸4象限マップ（x,yは0〜1、左下が原点）quads=[左上,右上,左下,右下]"""
    S, m = 186, 30
    inner = S - m * 2
    px, py = m + inner * x, m + inner * (1 - y)
    out = ['<rect x="%d" y="%d" width="%d" height="%d" fill="#fff" stroke="%s" stroke-width="1.6" rx="4"/>'
           % (m, m, inner, inner, K)]
    out.append('<rect x="%d" y="%d" width="%.1f" height="%.1f" fill="%s" fill-opacity=".10"/>'
               % (m, m, inner / 2, inner / 2, L))
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity=".09"/>'
               % (m + inner / 2, m + inner / 2, inner / 2, inner / 2, W))
    out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1" stroke-dasharray="3,2"/>'
               % (m, m + inner / 2, m + inner, m + inner / 2, K))
    out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1" stroke-dasharray="3,2"/>'
               % (m + inner / 2, m, m + inner / 2, m + inner, K))
    # 中央付近は YOU マーカーが入るので、ラベルは各象限の外寄りに置く
    pos = [(m + inner * .25, m + inner * .13), (m + inner * .75, m + inner * .13),
           (m + inner * .25, m + inner * .87), (m + inner * .75, m + inner * .87)]
    for (qx, qy), lab in zip(pos, quads):
        parts = lab.split("|")
        out.append('<text x="%.1f" y="%.1f" font-size="8.2" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                   % (qx, qy - 3, K, parts[0]))
        if len(parts) > 1:
            out.append('<text x="%.1f" y="%.1f" font-size="6.4" fill="%s" text-anchor="middle">%s</text>'
                       % (qx, qy + 8, SUB, parts[1]))
    out.append('<text x="%.1f" y="%d" font-size="7.2" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
               % (S / 2, S - 6, W, xlab))
    out.append('<text x="10" y="%.1f" font-size="7.2" font-weight="800" fill="%s" text-anchor="middle" '
               'transform="rotate(-90 10 %.1f)">%s</text>' % (S / 2, W, S / 2, ylab))
    out.append('<circle cx="%.1f" cy="%.1f" r="10" fill="%s" stroke="%s" stroke-width="1.8"/>' % (px, py, W, K))
    out.append('<text x="%.1f" y="%.1f" font-size="6" font-weight="800" fill="#fff" text-anchor="middle">%s</text>'
               % (px, py + 2.6, you))
    return '<svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg>' % (S, S, "".join(out))


def svg_triangle(a, b, c, la, lb, lc):
    """恋愛の三角理論：3値で塗り面積が変わる三角形"""
    S = 172
    cx, cy, R = S / 2, S / 2 + 5, 57
    P = _poly(cx, cy, R, 3)
    out = []
    for f in (0.33, 0.66):
        pts = " ".join("%.1f,%.1f" % (cx + (px - cx) * f, cy + (py - cy) * f) for px, py in P)
        out.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="1"/>' % (pts, G))
    out.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="1.4"/>'
               % (" ".join("%.1f,%.1f" % p for p in P), K))
    vals = [a, b, c]
    ip = [(cx + (px - cx) * (v / 100), cy + (py - cy) * (v / 100)) for (px, py), v in zip(P, vals)]
    out.append('<polygon points="%s" fill="%s" fill-opacity=".28" stroke="%s" stroke-width="2"/>'
               % (" ".join("%.1f,%.1f" % p for p in ip), W, W))
    for x, y in ip:
        out.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s" stroke="%s" stroke-width="1.2"/>' % (x, y, W, K))
    for (px, py), lab, v in zip(P, (la, lb, lc), vals):
        dx, dy = (px - cx) * 0.30, (py - cy) * 0.30
        out.append('<text x="%.1f" y="%.1f" font-size="7.6" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                   % (px + dx, py + dy, K, lab))
        out.append('<text x="%.1f" y="%.1f" font-size="9" font-weight="800" fill="%s" text-anchor="middle">%d</text>'
                   % (px + dx, py + dy + 10, W, v))
    return '<svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg>' % (S, S, "".join(out))


def svg_donut(pct, label, sub=""):
    """ドーナツゲージ"""
    S = 108
    cx = cy = S / 2
    r = 35
    C = 2 * math.pi * r
    return ('<svg viewBox="0 0 %d %d" style="width:100%%;height:auto">'
            '<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="13"/>'
            '<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="13" '
            'stroke-dasharray="%.1f %.1f" stroke-linecap="round" transform="rotate(-90 %.1f %.1f)"/>'
            '<text x="%.1f" y="%.1f" font-size="18" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
            '<text x="%.1f" y="%.1f" font-size="6.6" font-weight="700" fill="%s" text-anchor="middle">%s</text>'
            '</svg>' % (S, S, cx, cy, r, G, cx, cy, r, W, C * pct / 100, C, cx, cy,
                        cx, cy - 1, K, label, cx, cy + 12, SUB, sub))


def svg_compare(left, right, llab, rlab):
    """左右対比バー（愛の言語：与える／受け取りたい）
    中央にラベル列を確保し、バーはその外側にだけ伸ばす。"""
    VW = 250          # viewBox幅
    LABW = 76         # 中央ラベル列の幅
    cx = VW / 2
    lend = cx - LABW / 2      # 左バーの右端
    rstart = cx + LABW / 2    # 右バーの左端
    maxw = lend - 6           # バーの最大長
    n = len(left)
    H = n * 16 + 22
    out = ['<text x="%.1f" y="10" font-size="7.4" font-weight="800" fill="%s" text-anchor="end">%s</text>'
           % (lend, L, llab),
           '<text x="%.1f" y="10" font-size="7.4" font-weight="800" fill="%s">%s</text>' % (rstart, W, rlab)]
    for i, ((ln, lv), (_rn, rv)) in enumerate(zip(left, right)):
        y = 19 + i * 16
        lw, rw = maxw * (lv / 5), maxw * (rv / 5)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="10" rx="2.5" fill="%s" stroke="%s" '
                   'stroke-width=".8"/>' % (lend - lw, y, lw, L, K))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="10" rx="2.5" fill="%s" stroke="%s" '
                   'stroke-width=".8"/>' % (rstart, y, rw, W, K))
        # ラベルは中央列に収める（長ければ縮小）
        fs = 6.8 if len(ln) <= 7 else 6.0 if len(ln) <= 9 else 5.4
        out.append('<text x="%.1f" y="%.1f" font-size="%.1f" font-weight="800" fill="%s" '
                   'text-anchor="middle">%s</text>' % (cx, y + 7.4, fs, K, ln))
    return '<svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg>' % (VW, H, "".join(out))


def svg_stack(items):
    """認知機能の4段スタック（上が主導機能）"""
    H = len(items) * 27 + 4
    out = []
    for i, (code, role, desc) in enumerate(items):
        y = i * 27
        w = 236 - i * 17
        x0 = (236 - w) / 2
        op = 1 if i == 0 else max(.18, .55 - i * .12)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="22" rx="5" fill="%s" fill-opacity="%.2f" '
                   'stroke="%s" stroke-width="1.4"/>' % (x0, y + 2, w, W if i == 0 else L, op, K))
        out.append('<text x="%.1f" y="%.1f" font-size="10.5" font-weight="800" fill="%s">%s</text>'
                   % (x0 + 8, y + 17, K, code))
        out.append('<text x="%.1f" y="%.1f" font-size="6.6" font-weight="700" fill="%s">%s</text>'
                   % (x0 + 30, y + 17, K, role))
        out.append('<text x="%.1f" y="%.1f" font-size="6.4" fill="#4a3f52" text-anchor="end">%s</text>'
                   % (x0 + w - 8, y + 17, desc))
    PADX = 3
    return ('<svg viewBox="%d 0 %d %d" style="width:100%%;height:auto">%s</svg>'
            % (-PADX, 236 + PADX * 2, H, "".join(out)))


def _fit_lines(text, max_chars, max_lines=2):
    """全角前提で max_chars 文字ずつに折り返す。溢れる分は末尾を…で丸める。"""
    lines = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:max(1, max_chars - 1)] + "…"
    return lines


def svg_flow5(steps):
    """横並びステップの矢印フロー steps=[(番号, 見出し)]"""
    n = len(steps)
    W_ = 250
    bw = (W_ - (n - 1) * 8) / n
    fs = 7.2 if n > 3 else 7.6
    max_chars = max(4, int((bw - 5) / fs))
    # 全ボックスの行数を揃える
    wrapped = [_fit_lines(t, max_chars) for _, t in steps]
    rows = max(len(w) for w in wrapped)
    H = 26 + rows * (fs + 2.4)
    out = []
    for i, ((num, _t), lines) in enumerate(zip(steps, wrapped)):
        x = i * (bw + 8)
        out.append('<rect x="%.1f" y="4" width="%.1f" height="%.1f" rx="6" fill="#fff" stroke="%s" stroke-width="1.6"/>'
                   % (x, bw, H - 8, K))
        out.append('<circle cx="%.1f" cy="14" r="7" fill="%s" stroke="%s" stroke-width="1.2"/>' % (x + bw / 2, W, K))
        out.append('<text x="%.1f" y="16.6" font-size="7" font-weight="800" fill="#fff" text-anchor="middle">%s</text>'
                   % (x + bw / 2, num))
        for j, ln in enumerate(lines):
            out.append('<text x="%.1f" y="%.1f" font-size="%.1f" font-weight="800" fill="%s" '
                       'text-anchor="middle">%s</text>'
                       % (x + bw / 2, 27 + j * (fs + 2.4), fs, K, ln))
        if i < n - 1:
            out.append('<text x="%.1f" y="%.1f" font-size="8" font-weight="800" fill="%s" text-anchor="middle">▶</text>'
                       % (x + bw + 4, H / 2 + 2, L))
    PADX = 3
    return ('<svg viewBox="%d 0 %d %.1f" style="width:100%%;height:auto">%s</svg>'
            % (-PADX, W_ + PADX * 2, H, "".join(out)))


def svg_flip(pairs):
    """「◯◯ ➜ こう変える」の変換図 pairs=[(左ラベル, 右ラベル, 補足)]"""
    LW, RW = 92, 116
    rowsL = [_fit_lines(a, 11) for a, _b, _c in pairs]
    rowsR = [_fit_lines(b, 14) for _a, b, _c in pairs]
    lines = max(max(len(x) for x in rowsL), max(len(x) for x in rowsR))
    bh = 15 + (lines - 1) * 9
    gap = 7
    H = len(pairs) * (bh + gap) + 4
    out = []
    for i, ((_a, _b, desc), la, ra) in enumerate(zip(pairs, rowsL, rowsR)):
        y = i * (bh + gap) + 2
        out.append('<rect x="0" y="%.1f" width="%d" height="%.1f" rx="5" fill="%s" fill-opacity=".22" '
                   'stroke="%s" stroke-width="1.3"/>' % (y, LW, bh, L, K))
        for j, ln in enumerate(la):
            out.append('<text x="%.1f" y="%.1f" font-size="7" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                       % (LW / 2, y + bh / 2 - (len(la) - 1) * 4.5 + j * 9 + 2.4, K, ln))
        out.append('<text x="%.1f" y="%.1f" font-size="10" font-weight="800" fill="%s" text-anchor="middle">➜</text>'
                   % (LW + 8, y + bh / 2 + 3.4, W))
        out.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" rx="5" fill="%s" fill-opacity=".18" '
                   'stroke="%s" stroke-width="1.3"/>' % (LW + 18, y, RW, bh, W, K))
        for j, ln in enumerate(ra):
            out.append('<text x="%.1f" y="%.1f" font-size="7" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                       % (LW + 18 + RW / 2, y + bh / 2 - (len(ra) - 1) * 4.5 + j * 9 + 2.4, K, ln))
        if desc:
            out.append('<text x="%d" y="%.1f" font-size="6.3" fill="%s">%s</text>'
                       % (LW + RW + 24, y + bh / 2 + 2.4, SUB, desc[:14] + ("…" if len(desc) > 14 else "")))
    PADX = 3
    return ('<svg viewBox="%d 0 %d %.1f" style="width:100%%;height:auto">%s</svg>'
            % (-PADX, LW + RW + 24 + PADX * 2, H, "".join(out)))


def svg_gauge_row(rows):
    """相性スコアの帯グラフ（グループ別）rows=[(猫種, code, score)]"""
    H = len(rows) * 15 + 4
    out = []
    for i, (breed, code, sc) in enumerate(rows):
        y = i * 15 + 3
        bw = 96 * (sc / 100)
        col = W if sc >= 85 else (L if sc >= 75 else "#b9a9c6")
        out.append('<text x="0" y="%.1f" font-size="6.8" font-weight="700" fill="%s">%s</text>' % (y + 7.6, K, breed))
        out.append('<text x="0" y="%.1f" font-size="5.4" fill="%s">%s</text>' % (y + 13.6, SUB, code))
        out.append('<rect x="72" y="%.1f" width="96" height="8" rx="4" fill="%s" stroke="%s" stroke-width=".7"/>'
                   % (y + 2, G, K))
        out.append('<rect x="72" y="%.1f" width="%.1f" height="8" rx="4" fill="%s"/>' % (y + 2, bw, col))
        out.append('<text x="172" y="%.1f" font-size="7.4" font-weight="800" fill="%s">%d</text>' % (y + 8.6, col, sc))
    return '<svg viewBox="0 0 190 %d" style="width:100%%;height:auto">%s</svg>' % (H, "".join(out))


def svg_timeline(items):
    """横向きタイムライン items=[(期間, 見出し, 一言)]
    見出しが折り返した分だけ補足の位置と全体の高さを下げ、文字が重ならないようにする。"""
    n = len(items)
    W_ = 260
    seg = W_ / n
    wrapped = [_fit_lines(t, 7) for _p, t, _n in items]
    rows = max(len(w) for w in wrapped)
    note_y = 43 + rows * 9          # 見出しの行数ぶん下げる
    H = note_y + 8
    out = ['<line x1="10" y1="26" x2="%d" y2="26" stroke="%s" stroke-width="2"/>' % (W_ - 10, L)]
    for i, ((per, _ttl, note_), lines) in enumerate(zip(items, wrapped)):
        cx = seg * i + seg / 2
        out.append('<text x="%.1f" y="12" font-size="6.6" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                   % (cx, W, per))
        out.append('<circle cx="%.1f" cy="26" r="7.5" fill="#fff" stroke="%s" stroke-width="1.6"/>' % (cx, K))
        out.append('<text x="%.1f" y="28.8" font-size="7" font-weight="800" fill="%s" text-anchor="middle">%d</text>'
                   % (cx, K, i + 1))
        for j, ln in enumerate(lines):
            out.append('<text x="%.1f" y="%.1f" font-size="7.2" font-weight="800" fill="%s" '
                       'text-anchor="middle">%s</text>' % (cx, 43 + j * 9, K, ln))
        out.append('<text x="%.1f" y="%.1f" font-size="6.2" fill="%s" text-anchor="middle">%s</text>'
                   % (cx, note_y, SUB, note_))
    PADX = 3
    return ('<svg viewBox="%d 0 %d %d" style="width:100%%;height:auto">%s</svg>'
            % (-PADX, W_ + PADX * 2, H, "".join(out)))


def svg_vs(left_title, left_items, right_title, right_items):
    """左右の対比リスト図（執着 vs 愛情 など）"""
    n = max(len(left_items), len(right_items))
    H = n * 13 + 24
    out = ['<rect x="0" y="0" width="122" height="%d" rx="5" fill="%s" fill-opacity=".13" stroke="%s" stroke-width="1.3"/>'
           % (H, L, K),
           '<rect x="132" y="0" width="122" height="%d" rx="5" fill="%s" fill-opacity=".13" stroke="%s" stroke-width="1.3"/>'
           % (H, W, K),
           '<text x="61" y="13" font-size="7.6" font-weight="800" fill="%s" text-anchor="middle">%s</text>' % (K, left_title),
           '<text x="193" y="13" font-size="7.6" font-weight="800" fill="%s" text-anchor="middle">%s</text>' % (K, right_title)]
    for i, t in enumerate(left_items):
        out.append('<text x="8" y="%.1f" font-size="6.6" fill="#4a3f52">・%s</text>' % (26 + i * 13, t))
    for i, t in enumerate(right_items):
        out.append('<text x="140" y="%.1f" font-size="6.6" fill="#4a3f52">・%s</text>' % (26 + i * 13, t))
    PADX = 3
    return ('<svg viewBox="%d 0 %d %d" style="width:100%%;height:auto">%s</svg>'
            % (-PADX, 254 + PADX * 2, H, "".join(out)))
