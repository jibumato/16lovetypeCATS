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
    return '<svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg>' % (size, size, "".join(out))


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
    pos = [(m + inner * .25, m + inner * .25), (m + inner * .75, m + inner * .25),
           (m + inner * .25, m + inner * .75), (m + inner * .75, m + inner * .75)]
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
    """左右対比バー（愛の言語：与える／受け取りたい）"""
    n = len(left)
    H = n * 16 + 20
    out = ['<text x="82" y="9" font-size="7" font-weight="800" fill="%s" text-anchor="end">%s</text>' % (L, llab),
           '<text x="118" y="9" font-size="7" font-weight="800" fill="%s">%s</text>' % (W, rlab)]
    for i, ((ln, lv), (rn, rv)) in enumerate(zip(left, right)):
        y = 18 + i * 16
        lw, rw = 72 * (lv / 5), 72 * (rv / 5)
        out.append('<text x="100" y="%.1f" font-size="6.6" font-weight="700" fill="%s" text-anchor="middle">%s</text>'
                   % (y + 8, K, ln))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="9.5" rx="2.5" fill="%s" stroke="%s" stroke-width=".7"/>'
                   % (82 - lw, y + 1, lw, L, K))
        out.append('<rect x="118" y="%.1f" width="%.1f" height="9.5" rx="2.5" fill="%s" stroke="%s" stroke-width=".7"/>'
                   % (y + 1, rw, W, K))
    return '<svg viewBox="0 0 200 %d" style="width:100%%;height:auto">%s</svg>' % (H, "".join(out))


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
    return '<svg viewBox="0 0 236 %d" style="width:100%%;height:auto">%s</svg>' % (H, "".join(out))


def svg_flow5(steps):
    """5段ステップの矢印フロー steps=[(番号, 見出し)]"""
    n = len(steps)
    W_ = 250
    bw = (W_ - (n - 1) * 8) / n
    out = []
    for i, (num, ttl) in enumerate(steps):
        x = i * (bw + 8)
        out.append('<rect x="%.1f" y="6" width="%.1f" height="34" rx="6" fill="#fff" stroke="%s" stroke-width="1.6"/>'
                   % (x, bw, K))
        out.append('<circle cx="%.1f" cy="15" r="7" fill="%s" stroke="%s" stroke-width="1.2"/>' % (x + bw / 2, W, K))
        out.append('<text x="%.1f" y="17.6" font-size="7" font-weight="800" fill="#fff" text-anchor="middle">%s</text>'
                   % (x + bw / 2, num))
        out.append('<text x="%.1f" y="33" font-size="7.2" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                   % (x + bw / 2, K, ttl))
        if i < n - 1:
            out.append('<text x="%.1f" y="27" font-size="8" font-weight="800" fill="%s" text-anchor="middle">▶</text>'
                       % (x + bw + 4, L))
    return '<svg viewBox="0 0 %d 46" style="width:100%%;height:auto">%s</svg>' % (W_, "".join(out))


def svg_flip(pairs):
    """クセ → 長所 の変換図 pairs=[(クセ, 長所, 説明)]"""
    H = len(pairs) * 30 + 4
    out = []
    for i, (bad, good, desc) in enumerate(pairs):
        y = i * 30 + 2
        out.append('<rect x="0" y="%.1f" width="76" height="24" rx="5" fill="%s" fill-opacity=".22" '
                   'stroke="%s" stroke-width="1.3"/>' % (y, L, K))
        out.append('<text x="38" y="%.1f" font-size="7.4" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                   % (y + 15, K, bad))
        out.append('<text x="86" y="%.1f" font-size="10" font-weight="800" fill="%s" text-anchor="middle">➜</text>'
                   % (y + 16, W))
        out.append('<rect x="96" y="%.1f" width="86" height="24" rx="5" fill="%s" fill-opacity=".18" '
                   'stroke="%s" stroke-width="1.3"/>' % (y, W, K))
        out.append('<text x="139" y="%.1f" font-size="7.4" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                   % (y + 15, K, good))
        out.append('<text x="190" y="%.1f" font-size="6.3" fill="%s">%s</text>' % (y + 15, SUB, desc))
    return '<svg viewBox="0 0 300 %d" style="width:100%%;height:auto">%s</svg>' % (H, "".join(out))


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
    """横向きタイムライン items=[(期間, 見出し, 一言)]"""
    n = len(items)
    W_ = 260
    seg = W_ / n
    out = ['<line x1="10" y1="26" x2="%d" y2="26" stroke="%s" stroke-width="2"/>' % (W_ - 10, L)]
    for i, (per, ttl, note_) in enumerate(items):
        cx = seg * i + seg / 2
        out.append('<text x="%.1f" y="12" font-size="6.6" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                   % (cx, W, per))
        out.append('<circle cx="%.1f" cy="26" r="7.5" fill="%s" stroke="%s" stroke-width="1.6"/>' % (cx, "#fff", K))
        out.append('<text x="%.1f" y="28.8" font-size="7" font-weight="800" fill="%s" text-anchor="middle">%d</text>'
                   % (cx, K, i + 1))
        out.append('<text x="%.1f" y="43" font-size="7.4" font-weight="800" fill="%s" text-anchor="middle">%s</text>'
                   % (cx, K, ttl))
        out.append('<text x="%.1f" y="52" font-size="6.2" fill="%s" text-anchor="middle">%s</text>'
                   % (cx, SUB, note_))
    return '<svg viewBox="0 0 %d 58" style="width:100%%;height:auto">%s</svg>' % (W_, "".join(out))


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
    return '<svg viewBox="0 0 254 %d" style="width:100%%;height:auto">%s</svg>' % (H, "".join(out))
