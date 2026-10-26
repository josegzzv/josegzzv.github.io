#!/usr/bin/env python3
"""Builds assets/cv/CV-Jose-Antonio-Gonzalez-Villalon-{EN,ES}.pdf from tools/cv/data.py via Chromium (Playwright)."""
import asyncio, base64, pathlib
from playwright.async_api import async_playwright
from data import CV

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "cv"
PHOTO = ROOT / "assets" / "img" / "bioPic1.jpg"

CSS = """
@page { size: Letter; margin: 0; }
* { box-sizing: border-box; }
body { font-family: "Helvetica Neue", Arial, sans-serif; color:#1f2937; margin:0; font-size:9.6pt; line-height:1.38; }
.page { padding: 0.55in 0.6in 0.5in; }
header { display:flex; gap:18px; align-items:center; border-bottom:2px solid #0f3d5e; padding-bottom:12px; margin-bottom:12px; }
header img { width:86px; height:86px; border-radius:50%; object-fit:cover; border:2px solid #0f3d5e; }
h1 { margin:0; font-size:21pt; color:#0f3d5e; letter-spacing:.2px; }
.title { font-size:11pt; font-weight:600; color:#1b5e8a; margin:2px 0 4px; }
.contact { font-size:8.6pt; color:#4b5563; }
.contact span + span::before { content:"  ·  "; color:#9ca3af; }
h2 { font-size:10.5pt; color:#0f3d5e; text-transform:uppercase; letter-spacing:1px; border-bottom:1px solid #cbd5e1; padding-bottom:2px; margin:12px 0 6px; }
p { margin:0 0 5px; }
.kpis { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin:6px 0 2px; }
.kpi { background:#f1f5f9; border-left:3px solid #1b5e8a; padding:5px 8px; }
.kpi b { display:block; font-size:12.5pt; color:#0f3d5e; }
.kpi span { font-size:8.2pt; color:#475569; }
.job { margin-bottom:8px; }
.job-h { display:flex; justify-content:space-between; align-items:baseline; }
.job-h b { font-size:10.2pt; color:#111827; }
.job-h .org { color:#1b5e8a; font-weight:600; }
.job-h .dates { font-size:8.6pt; color:#6b7280; white-space:nowrap; }
.job .scope { color:#374151; margin:1px 0 3px; }
ul { margin:0; padding-left:14px; }
li { margin-bottom:2px; }
.two { display:grid; grid-template-columns:1.15fr 1fr; gap:18px; }
.edu div { margin-bottom:4px; }
.edu b { color:#111827; }
.edu small { color:#6b7280; }
.tags span { display:inline-block; background:#eef2f7; border-radius:3px; padding:1px 6px; margin:0 4px 4px 0; font-size:8.4pt; }
footer { position:fixed; bottom:0.3in; left:0.6in; right:0.6in; font-size:7.6pt; color:#9ca3af; display:flex; justify-content:space-between; }
.break { page-break-before: always; padding-top:0.55in; }
"""

def render(lang):
    d = CV[lang]
    photo = base64.b64encode(PHOTO.read_bytes()).decode()
    jobs = "".join(
        f'<div class="job{" break" if i==4 else ""}"><div class="job-h"><div><b>{j["title"]}</b> · <span class="org">{j["org"]}</span></div><span class="dates">{j["dates"]}</span></div>'
        + (f'<p class="scope">{j["scope"]}</p>' if j.get("scope") else "")
        + ("<ul>" + "".join(f"<li>{b}</li>" for b in j.get("bullets", [])) + "</ul>" if j.get("bullets") else "")
        + "</div>"
        for i,j in enumerate(d["jobs"]))
    edu = "".join(f'<div><b>{e[0]}</b><br>{e[1]} <small>· {e[2]}</small></div>' for e in d["education"])
    exe = "".join(f'<div><b>{e[0]}</b><br>{e[1]} <small>· {e[2]}</small></div>' for e in d["exec_ed"])
    kpis = "".join(f'<div class="kpi"><b>{k[0]}</b><span>{k[1]}</span></div>' for k in d["kpis"])
    comp = "".join(f"<span>{c}</span>" for c in d["competencies"])
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="page">
<header><img src="data:image/jpeg;base64,{photo}" alt=""><div>
<h1>{d["name"]}</h1><div class="title">{d["headline"]}</div>
<div class="contact"><span>{d["location"]}</span><span>{d["email"]}</span><span>linkedin.com/in/josegzzvillalon</span><span>josegzzv.github.io</span></div>
</div></header>
<h2>{d["h_summary"]}</h2><p>{d["summary"]}</p>
<div class="kpis">{kpis}</div>
<h2>{d["h_comp"]}</h2><div class="tags">{comp}</div>
<h2>{d["h_exp"]}</h2>{jobs}
<h2>{d["h_edu"]}</h2><div class="two"><div class="edu">{edu}</div><div class="edu"><p><b>{d["h_exec"]}</b></p>{exe}
<p style="margin-top:6px"><b>{d["h_lang"]}:</b> {d["languages"]}</p><p><b>{d["h_pub"]}:</b> {d["publication"]}</p></div></div>
</div>
<footer><span>{d["name"]} · {d["headline_short"]}</span><span>{d["updated"]}</span></footer>
</body></html>"""

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for lang in ("en", "es"):
            await pg.set_content(render(lang))
            path = OUT / f"CV-Jose-Antonio-Gonzalez-Villalon-{lang.upper()}.pdf"
            await pg.pdf(path=str(path), format="Letter", print_background=True, prefer_css_page_size=True)
            print("wrote", path)
        await b.close()

asyncio.run(main())
