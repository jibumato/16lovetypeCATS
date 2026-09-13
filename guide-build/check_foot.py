from playwright.sync_api import sync_playwright
SP="/tmp/claude-0/-home-user-16lovetypeCATS/ca9b5b1a-5375-5908-aa61-ec0aeb6a5928/scratchpad/"
FIT="""() => {document.querySelectorAll('.page').forEach(pg=>{
 const body=pg.querySelector('.pbody'); if(!body)return;
 let z=1.0; while(body.scrollHeight>body.clientHeight+1 && z>0.74){z-=0.01;body.style.zoom=z.toFixed(2);}});}"""
CHK="""() => {const out=[];
 document.querySelectorAll('.page').forEach((pg,i)=>{
   const foot=pg.querySelector('.pfoot'); const head=pg.querySelector('.phead');
   const body=pg.querySelector('.pbody'); if(!foot||!body)return;
   const fr=foot.getBoundingClientRect(), br=body.getBoundingClientRect();
   const hr=head?head.getBoundingClientRect():null;
   // pbody の最後の子と footer の重なり
   let lastB=0; body.querySelectorAll('*').forEach(el=>{const r=el.getBoundingClientRect();
     if(r.height>0) lastB=Math.max(lastB,r.bottom);});
   const overlapFoot = +(lastB - fr.top).toFixed(1);
   // ゴースト章番号とヘッダの重なり
   const gh=pg.querySelector('.chapno');
   let ghOver=0;
   if(gh&&hr){const gr=gh.getBoundingClientRect();
     ghOver=+(Math.min(gr.bottom,hr.bottom)-Math.max(gr.top,hr.top)).toFixed(1);}
   if(overlapFoot>0.5||ghOver>0) out.push({p:i+1,foot:overlapFoot,ghost:ghOver});
 });return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg=b.new_page(); pg.goto(f"file://{SP}guide_enfj.html", wait_until="domcontentloaded")
    pg.emulate_media(media="print"); pg.wait_for_timeout(3000)
    pg.evaluate(FIT); pg.wait_for_timeout(300)
    for r in pg.evaluate(CHK):
        msgs=[]
        if r['foot']>0.5: msgs.append(f"本文がフッターに {r['foot']}px 重なり")
        if r['ghost']>0: msgs.append(f"章番号がヘッダに {r['ghost']}px 重なり")
        print(f"p{r['p']:02d}: " + " / ".join(msgs))
    b.close()
