"""guide_*.html → PDF。

各ページの本文（.pbody）が下のフッター（.pfoot）に重ならなくなるまで自動縮小する。
判定に scrollHeight を使うと flex + overflow:visible では実際のはみ出しを取りこぼすため、
「本文の最下端」と「フッターの上端」の位置関係で直接判定している。
"""
import sys
from playwright.sync_api import sync_playwright

code = sys.argv[1] if len(sys.argv) > 1 else "enfj"
SP = "/tmp/claude-0/-home-user-16lovetypeCATS/ca9b5b1a-5375-5908-aa61-ec0aeb6a5928/scratchpad/"

FIT_JS = """() => {
  // .pbody は flex:1 で常に下端まで伸びるため、その「中身」が枠を超えているかで判定する。
  const log = [];
  document.querySelectorAll('.page').forEach((pg, i) => {
    const body = pg.querySelector('.pbody');
    if (!body) return;
    let z = 1.0;
    while (body.scrollHeight > body.clientHeight + 1 && z > 0.74) {
      z -= 0.01;
      body.style.zoom = z.toFixed(2);
    }
    const rest = body.scrollHeight - (body.clientHeight);
    if (z < 1.0 || rest > 1) log.push({page: i + 1, zoom: +z.toFixed(2), rest});
  });
  return log;
}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg = b.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"file://{SP}guide_{code}.html", wait_until="domcontentloaded")
    pg.emulate_media(media="print")
    pg.wait_for_timeout(3500)
    fitted = pg.evaluate(FIT_JS)
    pg.wait_for_timeout(400)
    pg.pdf(path=f"{SP}{code}_love_guide_cat.pdf", format="A4", print_background=True,
           margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
           prefer_css_page_size=True)
    print("errors:", errs or "none")
    if fitted:
        print("自動縮小:", ", ".join(f"p{f['page']}({f['zoom']})" for f in fitted))
        print("最小ズーム:", min(f["zoom"] for f in fitted))
        bad = [f for f in fitted if f["rest"] > 0]
        print("収まらなかったページ:", [f"p{f['page']}" for f in bad] or "なし")
    else:
        print("自動縮小: なし（全ページそのまま収まりました）")
    b.close()
