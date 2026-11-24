"""Reuse the verified legacy build for content and immutable download archives."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from html import unescape
from urllib.parse import urljoin, urlsplit

WEB=Path(__file__).resolve().parents[1]
ROOT=WEB.parent
BASE="/DailyToolsOps/"
ORIGIN="https://ankitparekh007.github.io"

def fragment(text, start, end):
    return text.split(start,1)[1].split(end,1)[0]

with tempfile.TemporaryDirectory() as tmp:
    old=Path(tmp)/"site"
    subprocess.run([sys.executable,str(ROOT/"scripts/build_site.py"),str(old)],check=True)
    catalog=json.loads((old/"catalog.json").read_text(encoding="utf-8"))
    guides={}
    by_id={p["id"]:p for p in catalog["packs"]}
    for page in sorted((old/"docs").rglob("index.html")):
        route="/"+page.parent.relative_to(old).as_posix()+"/"
        html=page.read_text(encoding="utf-8")
        main=fragment(html,'<main id="article" class="docs-main">','</main>')
        breadcrumb=fragment(main,'<div class="breadcrumbs">','</div>')
        article=main.split('</div>',1)[1]
        toc_html=fragment(html,'<aside class="docs-toc" aria-label="On this page">','</aside>')
        toc=[(a,unescape(h)) for a,h in re.findall(r'<a href="#([^"]+)">([^<]+)</a>',toc_html)]
        name=unescape(re.search(r'<h1>(.*?)</h1>',article).group(1))
        parts=route.strip("/").split("/")
        current=parts[1] if len(parts)>1 else None
        # Preserve the existing safe Markdown-rendered markup, resolving relative links
        # against the real page URL rather than the client router's current location.
        def fix(m):
            raw=unescape(m.group(1))
            if raw.startswith("#"): return m.group(0)
            absolute=urljoin(ORIGIN+BASE+route.lstrip("/"),raw)
            parsed=urlsplit(absolute)
            if parsed.netloc==urlsplit(ORIGIN).netloc:
                absolute=parsed.path+("?" + parsed.query if parsed.query else "")+("#"+parsed.fragment if parsed.fragment else "")
            from html import escape
            return 'href="'+escape(absolute,quote=True)+'"'
        article=re.sub(r'href="([^"]+)"',fix,article)
        breadcrumb=re.sub(r'href="([^"]+)"',fix,breadcrumb)
        p=by_id.get(current)
        description=(f'{name}: {p["description"]}. Learn prerequisites, installation, practical usage, verification and troubleshooting in the DailyToolsOps resource guide.' if p else 'Get started with DailyToolsOps. Browse every engineering resource pack, read installation instructions and download matching ZIP archives for your AI coding tool.')
        if len(parts)>2: description=f'{name} for {p["id"].replace("-"," ")}. Read supplemental engineering prompts and practical guidance for using the DailyToolsOps resource pack with your AI coding tool.'
        guides[route]={"route":route,"name":name,"current":current,"description":description,"article":article,"breadcrumb":breadcrumb,"toc":toc}
    (WEB/"src/data/generated.json").write_text(json.dumps({"packs":catalog["packs"],"guides":guides},ensure_ascii=False),encoding="utf-8")
    public=WEB/"public";public.mkdir(exist_ok=True)
    downloads=public/"downloads"
    if downloads.exists(): shutil.rmtree(downloads)
    shutil.copytree(old/"downloads",downloads)
    shutil.copyfile(old/"catalog.json",public/"catalog.json")
    (public/".nojekyll").touch()
print("Prepared",len(guides),"documentation routes")

subprocess.run([sys.executable,str(WEB/'scripts/social.py')],check=True)
