"""guide_enfj.html → PDF。はみ出すページは .pbody を自動縮小して必ず1ページに収める。"""
import sys
from playwright.sync_api import sync_playwright

code = sys.argv[1] if len(sys.argv) > 1 else "enfj"
SP = "/tmp/claude-0/-home-user-16lovetypeCATS/ca9b5b1a-5375-5908-aa61-ec0aeb6a5928/scratchpad/"

FIT_JS = """() => {
  const log = [];
  document.querySelectorAll('.page').forEach((pg, i) => {
    const inner = pg.querySelector('.inner');
    const body  = pg.querySelector('.pbody');
    if (!body) return;
    let z = 1.0;
    // 1%刻みで縮小し、収まった時点で停止（下限 0.80）
    while (inner.scrollHeight > inner.clientHeight + 1 && z > 0.80) {
      z -= 0.01;
      body.style.zoom = z.toFixed(2);
    }
    if (z < 1.0) log.push({page: i + 1, zoom: +z.toFixed(2),
                           over: inner.scrollHeight - inner.clientHeight});
  });
  return log;
}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg = b.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"file://{SP}guide_{code}.html", wait_until="networkidle")
    pg.emulate_media(media="print")
    pg.wait_for_timeout(3500)
    fitted = pg.evaluate(FIT_JS)
    pg.wait_for_timeout(400)
    pg.pdf(path=f"{SP}{code}_love_guide_cat.pdf", format="A4", print_background=True,
           margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
           prefer_css_page_size=True)
    print("errors:", errs or "none")
    if fitted:
        print("自動縮小したページ:", ", ".join(f"p{f['page']}({f['zoom']})" for f in fitted))
        worst = min(f["zoom"] for f in fitted)
        print(f"最小ズーム: {worst}")
    else:
        print("自動縮小: なし（全ページそのまま収まりました）")
    b.close()
