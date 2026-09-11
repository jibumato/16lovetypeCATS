import sys
from playwright.sync_api import sync_playwright
code = sys.argv[1] if len(sys.argv)>1 else "enfj"
SP="/tmp/claude-0/-home-user-16lovetypeCATS/ca9b5b1a-5375-5908-aa61-ec0aeb6a5928/scratchpad/"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg=b.new_page()
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"file://{SP}guide_{code}.html", wait_until="networkidle")
    pg.wait_for_timeout(3500)
    pg.emulate_media(media="print")
    pg.pdf(path=f"{SP}{code}_love_guide_cat.pdf", format="A4", print_background=True,
           margin={"top":"0","bottom":"0","left":"0","right":"0"}, prefer_css_page_size=True)
    print("errors:", errs or "none")
    b.close()
