#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""16にゃんこ恋愛診断 プレミアム恋愛攻略書 ビルダー
犬版（16わんこ）の32ページ構成・デザインを踏襲し、猫版を生成する。
相性スコアはサイト index.html の compatScore と完全一致。
"""
import json, os, sys

ORDER = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
         "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
SCRATCH = os.path.dirname(os.path.abspath(__file__))
LOC = json.load(open(os.path.join(SCRATCH, "LOC.json"), encoding="utf-8"))["ja"]
BREED = {c: LOC[c]["breed"] for c in ORDER}
ROLE  = {c: LOC[c]["role"] for c in ORDER}
PARAM = {"INTJ":[5,3,4,4,2],"INTP":[4,2,2,1,2],"ENTJ":[4,4,4,3,3],"ENTP":[2,2,2,2,5],
         "INFJ":[5,4,4,3,2],"INFP":[5,4,3,3,3],"ENFJ":[4,5,4,3,3],"ENFP":[3,4,2,4,5],
         "ISTJ":[5,3,5,2,1],"ISFJ":[5,5,5,3,1],"ESTJ":[4,4,5,3,2],"ESFJ":[4,5,4,5,3],
         "ISTP":[3,2,2,2,3],"ISFP":[3,3,3,2,3],"ESTP":[2,3,2,3,5],"ESFP":[3,4,3,5,5]}
RARITY = {"INTJ":2.1,"INTP":3.3,"ENTJ":1.8,"ENTP":3.2,"INFJ":1.5,"INFP":4.4,"ENFJ":2.5,
          "ENFP":8.1,"ISTJ":11.6,"ISFJ":13.8,"ESTJ":8.7,"ESFJ":12.3,"ISTP":5.4,"ISFP":8.8,
          "ESTP":4.3,"ESFP":8.5}
GROUPS = {"NT":["INTJ","INTP","ENTJ","ENTP"], "NF":["INFJ","INFP","ENFJ","ENFP"],
          "SJ":["ISTJ","ISFJ","ESTJ","ESFJ"], "SP":["ISTP","ISFP","ESTP","ESFP"]}

def compat(a, b):
    if a == b: return 70
    return (51 + (26 if a[1]==b[1] else 0) + (8 if a[2]==b[2] else 0)
            + (6 if a[0]!=b[0] else 0) + (7 if a[3]!=b[3] else 0))

def ranking(code):
    return sorted(((compat(code,b), b) for b in ORDER if b != code), reverse=True)

def stars(n):
    return '<span class="st">' + "★"*n + '</span><span class="st off">' + "☆"*(5-n) + "</span>"

def sp(s):
    """字間を空けた欧文ラベル"""
    return "&nbsp;".join(list(s))

# ══════════════════════════════════════════════════════════════
#  CSS（犬版デザイン踏襲：クリーム地＋ボルドー＋明朝）
# ══════════════════════════════════════════════════════════════
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;600;700;800&family=Cormorant+Garamond:wght@300;400;500;600&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --cream:#faf5ec; --cream2:#f5eddf; --paper:#fffdf9;
  --wine:#8c2f4a; --wine2:#a84462; --wine-l:#c98ea0;
  --pink:#fdeef2; --pinkbd:#f0cdd7;
  --gold:#c9a961; --gold-l:#e3d4b0;
  --ink:#4e4247; --ink2:#6f6167; --ink3:#9b8d93;
  --rule:#e5d9c8;
}
@page{size:A4;margin:0}
html,body{background:#888}
body{font-family:'Shippori Mincho','Noto Serif JP',serif;color:var(--ink);
  -webkit-font-smoothing:antialiased;font-feature-settings:"palt" 1}
.page{width:210mm;height:297mm;background:var(--cream);position:relative;
  overflow:hidden;page-break-after:always;padding:13mm 14mm 11mm}
.page:last-child{page-break-after:auto}
.page::before{content:"";position:absolute;inset:7mm;border:0.6pt solid var(--gold-l);pointer-events:none}
.page::after{content:"";position:absolute;inset:8.2mm;border:0.4pt solid var(--gold-l);opacity:.55;pointer-events:none}
.inner{position:relative;height:100%;display:flex;flex-direction:column}

/* ── ヘッダ ── */
.phead{display:flex;justify-content:space-between;align-items:flex-start;
  font-size:7.2pt;letter-spacing:.13em;color:var(--ink3);padding-bottom:1.5mm}
.chapno{position:absolute;top:-6mm;right:0;font-family:'Cormorant Garamond',serif;
  font-size:51.75pt;font-weight:300;color:var(--wine);opacity:.13;line-height:1;letter-spacing:.04em}
.clabel{font-size:7.42pt;letter-spacing:.34em;color:var(--wine-l);margin-top:3.5mm}
h1.ptitle{font-size:21.94pt;font-weight:700;color:var(--wine);letter-spacing:.055em;
  margin-top:1.2mm;line-height:1.35}
.hr-main{border:0;border-top:.5pt solid var(--rule);margin:3.2mm 0 3.4mm}

/* ── 共通部品 ── */
.lead{font-size:8.66pt;line-height:1.95;color:var(--ink2);margin-bottom:3.2mm}
.freeband{background:var(--cream2);border:.5pt solid var(--gold-l);border-radius:1.2mm;
  padding:2.4mm 3.4mm;display:flex;gap:4.5mm;align-items:center;font-size:7.88pt;margin-bottom:2.6mm}
.freeband .fb-t{font-size:6.52pt;letter-spacing:.22em;color:var(--wine-l);display:block}
.freeband .fb-h{font-size:9.0pt;font-weight:700;color:var(--wine);white-space:nowrap}
.freeband span.it{color:var(--ink2)}
.freeband b{color:var(--wine2);font-weight:600}
.centernote{text-align:center;font-size:7.65pt;color:var(--wine-l);letter-spacing:.08em;margin:2.4mm 0 3mm}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:3.4mm}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}
.panel{background:var(--paper);border:.5pt solid var(--rule);border-left:1.6pt solid var(--wine-l);
  border-radius:1mm;padding:2.8mm 3.4mm}
.panel.pink{background:var(--pink);border-left-color:var(--wine2);border-color:var(--pinkbd)}
.panel .pt{font-size:7.88pt;font-weight:700;color:var(--wine);letter-spacing:.1em;margin-bottom:1.6mm}
.panel p{font-size:8.33pt;line-height:1.9;color:var(--ink)}
.sect-h{font-size:8.55pt;font-weight:700;color:var(--wine);letter-spacing:.1em;
  margin:3.4mm 0 2mm;display:flex;align-items:center;gap:2mm}
.sect-h::after{content:"";flex:1;border-top:.4pt solid var(--rule)}
.tag{display:inline-block;border:.5pt solid var(--pinkbd);border-radius:99px;
  padding:.9mm 2.6mm;font-size:7.42pt;color:var(--wine2);margin:0 1.4mm 1.4mm 0;background:var(--paper)}
.stat{background:var(--cream2);border:.5pt solid var(--gold-l);border-radius:1mm;padding:2.6mm 3.2mm}
.stat .sh{font-size:7.88pt;font-weight:700;color:var(--wine);margin-bottom:1.6mm;letter-spacing:.08em}
.strow{display:flex;justify-content:space-between;font-size:8.1pt;padding:.75mm 0;color:var(--ink2)}
.st{color:var(--wine2);letter-spacing:.06em}.st.off{color:var(--gold-l)}
.deflist dt{font-size:8.1pt;font-weight:700;color:var(--wine2);float:left;width:13mm}
.deflist dd{font-size:8.1pt;line-height:1.85;margin-left:13mm;padding-bottom:1.5mm;
  border-bottom:.4pt dotted var(--rule);margin-bottom:1.5mm;color:var(--ink2)}
.foot-note{margin-top:auto;background:var(--pink);border:.5pt solid var(--pinkbd);border-radius:1mm;
  padding:2.2mm 3.2mm;font-size:7.54pt;line-height:1.8;color:var(--ink2)}
.foot-note b{color:var(--wine);font-weight:700;letter-spacing:.14em;font-size:6.98pt;margin-right:2mm}
.pfoot{display:flex;justify-content:space-between;font-size:6.75pt;letter-spacing:.2em;
  color:var(--ink3);margin-top:auto;padding-top:2.9mm}
.pfoot .pno{color:var(--wine-l)}
ul.check{list-style:none}
ul.check li{font-size:8.21pt;line-height:1.95;color:var(--ink2);padding-left:4.5mm;position:relative}
ul.check li::before{content:"♡";position:absolute;left:0;color:var(--wine-l);font-size:7.42pt}
ul.ng li::before{content:"✕";color:var(--ink3)}
ul.ok li::before{content:"✓";color:var(--wine2)}
.num{display:inline-flex;width:5mm;height:5mm;border-radius:50%;background:var(--wine);color:#fff;
  font-size:7.2pt;align-items:center;justify-content:center;font-family:'Cormorant Garamond',serif;flex:none}
.step{display:flex;gap:2.6mm;align-items:flex-start;margin-bottom:2.2mm}
.step .sbody{font-size:8.21pt;line-height:1.85}
.step .sbody b{color:var(--wine);font-weight:700;display:block;font-size:8.44pt;margin-bottom:.4mm}
"""

# ══════════════════════════════════════════════════════════════
#  ページ部品
# ══════════════════════════════════════════════════════════════
def page(code, body, chapno="", clabel="", title="", pno="", cls=""):
    d = LOC[code]
    head = ""
    if pno:
        head = f'''<div class="phead"><span>恋愛攻略書 　—　 {d["breed"]}（{sp(code)}）</span>
        <span>{clabel.split("・")[0] if clabel else ""}</span></div>'''
    chap = f'<div class="chapno">{chapno}</div>' if chapno else ""
    ttl = ""
    if title:
        ttl = f'<div class="clabel">{clabel}</div><h1 class="ptitle">{title}</h1><hr class="hr-main">'
    foot = ""
    if pno:
        foot = f'''<div class="pfoot"><span>{sp(d["breed"][:6])}　·　{sp(code)}</span>
        <span class="pno">♢　{pno}</span></div>'''
    return f'<section class="page {cls}"><div class="inner">{chap}{head}{ttl}{body}{foot}</div></section>'

def note(label, text):
    return f'<div class="foot-note"><b>{label}</b>{text}</div>'

# ══════════════════════════════════════════════════════════════
#  ENFJ（サイベリアン）専用コンテンツ
# ══════════════════════════════════════════════════════════════
C = {
 "code":"ENFJ",
 "subtitle":"寄り添って導く、みんなの安らぎ",
 "cover_lead":"包み込むカリスマ。寄り添うことで輝く、陽だまりのような恋。<br>あなただけの恋愛トリセツ、ここに完成。",
 "pedigree":"2891",
 "free_tags":["タイプはサイベリアン（ENFJ）","恋は寄り添い・献身タイプ","包容力・聞き上手・献身"],
 "outside":"あたたかくてカリスマ性があり、誰からも頼られる聞き上手。落ち込んだ人のそばにいつのまにか座っている、みんなの安らぎのような存在。恋愛でもモテるタイプで、誰にでも優しく見える。",
 "inside":"本命に対しては誰よりもまっすぐで一途。頼られ役の仮面の下では、好きな人の幸せだけを純粋に願っている。「みんなに優しい」のと「本当に大切な人」は、本人の中では全く別ものです。",
 "core":[("包容力","相手の幸せが自分の幸せ。寄り添うことに迷いがない。"),
         ("共感","相手の気持ちを察する力が高い。だからこそ抱え込んでしまう。"),
         ("献身","誰とでも心を通わせる魅力。でも本命への一途さは別格。")],
 "core_lead":"サイベリアンの恋愛は「包み込む」ことから始まります。相手の幸せを願う気持ちが先に立ち、自分の欲求は後回しになりやすい。でも本当に大切な関係は、支え合うことで初めて長続きします。",
 "keywords":["愛情深い","寄り添い型","聞き上手","一途","頼られ役","癒し系","世話好き","本命主義"],
 "tokimeki":["「ありがとう」と感謝を返してくれた時","気遣いを当然と思わず受け止めてくれた時","「無理しないで」と気遣われた時"],
 "jirai":["寄り添いを「当たり前」に扱われた時","「誰にでも優しいだけ」と言われた時","感謝のない一方通行が続いた時"],
 # CH02
 "stages":[("気配り","相手の様子を自然と気にかける"),("お世話","気づいたら支えている"),
           ("特別扱い","この人だけ特別かも"),("告白","まっすぐ気持ちを伝える"),
           ("全力愛情","惜しみなく愛を注ぐ")],
 "stage_warn":"Stage 2「お世話」が行き過ぎると、相手が受け取る前から与えてしまい、見返りを期待しすぎることも。「相手が望んでいるか」を確認する一手間が大切です。",
 "stage_str":"気持ちをまっすぐ伝えられるのは大きな強み。尽くし度★5・一途度★4が示す通り、伝えた気持ちはブレずに長く続きます。",
 "speed":[("早め","アプローチまで"),("穏やか","表現の質"),("安定","気持ちの持続力")],
 "loved":[("安心感が違う","静かに寄り添ってくれるあなたとの関係は、相手に「自分は大切にされている」という確信を与える。"),
          ("一緒にいて心がほどける","あなたのあたたかさは、相手の張りつめた日常をやわらかく緩めてくれる。"),
          ("裏表がない","誰にでも優しく見えても、本命への態度は誰よりも誠実。その一貫性が深い信頼を生む。")],
 # CH03 罠（サイトのcons＝無料版で見えている3つ）
 "traps":[("抱え込みがち","弱音を見せられず、一人で抱える",
           "頼られることには慣れていても、頼ることに慣れていない。しんどさを一人で処理し続け、限界が来るまで誰にも気づかれない。相手からは「何も困っていない人」に見えてしまう。",
           "週に一度でいい。「実はちょっと疲れてて」と、結論のない話を相手に渡してみて。弱さの共有は、relationship の距離をいちばん縮めます。"),
          ("自分を後回しにする","相手を優先するあまり、自分の希望が消える",
           "相手を優先するあまり、自分が本当はどうしたいのかを忘れてしまう。気づいたときには疲れ切っていて、急に距離を置きたくなることも。",
           "一日5分でいい。「自分が今どう感じているか」を確認する時間を作って。自分を満たすことも、相手への愛情の一部です。"),
          ("甘えるのが苦手","受け取る側になれず、関係が一方通行になる",
           "与えるのは得意でも、受け取るのが苦手。相手が何かしてくれようとすると「大丈夫」と遠慮してしまい、相手に「必要とされていない」と感じさせることがある。",
           "「ありがとう、助かる」と素直に受け取る練習を。甘えることは、相手に「役に立てた」という喜びを贈ることでもあります。")],
 "trap_flip":[("抱え込みがちの罠","静かな強さ","一人で立てる力があるからこそ、誰かを支えられる。"),
              ("自分を後回しの罠","深い思いやり","自分を後回しにできるのは、相手を本当に大切に思う証拠。"),
              ("甘え下手の罠","与える才能","受け取るより先に与えられる人は、それだけで稀有な存在。")],
 # CH04/05/06
 "grp_comment":{"NT":"感情表現が控えめでも愛情はある。クールな反応に焦らず、行動を見て判断して。",
                "NF":"感情を深く共有できる関係。お互いに抱え込みすぎないバランスを意識して。",
                "SJ":"安定志向が合う相手。あなたの包容力が、相手の緊張をほどいてくれる。",
                "SP":"一緒にいて楽しい組み合わせ。あなたの気配りが、相手の自由さを支える土台に。"},
 "why_high":"サイベリアンの惜しみなく与える力を、NFの深く受け止める感受性が循環させてくれるから。一方通行になりがちなあなたの愛が、ちゃんと返ってくる。同じ理想を語り合える同族だからこそ、満たし合える関係になります。",
 "top5_cm":["寄り添い合うソウルメイト。お互いの感情を深く理解し合える最高の相互理解ペア。あなたが与える愛を、相手は全力で受け止めてくれる。",
            "好奇心の塊のような相手。あなたの安心感が、ソマリの自由な冒険を支える帰る場所になる。飽きのこない関係に。",
            "洞察の深い相手との組み合わせ。言葉にしない部分まで読み合えるので、あなたが抱え込んでも気づいてもらえる稀有な相手。",
            "静かな思考家との組み合わせ。あなたの愛情表現が、INTPの内に秘めた感情を外に引き出すきっかけになる。",
            "発想が跳ねる相手。あなたの受け止める力と相手の刺激が組み合わさり、飽きのこない関係に。"],
 "top5_line":["「いつも受け止めてくれてありがとう」","「一緒にいると世界が広がる」","「あなたの気持ち、聞かせて」",
              "「あなたのこと、ちゃんと見てるよ」","「一緒にいると楽しい！」"],
 "top5_common":"5タイプに共通するのは「あなたの愛情をきちんと受け取り、お返しできる人」であること。一方的に与えるだけの関係ではなく、循環する愛情こそが、あなたを満たしてくれます。",
 "worst":[("課題","どちらも行動的だが、ESTPはスピードと刺激の人。あなたの心の充電が追いつかず、寄り添う余裕を失いやすい。",
           "対策","「今日は静かに過ごしたい」を早めに宣言。テンポの違いは、先に共有しておけば衝突になりません。"),
          ("課題","安定志向は似ているが、ISTJは感情表現が最小限。あなたの気遣いが言葉で返ってこず、「伝わっているのか」が見えにくい。",
           "対策","気持ちではなく「事実」で伝え合う。「週1で電話したい」など具体的な希望に翻訳すると、誠実に応えてくれます。"),
          ("課題","どちらも面倒見がよく責任感が強いが、ESTJは正論で解決しようとする。あなたの「気持ちを聞いてほしい」とすれ違いやすい。",
           "対策","話す前に「解決策じゃなくて、ただ聞いてほしい」と一言添える。目的を共有すれば、頼れる味方になります。")],
 "worst_line":[("◎「今日は一緒にのんびりしたい」","✕「ちょっと落ち着いてほしい」"),
               ("◎「あなたの誠実さ、ちゃんと伝わってる」","✕「もっと気持ちを言葉にしてよ」"),
               ("◎「聞いてくれるだけで助かる」","✕「正論はもういいから」")],
 # CH07 LINE
 "line_aru":["長文で気持ちをしっかり伝える","スタンプや絵文字で感情豊かに","相手の様子をすぐ気にかける",
             "すぐ返信したくなる","既読がつかないと少し心配になる"],
 "line_sign":["毎日連絡を取りたくなる","相手の予定を覚えていて聞く","褒め言葉が増える",
              "「会いたい」を素直に伝える","相手の好きなものをリサーチする"],
 "line_ng":["相手の負担を考えず尽くしすぎる","既読がつかないと連投してしまう","自分の気持ちを後回しにし続ける"],
 "line_ok":["「無理しないでね」で寄り添う","返信ペースは相手に合わせる","「実は私も…」と自分の話もする"],
 "omamori":[("心配しすぎた時","「気になったから連絡してみたよ」"),
            ("尽くしすぎた時","「私もこうしたかったから、気にしないで」"),
            ("本音を言いたい時","「実は私も、こう思ってたんだ」")],
 "line_talk":[("them","今日はちょっと疲れた…","19:04"),
              ("me","お疲れさま！無理しないでね、力になれることあったら言って","19:05"),
              ("them","ありがとう、それだけで元気出た","19:06")],
 "line_recv":"あなたは与えるのは得意でも、受け取るのが苦手。「ありがとう、助かる」と素直に甘えることも愛情です。たまには「○○してほしいな」と言ってみて——受け取る姿は、相手を安心させます。",
 "templates":[("デートに誘う","「今度〇〇行かない？ あなたとなら楽しそう」"),
              ("やんわり断る","「その日は難しいけど、また誘ってね」"),
              ("謝る","「言葉足らずでごめん。本当はこう思ってた」")],
 # CH08
 "fight_pat":[("笑顔で本音を隠す","傷ついていても「大丈夫」と笑顔を作ってしまい、相手は問題に気づかない。後から不満が一気に出ることも。"),
              ("抱え込んで疲弊する","ケンカの後も相手のために気を遣い続け、自分の心が回復する時間を取れない。"),
              ("過度に自分を責める","関係がうまくいかないと「自分のせいだ」と思いすぎ、自己否定が強くなる。")],
 "makeup3":[("「実は」と本音を言ってみる","笑顔の下の本当の気持ちを、信頼できる相手にだけは見せてみる。完璧でいる必要はない。"),
            ("自分のための時間を取る","仲直りを急がず、まず自分の心を休める。自分を満たしてから向き合う方がうまくいく。"),
            ("「私のせいじゃないかも」と考える","すべてを自分の責任にせず、相手にも責任の一部があると認める。バランスの取れた視点を。")],
 "kentai":"「寄り添っているのに満たされない…」という感覚が倦怠期のサイン。与えることに疲れているなら、それは伝えていいサイン。自分の欲求を伝えることは、関係を深める第一歩です。",
 "refire":[("「してほしい」を伝える","与えるだけでなく、受け取る日をつくる。甘えも愛情。"),
           ("感謝を言葉で交換","「ありがとう」を二人で言い合う習慣をつくる。"),
           ("自分を満たす日","寄り添いを少し休んで、自分のための時間を持つ。")],
 # CH09
 "marry_cond":[("あなたの気遣いに感謝を伝える人","「ありがとう」の言葉が、あなたの愛情を循環させる燃料になる。"),
               ("あなたの本音を引き出してくれる","笑顔の裏の本当の気持ちに気づき、言葉にする手助けをしてくれる人。"),
               ("時には甘えさせてくれる","与えるだけでなく、受け取る側にもなれる関係を作ってくれる人。"),
               ("人との関わりを尊重してくれる","友人関係や交流の広さを、嫉妬ではなく魅力として見てくれる人。"),
               ("一緒に成長を楽しめる","お互いに与え合いながら、人として成長していける関係を望む人。")],
 "chosen":[("毎日が記念日になる","尽くし度★5のあなたに選ばれた人は、日々の小さな愛情表現に満たされ続ける。"),
           ("心がほどける場所ができる","あなたとの関係は、相手にとって世界でいちばん安心できる居場所になる。"),
           ("本気の愛情を独占できる","一途度★4のあなたが選んだ相手は、誰にも奪われない特別な愛情を受け取れる。")],
 "marry_q":["お金の使い方・将来の貯め方は？","家族・親との距離感は？","子ども・暮らしの理想像は？",
            "一人時間と二人時間のバランスは？","ケンカの時、どう仲直りしたい？"],
 # CH10-12
 "attach_main":"基本は安定型。人を信じ、愛情を惜しみなく注げます。ただし「相手の役に立てているか」が自信の支えになっているため、寄り添っても反応が薄いと一気に不安型へ傾き、見捨てられ不安が顔を出します。",
 "anx_moment":["既読がついても返信がしばらく来ない","「ありがとう」が返ってこない",
               "相手が一人の時間を欲しがる","寄り添っているのに距離を感じる"],
 "anx_rx":["自分の価値を「役立つか」で測らない","返信の遅さ＝愛情の薄さ、ではない",
           "与える前に、まず受け取ってみる","相手の「一人時間」を信頼の証と捉える"],
 "give_lang":[("サービス行為","最も強い"),("肯定の言葉","強い"),("クオリティタイム","中"),
              ("スキンシップ","低"),("贈り物","低")],
 "recv_lang":[("肯定の言葉","最も欲しい"),("クオリティタイム","欲しい"),("スキンシップ","中"),
              ("サービス行為","中"),("贈り物","低")],
 "aruaru":["好きな人の機嫌をすぐ察してしまう","相手の長所を本気で見つけるのが得意",
  "つい世話を焼きすぎて重いと言われる","自分の弱音は最後まで言えない","恋人の友達にも好かれようとする",
  "頼られると断れない","ケンカの後すぐ自分から謝ってしまう","相手の予定に自分を合わせがち",
  "連絡が来ないと「何かした？」と考えてしまう","悩み相談を受けると放っておけない",
  "LINEの返信は丁寧で長め","「あなたのため」が口癖になりがち","恋人ができると一気にのめり込む",
  "別れた後も相手の幸せを願ってしまう","「重い」と「冷たい」の間で揺れる",
  "「で、あなたはどうしたい？」と聞かれると困る","感謝されると一週間がんばれる",
  "相手の元恋人の話まで覚えている","「嫌われたかも」で頭がいっぱいになる","記念日は誰よりも本気で準備する",
  "相手の成長が自分のことのように嬉しい","本音より「丸く収まる」言い方を選ぶ","「いい人」で終わった経験がある",
  "デートのプランをつい完璧に組んでしまう","周りから恋愛相談をよく持ちかけられる","相手の小さな変化によく気づく",
  "尽くした分だけ見返りを期待してしまう","別れ話を自分からは切り出せない","褒められると謙遜して受け取れない",
  "結局、人を幸せにするのが一番好き"],
 "pitfalls":[("付き合った途端、追いすぎて重くなる","安心したい一心で、連絡・予定を詰めすぎてしまう。",
              "相手の返信ペースに合わせる。「会えない時間」も信頼の練習。"),
             ("追いかけるべきでない相手に尽くす","「私が支えれば変わる」と、応えてくれない人に注ぎ込む。",
              "“与えた分が返ってくるか”で見極める。尽くす相手は選んでいい。"),
             ("別れ際を引きずり、決断が遅れる","相手を傷つけたくなくて、終わった関係にもしがみつく。",
              "「優しさ」と「情」を分ける。区切りをつけるのも相手への誠実。"),
             ("SNSを見て一喜一憂してしまう","相手の投稿・既読・オンライン表示を深読みして不安になる。",
              "通知をオフに。見る回数を決め、“画面の中の相手”で判断しない。")],
 "pitfall_quote":"愛とは、相手をどう変えるかではなく、<br>自分の優しさをどこへ向けるか。",
 "triangle":[("親密性",90,"とても高い","心を通わせ、深くつながる力は抜群。"),
             ("コミットメント",85,"高い","一度決めた相手に寄り添い続ける責任感。"),
             ("情熱",65,"中","燃え上がりより、穏やかな愛情が長く続く。")],
 "bigfive":[("協調性","Agreeableness",92,"思いやりと共感の塊。相手を優先しすぎる傾向にも注意。"),
            ("外向性","Extraversion",88,"人とのつながりが活力源。場をあたためる力がある。"),
            ("誠実性","Conscientiousness",80,"約束を守り、関係に責任を持つ。記念日も大切にする。"),
            ("開放性","Openness",70,"理想を描き、相手の可能性を信じる想像力がある。"),
            ("神経症傾向","Neuroticism",55,"普段は穏やか。ただし「嫌われ不安」で揺れやすい一面も。")],
 "cogfn":[("Fe","主導機能","外向的感情","相手の感情を瞬時に察知し、場を整える。「相手が何を求めているか」が自然にわかる、ENFJ最大の武器。恋愛では究極の気配り上手に。"),
          ("Ni","補助機能","内向的直観","関係の「未来像」を描く。この人とどうなりたいか、深いビジョンを持つ。一途で、相手の本質を見抜く洞察力にもなる。"),
          ("Se","第三機能","外向的感覚","今この瞬間を楽しむ力。デートや体験の共有でぐっと距離が縮まる。発達すると恋にメリハリと情熱が生まれる。"),
          ("Ti","劣等機能","内向的思考","ストレス時の弱点。感情で動くあなたが追い詰められると、急に理屈っぽく相手を分析・批判してしまうことが。疲れたら一人で休む時間を。")],
 # APPENDIX
 "reunite_type":[("ペルシャ（INFP）","価値観に寄り添う。復縁ワードより「あなたの世界を大切にしたい」という本心を静かに。急かさない。"),
                 ("ソマリ（ENFP）","楽しさで惹き直す。新しい体験に軽く誘い「一緒だと面白い」を再体感させる。重い話は厳禁。"),
                 ("ロシアンブルー（INFJ）","深い対話で。なぜ別れたかを一緒に内省し、表面でなく本質の理解を示す。誠実さが鍵。"),
                 ("シャルトリュー（INTP）","感情でなく論理で。別れの原因を冷静に分析し「何をどう変えたか」を具体的に示す。"),
                 ("デボンレックス（ENTP）","退屈させない。新しい話題と刺激で「一緒だと飽きない」を再認識。軽い議論も楽しんで。"),
                 ("ノルウェージャン（INTJ）","感情でなく論理で。分析を一旦封じ、変化を事実で示す。追わずに待つ姿勢が効く。"),
                 ("ラグドール（ISFJ）","焦らせず、穏やかに。安心できる距離から少しずつ。変わらぬ優しさを静かに見せ続ける。"),
                 ("バーマン（ESFJ）","誠実さと安心感。こまめな連絡と感謝を取り戻し「大切にされる」実感を丁寧に積む。"),
                 ("ブリティッシュ（ISTJ）","言葉より一貫した行動で。約束を守り、変わった姿を時間をかけて証明する。")],
 "breakup_fix":[("抱え込みすぎた","しんどさを見せず、限界で終わらせていた。戻る時は「弱音を先に渡す」ことから始める。"),
                ("自分を後回しにした","我慢を溜めて爆発しがち。本音を小出しに伝える練習をしてから再接触する。"),
                ("甘えられなかった","頼らなさが距離を生んだ。「あなたに頼りたい」と言える関係を目指す。")],
 "promise3":[("我慢を溜めない","不満は小さいうちに言葉に。爆発させない代わりに、こまめに本音を渡す。"),
             ("相手の領域を守る","尽くしすぎず、相手の時間・友人・自由を尊重。重さは少し引いて。"),
             ("月一の本音タイム","定期的に気持ちをすり合わせる時間を。すれ違いが大きくなる前に整える。")],
 "sns3":[("「見ている」を活かす","頑張り・挑戦の投稿にだけ短く温かい反応。応援はあなたにしか出せない誠実さ。"),
         ("世話焼きを我慢","「大丈夫？」のDMはこらえる。先回りせず、相手から頼られるまで待つ余裕を。"),
         ("聞き役を封印","尽くす側に戻らず、自分の充実をたまに見せる。温度が戻ったら早めにSNSの外へ。")],
 "closing":"あなたが与える愛は、<br>世界をあたためる才能です。",
 "enfj_msg":"あなたは「もっと寄り添えば戻れる」と考えがち。でも復縁に必要なのは尽くす量ではなく、二人が変わること。取り戻すより、お互いが成長して再会できるかを見てください。",
}

# ══════════════════════════════════════════════════════════════
#  追加CSS（専用レイアウト）
# ══════════════════════════════════════════════════════════════
CSS += """
/* 表紙 */
.cover{display:flex;flex-direction:column;align-items:center;text-align:center;height:100%;
  padding-top:8mm}
.cov-top{font-size:7.88pt;letter-spacing:.4em;color:var(--wine2)}
.cov-top .ln{display:inline-block;width:9mm;border-top:.5pt solid var(--wine-l);vertical-align:middle;margin:0 3mm}
.cov-ped{font-family:'Cormorant Garamond',serif;font-size:9.0pt;letter-spacing:.42em;color:var(--ink3);margin-top:3mm}
.cov-medal{width:52mm;height:52mm;border-radius:50%;border:.8pt solid var(--wine-l);
  margin:9mm auto 0;display:flex;align-items:center;justify-content:center;position:relative;background:var(--paper)}
.cov-medal::before{content:"";position:absolute;inset:2.2mm;border-radius:50%;border:.4pt solid var(--gold-l)}
.cov-medal img{width:41mm;height:41mm;border-radius:50%;object-fit:cover}
.cov-breed-en{font-family:'Cormorant Garamond',serif;font-size:9.0pt;letter-spacing:.32em;
  color:var(--ink3);margin-top:5mm}
.cov-sub{font-size:10.69pt;letter-spacing:.42em;color:var(--ink2);margin-top:6mm}
.cov-name{font-size:31.5pt;font-weight:700;color:var(--wine);letter-spacing:.1em;margin-top:4mm}
.cov-ln{width:18mm;border-top:.6pt solid var(--wine-l);margin:5mm auto}
.cov-code{font-size:12.38pt;letter-spacing:.42em;color:var(--ink2)}
.cov-lead{font-size:9.0pt;line-height:2.2;color:var(--ink2);margin-top:6mm}
.cov-seal{width:26mm;height:26mm;border:.6pt solid var(--wine-l);border-radius:1.5mm;
  margin:auto auto 0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1mm}
.cov-seal .s1{font-family:'Cormorant Garamond',serif;font-size:6.3pt;letter-spacing:.22em;color:var(--wine-l)}
.cov-seal .paw{font-size:12.38pt;color:var(--wine-l)}
.cov-bot{font-size:11.25pt;letter-spacing:.42em;color:var(--wine);margin-top:7mm}
.cov-bot2{font-size:6.52pt;letter-spacing:.3em;color:var(--ink3);margin-top:2.5mm}

/* もくじ */
.toc-part{font-size:7.88pt;letter-spacing:.3em;color:var(--wine-l);border-bottom:.5pt solid var(--rule);
  padding-bottom:1.2mm;margin:3.6mm 0 2mm;display:flex;justify-content:space-between}
.toc-part b{color:var(--wine);font-weight:700;letter-spacing:.2em}
.toc-row{display:flex;align-items:baseline;font-size:8.44pt;padding:.95mm 0;color:var(--ink2)}
.toc-row .dots{flex:1;border-bottom:.4pt dotted var(--ink3);margin:0 2mm;opacity:.5}
.toc-row .n{font-family:'Cormorant Garamond',serif;color:var(--wine2);font-size:8.78pt}

/* イントロ */
.intro-card{background:var(--paper);border:.5pt solid var(--rule);border-radius:1mm;padding:3mm;text-align:center}
.intro-card .ic{font-size:13.5pt;color:var(--wine-l)}
.intro-card .it{font-size:8.33pt;font-weight:700;color:var(--wine);margin:1.4mm 0 1mm}
.intro-card p{font-size:7.65pt;line-height:1.8;color:var(--ink2)}
.warnbar{border:.5pt solid var(--pinkbd);background:var(--pink);border-radius:1mm;
  padding:2mm 3mm;font-size:7.42pt;color:var(--ink2);line-height:1.8;margin-top:3mm}

/* 相性マップ */
.cmap-grp{margin-bottom:2.6mm}
.cmap-h{font-size:7.65pt;letter-spacing:.24em;color:var(--wine-l);margin-bottom:1.4mm}
.cmap-row{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm}
.cbox{background:var(--paper);border:.5pt solid var(--rule);border-radius:1mm;padding:1.8mm 2mm;text-align:center}
.cbox.you{background:var(--wine);border-color:var(--wine)}
.cbox.you .cb-b,.cbox.you .cb-s,.cbox.you .cb-c{color:#fff}
.cbox .cb-b{font-size:6.3pt;color:var(--ink2);line-height:1.35;min-height:7.6mm;
  display:flex;align-items:center;justify-content:center}
.cbox .cb-s{font-family:'Cormorant Garamond',serif;font-size:14.62pt;color:var(--wine);line-height:1}
.cbox .cb-c{font-size:6.3pt;letter-spacing:.14em;color:var(--ink3);margin-top:.6mm}
.legend{display:flex;gap:3mm;justify-content:center;font-size:6.75pt;color:var(--ink3);margin:2mm 0}
.legend i{font-style:normal;color:var(--wine2)}

/* TOP5 */
.t5{display:flex;gap:2.6mm;align-items:flex-start;border-bottom:.4pt dotted var(--rule);padding:2mm 0}
.t5 .rk{font-family:'Cormorant Garamond',serif;font-size:16.88pt;color:var(--wine-l);width:6mm;flex:none;line-height:1}
.t5 .t5b{flex:1}
.t5 .t5n{font-size:9.0pt;font-weight:700;color:var(--wine)}
.t5 .t5n small{font-size:7.2pt;color:var(--ink3);letter-spacing:.14em;margin-left:2mm}
.t5 .t5c{font-size:7.88pt;line-height:1.8;color:var(--ink2);margin-top:.6mm}
.t5 .t5s{font-family:'Cormorant Garamond',serif;font-size:15.75pt;color:var(--wine2);flex:none}

/* バー */
.bar{height:2.4mm;background:var(--cream2);border-radius:99px;overflow:hidden;margin-top:1mm}
.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--wine-l),var(--wine2));border-radius:99px}
.brow{margin-bottom:2.4mm}
.brow .bh{display:flex;justify-content:space-between;font-size:8.1pt;color:var(--ink2)}
.brow .bh b{color:var(--wine);font-weight:700}
.brow .bh .v{font-family:'Cormorant Garamond',serif;font-size:10.12pt;color:var(--wine2)}
.brow p{font-size:7.42pt;color:var(--ink3);line-height:1.7;margin-top:.7mm}

/* LINE風 */
.chat{background:var(--paper);border:.5pt solid var(--rule);border-radius:1.4mm;padding:2.6mm}
.chat .ch-h{font-size:7.2pt;color:var(--ink3);border-bottom:.4pt solid var(--rule);
  padding-bottom:1.2mm;margin-bottom:2mm;letter-spacing:.1em}
.bub{max-width:74%;font-size:7.76pt;line-height:1.75;padding:1.8mm 2.4mm;border-radius:2mm;margin-bottom:1.8mm}
.bub.them{background:var(--cream2);color:var(--ink)}
.bub.me{background:var(--pink);border:.4pt solid var(--pinkbd);margin-left:auto;color:var(--ink)}
.bub .tm{display:block;font-size:6.08pt;color:var(--ink3);margin-top:.6mm}

/* あるある30 */
.aru-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 5mm}
.aru-i{display:flex;gap:1.8mm;font-size:7.9pt;line-height:1.8;padding:1.72mm 0;
  border-bottom:.35pt dotted var(--rule);color:var(--ink2)}
.aru-i .an{font-family:'Cormorant Garamond',serif;color:var(--wine-l);font-size:7.42pt;width:4mm;flex:none}

/* ワーク罫線 */
.wline{border-bottom:.5pt solid var(--rule);height:7.5mm}
.wbox{background:var(--paper);border:.5pt solid var(--rule);border-radius:1mm;padding:2.6mm 3mm;margin-top:1.6mm}
.wlabel{font-size:8.1pt;font-weight:700;color:var(--wine);margin:3mm 0 1.4mm;display:flex;gap:2mm;align-items:center}

/* フローチャート */
.flow-q{background:var(--cream2);border:.5pt solid var(--gold-l);border-radius:1mm;
  padding:1.8mm 3mm;font-size:8.33pt;font-weight:700;color:var(--wine);text-align:center}
.flow-ar{text-align:center;color:var(--wine-l);font-size:7.88pt;margin:1.2mm 0}
.flow-2{display:grid;grid-template-columns:1fr 1fr;gap:2.6mm;margin-top:1.6mm}
.flow-b{border:.5pt solid var(--rule);background:var(--paper);border-radius:1mm;padding:1.8mm 2.4mm}
.flow-b .fl{font-size:6.98pt;letter-spacing:.14em;color:var(--wine-l);display:block;margin-bottom:.7mm}
.flow-b p{font-size:7.76pt;line-height:1.75;color:var(--ink2)}
.flow-goal{background:var(--wine);color:#fff;border-radius:1mm;padding:2.2mm;text-align:center;
  font-size:9.0pt;font-weight:700;letter-spacing:.1em;margin-top:2.4mm}

/* 比較表 */
.cmp{width:100%;border-collapse:collapse;font-size:7.76pt}
.cmp th{background:var(--cream2);color:var(--wine);font-weight:700;padding:1.6mm 2mm;
  border:.4pt solid var(--rule);letter-spacing:.08em;font-size:7.42pt}
.cmp td{padding:1.5mm 2mm;border:.4pt solid var(--rule);line-height:1.7;color:var(--ink2);vertical-align:top}
.cmp td.lb{background:var(--paper);color:var(--wine2);font-weight:700;white-space:nowrap;width:20mm}

/* 章扉 */
.divider{display:flex;flex-direction:column;justify-content:center;align-items:center;
  height:100%;text-align:center}
.divider .dl{font-size:7.65pt;letter-spacing:.4em;color:var(--wine-l)}
.divider h2{font-size:24.75pt;font-weight:700;color:var(--wine);line-height:1.6;margin-top:6mm;letter-spacing:.08em}
.divider .dp{font-size:8.78pt;line-height:2.1;color:var(--ink2);margin-top:5mm;max-width:120mm}
.divider .dlist{margin-top:9mm;font-size:8.33pt;letter-spacing:.2em;color:var(--ink2);line-height:2.6}
.divider .dq{margin-top:11mm;font-size:9.0pt;line-height:2.1;color:var(--wine2);font-style:italic}
.divider .dq small{display:block;font-family:'Cormorant Garamond',serif;font-size:7.42pt;
  letter-spacing:.24em;color:var(--ink3);margin-top:3mm;font-style:normal}
.refs{border-top:.5pt solid var(--rule);margin-top:3mm;padding-top:2.4mm}
.refs .rh{font-size:6.98pt;letter-spacing:.24em;color:var(--wine-l);margin-bottom:1.6mm}
.refs .rg{display:grid;grid-template-columns:1fr 1fr;gap:.8mm 4mm;font-size:6.75pt;color:var(--ink3);line-height:1.7}
"""

# ══════════════════════════════════════════════════════════════
#  各ページ
# ══════════════════════════════════════════════════════════════
def build(code, C, img_b64):
    d = LOC[code]; P = PARAM[code]; rk = ranking(code)
    B = d["breed"]; R = d["role"]
    pages = []
    A = pages.append
    PL = ["一途度","尽くし度","結婚向き","嫉妬深さ","ドキドキ度"]

    # ── P1 表紙 ──
    A(page(code, f'''<div class="cover">
      <div class="cov-top"><span class="ln"></span>恋愛血統書・完全版<span class="ln"></span></div>
      <div class="cov-ped">{sp("PEDIGREE")}&nbsp;&nbsp;{sp("No."+C["pedigree"])}</div>
      <div class="cov-medal"><img src="data:image/webp;base64,{img_b64}"></div>
      <div class="cov-breed-en">{sp(B[:12])}</div>
      <div class="cov-sub">{C["subtitle"]}</div>
      <div class="cov-name">{B}</div>
      <div class="cov-ln"></div>
      <div class="cov-code">{sp(code)}　·　{R}</div>
      <div class="cov-lead">{C["cover_lead"]}</div>
      <div class="cov-seal"><div class="s1">{code}</div><div class="paw">🐾</div>
        <div class="s1">No.{C["pedigree"]}</div></div>
      <div class="cov-bot">恋愛攻略書</div>
      <div class="cov-bot2">{sp("PREMIUM EDITION")}　·　16にゃんこ恋愛診断</div>
    </div>''', cls="cover-pg"))

    # ── P2 この本の使い方 ──
    cards = "".join(f'''<div class="intro-card"><div class="ic">{ic}</div>
      <div class="it">{t}</div><p>{p}</p></div>''' for ic,t,p in [
        ("♡","恋愛傾向の深掘り","外からは見えない内面の動きまで、余すことなく解説。"),
        ("★","全16タイプ相性表","スコア＋詳細コメントで「その人との相性」がわかる。"),
        ("✉","LINE攻略ガイド","あなたのLINEのクセと、相手への効果的な送り方。"),
        ("✎","書き込みワーク","読むだけで終わらない。自分の恋を整理する3つのシート。")])
    A(page(code, f'''<p class="lead">この「恋愛攻略書」は、あなた（{B} / {code}）の恋愛をとことん深掘りした、専用の取扱説明書です。無料版が“入口”なら、これは恋愛のすべてを網羅した完全版。あなたの無自覚なクセ・恋愛の罠・相性のいい相手の秘密まで解説します。</p>
      <div class="grid2" style="grid-template-columns:repeat(4,1fr);gap:2.4mm">{cards}</div>
      <div class="sect-h">{sp("GUIDE")}　読み方のコツ</div>
      <div class="grid3">
        <div class="panel"><div class="pt">① まず通し読み</div><p>P4〜P12（基礎編）を一度さらっと読んで、全体像をつかむ。</p></div>
        <div class="panel"><div class="pt">② 気になる人のページへ</div><p>好きな人ができたら、相性ページを見る。</p></div>
        <div class="panel"><div class="pt">③ ワークに書き込む</div><p>P22〜24に自分の言葉で書くと頭が整理される。</p></div>
      </div>
      <div class="sect-h">♢　この攻略書で、あなたが手に入れられること</div>
      <div class="grid3">
        <div class="panel pink"><div class="pt">自己理解</div><p>自分の恋愛のクセを知り、繰り返してきたパターンの理由がわかる。</p></div>
        <div class="panel pink"><div class="pt">相手選び</div><p>16タイプとの相性を知り、自分に合う人の見極め方がわかる。</p></div>
        <div class="panel pink"><div class="pt">伝える力</div><p>本音を我慢せず、相手を傷つけずに気持ちを伝える方法が身につく。</p></div>
      </div>
      <div class="warnbar">⚠　本書の内容はエンターテインメント目的です。心理学的・医学的な診断ではありません。自分を知る楽しみとして気軽にお読みください。</div>
      {note("恋愛雑学","心理学では、自分の気持ちを「言葉にする」だけでストレスが下がるとされています（感情ラベリング効果）。人に寄り添うあなたにこそ必要なセルフケアです。")}''',
      chapno="00", clabel=sp("INTRODUCTION"), title="この本の使い方", pno="02"))

    # ── P3 もくじ ──
    def toc(rows):
        return "".join(f'<div class="toc-row"><span>{t}</span><span class="dots"></span><span class="n">{n}</span></div>' for t,n in rows)
    A(page(code, f'''<p class="lead">全7部構成のあなた専用ガイドです。気になる章から開いても、頭から通し読みしても。基礎編で全体像を、理論編で深掘り、ワークで整理、巻末特集で復縁まで。</p>
      <div class="grid2" style="gap:6mm">
       <div>
        <div class="toc-part"><b>{sp("PART I")}</b><span>基礎編</span></div>
        {toc([(f"{B}という恋愛人格","04"),("恋に落ちるまでの5段階","05"),("無自覚なクセと恋愛の罠","06"),
              ("全16タイプ 相性マップ","07"),("ベスト相性 TOP5","08"),("要注意タイプとの付き合い方","09"),
              ("LINE・メッセージ攻略","10"),("ケンカ・倦怠期の乗り越え方","11"),("結婚観と長続きの条件","12")])}
        <div class="toc-part"><b>{sp("PART II")}</b><span>理論編</span></div>
        {toc([("あなたの愛着スタイル","14"),("相手のタイプ別・接し方","15"),("あなたの「愛の言語」","16"),
              (f"{code} 恋愛あるある30","17"),("恋の落とし穴と処方箋","18")])}
       </div>
       <div>
        <div class="toc-part"><b>{sp("THEORY")}</b><span>理論編 つづき</span></div>
        {toc([("恋愛の三角理論","19"),("ビッグファイブ恋愛分析","20"),("認知機能でみる恋愛","21")])}
        <div class="toc-part"><b>{sp("WORK")}</b><span>書き込みワーク</span></div>
        {toc([("理論で自己分析シート","22"),("理想と現実の棚卸しシート","23"),("本音を伝える練習シート","24")])}
        <div class="toc-part"><b>{sp("APPENDIX")}</b><span>巻末特集</span></div>
        {toc([("ケンカ仲直りフローチャート","25"),("復縁という選択","26"),("復縁の見極め","27"),
              ("復縁テクニック実践編","28"),("タイプ別・復縁アプローチ","29"),("復縁とSNS","30"),
              ("復縁とSNS 実践編","31")])}
       </div>
      </div>
      {note("読み方","迷ったら基礎編（P4〜P12）から。恋の悩みが具体的なら、巻末特集に直行してOKです。")}''',
      chapno="♢", clabel=sp("CONTENTS"), title="もくじ", pno="03"))

    # ── P4 CH01 恋愛人格 ──
    core = "".join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in C["core"])
    stat = "".join(f'<div class="strow"><span>{PL[i]}</span>{stars(P[i])}</div>' for i in range(5))
    kw = "".join(f'<span class="tag">#{k}</span>' for k in C["keywords"])
    tk = "".join(f'<li>{x}</li>' for x in C["tokimeki"])
    jr = "".join(f'<li>{x}</li>' for x in C["jirai"])
    ft = "".join(f'<span class="it">♡　{t}</span>' for t in C["free_tags"])
    A(page(code, f'''<div class="freeband"><span class="fb-h"><span class="fb-t">{sp("FREE ver.")}</span>無料版のおさらい</span>{ft}</div>
      <div class="centernote">＼ 無料版でわかるのはここまで。ここから先が、有料版だけの“深掘り”です ／</div>
      <div class="grid2">
        <div class="panel"><div class="pt">▶　外から見えるあなた</div><p>{C["outside"]}</p></div>
        <div class="panel pink"><div class="pt">▶　内側の本当のあなた</div><p>{C["inside"]}</p></div>
      </div>
      <div class="grid2" style="grid-template-columns:52mm 1fr;margin-top:3.4mm">
        <div class="stat"><div class="sh">恋愛ステータス</div>{stat}</div>
        <div><div class="pt" style="font-size:7.88pt;font-weight:700;color:var(--wine);letter-spacing:.1em;margin-bottom:1.8mm">コアバリュー　3つの軸</div>
          <dl class="deflist">{core}</dl></div>
      </div>
      <p class="lead" style="margin-top:3mm">{C["core_lead"]}</p>
      <div style="font-size:7.42pt;letter-spacing:.2em;color:var(--wine-l);margin-bottom:1.4mm">あなたの恋愛を表すキーワード</div>
      <div>{kw}</div>
      <div class="sect-h">{B}の“ときめき”＆“地雷”スイッチ</div>
      <div class="grid2">
        <div class="panel pink"><div class="pt">♡　グッとくる瞬間</div><ul class="check">{tk}</ul></div>
        <div class="panel"><div class="pt">✕　一気に冷める瞬間</div><ul class="check ng">{jr}</ul></div>
      </div>
      {note("豆知識",f"MBTIの{code}型は全人口の約{RARITY[code]}%という希少なタイプ。カリスマ性と献身を両立できる人は、実はとても珍しい存在です。")}''',
      chapno="01", clabel=f'{sp("CHAPTER")}　0 1', title=f"{B}という恋愛人格", pno="04"))

    # ── P5 CH02 5段階 ──
    stg = "".join(f'''<div class="cbox"><div class="cb-s">0{i+1}</div>
      <div style="font-size:8.33pt;font-weight:700;color:var(--wine);margin:.8mm 0 .6mm">{t}</div>
      <div style="font-size:7.2pt;line-height:1.65;color:var(--ink2)">{s}</div></div>'''
      for i,(t,s) in enumerate(C["stages"]))
    spd = "".join(f'''<div class="cbox"><div style="font-size:10.12pt;color:var(--wine);font-weight:700">{v}</div>
      <div class="cb-c">{k}</div></div>''' for v,k in C["speed"])
    lv = "".join(f'<div class="panel pink"><div class="pt">♡　{t}</div><p>{s}</p></div>' for t,s in C["loved"])
    A(page(code, f'''<div class="freeband"><span class="fb-h"><span class="fb-t">{sp("FREE ver.")}</span>無料版のおさらい</span>
        <span class="it">無料版では「寄り添って愛されるタイプ」と一言紹介しただけ。</span></div>
      <div class="panel" style="margin-bottom:3.2mm"><div class="pt">{sp("PREMIUM")}　・　この章で深掘りすること</div>
        <p>恋に落ちる“5段階”の心の動きを一つずつ解剖。各段階の「罠」と「強み」、恋愛スピードの特徴まで踏み込みます。</p></div>
      <div class="cmap-row" style="grid-template-columns:repeat(5,1fr)">{stg}</div>
      <div class="grid2" style="margin-top:3.4mm">
        <div class="panel"><div class="pt">注意　尽くしすぎの罠</div><p>{C["stage_warn"]}</p></div>
        <div class="panel pink"><div class="pt">強み　{sp("Stage 4")}の率直さ</div><p>{C["stage_str"]}</p></div>
      </div>
      <div class="sect-h">{sp("DATA")}　{B}の恋愛スピード</div>
      <div class="cmap-row" style="grid-template-columns:repeat(3,1fr)">{spd}</div>
      <div class="sect-h">寄り添うあなたが、愛される理由</div>
      <div class="grid3">{lv}</div>
      {note("ワンポイント","「単純接触効果」では、人は何度も接する相手に好意を持ちやすいとされます。あなたの気配りの多さは、自然と相手の好意を育てています。")}''',
      chapno="02", clabel=f'{sp("CHAPTER")}　0 2', title="恋に落ちるまでの5段階", pno="05"))

    # ── P6 CH03 罠 ──
    flip = "".join(f'''<div class="panel"><div style="font-size:7.2pt;color:var(--ink3)">{a}　↓</div>
      <div class="pt" style="margin:.8mm 0 .8mm">{b}</div><p>{c}</p></div>''' for a,b,c in C["trap_flip"])
    tr = ""
    for i,(nm,sub,body,sol) in enumerate(C["traps"]):
        tr += f'''<div class="panel {"pink" if i%2==0 else ""}" style="margin-bottom:2.4mm">
          <div style="display:flex;gap:2.4mm;align-items:baseline">
            <span style="font-size:6.75pt;letter-spacing:.2em;color:var(--wine-l)">罠 ⓪{i+1}</span>
            <b style="font-size:9.45pt;color:var(--wine)">{nm}</b>
            <span style="font-size:7.65pt;color:var(--ink3)">{sub}</span></div>
          <p style="margin-top:1.2mm">{body}</p>
          <p style="margin-top:1.4mm;padding-top:1.4mm;border-top:.4pt dotted var(--rule);font-size:7.99pt">
            <b style="color:var(--wine2);letter-spacing:.14em;font-size:7.2pt">{sp("SOLUTION")}</b>　{sol}</p></div>'''
    tr = tr.replace("罠 ⓪1","罠 ①").replace("罠 ⓪2","罠 ②").replace("罠 ⓪3","罠 ③")
    A(page(code, f'''<div class="freeband"><span class="fb-h"><span class="fb-t">{sp("FREE ver.")}</span>無料版のおさらい</span>
        <span class="it">無料版では「気をつけたいところ」を3語で示しただけ。</span></div>
      <div class="panel" style="margin-bottom:3mm"><div class="pt">{sp("PREMIUM")}　・　この章で深掘りすること</div>
        <p>3つの罠を「原因 → 具体例 → 対策」まで分解。優しさを空回りさせず、魅力に変える具体策まで提示します。</p></div>
      <div style="font-size:8.1pt;color:var(--wine);font-weight:700;margin-bottom:1.8mm">でも、忘れないで。罠は「才能の裏返し」</div>
      <div class="grid3" style="margin-bottom:3mm">{flip}</div>
      {tr}
      {note("恋愛雑学","研究では、適度な自己開示はむしろ親密度を高めるとされています。「本音を見せる」ことは、関係を深める有効な戦略です。")}''',
      chapno="03", clabel=f'{sp("CHAPTER")}　0 3', title="無自覚なクセと恋愛の罠", pno="06"))

    # ── P7 CH04 相性マップ ──
    grp_html = ""
    for g, members in GROUPS.items():
        gname = {"NT":"思考家","NF":"理想家","SJ":"堅実家","SP":"行動家"}[g]
        cells = ""
        ms = members + ([code] if code in GROUPS.get(code[1]+code[2] if False else "", []) else [])
        show = members if code not in members else members
        for m in members:
            if m == code: continue
            cells += f'''<div class="cbox"><div class="cb-b">{BREED[m]}</div>
              <div class="cb-s">{compat(code,m)}</div><div class="cb-c">{sp(m)}</div></div>'''
        if code in members:
            cells += f'''<div class="cbox you"><div class="cb-b">{B}</div>
              <div class="cb-s">{sp("YOU")}</div><div class="cb-c">{sp(code)}</div></div>'''
        grp_html += f'''<div class="cmap-grp"><div class="cmap-h">{sp(g)}　{gname}</div>
          <div class="cmap-row">{cells}</div></div>'''
    gc = "".join(f'''<div class="panel"><div class="pt">{g} {n}</div><p>{C["grp_comment"][g]}</p></div>'''
                 for g,n in [("NT","思考家"),("NF","理想家"),("SJ","堅実家"),("SP","行動家")])
    A(page(code, f'''<div class="freeband"><span class="fb-h"><span class="fb-t">{sp("FREE ver.")}</span>無料版のおさらい</span>
        <span class="it">無料版は「相性のいいタイプ TOP3」だけを公開。</span></div>
      <div class="panel" style="margin-bottom:2.8mm"><div class="pt">{sp("PREMIUM")}　・　この章で深掘りすること</div>
        <p>全16タイプの相性スコアを一覧化。NT・NF・SJ・SPの4群ごとに、あなたの立ち位置と相性の理由まで可視化します。あなたはボルドーの枠です。</p></div>
      {grp_html}
      <div class="legend"><span><i>85〜</i> ベスト</span><span><i>75〜84</i> 好相性</span>
        <span><i>65〜74</i> 普通</span><span><i>〜64</i> 要工夫</span></div>
      <div class="panel pink" style="margin-bottom:2.8mm"><div class="pt">スコアの読み方</div>
        <p>スコアは「出会った瞬間の合いやすさ」＝スタート地点で、恋の上限ではありません。85↑運命級／75↑好相性／65↑普通／〜64は伸びしろ大。低スコアでも、深い対話で育つ恋はいくらでもあります。</p></div>
      <div class="grid2" style="grid-template-columns:repeat(4,1fr);gap:2.4mm">{gc}</div>
      <div class="panel pink" style="margin-top:2.8mm"><div class="pt">{sp("WHY?")}　NF理想家と高相性なワケ</div>
        <p>{C["why_high"]}</p></div>
      {note("豆知識","相性研究では「似ているほど安心、違うほど刺激」と言われます。似た者同士の関係は安心感がある一方、刺激も意識すると長続きします。")}''',
      chapno="04", clabel=f'{sp("CHAPTER")}　0 4', title="全16タイプ 相性マップ", pno="07"))

    # ── P8 CH05 TOP5 ──
    t5 = ""
    for i in range(5):
        s, m = rk[i]
        t5 += f'''<div class="t5"><div class="rk">{i+1}</div><div class="t5b">
          <div class="t5n">{BREED[m]}<small>{sp(m)}</small></div>
          <div class="t5c">{C["top5_cm"][i]}</div></div><div class="t5s">{s}%</div></div>'''
    lines = "".join(f'''<div style="font-size:7.76pt;line-height:1.8;color:var(--ink2);padding:.5mm 0">
      <b style="color:var(--wine2);font-family:Cormorant Garamond,serif">{i+1}</b>　{BREED[rk[i][1]][:10]}　{C["top5_line"][i]}</div>'''
      for i in range(5))
    A(page(code, f'''<div style="margin-bottom:1mm">{t5}</div>
      <div class="sect-h">♡　{sp("TOP5")}に効く「最初の一言」</div>
      <div class="grid2" style="gap:1mm 5mm">{lines}</div>
      <div class="panel pink" style="margin-top:3mm"><div class="pt">共通点　{sp("TOP 5")}に共通していること</div>
        <p>{C["top5_common"]}</p></div>
      <div class="panel" style="margin-top:2.6mm"><div class="pt">共通点の活かし方</div>
        <p>“内面まで話せる人”かを見極める質問を。「最近ハマってることは？ なんで好き？」「一人の時間って何してる？」「将来こうなりたい、ってある？」——答えの深さで相性が見えます。</p></div>
      {note("ワンポイント","「ピグマリオン効果」では、期待された人はその通りに成長しやすいとされます。あなたの励ましは、相手の可能性を本当に開花させます。")}''',
      chapno="05", clabel=f'{sp("CHAPTER")}　0 5', title="ベスト相性 TOP 5", pno="08"))

    # ── P9 CH06 要注意 ──
    w = ""
    for i in range(3):
        s, m = rk[-(3-i)]
        k1,v1,k2,v2 = C["worst"][i]
        w += f'''<div style="border-bottom:.4pt dotted var(--rule);padding:4.4mm 0">
          <div style="display:flex;justify-content:space-between;align-items:baseline">
            <b style="font-size:9.22pt;color:var(--wine)">{BREED[m]}<small style="font-size:7.2pt;color:var(--ink3);letter-spacing:.14em;margin-left:2mm">{sp(m)}</small></b>
            <span style="font-family:Cormorant Garamond,serif;font-size:13.5pt;color:var(--wine2)">{s}%</span></div>
          <p style="font-size:7.88pt;line-height:1.8;color:var(--ink2);margin-top:1mm"><b style="color:var(--wine2)">{k1}</b>　{v1}</p>
          <p style="font-size:7.88pt;line-height:1.8;color:var(--ink2);margin-top:.7mm"><b style="color:var(--wine2)">{k2}</b>　{v2}</p></div>'''
    wl = "".join(f'''<div style="font-size:8.1pt;line-height:2;color:var(--ink2);padding:2.6mm 0;border-bottom:.35pt dotted var(--rule)">
      <b style="color:var(--wine)">{BREED[rk[-(3-i)][1]][:10]}</b>　{C["worst_line"][i][0]}　<span style="color:var(--ink3)">{C["worst_line"][i][1]}</span></div>'''
      for i in range(3))
    A(page(code, f'''<p class="lead">スコアが低いタイプとの恋愛が「ダメ」なわけではありません。相性スコアは「初期設定」であって「運命」ではありません。大切なのは、違いを知ったうえで歩み寄れるかどうか。この3タイプとの恋も、知識があれば全然戦えます。</p>
      {w}
      <div class="sect-h">♡　要注意タイプに「効く一言／NGな一言」</div>
      {wl}
      {note("恋愛雑学","心理学者ゴットマンの研究では、別れる夫婦の差は「ケンカの有無」ではなく「修復のうまさ」。あなたの共感力は、修復のスペシャリストです。")}''',
      chapno="06", clabel=f'{sp("CHAPTER")}　0 6', title="要注意タイプとの付き合い方", pno="09"))

    # ── P10 CH07 LINE ──
    def ul(items, cls="check"):
        return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
    bubs = ""
    for who, txt, tm in C["line_talk"]:
        bubs += f'<div class="bub {who}">{txt}<span class="tm">{tm}</span></div>'
    om = "".join(f'''<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>''' for t,s in C["omamori"])
    tp = "".join(f'''<div class="panel pink"><div class="pt">{t}</div><p>{s}</p></div>''' for t,s in C["templates"])
    A(page(code, f'''<div class="grid3" style="gap:2.8mm">
        <div class="panel"><div class="pt">あなたのLINEあるある</div>{ul(C["line_aru"],"check ok")}</div>
        <div class="panel pink"><div class="pt">脈ありのサイン（あなたから）</div>{ul(C["line_sign"])}</div>
        <div><div class="panel" style="margin-bottom:2.4mm"><div class="pt">{sp("NG")}　避けたいパターン</div>{ul(C["line_ng"],"check ng")}</div>
          <div class="panel"><div class="pt">{sp("OK")}　効果的なパターン</div>{ul(C["line_ok"],"check ok")}</div></div>
      </div>
      <div class="sect-h">返信に悩んだときの「お守りフレーズ」3選</div>
      <div class="grid3">{om}</div>
      <div class="grid2" style="grid-template-columns:1fr 1fr;gap:3.4mm;margin-top:3.4mm">
        <div class="chat"><div class="ch-h">‹　{BREED[rk[0][1]][:8]}　≡</div>{bubs}
          <div style="font-size:7.2pt;color:var(--wine2);margin-top:1mm">✓　気にかける一言が最大の魅力</div></div>
        <div class="panel pink"><div class="pt">受け取る練習</div><p>{C["line_recv"]}</p></div>
      </div>
      <div class="sect-h">♡　シーン別・そのまま使える神テンプレ</div>
      <div class="grid3">{tp}</div>
      {note("豆知識","メッセージのやり取りでは、感謝の表現が多いほど関係満足度が高いという研究も。あなたの素直な「ありがとう」は、科学的にも効果的です。")}''',
      chapno="07", clabel=f'{sp("CHAPTER")}　0 7', title="LINE・メッセージ攻略", pno="10"))

    # ── P11 CH08 ケンカ ──
    fp = "".join(f'''<div class="panel"><div style="display:flex;gap:2mm;align-items:center;margin-bottom:1mm">
      <span class="num">{i+1}</span><b style="font-size:8.55pt;color:var(--wine)">{t}</b></div><p>{s}</p></div>'''
      for i,(t,s) in enumerate(C["fight_pat"]))
    mk = "".join(f'''<div class="step"><span class="num">{i+1}</span><div class="sbody">
      <b>{sp("STEP "+str(i+1))}　{t}</b>{s}</div></div>''' for i,(t,s) in enumerate(C["makeup3"]))
    rf = "".join(f'''<div class="panel pink"><div class="pt">{"①②③"[i]}　{t}</div><p>{s}</p></div>'''
      for i,(t,s) in enumerate(C["refire"]))
    A(page(code, f'''<div class="freeband"><span class="fb-h"><span class="fb-t">{sp("FREE ver.")}</span>無料版のおさらい</span>
        <span class="it">無料版は「ケンカしたときの行動」の触りだけ。</span></div>
      <div class="panel" style="margin-bottom:3mm"><div class="pt">{sp("PREMIUM")}　・　この章で深掘りすること</div>
        <p>あなた特有のケンカ・倦怠期パターンを分析し、関係を壊さない仲直りの言葉と、冷めた空気を再点火する具体策まで提示します。</p></div>
      <div style="font-size:8.1pt;font-weight:700;color:var(--wine);margin-bottom:1.6mm">{B}のケンカパターン</div>
      <div class="grid3" style="margin-bottom:3.2mm">{fp}</div>
      <div class="sect-h">3ステップ仲直り法</div>
      {mk}
      <div class="grid2" style="margin-top:2.6mm">
        <div class="panel"><div class="pt">倦怠期</div><p>{C["kentai"]}</p></div>
        <div class="panel pink"><div class="pt">大丈夫　ケンカは本音を見せるチャンス</div>
          <p>表面的な笑顔より、本音を見せられた関係こそ長く続きます。仲直りのあとは「助けてくれて嬉しかった」と具体的に伝えてみて。</p></div>
      </div>
      <div class="panel" style="margin-top:2.6mm"><div class="pt">笑顔の裏ルール</div>
        <p>「大丈夫」と笑う前の30秒で、本当の気持ちを確かめて。「実は、ちょっと寂しかった」と一言。完璧な笑顔より、弱さを見せた方が、相手はあなたを大切にできます。</p></div>
      <div class="sect-h">♡　倦怠期の“再点火”アクション</div>
      <div class="grid3">{rf}</div>
      {note("ワンポイント","「I（アイ）メッセージ」は心理学者ゴードンが提唱した対話法。「私は」で始めることで、与えるだけでなく自分の気持ちも伝えられます。")}''',
      chapno="08", clabel=f'{sp("CHAPTER")}　0 8', title="ケンカ・倦怠期の乗り越え方", pno="11"))

    # ── P12 CH09 結婚観 ──
    mc = "".join(f'''<div style="display:flex;gap:2.4mm;padding:1.5mm 0;border-bottom:.35pt dotted var(--rule)">
      <span style="font-family:Cormorant Garamond,serif;color:var(--wine-l);font-size:8.33pt;width:5mm;flex:none">0{i+1}</span>
      <div style="flex:1"><b style="font-size:8.33pt;color:var(--wine)">{t}</b>
      <span style="font-size:7.76pt;color:var(--ink2);margin-left:2mm">{s}</span></div></div>'''
      for i,(t,s) in enumerate(C["marry_cond"]))
    ch = "".join(f'<div class="panel pink"><div class="pt">{t}</div><p>{s}</p></div>' for t,s in C["chosen"])
    mq = "".join(f'''<div style="font-size:7.76pt;color:var(--ink2);padding:.5mm 0">
      <b style="color:var(--wine2);font-family:Cormorant Garamond,serif">0{i+1}</b>　{q}</div>'''
      for i,q in enumerate(C["marry_q"]))
    A(page(code, f'''<div class="grid2" style="grid-template-columns:46mm 1fr;gap:4mm">
        <div class="stat" style="text-align:center">
          <div style="font-size:14.62pt;color:var(--wine2);letter-spacing:.06em">{"★"*P[2]}</div>
          <div class="cb-c" style="margin-top:1mm">結婚向き</div>
          <hr style="border:0;border-top:.4pt solid var(--gold-l);margin:2.2mm 0">
          <div style="font-size:9.45pt;color:var(--wine);font-weight:700">穏やか</div><div class="cb-c">絆の質</div>
          <hr style="border:0;border-top:.4pt solid var(--gold-l);margin:2.2mm 0">
          <div style="font-size:9.45pt;color:var(--wine);font-weight:700">家庭的</div><div class="cb-c">結婚像</div></div>
        <div class="panel"><div class="pt">結婚観</div><p>結婚向きは★{P[2]}と高め。愛情深く家庭的なため、結婚生活でも自然と相手や家族のために動ける。記念日や日々の気遣いを忘れない、温かい家庭を作るタイプ。</p></div>
      </div>
      <div class="sect-h">{B}が幸せになれる相手の条件</div>
      {mc}
      <p style="font-size:7.54pt;color:var(--ink3);line-height:1.8;margin-top:1.6mm">5つすべてに当てはまる必要はありません。「3つ以上あてはまるかどうか」を一つの目安に。足りないものを相手に変えてもらうより、互いに補い合える関係が理想です。</p>
      <div class="sect-h">逆に —— あなたを選んだ人は、こんなに幸せ</div>
      <div class="grid3">{ch}</div>
      <div class="sect-h">♡　結婚前に話しておきたい5つの質問</div>
      <div class="grid2" style="gap:.4mm 5mm">{mq}</div>
      <div class="panel pink" style="margin-top:2.4mm"><div class="pt">結婚かものサイン</div>
        <p>沈黙が心地いい／弱さも見せられる／一人の時間を邪魔されない／“5年後も隣にいる”が自然に想像できる —— これらが揃ったら、あなたの中ではもう“この人”です。</p></div>
      {note("恋愛雑学","長続きするカップルの共通点は「相手を変えようとしないこと」。与えることが好きなあなたも、相手のペースを尊重することが大切です。")}''',
      chapno="09", clabel=f'{sp("CHAPTER")}　0 9', title="結婚観と長続きの条件", pno="12"))

    # ── P13 PART II 扉 ──
    A(page(code, f'''<div class="divider">
      <div class="dl">{sp("PART II")}　·　{sp("ACADEMIC ANALYSIS")}</div>
      <h2>理論で読み解く、<br>あなたの恋愛</h2>
      <p class="dp">心理学の主要な恋愛・性格理論をもとに、あなたの恋愛を多角的に分析します。「なんとなく感じていた自分」を、確かな言葉で理解するための章です。</p>
      <div class="dlist">— 愛着スタイル理論 —<br>— ５つの愛の言語 —<br>— {sp("Sternberg")} 恋愛の三角理論 —<br>— ビッグファイブ・{sp("MBTI")}認知機能 —</div>
      <div class="dq">「愛とは、互いに見つめ合うことではなく、<br>共に同じ方向を見つめることである。」
        <small>—　{sp("ANTOINE DE SAINT-EXUPERY")}</small></div>
    </div>''', cls="divider-pg"))

    # ── P14 CH10 愛着スタイル ──
    att4 = "".join(f'''<div class="panel {c}"><div class="pt">{t}{y}</div><p>{s}</p></div>''' for t,s,c,y in [
      ("安定型","自分も相手も信頼できる。素直に甘え、素直に与えられる。ENFJの理想的な状態。","pink",'<span style="font-size:6.52pt;color:var(--wine2);margin-left:2mm">YOU寄り</span>'),
      ("不安型","見捨てられ不安が強い。尽くしすぎ・既読を気にしすぎる。ストレス時に傾く先。","",""),
      ("回避型","親密さを避け、距離を置きたがる。感情を見せるのが苦手。","",""),
      ("恐れ・回避型","近づきたいのに怖い。求めと拒絶が同居する。","","")])
    A(page(code, f'''<p class="lead">愛着スタイル理論（Bowlby／Ainsworth）は、幼少期に育まれた「人との距離の取り方」が恋愛にも表れるという考え方。あなたの不安や行動のクセの「根っこ」が見えてきます。</p>
      <div class="grid2" style="grid-template-columns:repeat(4,1fr);gap:2.4mm">{att4}</div>
      <div class="panel pink" style="margin-top:3mm"><div class="pt">{B}（{code}）の傾向</div><p>{C["attach_main"]}</p></div>
      <div class="grid2" style="margin-top:3mm">
        <div class="panel"><div class="pt">あなたが不安になる瞬間</div>
          <ul class="check">{"".join(f"<li>{x}</li>" for x in C["anx_moment"])}</ul></div>
        <div class="panel"><div class="pt">安定型でいるための処方箋</div>
          <ul class="check ok">{"".join(f"<li>{x}</li>" for x in C["anx_rx"])}</ul></div>
      </div>
      <div class="sect-h">▶　今日からの実践アクション</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　不安が湧いたら、連投せず「ひと呼吸おいて6時間」マイルールを試す。<br>
        ◇　1日1回、相手に小さなお願いをして“受け取る”練習をする。</div>
      {note("理論メモ","愛着スタイルは生涯固定ではなく、安定した関係の経験を通じて後天的に安定型へ変化しうるとされています（獲得安定型）。自分のクセを知ることが、その第一歩です。")}''',
      chapno="10", clabel=sp("ATTACHMENT STYLE"), title="あなたの愛着スタイル", pno="14"))

    # ── P15 CH11 相手のタイプ別 ──
    pt4 = "".join(f'''<div class="panel {c}"><div class="pt">{t}<span style="font-size:6.52pt;letter-spacing:.2em;color:var(--ink3);margin-left:2mm">{sp(e)}</span></div><p>{s}</p></div>'''
      for t,e,s,c in [
      ("安定型","SECURE","あなたの愛情を素直に受け取ってくれる相性◎。尽くしすぎず、対等に。あなたも安心して甘えられる理想の相手。","pink"),
      ("不安型","ANXIOUS","あなたの愛情表現が刺さる相手。ただし「尽くす者同士」で共倒れ注意。安心の言葉をこまめに、でも依存し合わない距離を。",""),
      ("回避型","AVOIDANT","最も注意が必要。あなたの愛情が「重い」と感じられがち。追わずに待つ・一人時間を尊重するのが正解。詰めると逃げます。",""),
      ("恐れ・回避型","FEARFUL","近づくと逃げ、離れると求める難しい相手。一貫した態度と安全基地になること。あなたの包容力が活きるが、消耗にも注意。","")])
    A(page(code, f'''<p class="lead">相手の愛着スタイルがわかると、すれ違いの9割は防げます。与え上手なあなたが「相手に合わせて愛を届ける」ための実践ガイドです。</p>
      <div style="display:grid;gap:2.6mm">{pt4}</div>
      <div class="sect-h">♡　相手の愛着タイプを見抜く3つの質問</div>
      <div class="grid3">
        <div class="panel"><p><b style="color:var(--wine2)">Q1</b>　不安なとき、連絡を増やす？減らす？</p></div>
        <div class="panel"><p><b style="color:var(--wine2)">Q2</b>　弱音を素直に言える人？隠す人？</p></div>
        <div class="panel"><p><b style="color:var(--wine2)">Q3</b>　一人時間と二人時間、どちらが好き？</p></div>
      </div>
      <div class="sect-h">▶　今日からの実践アクション</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　相手の連絡量の増減を1週間メモして、愛着タイプを見極める。<br>
        ◇　回避型には「追わず待つ」、不安型には「安心のひと言」を実践する。</div>
      {note("豆知識","研究では、カップルの一方が安定型だと、もう一方も時間とともに安定化しやすいとされます。あなたが「安全基地」になることが、二人の関係を育てます。")}''',
      chapno="11", clabel=sp("ATTACHMENT × PARTNER"), title="相手のタイプ別・接し方", pno="15"))

    # ── P16 CH12 愛の言語 ──
    def lang_rows(items):
        return "".join(f'''<div class="strow"><span>{k}</span><span style="color:var(--wine2)">{v}</span></div>''' for k,v in items)
    A(page(code, f'''<p class="lead">人が愛を感じ・伝える方法は5つに分かれるとされます（Chapman）。「伝え方」と「受け取り方」がズレると、愛があっても伝わりません。あなたの言語を知りましょう。</p>
      <div class="grid2">
        <div class="stat"><div class="sh">あなたが「与える」言語</div>{lang_rows(C["give_lang"])}</div>
        <div class="stat"><div class="sh">あなたが「受け取りたい」言語</div>{lang_rows(C["recv_lang"])}</div>
      </div>
      <div class="panel pink" style="margin-top:3.2mm"><div class="pt">⚠　あなたが陥りやすい「すれ違い」</div>
        <p>あなたは<b style="color:var(--wine)">行動（サービス）</b>で愛を伝えるのに、本当に欲しいのは<b style="color:var(--wine)">言葉（肯定）</b>。だから「こんなに寄り添っているのに、なぜ言葉が返ってこないの？」とすれ違いがち。「言葉が欲しい」と素直に伝えることが、満たされる近道です。</p></div>
      <div class="grid2" style="margin-top:3mm">
        <div class="panel"><div class="pt">相手に響かせるコツ</div><p>尽くす前に、まず相手の言語を観察。言葉が欲しい相手には言葉を、時間が欲しい相手には予定を空けて。</p></div>
        <div class="panel"><div class="pt">自分を満たすコツ</div><p>「ありがとう」「あなたのおかげ」を求めてOK。欲しい言葉は、リクエストして初めて届きます。</p></div>
      </div>
      <div class="sect-h">▶　今日からの実践アクション</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　今日、相手の具体的な行動をあげて「ありがとう」と言葉にする。<br>
        ◇　「○○してくれると嬉しい」と“欲しい言葉”を一つリクエストする。</div>
      {note("理論メモ","「与える言語」と「受け取りたい言語」が違う人は珍しくありません。両方を知っておくと、自分の不満の正体に気づけます。")}''',
      chapno="12", clabel=f'５　{sp("LOVE LANGUAGES")}', title="あなたの「愛の言語」", pno="16"))

    # ── P17 CH13 あるある30 ──
    L = C["aruaru"]
    left = "".join(f'<div class="aru-i"><span class="an">{i+1:02d}</span><span>{L[i]}</span></div>' for i in range(15))
    right = "".join(f'<div class="aru-i"><span class="an">{i+1:02d}</span><span>{L[i]}</span></div>' for i in range(15,30))
    A(page(code, f'''<p class="lead">いくつ当てはまる？　チェックしながら読んでみてください。「全部わたしだ…」となったら、それがあなたの恋愛の核です。</p>
      <div class="aru-grid"><div>{left}</div><div>{right}</div></div>
      <div class="panel pink" style="margin-top:3.4mm"><div class="pt">{sp("DIAGNOSIS")}　あてはまった数</div>
        <p>20個以上＝ 生粋の{code}恋愛体質　／　10〜19個＝ 状況で出るタイプ　／　9個以下＝ 他タイプの一面も。どれも「あなたらしさ」です。</p></div>''',
      chapno="13", clabel=f'{sp(code)}　{sp("LOVE ARUARU")}', title=f"{code} 恋愛あるある ３０", pno="17"))

    # ── P18 CH14 落とし穴 ──
    pf = "".join(f'''<div class="panel {"pink" if i%2==0 else ""}" style="margin-bottom:2.4mm">
      <div class="pt">落とし穴 {"①②③④"[i]}　{t}</div>
      <p><b style="color:var(--wine2);font-size:7.42pt">原因</b>　{c}</p>
      <p style="margin-top:.8mm"><b style="color:var(--wine2);font-size:7.42pt">処方箋</b>　{r}</p></div>'''
      for i,(t,c,r) in enumerate(C["pitfalls"]))
    A(page(code, f'''<p class="lead">CH03が「性格のクセ」なら、こちらは恋愛の“場面”で起きるつまずき。デート・付き合った後・別れ際など、シーンごとの落とし穴を原因と処方箋つきで。当てはまるものから手放していきましょう。</p>
      {pf}
      <div style="text-align:center;margin-top:3.4mm;font-size:10.12pt;line-height:2;color:var(--wine2);font-style:italic">
        <span style="font-size:16.88pt;color:var(--wine-l)">“</span><br>{C["pitfall_quote"]}</div>
      {note("ひとこと","落とし穴はすべて「優しさ」の裏返し。直すべき欠点ではなく、少しだけ向ける方向を変えるだけ。あなたの愛情は、そのままで十分に魅力です。")}''',
      chapno="14", clabel=sp("PITFALLS & REMEDY"), title="恋の落とし穴と処方箋", pno="18"))

    # ── P19 CH15 三角理論 ──
    tri = "".join(f'''<div class="brow"><div class="bh"><b>{k}</b>
      <span><span class="v">{v}</span>　<span style="font-size:7.2pt;color:var(--ink3)">・{lab}</span></span></div>
      <div class="bar"><i style="width:{v}%"></i></div><p>{d2}</p></div>''' for k,v,lab,d2 in C["triangle"])
    seven = "".join(f'''<div class="cbox"><div style="font-size:7.88pt;font-weight:700;color:{'var(--wine)' if st else 'var(--ink2)'}">{n}</div>
      <div class="cb-c">{s}</div></div>''' for n,s,st in [
      ("好意","親密のみ",0),("夢中","情熱のみ",0),("空虚な愛","コミットのみ",0),("ロマンチック","親密＋情熱",0),
      ("友愛的な愛","親密＋コミット",1),("愚かな愛","情熱＋コミット",0),("完全愛 ★","3つすべて",1),("非愛","どれもなし",0)])
    A(page(code, f'''<p class="lead">Sternbergは、愛は親密性・情熱・コミットメントの3要素でできていると説きました。バランスによって「愛の形」が決まります。</p>
      {tri}
      <div class="panel pink" style="margin-top:2.6mm"><div class="pt">あなたの愛の形　＝　「友愛的な愛」から「完全愛」へ</div>
        <p>親密性とコミットメントが高いあなたは、<b style="color:var(--wine)">深く長く続く「友愛的な愛」</b>が得意。あとは情熱を絶やさない工夫（新しい体験・ときめきの共有）を足せば、3要素が揃った<b style="color:var(--wine)">「完全愛（Consummate Love）」</b>に届きます。</p></div>
      <div class="sect-h">7つの愛のかたち（あなたの位置）</div>
      <div class="cmap-row" style="grid-template-columns:repeat(4,1fr);gap:2mm">{seven}</div>
      <div class="sect-h">▶　今日からの実践アクション</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　週に一度、二人で“初めての体験”を予定に入れる。<br>
        ◇　ときめいた瞬間は、その場で言葉にして相手に伝える。</div>
      {note("豆知識","情熱は時間とともに自然に下がるもの。長続きするカップルは、情熱を「育て直す」工夫をしています。あなたの強みである親密性が、その土台になります。")}''',
      chapno="15", clabel=sp("TRIANGULAR THEORY"), title="恋愛の三角理論", pno="19"))

    # ── P20 CH16 ビッグファイブ ──
    bf = "".join(f'''<div class="brow"><div class="bh"><b>{k}　<span style="font-size:6.75pt;letter-spacing:.12em;color:var(--ink3)">{e}</span></b>
      <span class="v">{v}</span></div><div class="bar"><i style="width:{v}%"></i></div><p>{d2}</p></div>'''
      for k,e,v,d2 in C["bigfive"])
    A(page(code, f'''<p class="lead">性格を5つの因子で測る、心理学で最も信頼されるモデル。あなたの恋愛での「出方」を因子ごとに見ていきます。</p>
      {bf}
      <div class="grid2" style="margin-top:2.6mm">
        <div class="panel pink"><div class="pt">この組み合わせの強み</div>
          <p>高い協調性＋外向性＝<b style="color:var(--wine)">誰からも好かれる愛され体質</b>。誠実性も高く、長期的な関係を築く力に恵まれています。</p></div>
        <div class="panel"><div class="pt">気をつけたい点</div>
          <p>協調性が高すぎると<b style="color:var(--wine)">自己主張が消えがち</b>。神経症傾向の揺れと重なると、尽くして疲れる悪循環に。</p></div>
      </div>
      <div class="sect-h">▶　今日からの実践アクション</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　1日1回、小さな「私はこうしたい」を声に出す。<br>
        ◇　不安が募ったら、事実と思い込みを紙に分けて書き出す。</div>
      {note("理論メモ","研究では、カップルの満足度に最も影響するのは「神経症傾向の低さ」と「協調性の高さ」とされます。あなたは協調性の強みを活かしつつ、不安との付き合い方を整えるのが鍵です。")}''',
      chapno="16", clabel=sp("BIG FIVE PROFILE"), title="ビッグファイブ恋愛分析", pno="20"))

    # ── P21 CH17 認知機能 ──
    cf = "".join(f'''<div class="panel {"pink" if i==0 else ""}" style="margin-bottom:2.4mm">
      <div style="display:flex;gap:2.6mm;align-items:baseline">
        <span style="font-family:Cormorant Garamond,serif;font-size:16.88pt;color:var(--wine);line-height:1">{fn}</span>
        <span style="font-size:6.98pt;letter-spacing:.16em;color:var(--wine-l)">{rank}</span>
        <b style="font-size:8.33pt;color:var(--wine2)">{jp}</b></div>
      <p style="margin-top:1mm">{desc}</p></div>''' for i,(fn,rank,jp,desc) in enumerate(C["cogfn"]))
    A(page(code, f'''<p class="lead">MBTIの奥にある「心の使い方の順番」が認知機能。{code}は Fe → Ni → Se → Ti の順で世界を捉えます。恋愛でどう働くのか見てみましょう。</p>
      {cf}
      <div class="sect-h">▶　今日からの実践アクション</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　疲れを感じたら抱え込まず、一人で休む時間を確保する。<br>
        ◇　責めたくなったら“事実→自分の気持ち”の順で伝える。</div>
      {note("理論メモ","主導のFeで相手に尽くし、劣等のTiが暴走するとロジックで責める —— この振れ幅を知っておくと、ケンカのときの自分を客観視できます。")}''',
      chapno="17", clabel=sp("COGNITIVE FUNCTIONS"), title="認知機能でみる恋愛", pno="21"))

    # ── P22 W3 理論で自己分析 ──
    refs = '''<div class="refs"><div class="rh">{}　・　主な参考理論</div><div class="rg">
      <span>Bowlby, J. (1969). Attachment and Loss.</span><span>Hazan, C. &amp; Shaver, P. (1987). Romantic love as attachment.</span>
      <span>Ainsworth, M. (1978). Patterns of Attachment.</span><span>Chapman, G. (1992). The Five Love Languages.</span>
      <span>Sternberg, R. (1986). A triangular theory of love.</span><span>Costa, P. &amp; McCrae, R. (1992). NEO-PI-R (Big Five).</span>
      <span>Jung, C.G. (1921). Psychological Types.</span><span>Myers, I. &amp; Briggs, K. MBTI® framework.</span></div>
      <p style="font-size:6.52pt;color:var(--ink3);line-height:1.7;margin-top:1.8mm">※本書は上記の理論を一般向けに分かりやすく再構成したものであり、学術的・臨床的診断ではありません。自己理解を深める読み物としてお楽しみください。</p></div>'''.format(sp("REFERENCES"))
    def wq(n, q, lines=2):
        return f'''<div class="wlabel"><span class="num">{n}</span>{q}</div>''' + \
               "".join('<div class="wline"></div>' for _ in range(lines))
    A(page(code, f'''<p class="lead">学んだ理論を、あなた自身の恋愛にあてはめて書き出しましょう。書くことで、知識が「自分のもの」になります。</p>
      {wq(1,"私の愛着スタイルは？　それが出た具体的な場面は？",2)}
      {wq(2,"私が「受け取りたい」愛の言語を、相手にどう伝える？",2)}
      {wq(3,"「完全愛」に近づくため、情熱を育てる工夫を一つ。",2)}
      {refs}
      {note("最後に","理論はあくまで「地図」。実際に歩くのはあなたです。知った自分を手がかりに、あなたらしい愛を育てていってください。")}''',
      chapno="W3", clabel=sp("THEORY WORKSHEET"), title="理論で自己分析シート", pno="22"))

    # ── P23 W1 棚卸し ──
    A(page(code, f'''<p class="lead">頭の中の「理想の恋人像」を一度すべて紙の上に出しましょう。書き出すことで、本当に譲れないものと手放せるものが見えてきます。</p>
      <div class="wlabel"><span class="num">1</span>理想の恋人像を、思いつくまま書き出す</div>
      {"".join('<div class="wline"></div>' for _ in range(4))}
      <div class="wlabel"><span class="num">2</span>「絶対に譲れないもの」を3つだけ選んで書く</div>
      <div class="grid3">
        <div class="wbox"><div class="cb-c">01</div><div class="wline" style="border-bottom:none;height:6mm"></div></div>
        <div class="wbox"><div class="cb-c">02</div><div class="wline" style="border-bottom:none;height:6mm"></div></div>
        <div class="wbox"><div class="cb-c">03</div><div class="wline" style="border-bottom:none;height:6mm"></div></div>
      </div>
      <div class="wlabel"><span class="num">3</span>3つに絞った感想・気づきを書く</div>
      {"".join('<div class="wline"></div>' for _ in range(3))}
      <div class="panel pink" style="margin-top:3mm"><div class="pt">{sp("HINT")}</div>
        <p>3つに絞れたら、それ以外は「あったらうれしいボーナス」。完璧な人を探すのではなく、譲れない3つを持っている人を探す —— これだけで恋のハードルが現実的になります。</p></div>
      {note("ワンポイント","目標は「紙に書くと実現しやすくなる」と言われます。誰かのためだけでなく、自分のための目標も書いてみましょう。")}''',
      chapno="W1", clabel=f'{sp("WORK")}　0 1', title="理想と現実の棚卸しシート", pno="23"))

    # ── P24 W2 本音を伝える ──
    A(page(code, f'''<p class="lead">我慢グセを手放すための「Iメッセージ」練習シートです。相手のせいにする言い方（Youメッセージ）から、自分の気持ちを伝える言い方（Iメッセージ）に変換する練習をします。</p>
      <div class="panel pink"><div class="pt">テンプレ　Iメッセージの型</div>
        <p style="font-size:9.0pt;line-height:2"><b style="color:var(--wine)">私は</b>〔状況・事実〕　▶　<b style="color:var(--wine)">〜と感じた</b>〔感情・気持ち〕　▶　<b style="color:var(--wine)">だから</b>〔お願い・希望〕</p></div>
      <div class="wlabel"><span class="num">1</span>最近「言えなかった本音」を一つ思い出す</div>
      {"".join('<div class="wline"></div>' for _ in range(3))}
      <div class="wlabel"><span class="num">2</span>Iメッセージに変換して書いてみる</div>
      <div class="wbox">
        <div style="font-size:8.33pt;color:var(--wine2);margin-bottom:1mm">私は</div><div class="wline"></div>
        <div style="font-size:8.33pt;color:var(--wine2);margin:1.6mm 0 1mm">〜と感じた。だから</div><div class="wline"></div>
        <div style="font-size:8.33pt;color:var(--wine2);margin:1.6mm 0 1mm">〜してほしい。</div><div class="wline"></div>
      </div>
      <div class="panel" style="margin-top:2.6mm"><div class="pt">{sp("HINT")}</div>
        <p>最初は紙に書くだけでOK。実際に伝えなくてもいいです。「言語化する」だけで気持ちが整理され、次に同じ状況が来たときに口から出やすくなります。</p></div>
      {note("豆知識","「言いたいことを我慢しすぎない人」ほど、長期的な関係満足度が高いという研究があります。あなたの本音も、関係に必要なピースです。")}''',
      chapno="W2", clabel=f'{sp("WORK")}　0 2', title="本音を伝える練習シート", pno="24"))

    # ── P25 A1 仲直りフローチャート ──
    def fq(q, no_l, no_t, yes_l, yes_t):
        return f'''<div class="flow-q">{q}</div><div class="flow-2">
          <div class="flow-b"><span class="fl">{no_l}</span><p>{no_t}</p></div>
          <div class="flow-b"><span class="fl">{yes_l}</span><p>{yes_t}</p></div></div><div class="flow-ar">▼</div>'''
    A(page(code, f'''<p class="lead">ケンカした直後は感情で動きがち。この順番どおりに進めば、関係を壊さず仲直りにたどり着けます。迷ったら、上から指でなぞってみてください。</p>
      <div class="flow-q" style="background:var(--pink);border-color:var(--pinkbd)">ケンカしてしまった…</div>
      <div class="flow-ar">▼</div>
      {fq("Q1　あなたの頭は冷えている？", sp("NO")+"・まだ感情的","「6時間ルール」で一旦離れる。落ち着いてからこの図に戻る。",
          sp("YES")+"・冷静になれた","次のステップへ進む。")}
      {fq("Q2　自分にも非があった？", sp("NO")+"・相手が悪い気が","責める前に<b style='color:var(--wine)'>相手の言い分を最後まで聴く</b>。",
          sp("YES"),"言い訳の前に<b style='color:var(--wine)'>「ごめんね」</b>から。何に謝るかを具体的に。")}
      {fq("Q3　相手は今、話せそう？", sp("NO")+"・まだ距離がある","「落ち着いたら話そう」と一言だけ送って待つ。",
          sp("YES"),"Iメッセージで<b style='color:var(--wine)'>「私は〜と感じた」</b>と本音を伝える。")}
      <div class="flow-goal">仲直り　▷　最後は感謝とスキンシップで締める　♡</div>
      {note("理論メモ","研究では、ケンカそのものより「修復のうまさ」が関係の長続きを左右するとされます。仲直りの型を持っておくことが、最大の保険です。")}''',
      chapno="A1", clabel=sp("MAKE UP FLOW"), title="ケンカ仲直りフローチャート", pno="25"))

    # ── P26 A2 復縁という選択 ──
    r3 = "".join(f'''<div class="panel"><div style="display:flex;gap:2mm;align-items:center;margin-bottom:1mm">
      <span class="num">{i+1}</span><b style="font-size:8.33pt;color:var(--wine)">{t}</b></div><p>{s}</p></div>'''
      for i,(t,s) in enumerate([
        ("冷却期間をおく","最低でも1〜3ヶ月、連絡を断つ。追わないことが、相手に「失った実感」を生む。"),
        ("自分を整える","別れの原因と向き合い、見た目・生活・心を立て直す。“変わった姿”が最大の説得力。"),
        ("さりげなく再接触","重い告白でなく「元気にしてる？」から。友人として軽く、焦らず距離を縮める。")]))
    ng3 = "".join(f'''<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>' ''' .strip().rstrip("'")
      for t,s in [("追いLINE","未読・既読を気にして連投する"),("泣き落とし","同情や罪悪感で引き止めようとする"),
                  ("SNS監視","相手の投稿に一喜一憂し続ける")])
    A(page(code, f'''<p class="lead">別れたあとに芽生える「もう一度」の気持ち。大切なのは、寂しさで動かず<b style="color:var(--wine)">「本当に戻るべきか」</b>を見極めること。寄り添い型のあなたほど、冷静な判断が必要です。</p>
      <div class="grid2">
        <div class="panel pink"><div class="pt">◎　復縁を考えていいサイン</div><ul class="check">
          <li>別れの原因が「解決できるもの」だった</li><li>二人とも成長・変化する意思がある</li>
          <li>感謝できる思い出のほうが多い</li><li>一人になっても相手を尊重できている</li></ul></div>
        <div class="panel"><div class="pt">✕　やめておくべきサイン</div><ul class="check ng">
          <li>ただ「寂しい・一人が不安」だけ</li><li>原因がモラハラ・浮気など根深い</li>
          <li>戻れば「また尽くせる」と思っている</li><li>相手は明確に終わりを望んでいる</li></ul></div>
      </div>
      <div class="sect-h">復縁の3ステップ</div>
      <div class="grid3">{r3}</div>
      <div class="sect-h">⚠　復縁でやってはいけないNG行動</div>
      <div class="grid3">{ng3}</div>
      {note(sp(code)+"へ", C["enfj_msg"])}''',
      chapno="A2", clabel=sp("RECONCILIATION"), title="復縁という選択", pno="26"))

    # ── P27 A3 復縁の見極め ──
    chk = "".join(f'<div style="font-size:7.99pt;color:var(--ink2);padding:.9mm 0">□　{x}</div>' for x in [
      "別れの原因が「解決できる」ものだ","一人の時間でも自分を保てている","相手の幸せを心から願える",
      "自分が変わる覚悟と行動がある","感謝できる思い出のほうが多い","相手もまだ完全には終わっていない"])
    judge = "".join(f'''<div class="panel {c}"><div class="pt">{t}</div><p>{s}</p></div>''' for t,s,c in [
      ("5〜6個  →  進んでよい","条件は十分。次章の手順で丁寧に。","pink"),
      ("3〜4個  →  保留","まず自分を整える期間を。焦らない。",""),
      ("0〜2個  →  やめる勇気","手放すほうが、あなたの幸せに近い。","")])
    rows = "".join(f'<tr><td class="lb">{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in [
      ("別れた直後","追わず、まず気持ちを落ち着けた","不安のまま追いLINEで連投した"),
      ("冷却期間","距離を置き、別れの原因と向き合った","寂しさに耐えられず、すぐ連絡を再開"),
      ("自分磨き","自分の課題を一つ変える努力をした","相手を変えようと説得を続けた"),
      ("再会の仕方","「変わった自分」で軽く短く会った","重い空気で「やり直したい」と迫った"),
      ("結果","前より対等な関係を築き直せた","同じすれ違いを繰り返し再び別れた")])
    A(page(code, f'''<p class="lead">「戻りたい」その気持ちは、<b style="color:var(--wine)">愛情</b>ですか、それとも<b style="color:var(--wine)">執着</b>ですか。動き出す前に、頭と心を静かに整理しておきましょう。</p>
      <div class="panel" style="margin-bottom:2.6mm"><div class="pt">復縁成功率セルフチェック</div>
        <p style="font-size:7.65pt;color:var(--ink3);margin-bottom:1mm">当てはまる□の数を数えてください。</p>
        <div class="grid2" style="gap:0 5mm">{chk}</div></div>
      <div class="grid3">{judge}</div>
      <div class="sect-h">執着？　それとも愛情？</div>
      <div class="grid2">
        <div class="panel"><div class="pt">執着（手放せない）</div>
          <p>・一人になるのが怖い<br>・相手のSNSが気になって仕方ない<br>・「失うのが怖い」が先に立つ<br>・過去のいい時間に戻りたいだけ</p></div>
        <div class="panel pink"><div class="pt">愛情（また大切にしたい）</div>
          <p>・相手の幸せを願える<br>・自分の非を認め、変われる<br>・感謝のほうが多く思い出せる<br>・二人の未来を具体的に描ける</p></div>
      </div>
      <div class="sect-h">分かれ道　— 戻れた人・また別れた人</div>
      <table class="cmp"><tr><th></th><th>◎　やり直せた人</th><th>✕　また別れた人</th></tr>{rows}</table>
      {note("手放す選択","諦めることは、負けでも失敗でもありません。「戻らない」と決めて前へ進む勇気もまた、自分を大切にする愛のかたち。どちらを選んでも、あなたの恋は次へつながります。")}''',
      chapno="A3", clabel=sp("REUNITE · DECISION"), title="復縁の見極め", pno="27"))

    # ── P28 A4 復縁テクニック ──
    s1 = "".join(f'<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>' for t,s in [
      ("連絡は断つ","1〜3ヶ月。追わないことで「失った実感」を相手に生ませる。"),
      ("SNSは静かに","監視も匂わせ投稿もNG。たまに前向きな近況だけ。"),
      ("自分を磨く","見た目・生活・心を立て直す。“変わった姿”が最大の武器。")])
    s3 = "".join(f'<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>' for t,s in [
      ("短く・軽く","初回はランチやお茶1時間。重い場所・長時間は避ける。"),
      ("昔話より今","別れの話は持ち出さない。変わった自分を自然に見せる。"),
      ("引き際よく","「楽しかった、またね」で先に切り上げ、余韻を残す。")])
    A(page(code, f'''<p class="lead">復縁は「気持ち」より<b style="color:var(--wine)">「順番と間（ま）」</b>。焦って動くほど遠ざかります。5つの局面に分けて、具体的な手順とセリフで攻略します。</p>
      <div class="sect-h">{sp("STEP 1")}　冷却期間の正しい過ごし方</div>
      <div class="grid3">{s1}</div>
      <div class="sect-h">{sp("STEP 2")}　再接触の最初の1通</div>
      <div class="grid2">
        <div class="panel"><div class="pt">✕　{sp("NG")}な切り出し</div>
          <p>「やり直したい」「会いたい」「まだ好き」<br><span style="color:var(--ink3)">→ 重く、相手の逃げ場を奪う</span></p></div>
        <div class="panel pink"><div class="pt">◎　{sp("OK")}な切り出し</div>
          <p>「久しぶり、元気にしてる？」<br>「これ、あなた好きそうだと思って」<br><span style="color:var(--wine2)">→ 軽く・用件は小さく</span></p></div>
      </div>
      <div class="sect-h">{sp("STEP 3")}　復縁デートの設計</div>
      <div class="grid3">{s3}</div>
      <div class="sect-h">{sp("STEP 4")}　復縁が近づいたサイン</div>
      <div class="grid2" style="gap:.4mm 5mm">
        <div style="font-size:7.88pt;color:var(--ink2);padding:.4mm 0">♢ 返信が早く・長くなってきた</div>
        <div style="font-size:7.88pt;color:var(--ink2);padding:.4mm 0">♢ 相手から近況や質問を振ってくる</div>
        <div style="font-size:7.88pt;color:var(--ink2);padding:.4mm 0">♢ 昔の楽しかった思い出に触れてくる</div>
        <div style="font-size:7.88pt;color:var(--ink2);padding:.4mm 0">♢ 「また会いたい」と言葉や態度に出る</div>
      </div>
      <div class="sect-h">{sp("STEP 5")}　やり直しの切り出し方</div>
      <div class="grid2">
        <div class="panel"><div class="pt">タイミング</div><p>数回会って空気が戻り、相手から会いたい素振りが出た時。会った帰り際、余韻が残る瞬間に。</p></div>
        <div class="panel"><div class="pt">伝え方</div><p>「あの頃と違う自分でいられる。もう一度、一緒にいたい」。過去の謝罪より<b style="color:var(--wine)">“これからどう変わるか”</b>を一言。</p></div>
      </div>
      <div class="panel pink" style="margin-top:2.4mm"><div class="pt">決め手の例</div>
        <p>「離れてみて、あなたといる時間がいちばん自分らしかったと気づいた。今度はもっと対等に、ちゃんと大事にしたい」<br>
        <span style="color:var(--ink3);font-size:7.54pt">— 重さや謝罪で押さず、“変わった自分”と“これから”だけを、短く正直に。</span></p></div>
      {note("心理メモ","人は別れ際（ピーク・エンド）の印象で記憶を上書きします。最後を良い余韻で終えるほど「もう一度会いたい」が生まれやすくなります。")}''',
      chapno="A4", clabel=sp("REUNITE · TECHNIQUE"), title="復縁テクニック実践編", pno="28"))

    # ── P29 A5 タイプ別復縁 ──
    rt = "".join(f'<div class="panel"><div class="pt">{t} には</div><p>{s}</p></div>' for t,s in C["reunite_type"])
    bfix = "".join(f'''<div style="display:flex;gap:2.6mm;padding:1.5mm 0;border-bottom:.35pt dotted var(--rule)">
      <b style="font-size:8.21pt;color:var(--wine);width:26mm;flex:none">{t}</b>
      <span style="font-size:7.88pt;line-height:1.8;color:var(--ink2)">{s}</span></div>''' for t,s in C["breakup_fix"])
    pr = "".join(f'''<div class="panel pink"><div style="display:flex;gap:2mm;align-items:center;margin-bottom:1mm">
      <span class="num">{i+1}</span><b style="font-size:8.33pt;color:var(--wine)">{t}</b></div><p>{s}</p></div>'''
      for i,(t,s) in enumerate(C["promise3"]))
    A(page(code, f'''<p class="lead">相手の性格で、響く戻り方は変わります。代表的な9タイプ別に「効く一手」をまとめました。さらに、{code}が別れやすい原因と、その修正法も。</p>
      <div class="grid3" style="gap:2.4mm">{rt}</div>
      <div class="sect-h">{sp(code)}が別れやすい原因　→　復縁での修正法</div>
      {bfix}
      <div class="sect-h">やり直してからの3つの約束</div>
      <div class="grid3">{pr}</div>
      {note("最後に","復縁のゴールは「元に戻る」ことではなく<b style='color:var(--wine)'>「前より良い二人になる」</b>こと。同じ別れを繰り返さない自分になれた時、本当の意味でやり直せます。")}''',
      chapno="A5", clabel=sp("REUNITE · BY TYPE"), title="タイプ別・復縁アプローチ", pno="29"))

    # ── P30 A6 復縁とSNS ──
    st3 = "".join(f'''<div class="panel"><div style="display:flex;gap:2mm;align-items:center;margin-bottom:1mm">
      <span class="num">{i+1}</span><b style="font-size:8.33pt;color:var(--wine)">{t}</b></div><p>{s}</p></div>'''
      for i,(t,s) in enumerate([("いいね","まずは投稿に軽く一つ。「見てるよ」を圧なく伝える最初の合図。"),
        ("ストーリー反応","スタンプや一言で軽く反応。「それ気になる！」程度の短さで止める。"),
        ("DM再開","反応が返るようになってから。用件は小さく「元気？」の一通で十分。")]))
    sns4 = "".join(f'<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>' for t,s in [
      ("Instagram","充実をさりげなく一枚。ストーリーの閲覧で毎回先頭に出ない。リアクションは控えめに。"),
      ("LINE","即レス・連投はしない。用件は短く一往復で。アイコン・ひとことを静かに整える程度に。"),
      ("X（旧Twitter）","病み・匂わせ厳禁。フォローは外さず、感情の垂れ流しだけを止める。沈黙が余裕に見える。")])
    A(page(code, f'''<p class="lead">現代の復縁は、SNSの使い方で半分決まります。相手の動向を察しやすいあなたほど、つい見すぎ・反応しすぎに。<b style="color:var(--wine)">「静けさ」が一番の武器</b>です。</p>
      <div class="sect-h">①　冷却期間のSNSルール</div>
      <div class="grid2">
        <div class="panel pink"><div class="pt">◎　すること</div><p>通知を切って見に行かない ／ 前向きな近況をたまに一つ ／ フォローはそのまま自然に。</p></div>
        <div class="panel"><div class="pt">✕　しないこと</div><p>投稿の巡回・足跡チェック ／「病んでる・匂わせ」投稿 ／ 衝動的なブロックや削除。</p></div>
      </div>
      <div class="sect-h">②　印象をリセットする見せ方</div>
      <div class="grid2">
        <div class="panel"><div class="pt">残していい投稿</div><p>自分磨き・新しい挑戦・自然な笑顔。「充実してそう」がさりげなく伝わるものだけ。</p></div>
        <div class="panel"><div class="pt">消したい投稿</div><p>未練・愚痴・意味深なポエム。二人の思い出は今は非公開に。重さは即ブレーキになる。</p></div>
      </div>
      <div class="sect-h">③　再接触の3ステップ</div>
      <div class="grid3">{st3}</div>
      <div class="sect-h">④　SNS別・距離の取り方</div>
      <div class="grid3">{sns4}</div>
      <div class="sect-h">⑤　相手の心が戻りかけたサイン</div>
      <div style="font-size:7.88pt;line-height:1.95;color:var(--ink2)">
        ♢ あなたの投稿へのいいね・閲覧が増える。ストーリーを最後まで見ている。<br>
        ♢ 過去の思い出に触れてくる。「あの店まだあるかな」など、二人の話題を出してくる。<br>
        ♢ 相手から近況を共有してくる。返信が早く・長くなったら、対面に移すサイン。</div>
      {note(sp("SNS NG"),"鍵垢・サブ垢での監視 ／ 共通の友人へのアピール投稿 ／ 既読・オンライン表示への一喜一憂。追うほど遠ざかります。静かに、余裕を見せる人が選ばれます。")}''',
      chapno="A6", clabel=sp("REUNITE · SNS"), title="復縁とSNS", pno="30"))

    # ── P31 A7 SNS実践編 ──
    stry = "".join(f'<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>' for t,s in [
      ("挑戦してる感","資格の勉強・ジム・新しい趣味。「前に進んでる」を一枚で。"),
      ("楽しそうな日常","友人とのカフェ・旅先の景色。人物を写しすぎず雰囲気だけ。"),
      ("共通の話題","昔ふたりで好きだったお店や音楽。返信のきっかけを置く。")])
    qa = "".join(f'''<div style="padding:1.6mm 0;border-bottom:.35pt dotted var(--rule)">
      <b style="font-size:8.21pt;color:var(--wine)">Q. {q}</b>
      <p style="font-size:7.88pt;line-height:1.8;color:var(--ink2);margin-top:.6mm">{a}</p></div>''' for q,a in [
      ("ブロックされていたら？","追わない。時間を置けば解除されることも多い。別アカでの接触は逆効果なので絶対にしない。"),
      ("新しい相手がいそうな時は？","詮索も牽制もしない。今は引いて、自分の充実に集中。関係が続くとは限らない。"),
      ("既読スルーされたら？","追撃しない。1〜2週間あけて、別の軽い話題で一度だけ。それでも無反応なら一旦休む。")])
    s3c = "".join(f'<div class="panel pink"><div class="pt">{t}</div><p>{s}</p></div>' for t,s in C["sns3"])
    A(page(code, f'''<p class="lead">「何を投稿する？」「どう送る？」を、そのまま使える文例で。迷いやすい場面はQ&amp;Aで答えます。</p>
      <div class="sect-h">さりげない近況ストーリーの例</div>
      <div class="grid3">{stry}</div>
      <div class="sect-h">DM再開のひとこと文例</div>
      <div class="grid2">
        <div class="panel"><div class="pt">✕　重い</div><p>「ずっと考えてた」「会えないかな」「まだ好き」<br><span style="color:var(--ink3)">→ 期待が見えて身構えさせる</span></p></div>
        <div class="panel pink"><div class="pt">◎　軽い</div><p>「この前◯◯行ったよ、懐かしくて笑」<br>「元気にしてる？ふと思い出して」<br><span style="color:var(--wine2)">→ 用件は小さく、返しやすく</span></p></div>
      </div>
      <div class="sect-h">こんな時どうする？　Q&amp;A</div>
      {qa}
      <div class="sect-h">{sp(code)}ならではの3つの一手</div>
      <div class="grid3">{s3c}</div>''',
      chapno="A7", clabel=sp("REUNITE · SNS Q&A"), title="復縁とSNS　実践編", pno="31"))

    # ── P32 裏表紙 ──
    A(page(code, f'''<div class="divider">
      <div class="dq" style="margin-top:0">「人は、自分が愛するものによって<br>形づくられてゆく。」
        <small>—　{sp("J. W. GOETHE")}</small></div>
      <h2 style="font-size:16.88pt;margin-top:14mm;line-height:1.9">{C["closing"]}</h2>
      <p class="dp" style="margin-top:8mm">本書を読んでくださってありがとうございます。<br>あなたの愛情が、ちゃんと返ってくる恋になりますように。</p>
      <div style="margin-top:auto;width:100%">
        <div class="refs"><div class="rh">{sp("REFERENCES")}　・　主な参考理論</div><div class="rg" style="text-align:left">
          <span>Bowlby, J. (1969). Attachment and Loss.</span><span>Hazan, C. &amp; Shaver, P. (1987). Romantic love as attachment.</span>
          <span>Ainsworth, M. (1978). Patterns of Attachment.</span><span>Chapman, G. (1992). The Five Love Languages.</span>
          <span>Sternberg, R. (1986). A triangular theory of love.</span><span>Costa, P. &amp; McCrae, R. (1992). NEO-PI-R (Big Five).</span>
          <span>Jung, C.G. (1921). Psychological Types.</span><span>Myers, I. &amp; Briggs, K. MBTI® framework.</span></div></div>
        <div style="text-align:center;margin-top:5mm;font-size:7.88pt;letter-spacing:.2em;color:var(--ink2)">
          16にゃんこ恋愛診断　／　恋愛攻略書　{B}（{sp(code)}）版</div>
        <div style="text-align:center;margin-top:2mm;font-size:7.2pt;letter-spacing:.14em;color:var(--ink3)">
          発行：Type&amp;Co　／　診断サイト：16lovetypecats.com</div>
        <div style="text-align:center;margin-top:2.4mm;font-size:6.52pt;color:var(--ink3);line-height:1.7">
          本書は娯楽目的のコンテンツです。心理学的・医学的診断ではありません。無断複製・転載を禁じます。<br>
          ©　2026　Type&amp;Co　/　16にゃんこ恋愛診断</div>
      </div></div>''', cls="back-pg"))

    return pages


# ══════════════════════════════════════════════════════════════
def main():
    import base64, io
    from PIL import Image
    code = sys.argv[1] if len(sys.argv) > 1 else "ENFJ"
    src = f"/home/user/16lovetypeCATS/{code.lower()}.png"
    im = Image.open(src).convert("RGBA"); im.thumbnail((520, 520))
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=92)
    b64 = base64.b64encode(buf.getvalue()).decode()
    pages = build(code, C, b64)
    html = (f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
            f'<title>恋愛攻略書 — {BREED[code]}（{code}）</title><style>{CSS}</style></head><body>'
            + "".join(pages) + "</body></html>")
    out = os.path.join(SCRATCH, f"guide_{code.lower()}.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"pages={len(pages)}  ->  {out}  ({len(html)//1024}KB)")

if __name__ == "__main__":
    main()
