#!/usr/bin/env python3
# ogp/article/*.png (183枚・記事シェア画像) を猫版に統一生成。
# 右カードのイラストは記事固有の犬絵ではなく、確定した16タイプ集合イラストの
# 固定クロップを使い回す（ユーザー承認の「集合イラストで統一」方針）。
# 依存: /tmp/MPLUSRounded1c-{Regular,ExtraBold}.ttf, WQY Zen Hei, DejaVu Sans(Bold)
import glob, os, re, html
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
GROUP_ART = "/tmp/claude-0/-home-user-16lovetypeCATS/ca9b5b1a-5375-5908-aa61-ec0aeb6a5928/scratchpad/group_ogp/16nyanko-ogp-group-illustration.png"
MPB = "/tmp/MPLUSRounded1c-ExtraBold.ttf"
MPR = "/tmp/MPLUSRounded1c-Regular.ttf"
WQY = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEJA_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CREAM = (252, 244, 239)
PINK = (210, 98, 143)
PILL_BG = (247, 217, 228)
INK = (60, 55, 68)
INK_SOFT = (140, 132, 152)
WHITE = (255, 255, 255)

EYEBROW = {"ja": "MBTI × 恋愛", "en": "MBTI × LOVE", "ko": "MBTI 연애", "zh": "MBTI 恋爱", "tw": "MBTI 戀愛"}
HASHTAG = {"ja": "#16にゃんこ恋愛診断", "en": "#16LoveTypeCats", "ko": "#16연애묘진단",
           "zh": "#16恋爱猫测验", "tw": "#16戀愛貓測驗"}
DOMAIN = "16lovetypecats.com"

def bold_font(lang, size):
    return ImageFont.truetype(MPB if lang == "ja" else DEJA_B if lang == "en" else WQY, size)

def reg_font(lang, size):
    return ImageFont.truetype(MPR if lang == "ja" else DEJA_R if lang == "en" else WQY, size)

def wrap(dr, text, font, max_w):
    out, ln = [], ""
    # CJK: char-by-char; en: word-by-word
    units = list(text) if any(ord(c) > 0x3000 for c in text) or True else text.split(" ")
    # simpler: for en use word wrap, else char wrap
    if all(ord(c) < 0x3000 for c in text):
        words = text.split(" ")
        for w in words:
            trial = (ln + " " + w).strip()
            if dr.textlength(trial, font=font) > max_w and ln:
                out.append(ln); ln = w
            else:
                ln = trial
        if ln:
            out.append(ln)
    else:
        for ch in text:
            if dr.textlength(ln + ch, font=font) > max_w and ln:
                out.append(ln); ln = ch
            else:
                ln += ch
        if ln:
            out.append(ln)
    return out

def get_card_crop():
    art = Image.open(GROUP_ART).convert("RGB")
    # crop a clean, representative slice: top-row cats (chess/heart/lantern), left side avoids logo
    box = (800, 40, 1140, 380)  # tight square on 2 clean row-1 cats, no logo/text
    c = art.crop(box)
    side = min(c.size)
    c = c.crop((0, 0, side, side))
    return c

CARD_CROP = get_card_crop()

def extract_meta(htmlpath):
    s = open(htmlpath, encoding="utf-8").read()
    m_title = re.search(r'property="og:title"\s+content="([^"]*)"', s)
    m_desc = re.search(r'property="og:description"\s+content="([^"]*)"', s)
    lang_m = re.search(r'<html\s+lang="([a-zA-Z-]+)"', s)
    title = html.unescape(m_title.group(1)) if m_title else os.path.basename(htmlpath)
    desc = html.unescape(m_desc.group(1)) if m_desc else ""
    htmllang = lang_m.group(1) if lang_m else "ja"
    return title, desc, htmllang

def lang_from_filename(name):
    m = re.search(r'-(en|ko|zh|tw)$', name)
    return m.group(1) if m else "ja"

def make(name):
    htmlpath = os.path.join(ROOT, name + ".html")
    title, desc, _ = extract_meta(htmlpath)
    lang = lang_from_filename(name)
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), CREAM)
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    bd.ellipse([-140, -180, 220, 180], fill=(247, 224, 233, 120))
    bd.ellipse([W - 260, H - 220, W + 120, H + 160], fill=(247, 224, 233, 110))
    img = Image.alpha_composite(img.convert("RGBA"), blob).convert("RGB")
    dr = ImageDraw.Draw(img)

    LX, LW = 60, 660

    ef = bold_font(lang, 26)
    et = EYEBROW[lang]
    ew = dr.textlength(et, font=ef)
    dr.rounded_rectangle([LX, 44, LX + ew + 48, 96], 26, fill=PILL_BG)
    dr.text((LX + 24, 70), et, font=ef, fill=PINK, anchor="lm")

    y = 158
    tsize = 54
    tf = bold_font(lang, tsize)
    tlines = wrap(dr, title, tf, LW)
    while len(tlines) > 2 and tsize > 34:
        tsize -= 2
        tf = bold_font(lang, tsize)
        tlines = wrap(dr, title, tf, LW)
    tlines = tlines[:2]
    for ln in tlines:
        dr.text((LX, y), ln, font=tf, fill=INK, anchor="lm")
        y += int(tsize * 1.28)
    y += 14

    df = reg_font(lang, 26)
    dlines = wrap(dr, desc, df, LW)[:3]
    for ln in dlines:
        dr.text((LX, y), ln, font=df, fill=INK_SOFT, anchor="lm")
        y += 38

    # right card
    CW, CH = 360, 340
    CX, CY = W - CW - 60, 160
    img.paste(Image.new("RGB", (CW, CH), WHITE), (CX, CY))
    thumb = CARD_CROP.resize((CW - 16, CH - 16))
    img.paste(thumb, (CX + 8, CY + 8))
    dr.rounded_rectangle([CX, CY - 6, CX + CW, CY + 2], 4, fill=PINK)

    # footer
    dr.line([LX, H - 92, LX + LW, H - 92], fill=(242, 184, 204), width=2)
    ff = bold_font(lang, 26)
    dr.text((LX, H - 58), DOMAIN, font=ff, fill=PINK, anchor="lm")
    dw = dr.textlength(DOMAIN, font=ff)
    hf = reg_font(lang, 24)
    dr.text((LX + dw + 40, H - 58), HASHTAG[lang], font=hf, fill=INK_SOFT, anchor="lm")

    img.save(os.path.join(ROOT, "ogp", "article", name + ".png"))

if __name__ == "__main__":
    names = [os.path.basename(p)[:-4] for p in sorted(glob.glob(os.path.join(ROOT, "ogp", "article", "*.png")))]
    ok, fail = 0, []
    for n in names:
        try:
            make(n)
            ok += 1
        except Exception as e:
            fail.append((n, str(e)))
    print(f"generated {ok}/{len(names)}")
    if fail:
        print("failures:")
        for n, e in fail[:20]:
            print(" ", n, e)
