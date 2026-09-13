from playwright.sync_api import sync_playwright
SP="/tmp/claude-0/-home-user-16lovetypeCATS/ca9b5b1a-5375-5908-aa61-ec0aeb6a5928/scratchpad/"
FIT="""() => {const log=[];document.querySelectorAll('.page').forEach((pg,i)=>{
 const inner=pg.querySelector('.inner'), body=pg.querySelector('.pbody'); if(!body)return;
 let z=1.0; while(inner.scrollHeight>inner.clientHeight+1 && z>0.80){z-=0.01;body.style.zoom=z.toFixed(2);}
 const rest=inner.scrollHeight-inner.clientHeight;
 if(z<1.0||rest>1) log.push({page:i+1,zoom:+z.toFixed(2),over:rest});});return log;}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg=b.new_page(); pg.goto(f"file://{SP}guide_enfj.html", wait_until="networkidle")
    pg.emulate_media(media="print"); pg.wait_for_timeout(3200)
    for r in pg.evaluate(FIT):
        st = "❌ 収まらず" if r['over']>1 else "✔ 収まった"
        print(f"p{r['page']:02d} zoom={r['zoom']} 残りはみ出し={r['over']}px  {st}")
    b.close()
