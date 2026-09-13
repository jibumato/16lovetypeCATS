#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""16にゃんこ恋愛診断 プレミアム恋愛攻略書 ビルダー
犬版（16わんこ）の32ページ構成・デザインを踏襲し、猫版を生成する。
相性スコアはサイト index.html の compatScore と完全一致。
"""
import json, os, sys
from diagrams import *

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
/*FONTFACE*/
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --cream:#fdf6fa; --cream2:#fbeaf2; --paper:#ffffff;
  --wine:#2c1b3d; --wine2:#e0559a; --wine-l:#b98af0;
  --pink:#fff0f6; --pinkbd:#2c1b3d;
  --gold:#ffe27a; --gold-l:#ffe27a;
  --ink:#3d3047; --ink2:#5d4f68; --ink3:#9b8da8;
  --rule:#efe2f4; --lav:#c9a0f0; --mint:#9ad9c4;
  --sh:3px 3px 0 var(--lav);
}
@page{size:A4;margin:0}
html,body{background:#999}
body{font-family:'M PLUS Rounded 1c','Zen Maru Gothic',sans-serif;color:var(--ink);
  -webkit-font-smoothing:antialiased;font-feature-settings:"palt" 1;line-height:1.8}
.page{width:210mm;height:297mm;background:var(--cream);position:relative;
  overflow:hidden;page-break-after:always;padding:11mm 12mm 9mm}
.page:last-child{page-break-after:auto}
.page::before{content:"";position:absolute;inset:5mm;border:2.2pt solid var(--wine);
  border-radius:5mm;pointer-events:none}
.page::after{display:none}
.inner{position:relative;height:100%;display:flex;flex-direction:column;padding:3mm 3mm 0}
.pbody{flex:1;display:flex;flex-direction:column;min-height:0}

/* ── ヘッダ ── */
.phead{display:flex;justify-content:space-between;align-items:center;
  font-size:7.2pt;font-weight:700;color:var(--ink3);padding-bottom:2mm}
.chapno{position:absolute;top:-1mm;right:0;font-family:'Baloo 2',cursive;
  font-size:30pt;font-weight:800;color:var(--lav);opacity:.3;line-height:1}
.clabel{display:inline-block;font-size:7.4pt;font-weight:800;letter-spacing:.1em;color:var(--wine);
  background:var(--gold);border:2pt solid var(--wine);border-radius:99px;padding:1mm 3.4mm;
  box-shadow:2px 2px 0 var(--wine);margin-top:2mm}
h1.ptitle{font-size:21pt;font-weight:900;color:var(--wine);letter-spacing:.01em;
  margin-top:2.4mm;line-height:1.4}
.hr-main{border:0;border-top:2pt dotted var(--lav);margin:3mm 0 3.6mm}

/* ── 共通部品 ── */
.lead{font-size:8.6pt;line-height:1.95;color:var(--ink2);margin-bottom:3.4mm}
.freeband{background:var(--gold);border:2.2pt solid var(--wine);border-radius:4mm;
  padding:2.6mm 4mm;display:flex;gap:4mm;align-items:center;font-size:7.8pt;margin-bottom:3mm;
  box-shadow:3px 3px 0 var(--wine)}
.freeband .fb-t{font-size:6.4pt;font-weight:800;letter-spacing:.14em;color:var(--wine2);display:block}
.freeband .fb-h{font-size:8.6pt;font-weight:900;color:var(--wine);white-space:nowrap}
.freeband span.it{color:var(--wine);font-weight:700}
.freeband b{color:var(--wine2);font-weight:800}
.centernote{text-align:center;font-size:7.6pt;font-weight:700;color:var(--wine2);margin:2.6mm 0 3.2mm}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:3.4mm}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}
.panel{background:var(--paper);border:2.2pt solid var(--wine);border-radius:4mm;
  padding:3mm 3.6mm;box-shadow:var(--sh)}
.panel.pink{background:var(--pink)}
.panel .pt{font-size:8pt;font-weight:900;color:var(--wine2);margin-bottom:1.8mm}
.panel p{font-size:8pt;line-height:1.9;color:var(--ink)}
.sect-h{font-size:9pt;font-weight:900;color:var(--wine);margin:4mm 0 2.4mm;
  display:flex;align-items:center;gap:2.4mm}
.sect-h::after{content:"";flex:1;border-top:2pt dotted var(--lav)}
.tag{display:inline-block;border:1.8pt solid var(--wine);border-radius:99px;
  padding:1mm 3mm;font-size:7.4pt;font-weight:700;color:var(--wine);margin:0 1.6mm 1.8mm 0;
  background:var(--paper);box-shadow:2px 2px 0 var(--lav)}
.stat{background:var(--paper);border:2.2pt solid var(--wine);border-radius:4mm;
  padding:3mm 3.6mm;box-shadow:var(--sh)}
.stat .sh{font-size:8pt;font-weight:900;color:var(--wine2);margin-bottom:2mm}
.strow{display:flex;justify-content:space-between;font-size:8pt;padding:1mm 0;color:var(--ink2);font-weight:700}
.st{color:var(--wine2);letter-spacing:.06em}.st.off{color:#e6dcec}
.deflist dt{font-size:8pt;font-weight:900;color:var(--wine2);float:left;width:14mm}
.deflist dd{font-size:8pt;line-height:1.85;margin-left:14mm;padding-bottom:1.8mm;
  border-bottom:1.6pt dotted var(--rule);margin-bottom:1.8mm;color:var(--ink2)}
.foot-note{margin-top:auto;background:var(--cream2);border:2pt solid var(--wine);border-radius:4mm;
  padding:2.6mm 3.6mm;font-size:7.6pt;line-height:1.85;color:var(--ink2);box-shadow:2px 2px 0 var(--lav)}
.foot-note b{color:var(--wine2);font-weight:900;font-size:7.4pt;margin-right:2mm}
.pfoot{display:flex;justify-content:space-between;font-size:7pt;font-weight:700;
  color:var(--ink3);margin-top:auto;padding-top:3mm}
.pfoot .pno{color:var(--wine2);font-weight:800}
ul.check{list-style:none}
ul.check li{font-size:8pt;line-height:1.95;color:var(--ink2);padding-left:5mm;position:relative;font-weight:500}
ul.check li::before{content:"💗";position:absolute;left:0;font-size:7pt}
ul.ng li::before{content:"💔";font-size:7pt}
ul.ok li::before{content:"✅";font-size:7pt}
.num{display:inline-flex;width:5.6mm;height:5.6mm;border-radius:50%;background:var(--wine2);color:#fff;
  font-size:7.4pt;font-weight:800;align-items:center;justify-content:center;
  font-family:'Baloo 2',cursive;flex:none;border:1.6pt solid var(--wine)}
.step{display:flex;gap:2.8mm;align-items:flex-start;margin-bottom:2.6mm}
.step .sbody{font-size:8pt;line-height:1.9}
.step .sbody b{color:var(--wine2);font-weight:900;display:block;font-size:8.4pt;margin-bottom:.6mm}
"""


# ══════════════════════════════════════════════════════════════
#  ページ部品
# ══════════════════════════════════════════════════════════════
def page(code, body, chapno="", clabel="", title="", pno="", cls=""):
    d = LOC[code]
    head = ""
    if pno:
        head = f'''<div class="phead"><span>🐾 {d["breed"]}の恋愛トリセツ</span>
        <span>{clabel.split("・")[0] if clabel else ""}</span></div>'''
    chap = f'<div class="chapno">{chapno}</div>' if chapno else ""
    ttl = ""
    if title:
        ttl = f'<div class="clabel">{clabel}</div><h1 class="ptitle">{title}</h1><hr class="hr-main">'
    foot = ""
    if pno:
        foot = f'''<div class="pfoot"><span>{sp(d["breed"][:6])}　·　{sp(code)}</span>
        <span class="pno">♢　{pno}</span></div>'''
    return f'<section class="page {cls}"><div class="inner">{chap}{head}{ttl}<div class="pbody">{body}</div>{foot}</div></section>'

def note(label, text):
    return f'<div class="foot-note"><b>{label}</b>{text}</div>'

# ══════════════════════════════════════════════════════════════
#  ENFJ（サイベリアン）専用コンテンツ
# ══════════════════════════════════════════════════════════════
C = {
 "code":"ENFJ",
 "subtitle":"寄り添い上手な、みんなの安らぎ",
 "cover_lead":"みんなの安らぎ担当。だけど本命の前では、ちょっと不器用。<br>そんなあなたの恋を、ぜんぶ解説するトリセツです🐾",
 "pedigree":"2891",
 "free_tags":["タイプはサイベリアン（ENFJ）","恋は寄り添い・献身タイプ","包容力・聞き上手・献身"],
 "outside":"あったかくて、誰からも頼られる聞き上手。落ち込んでる人のそばにいつのまにか座ってる、みんなの安らぎ担当。恋愛でもモテるけど、「誰にでも優しい人」に見られがち。",
 "inside":"でも本命には、誰よりまっすぐで一途。頼られ役の顔の裏では、好きな人の幸せだけをひたすら願ってる。「みんなに優しい」と「本当に大事な人」は、自分の中では完全に別ものなんです。",
 "core":[("包容力","相手の幸せ＝自分の幸せ。寄り添うのに迷いがない。"),
         ("共感","察する力が高すぎる。だから一人で抱え込んじゃう。"),
         ("献身","誰とでも心を通わせられる。でも本命への一途さは別格。")],
 "core_lead":"サイベリアンの恋は「包み込む」ことから始まる。相手の幸せを願う気持ちが先に出ちゃうから、自分のことはどうしても後回し。でもね、本当に大事な関係って、支え合ってはじめて長続きします。",
 "keywords":["愛情深い","寄り添い型","聞き上手","一途","頼られ役","癒し系","世話好き","本命主義"],
 "tokimeki":["ちゃんと「ありがとう」と言ってくれた時","気遣いを当たり前にせず受け取ってくれた時","「無理しないでね」と言われた時"],
 "jirai":["優しさを「当たり前」に扱われた時","「誰にでも優しいだけでしょ」と言われた時","感謝がない一方通行がずっと続いた時"],
 # CH02
 "stages":[("気配り","相手の様子を自然と気にかける"),("お世話","気づいたら支えている"),
           ("特別扱い","この人だけ特別かも"),("告白","まっすぐ気持ちを伝える"),
           ("全力愛情","惜しみなく愛を注ぐ")],
 "stage_warn":"Stage2の「お世話」が行きすぎると、相手が求める前から与えちゃって、つい見返りを期待しがち。「これ、相手は望んでる？」と一度確認するクセをつけましょう。",
 "stage_str":"気持ちをまっすぐ言えるのは、とても大きな強みです。尽くし度★5・一途度★4の通り、一度伝えた気持ちはブレずに続くタイプです。",
 "speed":[("早め","アプローチまで"),("穏やか","表現の質"),("安定","気持ちの持続力")],
 "loved":[("とにかく安心感がすごい","そばにいてくれるだけで、相手は「自分は大切にされている」と確信できます。"),
          ("一緒にいると心がほどける","あなたのあたたかさが、相手の張りつめた日常をゆるめてくれます。"),
          ("裏表がまったくない","誰にでも優しく見えても、本命への態度は誰より誠実。そのブレなさが信頼になります。")],
 # CH03 罠（サイトのcons＝無料版で見えている3つ）
 "traps":[("抱え込みがち","弱音を見せられず、一人で抱える",
           "頼られるのは慣れてても、頼るのは全然慣れてない。しんどさを一人で処理し続けて、限界がくるまで誰にも気づかれない。相手からは「何も困っていない人」に見えてしまいます。",
           "週に一度でかまいません。「実はちょっと疲れてて」って、オチのない話を渡してみてください。弱さの共有は、実は距離をいちばん縮めます。"),
          ("自分を後回しにする","相手を優先するあまり、自分の希望が消える",
           "相手を優先しすぎて、自分がどうしたいのか分からなくなる。気づいたらヘトヘトで、急に距離を置きたくなることもあります。",
           "1日5分でかまいません。「今、自分どう感じてる？」って確認する時間を作りましょう。自分を満たすのも、ちゃんと愛情のうちです。"),
          ("甘えるのが苦手","受け取る側になれず、関係が一方通行になる",
           "あげるのは得意なのに、もらうのは苦手。相手が何かしようとすると「大丈夫」と遠慮してしまい、相手に「必要とされていないのかな」と思わせることもあります。",
           "「ありがとう、助かる」と素直に🎁 受け取る練習を。甘えることは、相手に「役に立てた」という喜びを贈ることでもあります。")],
 "trap_flip":[("抱え込みグセ","一人で立てる強さ","自分で立てる力があるから、誰かを支えられるんです。"),
              ("後回しグセ","思いやりの深さ","自分を後にできるのは、相手を本気で大切にしている証拠です。"),
              ("甘え下手","与えられる才能","もらう前に与えられる人は、それだけでレアな存在です。")],
 # CH04/05/06
 "grp_comment":{"NT":"リアクション薄めでも、ちゃんと愛情はあります。焦らず行動を見て判断を。",
                "NF":"感情を深く分かち合える相手。お互い抱え込みすぎないのがコツです。",
                "SJ":"安定志向が合う相手。あなたの包容力が、相手の緊張をほどきます。",
                "SP":"一緒にいて楽しい組み合わせ。あなたの気配りが相手の自由を支える土台に。"},
 "why_high":"サイベリアンの「惜しみなく与える力」を、NFの「深く受け止める感受性」が循環させてくれるから。一方通行になりがちなあなたの愛が、ちゃんと返ってくる。同じ理想を語り合える仲間だからこそ、お互い満たし合える関係になれます🐾",
 "top5_cm":["寄り添い合うソウルメイト。お互いの感情を深く理解し合える最高の相互理解ペア。あなたが与える愛を、相手は全力で受け止めてくれる。",
            "好奇心の塊のような相手。あなたの安心感が、ソマリの自由な冒険を支える帰る場所になる。飽きのこない関係に。",
            "洞察の深い相手との組み合わせ。言葉にしない部分まで読み合えるので、あなたが抱え込んでも気づいてもらえる稀有な相手。",
            "静かな思考家との組み合わせ。あなたの愛情表現が、INTPの内に秘めた感情を外に引き出すきっかけになる。",
            "発想が跳ねる相手。あなたの受け止める力と相手の刺激が組み合わさり、飽きのこない関係に。"],
 "top5_line":["「いつも受け止めてくれてありがとう」","「一緒にいると世界が広がる」","「あなたの気持ち、聞かせて」",
              "「あなたのこと、ちゃんと見ています」","「一緒にいると楽しい！」"],
 "top5_common":"5タイプに共通するのは「あなたの愛情をきちんと受け取り、お返しできる人」であること。一方的に与えるだけの関係ではなく、循環する愛情こそが、あなたを満たしてくれます。",
 "worst":[("課題","どちらも行動的だが、ESTPはスピードと刺激の人。あなたの心の充電が追いつかず、寄り添う余裕を失いやすい。",
           "対策","「今日は静かに過ごしたい」を早めに宣言。テンポの違いは、先に共有しておけば衝突になりません。"),
          ("課題","安定志向は似ているが、ISTJは感情表現が最小限。あなたの気遣いが言葉で返ってこず、「伝わっているのか」が見えにくい。",
           "対策","気持ちではなく「事実」で伝え合う。「週1で電話したい」など具体的な希望に翻訳すると、誠実に応えてくれます。"),
          ("課題","どちらも面倒見がよく責任感が強いが、ESTJは正論で解決しようとする。あなたの「気持ちを聞いてほしい」とすれ違いやすい。",
           "対策","話す前に「解決策ではなく、ただ聞いてほしい」と一言添える。目的を共有すれば、頼れる味方になります。")],
 "worst_line":[("◎「今日は一緒にのんびりしたい」","✕「ちょっと落ち着いてほしい」"),
               ("◎「あなたの誠実さ、ちゃんと伝わってる」","✕「もっと気持ちを言葉にしてよ」"),
               ("◎「聞いてくれるだけで助かる」","✕「正論はもういいから」")],
 # CH07 LINE
 "line_aru":["つい長文で気持ちを伝えちゃう","スタンプと絵文字で感情マシマシ","相手の様子をすぐ気にしちゃう",
             "既読つけたらすぐ返したくなる","既読つかないとちょっとソワソワ"],
 "line_sign":["毎日連絡したくなってる","相手の予定を覚えてて聞いちゃう","褒め言葉が自然と増える",
              "「会いたい」が素直に出る","相手の好きなもの、こっそり調べてる"],
 "line_ng":["相手の負担を考えず尽くしすぎ","既読つかなくて連投しちゃう","自分の気持ちをずっと後回し"],
 "line_ok":["「無理しないでね」で寄り添う","返信ペースは相手に合わせる","「実は私も…」と自分の話もする"],
 "omamori":[("心配しすぎた時","「気になったから連絡してみたよ」"),
            ("尽くしすぎた時","「私もこうしたかったから、気にしないで」"),
            ("本音を言いたい時","「実は私も、こう思ってたんだ」")],
 "line_talk":[("them","今日はちょっと疲れた…","19:04"),
              ("me","お疲れさま！無理しないでね、力になれることあったら言って","19:05"),
              ("them","ありがとう、それだけで元気出た","19:06")],
 "line_recv":"与えるのは得意でも、受け取るのが苦手なあなた。「ありがとう、助かる！」って甘えるのも、ちゃんと愛情です。たまには「○○してほしいな」と言ってみてください。受け取る姿は、相手をとても安心させます。",
 "templates":[("デートに誘う","「今度〇〇行かない？ あなたとなら楽しそう」"),
              ("やんわり断る","「その日は難しいけど、また誘ってね」"),
              ("謝る","「言葉足らずでごめん。本当はこう思ってた」")],
 # CH08
 "fight_pat":[("笑顔で本音を隠しちゃう","傷ついてても「大丈夫」って笑っちゃうから、相手は問題に気づけません。あとから不満が一気に出ることもあります。"),
              ("抱え込んで消耗する","ケンカのあとも相手に気を遣い続けて、自分の心を休ませる時間が取れません。"),
              ("自分を責めすぎる","うまくいかないと「私のせいかも」って抱え込んで、どんどん自己否定モードになってしまいます。")],
 "makeup3":[("「実は」から始めてみる","笑顔の下の本当の気持ちを、信頼できる相手にだけは見せてみましょう。完璧でいなくて大丈夫です。"),
            ("まず自分を休ませる","仲直りを急がなくて大丈夫。自分を満たしてから向き合う方が、ずっとうまくいきます。"),
            ("「私のせいじゃないかも」と思ってみる","全部を自分の責任にしないこと。相手にも半分ある、くらいがちょうどいいです。")],
 "kentai":"「寄り添っているのに満たされない…」って感じたら、それがマンネリのサインです。与えることに疲れているなら、伝えていい合図。自分の希望を言うのは、関係を深める第一歩です。",
 "refire":[("「してほしい」を言ってみる","与えるだけでなく、受け取る日をつくりましょう。甘えるのも愛情です。"),
           ("ありがとうを交換する","「ありがとう」を二人で言い合う習慣をつくりましょう。"),
           ("自分を満たす日をつくる","寄り添いはちょっとお休みして、自分のための時間を持ちましょう。")],
 # CH09
 "marry_cond":[("気遣いに「ありがとう」を言える人","その一言が、あなたの愛情を回し続ける燃料になる。"),
               ("本音を引き出してくれる人","笑顔の裏の気持ちに気づいて、言葉にするのを手伝ってくれる人。"),
               ("たまには甘えさせてくれる人","あげるだけじゃなく、もらう側にもなれる関係をつくってくれる人。"),
               ("交友関係を尊重してくれる人","友達の多さを、嫉妬じゃなく魅力として見てくれる人。"),
               ("一緒に成長を楽しめる人","お互い与え合いながら、二人で伸びていける関係を望む人。")],
 "chosen":[("毎日が記念日みたいになる","尽くし度★5のあなたに選ばれた人は、小さな愛情表現で満たされ続けます。"),
           ("心がほどける居場所ができる","あなたとの関係は、相手にとって世界でいちばん安心できる場所になります。"),
           ("本気の愛情を独り占めできる","一途度★4のあなたが選んだ相手は、誰にも奪われない愛情を受け取れます。")],
 "marry_q":["お金の使い方・将来の貯め方は？","家族・親との距離感は？","子ども・暮らしの理想像は？",
            "一人時間と二人時間のバランスは？","ケンカの時、どう仲直りしたい？"],
 # CH10-12
 "attach_main":"基本は安定型。人を信じて、愛情を惜しみなく注げるタイプ。ただ「相手の役に立てているか」が自信の土台になっているため、寄り添っても反応が薄いと一気に不安型に傾いて、見捨てられ不安が出てきます。",
 "anx_moment":["既読ついたのに返信がこない","「ありがとう」が返ってこない",
               "相手が一人の時間を欲しがっている","寄り添っているのに距離を感じる"],
 "anx_rx":["自分の価値を「役に立つか」で測らない","返信が遅い＝愛が薄い、ではない",
           "与える前に、まず受け取ってみる","相手の「一人時間」は信頼の証だと思う"],
 "give_lang":[("サービス行為","最も強い"),("肯定の言葉","強い"),("クオリティタイム","中"),
              ("スキンシップ","低"),("贈り物","低")],
 "recv_lang":[("肯定の言葉","最も欲しい"),("クオリティタイム","欲しい"),("スキンシップ","中"),
              ("サービス行為","中"),("贈り物","低")],
 # 図解用：give_langの並び順に対応した [与える強さ, 受け取りたい強さ]（各5段階）
 "lang_score":[[5,4,3,2,1],[3,5,3,4,1]],
 # 図解用：愛着スタイル4象限の座標（0〜1／x=回避の強さ, y=不安の強さ）
 "quad_x":0.30, "quad_y":0.62,
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
 "pitfall_quote":"恋とは、相手をどう変えるかではなく、<br>自分の優しさをどこに向けるか、なんですよね。",
 "triangle":[("親密性",90,"とても高い","心を通わせ、深くつながる力は抜群。"),
             ("コミットメント",85,"高い","一度決めた相手に寄り添い続ける責任感。"),
             ("情熱",65,"中","燃え上がりより、穏やかな愛情が長く続く。")],
 "bigfive":[("協調性","Agreeableness",92,"思いやりと共感のかたまり。相手を優先しすぎるのは注意。"),
            ("外向性","Extraversion",88,"人とのつながりがエネルギー源。場をあたためる力あり。"),
            ("誠実性","Conscientiousness",80,"約束を守るし、関係にちゃんと責任を持つ。記念日も大事。"),
            ("開放性","Openness",70,"理想を描いて、相手の可能性を信じる想像力がある。"),
            ("神経症傾向","Neuroticism",55,"普段は穏やか。でも「嫌われたかも」で揺れやすい一面も。")],
 "cogfn":[("Fe","主導機能","外向的感情","相手の感情を一瞬で察知して、場を整える力。「この人が今なにを求めているか」が自然にわかる、ENFJ最大の武器。恋愛では究極の気配り上手。"),
          ("Ni","補助機能","内向的直観","関係の「未来像」を描く力。この人とどうなりたいか、ちゃんと絵が見えています。一途さと、相手の本質を見抜く洞察力になる。"),
          ("Se","第三機能","外向的感覚","今この瞬間を楽しむ力。デートや体験の共有で距離がぐっと縮まる。ここが育つと、恋にメリハリと情熱が出てくる。"),
          ("Ti","劣等機能","内向的思考","ストレス時の弱点。感情で動くあなたが追い詰められると、急に理屈っぽく相手を分析・批判してしまうことが。疲れたら一人で休みましょう。")],
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
 "closing":"あなたが与える愛は、<br>まわりをあたためる才能です。",
 "enfj_msg":"あなたは「もっと寄り添えば戻れる」って考えがち。でも復縁に必要なのは尽くす量ではなく、二人が変わること。取り戻すより、お互い成長して再会できるかを見てみて🐾",
}

# ══════════════════════════════════════════════════════════════
#  追加CSS（専用レイアウト）
# ══════════════════════════════════════════════════════════════
CSS += """
/* 表紙 */
.cover{display:flex;flex-direction:column;align-items:center;text-align:center;height:100%;padding-top:3mm}
.cov-top{display:inline-block;font-size:8pt;font-weight:800;color:var(--wine);background:var(--gold);
  border:2.2pt solid var(--wine);border-radius:99px;padding:1.4mm 5mm;box-shadow:3px 3px 0 var(--wine)}
.cov-top .ln{display:none}
.cov-ped{font-family:'Baloo 2',cursive;font-size:8pt;font-weight:700;letter-spacing:.2em;
  color:var(--ink3);margin-top:3.4mm}
.cov-medal{width:66mm;height:66mm;border-radius:50%;border:2.6pt solid var(--wine);
  margin:6mm auto 0;display:flex;align-items:center;justify-content:center;position:relative;
  background:var(--paper);box-shadow:5px 5px 0 var(--lav)}
.cov-medal::before{display:none}
.cov-medal img{width:57mm;height:57mm;border-radius:50%;object-fit:cover}
.cov-breed-en{display:none}
.cov-sub{font-size:10pt;font-weight:800;color:var(--wine2);margin-top:6mm;letter-spacing:.02em}
.cov-name{font-size:33pt;font-weight:900;color:var(--wine);letter-spacing:.02em;margin-top:2.4mm;line-height:1.3}
.cov-ln{width:0;border:0;margin:3mm auto}
.cov-code{display:inline-block;font-size:10pt;font-weight:800;color:var(--wine);
  background:var(--paper);border:2.2pt solid var(--wine);border-radius:99px;padding:1.4mm 5mm;
  box-shadow:3px 3px 0 var(--lav)}
.cov-lead{font-size:9pt;line-height:2;color:var(--ink2);margin-top:6mm;font-weight:500}
.cov-chips{display:flex;flex-wrap:wrap;justify-content:center;gap:2.2mm;margin-top:8mm;max-width:135mm}
.cov-chips span{font-size:8pt;font-weight:800;color:var(--wine);background:var(--paper);
  border:2pt solid var(--wine);border-radius:99px;padding:1.2mm 3.4mm;box-shadow:2px 2px 0 var(--lav)}
.cov-pages{margin-top:6mm;font-size:9pt;font-weight:700;color:var(--ink2)}
.cov-pages b{font-family:'Baloo 2',cursive;font-size:15pt;font-weight:800;color:var(--wine2);margin:0 1mm}
.cov-seal{width:0;height:0;border:0;margin:0;display:none}
.cov-bot{display:inline-block;font-size:13pt;font-weight:900;color:var(--wine);
  background:var(--gold);border:2.4pt solid var(--wine);border-radius:99px;padding:2mm 7mm;
  box-shadow:4px 4px 0 var(--wine);margin-top:auto}
.cov-bot2{font-size:7.4pt;font-weight:700;letter-spacing:.06em;color:var(--ink3);margin-top:3.4mm}

/* もくじ */
.toc-part{font-size:8.4pt;font-weight:900;color:var(--wine);background:var(--cream2);
  border:2pt solid var(--wine);border-radius:99px;padding:1.2mm 3.6mm;margin:3.6mm 0 2.2mm;
  display:flex;justify-content:space-between;box-shadow:2px 2px 0 var(--lav)}
.toc-part b{color:var(--wine2);font-weight:900}
.toc-row{display:flex;align-items:baseline;font-size:8.2pt;padding:1.2mm 0;color:var(--ink2);font-weight:600}
.toc-row .dots{flex:1;border-bottom:1.6pt dotted var(--lav);margin:0 2.4mm}
.toc-row .n{font-family:'Baloo 2',cursive;color:var(--wine2);font-size:8.6pt;font-weight:800}

/* イントロ */
.intro-card{background:var(--paper);border:2.2pt solid var(--wine);border-radius:4mm;
  padding:3.2mm 2.6mm;text-align:center;box-shadow:var(--sh)}
.intro-card .ic{font-size:16pt}
.intro-card .it{font-size:8pt;font-weight:900;color:var(--wine2);margin:1.6mm 0 1.2mm}
.intro-card p{font-size:7.4pt;line-height:1.8;color:var(--ink2)}
.warnbar{border:2pt solid var(--wine);background:var(--cream2);border-radius:4mm;
  padding:2.6mm 3.6mm;font-size:7.4pt;color:var(--ink2);line-height:1.85;margin-top:3.4mm;
  box-shadow:2px 2px 0 var(--lav)}

/* 相性マップ */
.cmap-grp{margin-bottom:3mm}
.cmap-h{display:inline-block;font-size:7.6pt;font-weight:900;color:var(--wine);background:var(--gold);
  border:1.8pt solid var(--wine);border-radius:99px;padding:.7mm 3mm;margin-bottom:1.8mm}
.cmap-row{display:grid;grid-template-columns:repeat(4,1fr);gap:2.4mm}
.cbox{background:var(--paper);border:2pt solid var(--wine);border-radius:3.4mm;
  padding:2mm 1.6mm;text-align:center;box-shadow:2px 2px 0 var(--lav)}
.cbox.you{background:var(--wine2);box-shadow:2px 2px 0 var(--wine)}
.cbox.you .cb-b,.cbox.you .cb-s,.cbox.you .cb-c{color:#fff}
.cbox .cb-b{font-size:6.8pt;font-weight:700;color:var(--ink2);line-height:1.4;min-height:8mm;
  display:flex;align-items:center;justify-content:center}
.cbox .cb-s{font-family:'Baloo 2',cursive;font-size:15pt;font-weight:800;color:var(--wine2);line-height:1}
.cbox .cb-c{font-size:6.2pt;font-weight:700;letter-spacing:.1em;color:var(--ink3);margin-top:.8mm}
.legend{display:flex;gap:4mm;justify-content:center;font-size:7pt;font-weight:700;color:var(--ink3);margin:2.6mm 0}
.legend i{font-style:normal;color:var(--wine2);font-weight:800}

/* TOP5 */
.t5{display:flex;gap:3mm;align-items:center;background:var(--paper);border:2pt solid var(--wine);
  border-radius:3.6mm;padding:2.4mm 3mm;margin-bottom:2.4mm;box-shadow:2px 2px 0 var(--lav)}
.t5 .rk{font-family:'Baloo 2',cursive;font-size:17pt;font-weight:800;color:var(--wine2);width:7mm;flex:none;line-height:1}
.t5 .t5b{flex:1}
.t5 .t5n{font-size:9pt;font-weight:900;color:var(--wine)}
.t5 .t5n small{font-size:7pt;color:var(--ink3);font-weight:700;margin-left:2mm}
.t5 .t5c{font-size:7.6pt;line-height:1.8;color:var(--ink2);margin-top:.8mm}
.t5 .t5s{font-family:'Baloo 2',cursive;font-size:16pt;font-weight:800;color:var(--wine2);flex:none}

/* バー */
.bar{height:3.4mm;background:#f0e6f6;border:1.6pt solid var(--wine);border-radius:99px;overflow:hidden;margin-top:1.2mm}
.bar i{display:block;height:100%;background:repeating-linear-gradient(45deg,var(--wine2),var(--wine2) 2mm,var(--lav) 2mm,var(--lav) 4mm)}
.brow{margin-bottom:2.8mm}
.brow .bh{display:flex;justify-content:space-between;font-size:8pt;color:var(--ink2);font-weight:700}
.brow .bh b{color:var(--wine);font-weight:900}
.brow .bh .v{font-family:'Baloo 2',cursive;font-size:10pt;font-weight:800;color:var(--wine2)}
.brow p{font-size:7.4pt;color:var(--ink3);line-height:1.75;margin-top:.9mm}

/* LINE風 */
.chat{background:#eaf4ea;border:2.2pt solid var(--wine);border-radius:4mm;padding:3mm;box-shadow:var(--sh)}
.chat .ch-h{font-size:7.2pt;font-weight:800;color:var(--wine);border-bottom:1.6pt solid var(--wine);
  padding-bottom:1.4mm;margin-bottom:2.4mm}
.bub{max-width:76%;font-size:7.6pt;line-height:1.8;padding:2mm 2.8mm;border-radius:3mm;margin-bottom:2mm;
  border:1.6pt solid var(--wine)}
.bub.them{background:#fff;color:var(--ink)}
.bub.me{background:#b6e3a8;margin-left:auto;color:var(--wine)}
.bub .tm{display:block;font-size:5.8pt;color:var(--ink3);margin-top:.7mm;font-weight:700}

/* あるある30 */
.aru-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 5mm}
.aru-i{display:flex;gap:2mm;font-size:7.9pt;line-height:1.8;padding:1.75mm 0;
  border-bottom:1.4pt dotted var(--rule);color:var(--ink2);font-weight:500}
.aru-i .an{font-family:'Baloo 2',cursive;color:var(--wine2);font-size:7.4pt;font-weight:800;width:4.6mm;flex:none}

/* ワーク罫線 */
.wline{border-bottom:1.6pt dashed var(--lav);height:8mm}
.wbox{background:var(--paper);border:2.2pt solid var(--wine);border-radius:4mm;padding:3mm 3.4mm;
  margin-top:1.8mm;box-shadow:var(--sh)}
.wlabel{font-size:8.2pt;font-weight:900;color:var(--wine);margin:3.4mm 0 1.6mm;display:flex;gap:2.4mm;align-items:center}

/* フローチャート */
.flow-q{background:var(--gold);border:2.2pt solid var(--wine);border-radius:99px;
  padding:2mm 3.4mm;font-size:8.4pt;font-weight:900;color:var(--wine);text-align:center;
  box-shadow:3px 3px 0 var(--wine)}
.flow-ar{text-align:center;color:var(--wine2);font-size:9pt;font-weight:800;margin:1.6mm 0}
.flow-2{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:1.8mm}
.flow-b{border:2pt solid var(--wine);background:var(--paper);border-radius:3.6mm;padding:2.2mm 2.8mm;
  box-shadow:2px 2px 0 var(--lav)}
.flow-b .fl{font-size:7pt;font-weight:900;color:var(--wine2);display:block;margin-bottom:.9mm}
.flow-b p{font-size:7.6pt;line-height:1.8;color:var(--ink2)}
.flow-goal{background:var(--wine2);color:#fff;border:2.2pt solid var(--wine);border-radius:99px;
  padding:2.6mm;text-align:center;font-size:9.4pt;font-weight:900;margin-top:2.8mm;
  box-shadow:3px 3px 0 var(--wine)}

/* 比較表 */
.cmp{width:100%;border-collapse:separate;border-spacing:0;font-size:7.6pt;
  border:2pt solid var(--wine);border-radius:3.4mm;overflow:hidden}
.cmp th{background:var(--cream2);color:var(--wine);font-weight:900;padding:2mm;
  border-bottom:1.8pt solid var(--wine);font-size:7.4pt}
.cmp td{padding:1.9mm 2.2mm;border-bottom:1.4pt dotted var(--rule);line-height:1.75;
  color:var(--ink2);vertical-align:top}
.cmp td.lb{background:var(--pink);color:var(--wine2);font-weight:900;white-space:nowrap;width:21mm}
.cmp tr:last-child td{border-bottom:0}

/* 章扉 */
.divider{display:flex;flex-direction:column;justify-content:center;align-items:center;height:100%;text-align:center}
.divider .dl{display:inline-block;font-size:8pt;font-weight:900;color:var(--wine);background:var(--gold);
  border:2.2pt solid var(--wine);border-radius:99px;padding:1.4mm 5mm;box-shadow:3px 3px 0 var(--wine)}
.divider h2{font-size:24pt;font-weight:900;color:var(--wine);line-height:1.6;margin-top:7mm}
.divider .dp{font-size:8.6pt;line-height:2.1;color:var(--ink2);margin-top:5mm;max-width:124mm}
.divider .dlist{margin-top:9mm;font-size:8.4pt;font-weight:700;color:var(--ink2);line-height:2.6}
.divider .dq{margin-top:11mm;font-size:9pt;line-height:2.1;color:var(--wine2);font-weight:700}
.divider .dq small{display:block;font-family:'Baloo 2',cursive;font-size:7.2pt;
  letter-spacing:.14em;color:var(--ink3);margin-top:3mm;font-weight:700}
.refs{border-top:2pt dotted var(--lav);margin-top:3.4mm;padding-top:2.8mm}
.refs .rh{font-size:7pt;font-weight:900;color:var(--wine2);margin-bottom:1.8mm}
.refs .rg{display:grid;grid-template-columns:1fr 1fr;gap:1mm 4mm;font-size:6.6pt;color:var(--ink3);line-height:1.7}
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
      <div class="cov-top">🐾 にゃんこ恋愛トリセツ</div>
      <div class="cov-ped">for {code} ・ 完全版</div>
      <div class="cov-medal"><img src="data:image/webp;base64,{img_b64}"></div>
      <div class="cov-breed-en">{sp(B[:12])}</div>
      <div class="cov-sub">{C["subtitle"]}</div>
      <div class="cov-name">{B}</div>
      <div class="cov-ln"></div>
      <div class="cov-code">{sp(code)}　·　{R}</div>
      <div class="cov-lead">{C["cover_lead"]}</div>
      <div class="cov-chips">
        <span>#全16タイプ相性</span><span>#LINEの送り方</span><span>#ケンカ仲直り</span>
        <span>#甘え方のクセ</span><span>#長続きの条件</span><span>#復縁のすべて</span>
      </div>
      <div class="cov-pages">ぜんぶで <b>32</b> ページ</div>
      <div class="cov-seal"><div class="s1">{code}</div><div class="paw">🐾</div>
        <div class="s1">No.{C["pedigree"]}</div></div>
      <div class="cov-bot">恋愛トリセツ 完全版</div>
      <div class="cov-bot2">あなただけの1冊　·　16にゃんこ恋愛診断</div>
    </div>''', cls="cover-pg"))

    # ── P2 この本の使い方 ──
    cards = "".join(f'''<div class="intro-card"><div class="ic">{ic}</div>
      <div class="it">{t}</div><p>{p}</p></div>''' for ic,t,p in [
        ("♡","恋愛傾向の深掘り","外からは見えない、心の中の動きまで全部解説します。"),
        ("★","全16タイプ相性表","スコアとコメントで「あのコとの相性」が丸わかりです。"),
        ("✉","LINE攻略ガイド","自分のLINEのクセと、刺さる送り方がわかります。"),
        ("✎","書き込みワーク","読むだけで終わらせない、書いて整理する3枚。")])
    A(page(code, f'''<p class="lead">これは、{B}（{code}）のあなた専用の恋愛トリセツ。無料版が“入口”なら、こちらは全部のせの完全版です。自分でも気づいてないクセ、ハマりがちな落とし穴、相性のいいコの見つけ方まで、ぜんぶ書いてあります🐾</p>
      <div class="grid2" style="grid-template-columns:repeat(4,1fr);gap:2.4mm">{cards}</div>
      <div class="sect-h">📖 読み方のコツ</div>
      <div class="grid3">
        <div class="panel"><div class="pt">① まず通し読み</div><p>P4〜P12をさらっと読んで、まず全体をつかみましょう。</p></div>
        <div class="panel"><div class="pt">② 気になる人のページへ</div><p>好きな人ができたら、相性ページへ直行してください。</p></div>
        <div class="panel"><div class="pt">③ ワークに書き込む</div><p>P22〜24に自分の言葉で書くと、頭がスッキリします。</p></div>
      </div>
      <div class="sect-h">🎁 このトリセツで手に入るもの</div>
      <div class="grid3">
        <div class="panel pink"><div class="pt">自己理解</div><p>なんで毎回おなじパターンなのか、その理由がわかります。</p></div>
        <div class="panel pink"><div class="pt">相手選び</div><p>16タイプとの相性から、自分に合う人が見えてきます。</p></div>
        <div class="panel pink"><div class="pt">伝える力</div><p>我慢しないで、でも相手を責めずに気持ちを伝えられます。</p></div>
      </div>
      <div class="warnbar">⚠　このトリセツは楽しむためのコンテンツです。心理学的・医学的な診断ではないので、自分を知るきっかけとして、気軽にお読みください。</div>
      {note("💡 恋のまめ知識","心理学では、自分の気持ちを「言葉にする」だけでストレスが下がるとされています（感情ラベリング効果）。人に寄り添うあなたにこそ必要なセルフケアです。")}''',
      chapno="00", clabel=sp("INTRODUCTION"), title="このトリセツの使い方", pno="02"))

    # ── P3 もくじ ──
    def toc(rows):
        return "".join(f'<div class="toc-row"><span>{t}</span><span class="dots"></span><span class="n">{n}</span></div>' for t,n in rows)
    A(page(code, f'''<p class="lead">全7部構成。気になるページから開いてもOK、頭から読んでもOK。基礎編でざっくり知って、理論編で深掘り、ワークで整理、巻末で復縁まで。</p>
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
      {note("📌 読み方","迷ったら基礎編（P4〜P12）から。悩みがハッキリしてるなら、巻末に直行でも大丈夫です。")}''',
      chapno="♢", clabel=sp("CONTENTS"), title="もくじ", pno="03"))

    # ── P4 CH01 恋愛人格 ──
    core = "".join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in C["core"])
    stat = "".join(f'<div class="strow"><span>{PL[i]}</span>{stars(P[i])}</div>' for i in range(5))
    kw = "".join(f'<span class="tag">#{k}</span>' for k in C["keywords"])
    tk = "".join(f'<li>{x}</li>' for x in C["tokimeki"])
    jr = "".join(f'<li>{x}</li>' for x in C["jirai"])
    ft = "".join(f'<span class="it">♡　{t}</span>' for t in C["free_tags"])
    A(page(code, f'''<div class="freeband"><span class="fb-h"><span class="fb-t">{sp("FREE ver.")}</span>無料版のおさらい</span>{ft}</div>
      <div class="centernote">＼ 無料版はここまで。ここから先が、ぜんぶ本音のトリセツ ／</div>
      <div class="grid2">
        <div class="panel"><div class="pt">▶　外から見えるあなた</div><p>{C["outside"]}</p></div>
        <div class="panel pink"><div class="pt">▶　内側の本当のあなた</div><p>{C["inside"]}</p></div>
      </div>
      <div class="grid2" style="grid-template-columns:60mm 1fr;margin-top:3.4mm">
        <div class="stat"><div class="sh">📊 恋愛ステータス</div>
          {svg_radar(["一途度","尽くし度","結婚向き","嫉妬深さ","ドキドキ度"], P)}</div>
        <div><div class="pt" style="font-size:7.88pt;font-weight:700;color:var(--wine);letter-spacing:.1em;margin-bottom:1.8mm">💎 あなたの3つの軸</div>
          <dl class="deflist">{core}</dl></div>
      </div>
      <p class="lead" style="margin-top:3mm">{C["core_lead"]}</p>
      <div style="font-size:7.42pt;letter-spacing:.2em;color:var(--wine-l);margin-bottom:1.4mm">🏷 あなたの恋愛キーワード</div>
      <div>{kw}</div>
      <div class="sect-h">💘 ときめきスイッチ＆地雷スイッチ</div>
      <div class="grid2">
        <div class="panel pink"><div class="pt">♡　グッとくる瞬間</div><ul class="check">{tk}</ul></div>
        <div class="panel"><div class="pt">✕　一気に冷める瞬間</div><ul class="check ng">{jr}</ul></div>
      </div>
      {note("💡 知っとくと得",f"{code}型は全人口の約{RARITY[code]}%しかいないレアタイプ。人を惹きつける力と、尽くす優しさを両立できる人って、実はかなり珍しい存在です。")}''',
      chapno="01", clabel=f'{sp("CHAPTER")}　0 1', title=f"{B}って、こういう人", pno="04"))

    # ── P5 CH02 5段階 ──
    stg = "".join(f'''<div class="cbox"><div class="cb-s">0{i+1}</div>
      <div style="font-size:8.33pt;font-weight:700;color:var(--wine);margin:.8mm 0 .6mm">{t}</div>
      <div style="font-size:7.2pt;line-height:1.65;color:var(--ink2)">{s}</div></div>'''
      for i,(t,s) in enumerate(C["stages"]))
    spd = "".join(f'''<div class="cbox"><div style="font-size:10.12pt;color:var(--wine);font-weight:700">{v}</div>
      <div class="cb-c">{k}</div></div>''' for v,k in C["speed"])
    lv = "".join(f'<div class="panel pink"><div class="pt">♡　{t}</div><p>{s}</p></div>' for t,s in C["loved"])
    A(page(code, f'''<div class="freeband"><span class="fb-h"><span class="fb-t">{sp("FREE ver.")}</span>無料版のおさらい</span>
        <span class="it">無料版では「寄り添うタイプ」ってひとこと言っただけ。</span></div>
      <div class="panel" style="margin-bottom:3.2mm"><div class="pt">🔓 この章でわかること</div>
        <p>恋に落ちるまでの5ステップを、心の動きごとに分解。それぞれの落とし穴と強み、恋のスピード感まで解説します。</p></div>
      <div class="wbox" style="margin:0 0 3mm;padding:2.6mm 3.4mm">
        {svg_flow5([(f"0{{i+1}}", t) for i,(t,_) in enumerate(C["stages"])])}</div>
      <div class="cmap-row" style="grid-template-columns:repeat(5,1fr)">{stg}</div>
      <div class="grid2" style="margin-top:3.4mm">
        <div class="panel"><div class="pt">⚠️ やりすぎ注意ポイント</div><p>{C["stage_warn"]}</p></div>
        <div class="panel pink"><div class="pt">💪 Stage4のまっすぐさが強み</div><p>{C["stage_str"]}</p></div>
      </div>
      <div class="sect-h">⚡ {B}の恋愛スピード</div>
      <div class="cmap-row" style="grid-template-columns:repeat(3,1fr)">{spd}</div>
      <div class="sect-h">💗 寄り添うあなたが愛される理由</div>
      <div class="grid3">{lv}</div>
      {note("💡 ひとくちメモ","「単純接触効果」といって、人は何度も接する相手を好きになりやすいとされています。あなたの気配りの多さは、知らないうちに相手の好意を育てています。")}''',
      chapno="02", clabel=f'{sp("CHAPTER")}　0 2', title="恋に落ちるまでの5ステップ", pno="05"))

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
        <span class="it">無料版では「気をつけたいところ」を3語出しただけ。</span></div>
      <div class="panel" style="margin-bottom:3mm"><div class="pt">🔓 この章でわかること</div>
        <p>3つのクセを「なんで起きる？→どうなる？→どうする？」まで分解。優しさを空回りさせず、ちゃんと魅力にする方法をお伝えします。</p></div>
      <div style="font-size:8.1pt;color:var(--wine);font-weight:700;margin-bottom:1.8mm">💭 でも、クセは「長所の裏返し」です</div>
      <div class="wbox" style="margin:0 0 3mm;padding:2.6mm 3.4mm">
        {svg_flip([(a, b, "") for a,b,c in C["trap_flip"]])}</div>
      {tr}
      {note("💡 恋のまめ知識","適度な自己開示は、むしろ親密度を上げるという研究があります。「本音を見せる」ことは、関係を深めるいちばんの近道です。")}''',
      chapno="03", clabel=f'{sp("CHAPTER")}　0 3', title="無意識にやりがちな3つのクセ", pno="06"))

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
        <span class="it">無料版では「相性のいいタイプTOP3」だけを公開していました。</span></div>
      <div class="panel" style="margin-bottom:2.8mm"><div class="pt">🔓 この章でわかること</div>
        <p>全16タイプの相性スコアを一気に公開。NT・NF・SJ・SPの4グループごとに、あなたの立ち位置と「なんで合うのか」まで見えてきます。ピンクの枠があなたです。</p></div>
      {grp_html}
      <div class="legend"><span><i>85〜</i> ベスト</span><span><i>75〜84</i> 好相性</span>
        <span><i>65〜74</i> 普通</span><span><i>〜64</i> 要工夫</span></div>
      <div class="panel pink" style="margin-bottom:2.8mm"><div class="pt">📏 スコアの読み方</div>
        <p>スコアは「出会った瞬間の合いやすさ」＝スタート地点で、恋の上限ではありません。85↑運命級／75↑good／65↑ふつう／〜64は伸びしろ大。低スコアでも、ちゃんと話せば育つ恋はいくらでもあります。</p></div>
      <div class="panel pink" style="margin-top:2.6mm"><div class="pt">💡 NF理想家と相性がいいワケ</div>
        <p>{C["why_high"]}</p></div>
      {note("💡 知っとくと得","相性の研究では「似ているほど安心、違うほど刺激」と言われます。似た者同士は安心ですが、たまに刺激も足すと長続きします。")}''',
      chapno="04", clabel=f'{sp("CHAPTER")}　0 4', title="全16タイプ 相性まるわかり表", pno="07"))

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
    A(page(code, f'''<div class="wbox" style="margin:0 0 3mm;padding:2.6mm 5mm">
        {svg_hbars([(BREED[rk[i][1]][:11], rk[i][0]) for i in range(5)], unit="%")}
        <div style="font-size:6.8pt;color:var(--ink3);text-align:center;margin-top:1mm">相性スコア上位5タイプ</div></div>
      <div style="margin-bottom:1mm">{t5}</div>
      <div class="sect-h">♡　💬 TOP5に効く「最初のひとこと」</div>
      <div class="grid2" style="gap:1mm 5mm">{lines}</div>
      <div class="panel pink" style="margin-top:2.6mm"><div class="pt">🔑 TOP5に共通していること</div>
        <p>{C["top5_common"]}</p>
        <p style="margin-top:1.4mm;padding-top:1.4mm;border-top:1.4pt dotted var(--rule)"><b style="color:var(--wine2)">見極める質問</b>　「最近ハマってることは？ なんで好き？」「一人の時間って何してる？」——答えの深さで相性が見えます。</p></div>
      {note("💡 ひとくちメモ","「ピグマリオン効果」では、期待された人はその通りに成長しやすいとされます。あなたの励ましは、相手の可能性を本当に開花させます。")}''',
      chapno="05", clabel=f'{sp("CHAPTER")}　0 5', title="相性いいコ TOP5", pno="08"))

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
    A(page(code, f'''<div class="wbox" style="margin:0 0 3mm;padding:2.6mm 4mm">
        {svg_gauge_row([(BREED[m][:10], m, sc) for sc,m in rk[-3:]])}
        <div style="font-size:6.8pt;color:var(--ink3);text-align:center;margin-top:1mm">この3タイプとの相性スコア（低いほど“工夫しがい”があります）</div></div>
      <p class="lead">スコアが低い＝ダメ、ではありません。相性スコアは「初期設定」であって「運命」ではありません。大事なのは、違いを知ったうえで歩み寄れるかどうか。この3タイプとの恋も、コツさえ知っていれば十分うまくいきます。</p>
      {w}
      <div class="sect-h">♡　💬 効くひとこと／NGなひとこと</div>
      {wl}
      {note("💡 恋のまめ知識","心理学者心理学者ゴットマンによれば、別れるカップルの差は「ケンカの有無」ではなく「仲直りのうまさ」なのだそうです。あなたの共感力は、そこでとても強い武器になります。")}''',
      chapno="06", clabel=f'{sp("CHAPTER")}　0 6', title="ちょっと手ごわいコとの付き合い方", pno="09"))

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
      <div class="sect-h">🫧 迷ったときのお守りフレーズ3選</div>
      <div class="grid3">{om}</div>
      <div class="grid2" style="grid-template-columns:1fr 1fr;gap:3.4mm;margin-top:3.4mm">
        <div class="chat"><div class="ch-h">‹　{BREED[rk[0][1]][:8]}　≡</div>{bubs}
          <div style="font-size:7.2pt;color:var(--wine2);margin-top:1mm">✓　この気にかける一言が最大の武器</div></div>
        <div class="panel pink"><div class="pt">🎁 受け取る練習</div><p>{C["line_recv"]}</p></div>
      </div>
      <div class="sect-h">♡　📝 そのままコピペOKな神テンプレ</div>
      <div class="grid3">{tp}</div>
      {note("💡 知っとくと得","メッセージで感謝を伝える回数が多いほど、関係の満足度が高いという研究もあります。あなたの素直な「ありがとう」は、科学的にも効いています。")}''',
      chapno="07", clabel=f'{sp("CHAPTER")}　0 7', title="LINEの送り方、これが正解", pno="10"))

    # ── P11 CH08 ケンカ ──
    fp = "".join(f'''<div class="panel"><div style="display:flex;gap:2mm;align-items:center;margin-bottom:1mm">
      <span class="num">{i+1}</span><b style="font-size:8.55pt;color:var(--wine)">{t}</b></div><p>{s}</p></div>'''
      for i,(t,s) in enumerate(C["fight_pat"]))
    mk = "".join(f'''<div class="step"><span class="num">{i+1}</span><div class="sbody">
      <b>{sp("STEP "+str(i+1))}　{t}</b>{s}</div></div>''' for i,(t,s) in enumerate(C["makeup3"]))
    rf = "".join(f'''<div class="panel pink"><div class="pt">{"①②③"[i]}　{t}</div><p>{s}</p></div>'''
      for i,(t,s) in enumerate(C["refire"]))
    A(page(code, f'''<div class="freeband"><span class="fb-h"><span class="fb-t">{sp("FREE ver.")}</span>無料版のおさらい</span>
        <span class="it">無料版は「ケンカしたときの行動」をちらっと出しただけ。</span></div>
      <div class="panel" style="margin-bottom:3mm"><div class="pt">🔓 この章でわかること</div>
        <p>あなたのケンカ＆マンネリのパターンを分析して、関係を壊さない仲直りの言葉と、冷めた空気を温め直す方法まで解説します。</p></div>
      <div style="font-size:8.1pt;font-weight:700;color:var(--wine);margin-bottom:1.6mm">{B}のケンカあるある</div>
      <div class="grid3" style="margin-bottom:3.2mm">{fp}</div>
      <div class="sect-h">🤝 3ステップ仲直り法</div>
      <div class="wbox" style="margin:0 0 2mm;padding:1.8mm 4mm">
        {svg_flow5([("1", C["makeup3"][0][0]), ("2", C["makeup3"][1][0]), ("3", C["makeup3"][2][0])])}</div>
      {mk}
      <div class="grid2" style="margin-top:2.6mm">
        <div class="panel"><div class="pt">倦怠期</div><p>{C["kentai"]}</p></div>
        <div class="panel pink"><div class="pt">🫣 笑顔の裏ルール</div>
          <p>「大丈夫」と笑う前の30秒、本当の気持ちを確かめてみてください。「実は、ちょっと寂しかった」のひとことで十分。完璧な笑顔より、弱さを見せた方が相手はあなたを大切にできます。</p></div>
      </div>
      <div class="sect-h">♡　🔥 マンネリ脱出アクション</div>
      <div class="grid3">{rf}</div>
      {note("💡 ひとくちメモ","「Iメッセージ」は心理学者ゴードンが提唱した伝え方。「私は」で始めるだけで、責める感じにならずに気持ちが伝わります。")}''',
      chapno="08", clabel=f'{sp("CHAPTER")}　0 8', title="ケンカ＆マンネリの抜け出し方", pno="11"))

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
        <div class="panel"><div class="pt">結婚観</div><p>結婚向きは★{P[2]}でかなり高め。愛情深くて家庭的だから、結婚してからも自然と相手や家族のために動けるタイプ。記念日も日々の気遣いも忘れない、あたたかい家庭をつくります。</p></div>
      </div>
      <div class="sect-h">💗 {B}が幸せになれる相手の条件</div>
      {mc}
      <p style="font-size:7.54pt;color:var(--ink3);line-height:1.8;margin-top:1.6mm">5つ全部そろっていなくて大丈夫です。「3つ以上あるかな？」くらいが目安です。足りないところを相手に変えてもらうより、お互い補い合える関係のほうが理想です。</p>
      <div class="sect-h">🎉 逆に、あなたを選んだ人はこんなに幸せ</div>
      <div class="grid3">{ch}</div>
      <div class="sect-h">♡　💍 結婚前に話しておきたい5つのこと</div>
      <div class="grid2" style="gap:.4mm 5mm">{mq}</div>
      <div class="panel pink" style="margin-top:2.4mm"><div class="pt">💍 「結婚かも」のサイン</div>
        <p>沈黙が心地いい／弱さも見せられる／一人の時間を邪魔されない／“5年後も隣にいる”が自然に想像できる。これが揃ったら、あなたの中ではもう“この人”です。</p></div>
      {note("💡 恋のまめ知識","長続きするカップルの共通点は「相手を変えようとしないこと」。与えるのが好きなあなたも、相手のペースを尊重するのが大切です。")}''',
      chapno="09", clabel=f'{sp("CHAPTER")}　0 9', title="長続きするのは、こんな人", pno="12"))

    # ── P13 PART II 扉 ──
    A(page(code, f'''<div class="divider">
      <div class="dl">{sp("PART II")}　·　{sp("ACADEMIC ANALYSIS")}</div>
      <h2>ちょっと理論で<br>読み解いてみる</h2>
      <p class="dp">心理学の有名な理論をもとに、あなたの恋愛をいろんな角度から分析します。「なんとなく感じていた自分」に、ちゃんと名前をつける章です。</p>
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
    A(page(code, f'''<p class="lead">愛着スタイル理論（Bowlby／Ainsworth）は、小さい頃に育った「人との距離の取り方」が恋愛にも表れるという考え方です。あなたの不安やクセの“根っこ”が見えてきます。</p>
      <div class="grid2" style="grid-template-columns:70mm 1fr;gap:4mm;align-items:start">
        <div class="wbox" style="margin:0;padding:2.4mm">
          {svg_quad(C["quad_x"], C["quad_y"], "回避（距離を置きたい）→", "不安（見捨てられ不安）→",
            ["不安型|尽くしすぎ","恐れ・回避型|求めと拒絶","安定型|ちょうどいい","回避型|一人が好き"])}
          <div style="font-size:6.6pt;color:var(--ink3);text-align:center;margin-top:1mm">●があなたの位置です</div></div>
        <div><div class="grid2" style="grid-template-columns:1fr 1fr;gap:2.2mm">{att4}</div>
          <div class="panel pink" style="margin-top:2.4mm"><div class="pt">{B}（{code}）の傾向</div><p>{C["attach_main"]}</p></div></div>
      </div>
      <div class="grid2" style="margin-top:3mm">
        <div class="panel"><div class="pt">あなたが不安になる瞬間</div>
          <ul class="check">{"".join(f"<li>{x}</li>" for x in C["anx_moment"])}</ul></div>
        <div class="panel"><div class="pt">安定型でいるための処方箋</div>
          <ul class="check ok">{"".join(f"<li>{x}</li>" for x in C["anx_rx"])}</ul></div>
      </div>
      <div class="sect-h">✨ 今日からできること</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　不安になったら連投せず、「ひと呼吸おいて6時間」ルールを試す。<br>
        ◇　1日1回、小さなお願いをして“受け取る”練習をする。</div>
      {note("📖 ちょっと理論の話","愛着スタイルは一生固定ではなく、安心できる関係を経験すると後から安定型に変われるとされています（獲得安定型）。自分のクセを知るのが、その第一歩。")}''',
      chapno="10", clabel=sp("ATTACHMENT STYLE"), title="あなたの甘え方のクセ", pno="14"))

    # ── P15 CH11 相手のタイプ別 ──
    pt4 = "".join(f'''<div class="panel {c}"><div class="pt">{t}<span style="font-size:6.52pt;letter-spacing:.2em;color:var(--ink3);margin-left:2mm">{sp(e)}</span></div><p>{s}</p></div>'''
      for t,e,s,c in [
      ("安定型","SECURE","あなたの愛情を素直に受け取ってくれる相性◎。尽くしすぎず、対等に。あなたも安心して甘えられる理想の相手。","pink"),
      ("不安型","ANXIOUS","あなたの愛情表現が刺さる相手。ただし「尽くす者同士」で共倒れ注意。安心の言葉をこまめに、でも依存し合わない距離を。",""),
      ("回避型","AVOIDANT","最も注意が必要。あなたの愛情が「重い」と感じられがち。追わずに待つ・一人時間を尊重するのが正解。詰めると逃げます。",""),
      ("恐れ・回避型","FEARFUL","近づくと逃げ、離れると求める難しい相手。一貫した態度と安全基地になること。あなたの包容力が活きるが、消耗にも注意。","")])
    A(page(code, f'''<p class="lead">相手の愛着スタイルがわかると、すれ違いの9割は防げます。与え上手なあなたが「相手に合わせて愛を届ける」ための実践ガイド。</p>
      <div style="display:grid;gap:2.6mm">{pt4}</div>
      <div class="wbox" style="margin:2.8mm 0 0;padding:3mm 5mm">
        {svg_hbars([("安定型", 95, "そのままで◎"),("不安型", 72, "安心の言葉を"),
                    ("回避型", 45, "追わず待つ"),("恐れ回避型", 55, "一貫した態度")], unit="")}
        <div style="font-size:6.8pt;color:var(--ink3);text-align:center;margin-top:1mm">
          バーはあなた（{code}）との相性のラクさ。低いほど“やり方”が必要です。</div></div>
      <div class="sect-h">♡　🔍 相手のタイプを見抜く3つの質問</div>
      <div class="grid3">
        <div class="panel"><p><b style="color:var(--wine2)">Q1</b>　不安なとき、連絡を増やす？減らす？</p></div>
        <div class="panel"><p><b style="color:var(--wine2)">Q2</b>　弱音を素直に言える人？隠す人？</p></div>
        <div class="panel"><p><b style="color:var(--wine2)">Q3</b>　一人時間と二人時間、どちらが好き？</p></div>
      </div>
      <div class="sect-h">✨ 今日からできること</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　相手の連絡量の増減を1週間メモして、愛着タイプを見極める。<br>
        ◇　回避型には「追わず待つ」、不安型には「安心のひと言」を実践する。</div>
      {note("💡 知っとくと得","研究では、カップルの一方が安定型だと、もう一方も時間とともに安定化しやすいとされます。あなたが「安全基地」になることが、二人の関係を育てます。")}''',
      chapno="11", clabel=sp("ATTACHMENT × PARTNER"), title="相手のタイプ別・接し方のコツ", pno="15"))

    # ── P16 CH12 愛の言語 ──
    def lang_rows(items):
        return "".join(f'''<div class="strow"><span>{k}</span><span style="color:var(--wine2)">{v}</span></div>''' for k,v in items)
    A(page(code, f'''<p class="lead">人が愛を感じる・伝える方法は5つに分かれるとされています（Chapman）。「伝え方」と「受け取り方」がズレてると、愛があっても届かない。まずは自分の言語を知りましょう。</p>
      <div class="wbox" style="margin:0 0 3mm;padding:3mm 5mm">
        {svg_compare([(k, C["lang_score"][0][i]) for i,(k,_) in enumerate(C["give_lang"])],
                     [(k, C["lang_score"][1][i]) for i,(k,_) in enumerate(C["give_lang"])],
                     "◀ 与える", "受け取りたい ▶")}
        <div style="font-size:6.8pt;color:var(--ink3);text-align:center;margin-top:1.4mm">
          左（紫）＝あなたが愛を伝える手段　／　右（ピンク）＝あなたが愛を感じ取る手段</div></div>
      <div class="panel pink" style="margin-top:3.2mm"><div class="pt">⚠　あなたが陥りやすい「すれ違い」</div>
        <p>あなたは<b style="color:var(--wine2)">行動</b>で愛を伝えるのに、本当に欲しいのは<b style="color:var(--wine2)">言葉</b>。だから「こんなに寄り添っているのに、なぜ言葉が返ってこないの？」となりがちです。「言葉が欲しい」と素直に伝えるのが、満たされる近道です。</p></div>
      <div class="grid2" style="margin-top:3mm">
        <div class="panel"><div class="pt">相手に響かせるコツ</div><p>尽くす前に、まず相手の言語を観察してみてください。言葉が欲しい人には言葉を、時間が欲しい人には予定を空けて。</p></div>
        <div class="panel"><div class="pt">自分を満たすコツ</div><p>「ありがとう」「あなたのおかげ」を求めてOK。欲しい言葉は、言わないと届きません。</p></div>
      </div>
      <div class="sect-h">✨ 今日からできること</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　今日、相手の具体的な行動をあげて「ありがとう」と言葉にする。<br>
        ◇　「○○してくれると嬉しい」と“欲しい言葉”を一つリクエストする。</div>
      {note("📖 ちょっと理論の話","「与える言語」と「受け取りたい言語」が違う人は、実は多いです。両方知っておくと、モヤモヤの正体に気づけます。")}''',
      chapno="12", clabel=f'５　{sp("LOVE LANGUAGES")}', title="あなたの愛の伝わり方", pno="16"))

    # ── P17 CH13 あるある30 ──
    L = C["aruaru"]
    left = "".join(f'<div class="aru-i"><span class="an">{i+1:02d}</span><span>{L[i]}</span></div>' for i in range(15))
    right = "".join(f'<div class="aru-i"><span class="an">{i+1:02d}</span><span>{L[i]}</span></div>' for i in range(15,30))
    A(page(code, f'''<p class="lead">いくつ当てはまる？ チェックしながら読んでみてください。「全部わたしだ…」となったら、それがあなたの恋の核です。</p>
      <div class="aru-grid"><div>{left}</div><div>{right}</div></div>
      <div class="panel pink" style="margin-top:3.4mm"><div class="pt">📊 いくつ当てはまった？</div>
        <p>20個以上＝ 生粋の{code}恋愛体質／10〜19個＝ 状況で出るタイプ／9個以下＝ 他タイプの一面も。どれも「あなたらしさ」です🐾</p></div>''',
      chapno="13", clabel=f'{sp(code)}　{sp("LOVE ARUARU")}', title=f"{code}の恋愛あるある30", pno="17"))

    # ── P18 CH14 落とし穴 ──
    pf = "".join(f'''<div class="panel {"pink" if i%2==0 else ""}" style="margin-bottom:2.4mm">
      <div class="pt">落とし穴 {"①②③④"[i]}　{t}</div>
      <p><b style="color:var(--wine2);font-size:7.42pt">原因</b>　{c}</p>
      <p style="margin-top:.8mm"><b style="color:var(--wine2);font-size:7.42pt">処方箋</b>　{r}</p></div>'''
      for i,(t,c,r) in enumerate(C["pitfalls"]))
    A(page(code, f'''<div class="wbox" style="margin:0 0 3mm;padding:2.6mm 4mm">
        {svg_flip([(t, r.split("。")[0], "") for t,_c,r in C["pitfalls"]])}</div>
      <p class="lead" style="margin-bottom:2.4mm">CH03が「性格のクセ」なら、こちらは“場面”で起きるつまずき。シーンごとの落とし穴を、原因と処方箋つきで整理しました。</p>
      {pf}
      <div style="text-align:center;margin-top:3.4mm;font-size:10.12pt;line-height:2;color:var(--wine2);font-style:italic">
        <span style="font-size:16.88pt;color:var(--wine-l)">“</span><br>{C["pitfall_quote"]}</div>
      {note("🐾 ひとこと","落とし穴は全部「優しさ」の裏返し。直すべき欠点ではなく、向ける方向をちょっと変えるだけ。あなたの愛情は、そのままで十分すぎるくらい魅力です🐾")}''',
      chapno="14", clabel=sp("PITFALLS & REMEDY"), title="ハマりがちな落とし穴", pno="18"))

    # ── P19 CH15 三角理論 ──
    tri = "".join(f'''<div class="brow"><div class="bh"><b>{k}</b>
      <span><span class="v">{v}</span>　<span style="font-size:7.2pt;color:var(--ink3)">・{lab}</span></span></div>
      <div class="bar"><i style="width:{v}%"></i></div><p>{d2}</p></div>''' for k,v,lab,d2 in C["triangle"])
    seven = "".join(f'''<div class="cbox"><div style="font-size:7.88pt;font-weight:700;color:{'var(--wine)' if st else 'var(--ink2)'}">{n}</div>
      <div class="cb-c">{s}</div></div>''' for n,s,st in [
      ("好意","親密のみ",0),("夢中","情熱のみ",0),("空虚な愛","コミットのみ",0),("ロマンチック","親密＋情熱",0),
      ("友愛的な愛","親密＋コミット",1),("愚かな愛","情熱＋コミット",0),("完全愛 ★","3つすべて",1),("非愛","どれもなし",0)])
    A(page(code, f'''<p class="lead">Sternbergによれば、愛は「親密性・情熱・コミットメント」の3つでできているとされています。このバランスで「愛のかたち」が決まります。</p>
      <div class="grid2" style="grid-template-columns:58mm 1fr;gap:4mm;align-items:center">
        <div class="wbox" style="margin:0;padding:2mm">
          {svg_triangle(C["triangle"][0][1], C["triangle"][2][1], C["triangle"][1][1], "親密性", "情熱", "コミット")}</div>
        <div>{tri}</div>
      </div>
      <div class="panel pink" style="margin-top:2.6mm"><div class="pt">あなたの愛の形　＝　「友愛的な愛」から「完全愛」へ</div>
        <p>親密性とコミットメントが高いあなたは、<b style="color:var(--wine2)">深く長く続く「友愛的な愛」</b>が得意。あとは情熱をキープする工夫（新しい体験・ときめきの共有）を足せば、3つ揃った<b style="color:var(--wine2)">「完全愛」</b>に届きます。</p></div>
      <div class="sect-h">💞 7つの愛のかたち</div>
      <div class="cmap-row" style="grid-template-columns:repeat(4,1fr);gap:2mm">{seven}</div>
      <div class="sect-h">✨ 今日からできること</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　週に一度、二人で“はじめてのこと”を予定に入れる。<br>
        ◇　ときめいた瞬間は、その場で言葉にして伝える。</div>
      {note("💡 知っとくと得","情熱って、時間とともに自然に下がるものです。長続きするカップルは、情熱を「育て直す」工夫をしています。あなたの強みの親密性が、その土台になります。")}''',
      chapno="15", clabel=sp("TRIANGULAR THEORY"), title="あなたの愛のバランス", pno="19"))

    # ── P20 CH16 ビッグファイブ ──
    bf = "".join(f'''<div class="brow"><div class="bh"><b>{k}　<span style="font-size:6.75pt;letter-spacing:.12em;color:var(--ink3)">{e}</span></b>
      <span class="v">{v}</span></div><div class="bar"><i style="width:{v}%"></i></div><p>{d2}</p></div>'''
      for k,e,v,d2 in C["bigfive"])
    A(page(code, f'''<p class="lead">性格を5つの要素で測る、心理学でいちばん信頼されてるモデル。あなたの恋愛での「出方」を要素ごとに見ていきます。</p>
      <div class="grid2" style="grid-template-columns:1fr 56mm;gap:4mm;align-items:center">
        <div>{bf}</div>
        <div class="wbox" style="margin:0;padding:2mm">
          {svg_radar([k for k,_,_,_ in C["bigfive"]], [round(v/20) for _,_,v,_ in C["bigfive"]], maxv=5)}</div>
      </div>
      <div class="grid2" style="margin-top:2.6mm">
        <div class="panel pink"><div class="pt">この組み合わせの強み</div>
          <p>協調性＋外向性の高さ＝<b style="color:var(--wine2)">誰からも好かれる愛され体質</b>。誠実性も高いから、長く続く関係をつくる力がある。</p></div>
        <div class="panel"><div class="pt">気をつけたい点</div>
          <p>協調性が高すぎると<b style="color:var(--wine2)">自己主張が消えがち</b>。不安の揺れと重なると、尽くして疲れる悪循環にハマる。</p></div>
      </div>
      <div class="sect-h">✨ 今日からできること</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　1日1回、小さな「私はこうしたい」を口に出す。<br>
        ◇　不安になったら、事実と思い込みを紙に分けて書き出す。</div>
      {note("📖 ちょっと理論の話","カップルの満足度にいちばん効くのは「不安の少なさ」と「協調性の高さ」なのだそうです。あなたは協調性が強みだから、あとは不安との付き合い方を整えればOK。")}''',
      chapno="16", clabel=sp("BIG FIVE PROFILE"), title="性格5factorで見る恋愛", pno="20"))

    # ── P21 CH17 認知機能 ──
    cf = "".join(f'''<div class="panel {"pink" if i==0 else ""}" style="margin-bottom:2.4mm">
      <div style="display:flex;gap:2.6mm;align-items:baseline">
        <span style="font-family:Cormorant Garamond,serif;font-size:16.88pt;color:var(--wine);line-height:1">{fn}</span>
        <span style="font-size:6.98pt;letter-spacing:.16em;color:var(--wine-l)">{rank}</span>
        <b style="font-size:8.33pt;color:var(--wine2)">{jp}</b></div>
      <p style="margin-top:1mm">{desc}</p></div>''' for i,(fn,rank,jp,desc) in enumerate(C["cogfn"]))
    A(page(code, f'''<p class="lead">MBTIの奥にある「心の使い方の順番」が認知機能。{code}は Fe → Ni → Se → Ti の順で世界を見ています。恋愛でどう働くのか見てみましょう。</p>
      <div class="wbox" style="margin:0 0 2.4mm;padding:1.8mm 4mm">
        {svg_stack([(fn, rank, jp) for fn, rank, jp, _d in C["cogfn"]])}</div>
      {cf}
      <div class="sect-h">✨ 今日からできること</div>
      <div style="font-size:8.1pt;line-height:2;color:var(--ink2)">
        ◇　疲れを感じたら抱え込まず、一人で休む時間をとる。<br>
        ◇　責めたくなったら“事実→自分の気持ち”の順で伝える。</div>
      {note("📖 ちょっと理論の話","Feで尽くして、Tiが暴走すると理屈で責める。この振れ幅を知っておくと、ケンカのときの自分を一歩引いて見られるよ。")}''',
      chapno="17", clabel=sp("COGNITIVE FUNCTIONS"), title="頭の使い方でみる恋愛", pno="21"))

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
    A(page(code, f'''<p class="lead">ここまでの理論を、自分の恋にあてはめて書き出してみよう。書くと、知識がちゃんと「自分のもの」になります。</p>
      {wq(1,"私の愛着スタイルは？　それが出た具体的な場面は？",2)}
      {wq(2,"私が「受け取りたい」愛の言語を、相手にどう伝える？",2)}
      {wq(3,"「完全愛」に近づくため、情熱を育てる工夫を一つ。",2)}
      {refs}
      {note("🐾 さいごに","理論はあくまで「地図」。実際に歩くのはあなた。知った自分を手がかりに、あなたらしい恋を育ててね🐾")}''',
      chapno="W3", clabel=sp("THEORY WORKSHEET"), title="書いて整理する自己分析", pno="22"))

    # ── P23 W1 棚卸し ──
    A(page(code, f'''<p class="lead">頭の中の「理想の恋人像」を、一回ぜんぶ紙に出してみよう。書き出すと、本当に譲れないものと手放せるものが見えてくる。</p>
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
      <div class="panel pink" style="margin-top:3mm"><div class="pt">💡 ヒント</div>
        <p>3つに絞れたら、それ以外は「あったら嬉しいボーナス」。完璧な人を探すのではなく、譲れない3つを持ってる人を探す。これだけで恋のハードルがぐっと現実的になります。</p></div>
      {note("💡 ひとくちメモ","目標って「紙に書くと叶いやすくなる」と言われています。誰かのためだけじゃなく、自分のための目標も書いてみてください。")}''',
      chapno="W1", clabel=f'{sp("WORK")}　0 1', title="理想の相手、棚おろし", pno="23"))

    # ── P24 W2 本音を伝える ──
    A(page(code, f'''<p class="lead">我慢グセを手放すための「Iメッセージ」練習シート。相手のせいにする言い方から、自分の気持ちを伝える言い方に変換する練習です。</p>
      <div class="panel pink"><div class="pt">📝 Iメッセージの型</div>
        <p style="font-size:9.0pt;line-height:2"><b style="color:var(--wine)">私は</b>〔状況・事実〕　▶　<b style="color:var(--wine)">〜と感じた</b>〔感情・気持ち〕　▶　<b style="color:var(--wine)">だから</b>〔お願い・希望〕</p></div>
      <div class="wlabel"><span class="num">1</span>最近「言えなかった本音」を一つ思い出す</div>
      {"".join('<div class="wline"></div>' for _ in range(3))}
      <div class="wlabel"><span class="num">2</span>Iメッセージに変換して書いてみる</div>
      <div class="wbox">
        <div style="font-size:8.33pt;color:var(--wine2);margin-bottom:1mm">私は</div><div class="wline"></div>
        <div style="font-size:8.33pt;color:var(--wine2);margin:1.6mm 0 1mm">〜と感じた。だから</div><div class="wline"></div>
        <div style="font-size:8.33pt;color:var(--wine2);margin:1.6mm 0 1mm">〜してほしい。</div><div class="wline"></div>
      </div>
      <div class="panel" style="margin-top:2.6mm"><div class="pt">💡 ヒント</div>
        <p>最初は紙に書くだけでOK。実際に伝えなくていいよ。言葉にするだけで気持ちが整理されて、次に同じ場面が来たとき自然に口から出るようになる。</p></div>
      {note("💡 知っとくと得","「言いたいことを我慢しすぎない人」ほど、関係の満足度が高いという研究があります。あなたの本音も、ちゃんと関係に必要なパーツ。")}''',
      chapno="W2", clabel=f'{sp("WORK")}　0 2', title="本音の言い方 練習シート", pno="24"))

    # ── P25 A1 仲直りフローチャート ──
    def fq(q, no_l, no_t, yes_l, yes_t):
        return f'''<div class="flow-q">{q}</div><div class="flow-2">
          <div class="flow-b"><span class="fl">{no_l}</span><p>{no_t}</p></div>
          <div class="flow-b"><span class="fl">{yes_l}</span><p>{yes_t}</p></div></div><div class="flow-ar">▼</div>'''
    A(page(code, f'''<p class="lead">ケンカ直後は、どうしても感情で動いてしまいがちです。この順番どおり進めば、関係を壊さず仲直りまでたどり着けるよ。迷ったら上から指でなぞってみてください。</p>
      <div class="flow-q" style="background:var(--pink);border-color:var(--pinkbd)">ケンカしてしまった…</div>
      <div class="flow-ar">▼</div>
      {fq("Q1　あなたの頭は冷えている？", sp("NO")+"・まだ感情的","「6時間ルール」で一旦離れる。落ち着いてからこの図に戻る。",
          sp("YES")+"・冷静になれた","次のステップへ進む。")}
      {fq("Q2　自分にも非があった？", sp("NO")+"・相手が悪い気が","責める前に<b style='color:var(--wine)'>相手の言い分を最後まで聴く</b>。",
          sp("YES"),"言い訳の前に<b style='color:var(--wine)'>「ごめんね」</b>から。何に謝るかを具体的に。")}
      {fq("Q3　相手は今、話せそう？", sp("NO")+"・まだ距離がある","「落ち着いたら話そう」と一言だけ送って待つ。",
          sp("YES"),"Iメッセージで<b style='color:var(--wine)'>「私は〜と感じた」</b>と本音を伝える。")}
      <div class="flow-goal">仲直り　▷　最後は感謝とスキンシップで締める　♡</div>
      {note("📖 ちょっと理論の話","ケンカそのものより「仲直りのうまさ」が長続きを左右するとされています。自分なりの仲直りの型を持っておくのが、最大の保険です。")}''',
      chapno="A1", clabel=sp("MAKE UP FLOW"), title="仲直りフローチャート", pno="25"))

    # ── P26 A2 復縁という選択 ──
    r3 = "".join(f'''<div class="panel"><div style="display:flex;gap:2mm;align-items:center;margin-bottom:1mm">
      <span class="num">{i+1}</span><b style="font-size:8.33pt;color:var(--wine)">{t}</b></div><p>{s}</p></div>'''
      for i,(t,s) in enumerate([
        ("冷却期間をおく","最低でも1〜3ヶ月は連絡しない。追わないことで、相手に「失った実感」が生まれる。"),
        ("自分を整える","別れの原因と向き合って、見た目・生活・心を立て直す。“変わった姿”がいちばんの説得力。"),
        ("さりげなく再接触","重い告白じゃなく「元気にしてる？」から。友達として軽く、焦らず距離を縮めよう。")]))
    ng3 = "".join(f'''<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>' ''' .strip().rstrip("'")
      for t,s in [("追いLINE","未読・既読が気になって連投しちゃう"),("泣き落とし","同情や罪悪感で引き止めようとする"),
                  ("SNS監視","相手の投稿に一喜一憂し続ける")])
    A(page(code, f'''<p class="lead">別れたあとに出てくる「もう一度…」の気持ち。大事なのは、寂しさで動かずに<b style="color:var(--wine2)">「本当に戻るべき？」</b>を見極めること。寄り添い型のあなたほど、冷静さが必要です。</p>
      <div class="grid2">
        <div class="panel pink"><div class="pt">◎　復縁を考えていいサイン</div><ul class="check">
          <li>別れの原因が「解決できること」だった</li><li>二人とも変わる気がある</li>
          <li>感謝できる思い出のほうが多い</li><li>一人になっても相手を尊重できてる</li></ul></div>
        <div class="panel"><div class="pt">✕　やめておくべきサイン</div><ul class="check ng">
          <li>ただ「寂しい・一人がこわい」だけ</li><li>原因がモラハラ・浮気とかで根深い</li>
          <li>戻れば「また尽くせる」と思ってる</li><li>相手ははっきり終わりを望んでる</li></ul></div>
      </div>
      <div class="sect-h">🐾 復縁の3ステップ</div>
      <div class="wbox" style="margin:0 0 2.4mm;padding:2.4mm 4mm">
        {svg_timeline([("0〜3ヶ月","冷却期間","連絡を断つ"),("1〜2ヶ月","自分を整える","変わった姿を"),("3ヶ月〜","さりげなく再接触","軽い一通から")])}</div>
      <div class="grid3">{r3}</div>
      <div class="sect-h">⚠　🙅 これだけはやっちゃダメ</div>
      <div class="grid3">{ng3}</div>
      {note(sp(code)+"へ", C["enfj_msg"])}''',
      chapno="A2", clabel=sp("RECONCILIATION"), title="ヨリを戻す、その前に", pno="26"))

    # ── P27 A3 復縁の見極め ──
    chk = "".join(f'<div style="font-size:7.99pt;color:var(--ink2);padding:.9mm 0">□　{x}</div>' for x in [
      "別れの原因が「解決できる」ものだ","一人の時間でも自分を保てている","相手の幸せを心から願える",
      "自分が変わる覚悟と行動がある","感謝できる思い出のほうが多い","相手もまだ完全には終わっていない"])
    judge = "".join(f'''<div class="panel {c}"><div class="pt">{t}</div><p>{s}</p></div>''' for t,s,c in [
      ("5〜6個  →  進んでよい","条件は十分。次のページの手順で丁寧に。","pink"),
      ("3〜4個  →  保留","まずは自分を整える期間を。焦らないで。",""),
      ("0〜2個  →  やめる勇気","手放すほうが、あなたの幸せに近いかも。","")])
    rows = "".join(f'<tr><td class="lb">{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in [
      ("別れた直後","追わず、まず気持ちを落ち着けた","不安のまま追いLINEで連投した"),
      ("冷却期間","距離を置き、別れの原因と向き合った","寂しさに耐えられず、すぐ連絡を再開"),
      ("自分磨き","自分の課題を一つ変える努力をした","相手を変えようと説得を続けた"),
      ("再会の仕方","「変わった自分」で軽く短く会った","重い空気で「やり直したい」と迫った"),
      ("結果","前より対等な関係を築き直せた","同じすれ違いを繰り返し再び別れた")])
    A(page(code, f'''<p class="lead">その「戻りたい」は、<b style="color:var(--wine2)">愛情</b>？ それとも<b style="color:var(--wine2)">執着</b>？ 動き出す前に、頭と心をいったん整理しておこう。</p>
      <div class="panel" style="margin-bottom:2.6mm"><div class="pt">✅ 復縁できそう度チェック</div>
        <p style="font-size:7.65pt;color:var(--ink3);margin-bottom:1mm">当てはまる□の数を数えてみてください。</p>
        <div class="grid2" style="gap:0 5mm">{chk}</div></div>
      <div class="grid3">{judge}</div>
      <div class="sect-h">🤔 執着？　それとも愛情？</div>
      <div class="wbox" style="margin:0;padding:3mm 5mm">
        {svg_vs("執着（手放せない）", ["一人になるのが怖い","相手のSNSが気になって仕方ない","「失うのが怖い」が先に立つ","過去のいい時間に戻りたいだけ"],
                "愛情（また大切にしたい）", ["相手の幸せを願える","自分の非を認め、変われる","感謝のほうが多く思い出せる","二人の未来を具体的に描ける"])}</div>
      <div class="sect-h">🔀 戻れた人と、また別れた人の差</div>
      <table class="cmp"><tr><th></th><th>◎　やり直せた人</th><th>✕　また別れた人</th></tr>{rows}</table>
      {note("🌱 手放すという選択","諦めるのは、負けでも失敗でもありません。「戻らない」と決めて前に進む勇気も、自分を大事にする愛のかたち。どっちを選んでも、あなたの恋はちゃんと次につながる。")}''',
      chapno="A3", clabel=sp("REUNITE · DECISION"), title="それ、愛情？それとも執着？", pno="27"))

    # ── P28 A4 復縁テクニック ──
    s1 = "".join(f'<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>' for t,s in [
      ("連絡は断つ","1〜3ヶ月。追わないことで、相手に「失った実感」を持たせる。"),
      ("SNSは静かに","監視も匂わせ投稿もNG。たまに前向きな近況だけでOK。"),
      ("自分を磨く","見た目・生活・心を立て直そう。“変わった姿”が最大の武器。")])
    s3 = "".join(f'<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>' for t,s in [
      ("短く・軽く","初回はランチかお茶で1時間。重い場所・長時間はナシで。"),
      ("昔話より今","別れの話は持ち出さない。変わった自分を自然に見せよう。"),
      ("引き際よく","「楽しかった、またね」で自分から切り上げて、余韻を残す。")])
    A(page(code, f'''<p class="lead">復縁は「気持ち」より<b style="color:var(--wine2)">「順番と間（ま）」</b>。焦って動くほど遠ざかるよ。5つのステップに分けて、具体的な手順とセリフで解説するね。</p>
      <div class="wbox" style="margin:0 0 2mm;padding:1.6mm 4mm">
        {svg_timeline([("STEP 1","冷却期間","連絡を断つ"),("STEP 2","再接触","軽い一通"),("STEP 3","復縁デート","短く・軽く"),
                       ("STEP 4","近づくサイン","返信が早く"),("STEP 5","切り出す","帰り際に")])}</div>
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
        <div class="panel"><div class="pt">タイミング</div><p>何回か会って空気が戻って、相手から会いたそうな素振りが出た時。帰り際の、余韻が残る瞬間がベスト。</p></div>
        <div class="panel"><div class="pt">伝え方</div><p>「あの頃と違う自分でいられる。もう一度、一緒にいたい」。過去の謝罪より<b style="color:var(--wine2)">“これからどう変わるか”</b>を一言。</p></div>
      </div>
      <div class="panel pink" style="margin-top:2.4mm"><div class="pt">決め手の例</div>
        <p>「離れてみて、あなたといる時間がいちばん自分らしかったと気づいた。今度はもっと対等に、ちゃんと大事にしたい」<br>
        <span style="color:var(--ink3);font-size:7.54pt">— 重さや謝罪で押さず、“変わった自分”と“これから”だけを、短く正直に。</span></p></div>
      {note("🧠 心理のはなし","人は別れ際の印象で記憶を上書きします（ピーク・エンドの法則）。最後をいい余韻で終えるほど「もう一度会いたい」が生まれるよ。")}''',
      chapno="A4", clabel=sp("REUNITE · TECHNIQUE"), title="復縁の進め方、順番が9割", pno="28"))

    # ── P29 A5 タイプ別復縁 ──
    rt = "".join(f'<div class="panel"><div class="pt">{t} には</div><p>{s}</p></div>' for t,s in C["reunite_type"])
    bfix = "".join(f'''<div style="display:flex;gap:2.6mm;padding:1.5mm 0;border-bottom:.35pt dotted var(--rule)">
      <b style="font-size:8.21pt;color:var(--wine);width:26mm;flex:none">{t}</b>
      <span style="font-size:7.88pt;line-height:1.8;color:var(--ink2)">{s}</span></div>''' for t,s in C["breakup_fix"])
    pr = "".join(f'''<div class="panel pink"><div style="display:flex;gap:2mm;align-items:center;margin-bottom:1mm">
      <span class="num">{i+1}</span><b style="font-size:8.33pt;color:var(--wine)">{t}</b></div><p>{s}</p></div>'''
      for i,(t,s) in enumerate(C["promise3"]))
    A(page(code, f'''<p class="lead">相手の性格で、響く戻り方は変わるよ。代表的な9タイプ別に「効く一手」をまとめたよ。あと、{code}が別れやすい原因と、その直し方も。</p>
      <div class="grid3" style="gap:2.4mm">{rt}</div>
      <div class="sect-h">{sp(code)}が別れやすい原因　→　復縁での修正法</div>
      {bfix}
      <div class="sect-h">やり直してからの3つの約束</div>
      <div class="grid3">{pr}</div>
      {note("🐾 さいごに","復縁のゴールは「元に戻る」ことではなく<b style='color:var(--wine2)'>「前より良い二人になる」</b>こと。同じ別れを繰り返さない自分になれた時、本当の意味でやり直せるよ。")}''',
      chapno="A5", clabel=sp("REUNITE · BY TYPE"), title="相手のタイプ別・戻り方", pno="29"))

    # ── P30 A6 復縁とSNS ──
    st3 = "".join(f'''<div class="panel"><div style="display:flex;gap:2mm;align-items:center;margin-bottom:1mm">
      <span class="num">{i+1}</span><b style="font-size:8.33pt;color:var(--wine)">{t}</b></div><p>{s}</p></div>'''
      for i,(t,s) in enumerate([("いいね","まずは投稿に軽く一つ。「見ています」を圧なく伝える最初の合図。"),
        ("ストーリー反応","スタンプや一言で軽く反応。「それ気になる！」程度の短さで止める。"),
        ("DM再開","反応が返るようになってから。用件は小さく「元気？」の一通で十分。")]))
    sns4 = "".join(f'<div class="panel"><div class="pt">{t}</div><p>{s}</p></div>' for t,s in [
      ("Instagram","充実をさりげなく一枚。ストーリーの閲覧で毎回先頭に出ない。リアクションは控えめに。"),
      ("LINE","即レス・連投はしない。用件は短く一往復で。アイコン・ひとことを静かに整える程度に。"),
      ("X（旧Twitter）","病み・匂わせ厳禁。フォローは外さず、感情の垂れ流しだけを止める。沈黙が余裕に見える。")])
    A(page(code, f'''<p class="lead">今どきの復縁は、SNSの使い方で半分決まる。相手の動きを察しやすいあなたほど、つい見すぎ・反応しすぎてしまいます。<b style="color:var(--wine2)">「静けさ」が一番の武器</b>です。</p>
      <div class="sect-h">①　冷却期間のSNSルール</div>
      <div class="wbox" style="margin:0;padding:3mm 5mm">
        {svg_vs("✕ しないこと", ["投稿の巡回・足跡チェック","「病んでる・匂わせ」投稿","衝動的なブロックや削除","既読やオンライン表示の確認"],
                "◎ すること", ["通知を切って見に行かない","前向きな近況をたまに一つ","フォローはそのまま自然に","静かに余裕を見せる"])}</div>
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
      chapno="A6", clabel=sp("REUNITE · SNS"), title="復縁とSNSのキョリ感", pno="30"))

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
    A(page(code, f'''<p class="lead">「何を投稿する？」「どう送る？」を、そのまま使える文例で。迷いやすい場面はQ&amp;Aで答えるよ。</p>
      <div class="sect-h">📸 さりげない近況ストーリー例</div>
      <div class="grid3">{stry}</div>
      <div class="sect-h">💬 DM再開のひとこと文例</div>
      <div class="grid2">
        <div class="panel"><div class="pt">✕　重い</div><p>「ずっと考えてた」「会えないかな」「まだ好き」<br><span style="color:var(--ink3)">→ 期待が見えて身構えさせる</span></p></div>
        <div class="panel pink"><div class="pt">◎　軽い</div><p>「この前◯◯行ったよ、懐かしくて笑」<br>「元気にしてる？ふと思い出して」<br><span style="color:var(--wine2)">→ 用件は小さく、返しやすく</span></p></div>
      </div>
      <div class="sect-h">🙋 こんな時どうする？ Q&amp;A</div>
      {qa}
      <div class="sect-h">{sp(code)}ならではの3つの一手</div>
      <div class="grid3">{s3c}</div>''',
      chapno="A7", clabel=sp("REUNITE · SNS Q&A"), title="SNS、実際どう使う？", pno="31"))

    # ── P32 裏表紙 ──
    A(page(code, f'''<div class="divider">
      <div class="dq" style="margin-top:0">「人は、自分が愛するものによって<br>形づくられてゆく。」
        <small>—　{sp("J. W. GOETHE")}</small></div>
      <h2 style="font-size:16.88pt;margin-top:14mm;line-height:1.9">{C["closing"]}</h2>
      <p class="dp" style="margin-top:8mm">最後まで読んでくれてありがとう🐾<br>あなたの愛情が、ちゃんと返ってくる恋になりますように。</p>
      <div style="margin-top:auto;width:100%">
        <div class="refs"><div class="rh">📚 参考にした主な理論</div><div class="rg" style="text-align:left">
          <span>Bowlby, J. (1969). Attachment and Loss.</span><span>Hazan, C. &amp; Shaver, P. (1987). Romantic love as attachment.</span>
          <span>Ainsworth, M. (1978). Patterns of Attachment.</span><span>Chapman, G. (1992). The Five Love Languages.</span>
          <span>Sternberg, R. (1986). A triangular theory of love.</span><span>Costa, P. &amp; McCrae, R. (1992). NEO-PI-R (Big Five).</span>
          <span>Jung, C.G. (1921). Psychological Types.</span><span>Myers, I. &amp; Briggs, K. MBTI® framework.</span></div></div>
        <div style="text-align:center;margin-top:5mm;font-size:7.88pt;letter-spacing:.2em;color:var(--ink2)">
          16にゃんこ恋愛診断　／　恋愛トリセツ　{B}（{code}）版</div>
        <div style="text-align:center;margin-top:2mm;font-size:7.2pt;letter-spacing:.14em;color:var(--ink3)">
          発行：Type&amp;Co　／　診断サイト：16lovetypecats.com</div>
        <div style="text-align:center;margin-top:2.4mm;font-size:6.52pt;color:var(--ink3);line-height:1.7">
          このトリセツは娯楽目的のコンテンツです。心理学的・医学的診断ではありません。無断複製・転載を禁じます。<br>
          ©　2026　Type&amp;Co　/　16にゃんこ恋愛診断</div>
      </div></div>''', cls="back-pg"))

    return pages


# ══════════════════════════════════════════════════════════════

def font_face_css():
    """使用文字だけにサブセット化した woff2 を data URI で埋め込む。
    Playwright の Chromium はプロキシを通らず Google Fonts を取得できないため、
    ネットワークに依存しないこの方式にしている（未取得なら空を返しフォールバック）。"""
    import base64, glob
    css = []
    fdir = os.path.join(SCRATCH, "fonts")
    for weight, fn in ((400, "mpr-400.woff2"), (700, "mpr-700.woff2"), (800, "mpr-800.woff2")):
        path = os.path.join(fdir, fn)
        if not os.path.exists(path):
            continue
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        css.append("@font-face{font-family:'M PLUS Rounded 1c';font-style:normal;"
                   "font-weight:%d;font-display:block;"
                   "src:url(data:font/woff2;base64,%s) format('woff2');}" % (weight, b64))
    if not css:
        print("  ! フォント未取得のためシステムフォントで描画されます")
    return "\n".join(css)


def main():
    import base64, io
    from PIL import Image
    code = sys.argv[1] if len(sys.argv) > 1 else "ENFJ"
    src = f"/home/user/16lovetypeCATS/{code.lower()}.png"
    im = Image.open(src).convert("RGBA"); im.thumbnail((520, 520))
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=92)
    b64 = base64.b64encode(buf.getvalue()).decode()
    pages = build(code, C, b64)
    css = CSS.replace("/*FONTFACE*/", font_face_css())
    html = (f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
            f'<title>恋愛攻略書 — {BREED[code]}（{code}）</title><style>{css}</style></head><body>'
            + "".join(pages) + "</body></html>")
    out = os.path.join(SCRATCH, f"guide_{code.lower()}.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"pages={len(pages)}  ->  {out}  ({len(html)//1024}KB)")

if __name__ == "__main__":
    main()
