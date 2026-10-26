"""Build the one-page A3 landscape PDF of the map from data.json.

Usage: python3 render_pdf.py . "Catapult Accelerator Map - <date>.pdf"
Needs Python Playwright with Chromium.
"""
import json, subprocess, sys, time, html
from playwright.sync_api import sync_playwright
repo, out = sys.argv[1], sys.argv[2]
d = json.load(open(f"{repo}/data.json"))
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8765"], cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
import base64, glob, os, re
def _faces(folder):
    out = ""
    for f in sorted(glob.glob(os.path.join(folder, "*.woff2"))):
        fam = "IBM Plex Sans Condensed" if "condensed" in f else "IBM Plex Sans"
        w = re.search(r"-(\d00)-", f).group(1)
        out += "@font-face{font-family:'%s';font-weight:%s;src:url(data:font/woff2;base64,%s) format('woff2')}\n" % (fam, w, base64.b64encode(open(f, "rb").read()).decode())
    return out
css = _faces(os.path.join(repo, "fonts")) + """
svg{font-family:"IBM Plex Sans Condensed",sans-serif!important}
@page{size:A3 landscape;margin:10mm}
body{padding:0!important;background:#fff!important}
.wrap{max-width:none!important;gap:10px!important}
.scroll{overflow:visible!important;border:none!important;padding:0!important}
svg{width:100%!important;height:auto!important}
figcaption,h1 + p a{display:none}
.notes{font-size:9.5px;color:#5b6577;line-height:1.45;border-top:1px solid #9aa5b8;padding-top:8px}
.notes h2{font-size:11px;margin:0 0 4px;color:#1b2230}
.notes ul{margin:0;padding-left:16px;columns:2;column-gap:28px}.notes li{break-inside:avoid;margin-bottom:2px}h1{font-size:1.6rem!important}
"""
gaps = "".join(f"<li>{html.escape(g)}</li>" for g in d["gaps"])
notes = f"""<div class='notes'><h2>Notes</h2><ul>
<li>Source: each Catapult's own programme, opportunity, funding, news and event pages, checked {d['lastChecked']}. Click any box to open its source page. Confirm deadlines on the source page before applying.</li>
<li>Long columns wrap into side-by-side sub-columns. Ordering within each Catapult: closing soon, on the horizon, open or rolling, then running or recently closed.</li>{gaps}</ul></div>"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(color_scheme="light", viewport={"width":1500,"height":1000})
    pg.goto("http://localhost:8765/map.html"); pg.wait_for_selector("#map svg")
    pg.evaluate("document.documentElement.dataset.theme='light'")

    pg.evaluate("""async()=>{const D=await (await fetch('data.json',{cache:'no-store'})).json();
const R=10,items=["closingSoon","openRolling","running","horizon"].flatMap(k=>D[k]||[]);
const sw=132,bw=122,x0=14,cy=118,ch=44,bus=86,top=cy+ch+30,rowh=54;
const cols=ORGS.map(([org])=>{const m=items.filter(x=>x.org===org).sort((a,b)=>ORDER[a.status]-ORDER[b.status]);return m.length?m:[{short:"No active|accelerator",status:"n"}]});
let start=0;const geo=cols.map(b=>{const k=Math.ceil(b.length/R);const g={start,k};start+=k;return g});
const W=x0*2+sw*start,ix=W/2,sx=i=>x0+sw*i+sw/2;
const maxr=Math.max(...cols.map(b=>Math.min(b.length,R)));const H=top+(maxr-1)*rowh+44+12;
const ccx=i=>(sx(geo[i].start)+sx(geo[i].start+geo[i].k-1))/2;
let o=`<a href="https://iuk-business-connect.org.uk/" target="_blank" rel="noopener"><rect x="${ix-110}" y="14" width="220" height="42" rx="6" class="iuk"/>${tl(ix,35,"Innovate UK","t1")}</a><path d="M${ix} 56V${bus}M${ccx(0)} ${bus}H${ccx(8)}" class="ln"/>`;
ORGS.forEach(([org,lab,home],i)=>{const b=cols[i],g=geo[i],c=ccx(i),w=bw+(g.k-1)*sw;
 o+=`<path d="M${c} ${bus}V${cy}" class="ln"/>`;
 o+=`<a href="${home}" target="_blank" rel="noopener"><rect x="${c-w/2}" y="${cy}" width="${w}" height="${ch}" rx="6" class="cat"/>${tl(c,cy+22,g.k>1?lab.replace("|"," "):lab,"t2")}</a>`;
 const by=cy+ch+15;if(g.k>1)o+=`<path d="M${c} ${cy+ch}V${by}M${sx(g.start)} ${by}H${sx(g.start+g.k-1)}" class="ln"/>`;
 for(let s=0;s<g.k;s++){const part=b.slice(s*R,(s+1)*R),x=sx(g.start+s);
  o+=`<path d="M${x} ${g.k>1?by:cy+ch}V${top+(part.length-1)*rowh+22}" class="ln"/>`;
  part.forEach((p,j)=>{const y=top+j*rowh;const r=`<rect x="${x-bw/2}" y="${y}" width="${bw}" height="44" rx="6" class="p ${p.status}"/>${tl(x,y+22,p.short||p.name,"t3")}`;
   o+=p.url?`<a href="${esc(p.url)}" target="_blank" rel="noopener"><title>${esc(p.name)}</title>${r}</a>`:r});}
});
document.getElementById("map").innerHTML=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">${o}</svg>`;}""")
    pg.add_style_tag(content=css)
    pg.evaluate("""n=>{const p=document.querySelector('h1+p');p.innerHTML=p.innerHTML.replace(/\\. <a[^>]*>.*?<\\/a>\\./,'.');document.querySelector('.wrap').insertAdjacentHTML('beforeend',n)}""", notes)
    pg.evaluate("document.fonts.ready")
    over = pg.evaluate("""()=>[...document.querySelectorAll('svg text.t3')].map(t=>[t.textContent,Math.round(t.getComputedTextLength())]).filter(x=>x[1]>118)""")
    print("labels wider than box:", over)
    pg.pdf(path=out, format="A3", print_background=True, prefer_css_page_size=True)
    b.close()
srv.terminate()
