"""Static docs renderer for the Markdown subset used by resource packs."""
from html import escape
import re
from urllib.parse import urlsplit

LABELS={"foundations":"Foundations","ai-engineering":"AI engineering","development":"Development","quality-security":"Quality & security","devops":"DevOps","productivity":"Productivity","frameworks":"Frameworks"}
TOKEN=re.compile(r"`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*")

def title(key):
    special={"ai":"AI","ui":"UI","ux":"UX","mcp":"MCP","rag":"RAG","llm":"LLM","ci":"CI","cd":"CD","api":"API","nextjs":"Next.js","nodejs":"Node.js","swiftui":"SwiftUI","fastapi":"FastAPI","postgresql":"PostgreSQL","github":"GitHub"}
    return " ".join(special.get(w,w.capitalize()) for w in key.split("-"))

def inline(text,links):
    parts=[]; pos=0
    for m in TOKEN.finditer(text):
        parts.append(escape(text[pos:m.start()]))
        code,label,url,bold=m.groups()
        if code is not None:
            parts.append("<code>"+escape(code)+"</code>")
        elif label is not None:
            dest=links.get(url)
            if dest is None and urlsplit(url).scheme in ("http","https") and urlsplit(url).netloc:
                dest=url
            parts.append('<a href="'+escape(dest,quote=True)+'">'+escape(label)+'</a>' if dest else escape(label)+" ("+escape(url)+")")
        else:
            parts.append("<strong>"+escape(bold)+"</strong>")
        pos=m.end()
    return "".join(parts)+escape(text[pos:])

def markdown(source,links=None):
    lines=source.splitlines(); html=[]; toc=[]; seen={}; i=0
    def fmt(s): return inline(s,links or {})
    def boundary(s): return not s.strip() or re.match(r"^(#{1,6} |\s*```|\s*[-*] |\s*\d+\. |>|\|)",s)
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line.startswith("```"):
            lang=line[3:].strip() or "text"; code=[]; i+=1
            while i<len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i+=1
            if i==len(lines): raise ValueError("Unclosed code fence")
            html.append('<div class="code-wrap"><div class="code-bar"><span>'+escape(lang)+'</span><button type="button" class="copy-code" aria-label="Copy code">Copy</button></div><pre><code>'+escape("\n".join(code))+'</code></pre></div>')
        elif re.match(r"^#{1,6} ",line):
            prefix,heading=line.split(" ",1)
            if prefix=="#": i+=1; continue
            slug=re.sub(r"[^a-z0-9]+","-",heading.lower()).strip("-") or "section"
            seen[slug]=seen.get(slug,0)+1
            anchor=slug if seen[slug]==1 else slug+"-"+str(seen[slug])
            level=len(prefix); html.append(f'<h{level} id="{anchor}">'+fmt(heading)+f'</h{level}>')
            if level==2: toc.append((anchor,heading))
        elif line.startswith("|") and i+1<len(lines) and re.fullmatch(r"[| :\-]+",lines[i+1].strip()):
            def cells(s): return [fmt(c.strip()) for c in s.strip().strip("|").split("|")]
            heads=cells(line); rows=[]; i+=2
            while i<len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i])); i+=1
            html.append('<div class="table-wrap" tabindex="0" role="region" aria-label="Documentation table"><table><thead><tr>'+''.join('<th scope="col">'+c+'</th>' for c in heads)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+c+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>')
            continue
        elif re.match(r"^(?:[-*] |\d+\. )",line):
            ordered=bool(re.match(r"^\d+\. ",line)); tag="ol" if ordered else "ul"
            pattern=r"^\d+\. (.*)" if ordered else r"^[-*] (.*)"
            start=int(line.split(".")[0]) if ordered else 1
            html.append("<"+tag+(' start="'+str(start)+'"' if ordered and start!=1 else "")+">")
            while i<len(lines):
                m=re.match(pattern,lines[i].strip())
                if not m: break
                body=m.group(1); check=re.match(r"^\[([ xX])\] (.*)",body)
                if check: body=("☑ " if check.group(1).lower()=="x" else "☐ ")+check.group(2)
                html.append("<li>"+fmt(body)+"</li>"); i+=1
            html.append("</"+tag+">"); continue
        elif line.startswith(">"):
            quote=[]
            while i<len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip()); i+=1
            html.append("<blockquote>"+fmt(" ".join(quote))+"</blockquote>"); continue
        else:
            paragraph=[line]; i+=1
            while i<len(lines) and not boundary(lines[i]):
                paragraph.append(lines[i].strip()); i+=1
            html.append("<p>"+fmt(" ".join(paragraph))+"</p>"); continue
        i+=1
    return "\n".join(html),toc

def build_docs(root,out,packs):
    template=(root/"website/docs-template.html").read_text(encoding="utf-8")
    (out/"docs-template.html").unlink()
    docs=out/"docs"; docs.mkdir()
    groups={}
    for p in packs: groups.setdefault(p["category"],[]).append(p)
    def navigation(current,prefix):
        html=['<a href="'+prefix+'docs/"'+(' aria-current="page"' if current is None else '')+'>Getting started</a>']
        for category,items in groups.items():
            html.append('<div class="docs-group"><h2>'+escape(LABELS.get(category,category))+'</h2>')
            for p in items:
                active=' aria-current="page"' if p["id"]==current else ''
                html.append('<a href="'+prefix+'docs/'+p["id"]+'/"'+active+' data-search="'+escape(p["id"]+" "+p["description"]+" "+category+" "+" ".join(p["tools"]),quote=True)+'">'+escape(title(p["id"]))+'</a>')
            html.append("</div>")
        return "".join(html)
    def page(dest,name,current,prefix,article,crumb,toc):
        aside="<strong>On this page</strong>"+''.join('<a href="#'+a+'">'+escape(h)+'</a>' for a,h in toc) if toc else ""
        values={"TITLE":escape(name),"ROOT":prefix,"NAV":navigation(current,prefix),"ARTICLE":article,"BREADCRUMB":crumb,"TOC":aside}
        rendered=re.sub(r"@@([A-Z]+)@@",lambda m:values[m.group(1)],template)
        dest.mkdir(parents=True,exist_ok=True); (dest/"index.html").write_text(rendered,encoding="utf-8")
    overview='<p class="eyebrow">DOCUMENTATION</p><h1>Get started with DailyToolsOps.</h1><p class="doc-lede">Read the actual instructions for every resource pack, download the matching archive and use it with your preferred AI coding agent.</p><div class="doc-actions"><a class="primary" href="../downloads/dailytools-all.zip" download>Download all packs</a><a class="secondary" href="../#catalog">Browse resource catalog</a></div><div class="doc-body"><h2 id="quick-start">Quick start</h2><ol><li>Choose a pack.</li><li>Download and extract its ZIP. Review the instructions and scripts.</li><li>Preview installation, then apply it if appropriate.</li><li>Use the installed artifacts and verify actual results.</li></ol><h2 id="guides">Explore '+str(len(packs))+' guides</h2><div class="docs-overview-grid">'
    for cat,items in groups.items():
        overview+='<a class="docs-overview-card" href="'+items[0]["id"]+'/"><small>'+str(len(items))+' guides</small><strong>'+escape(LABELS.get(cat,cat))+'</strong><p>'+escape(items[0]["description"])+' and more.</p></a>'
    overview+='</div><p>Most packs are guided templates, not autonomous services. Individual instructions describe their capabilities and limits.</p></div>'
    page(docs,"Getting started",None,"../",overview,"<span>Documentation</span>",[("quick-start","Quick start"),("guides","Explore guides")])
    for i,p in enumerate(packs):
        key=p["id"]; folder=root/p["path"]; prefix="../../"; name=title(key)
        download=prefix+"downloads/"+key+"-"+p["version"]+".zip"
        links={"README.md":"./","INSTRUCTIONS.md":"./"}; extras=[]
        for extra in sorted(folder.glob("*.md")):
            slug=extra.stem.lower()
            if extra.name not in ("README.md","INSTRUCTIONS.md") and re.fullmatch(r"[a-z0-9-]+",slug):
                links[extra.name]=slug+"/"; extras.append((extra,slug))
        body,toc=markdown((folder/"INSTRUCTIONS.md").read_text(encoding="utf-8"),links)
        intro='<p class="eyebrow">PACK GUIDE</p><h1>'+escape(name)+'</h1><p class="doc-lede">'+escape(p["description"])+'</p><div class="doc-meta"><span class="tag">v'+escape(p["version"])+'</span><span>'+escape(LABELS.get(p["category"],p["category"]))+'</span></div><div class="doc-actions"><a class="primary" href="'+download+'" download>Download ZIP</a><a class="secondary" href="'+download+'.sha256" download>SHA-256</a></div>'
        prev=packs[i-1] if i else None; nxt=packs[i+1] if i+1<len(packs) else None
        pagination='<div class="docs-pagination">'+(('<a href="../'+prev["id"]+'/"><small>← Previous</small>'+escape(title(prev["id"]))+'</a>') if prev else '<a href="../"><small>← Previous</small>Getting started</a>')+(('<a href="../'+nxt["id"]+'/"><small>Next →</small>'+escape(title(nxt["id"]))+'</a>') if nxt else '<a href="../"><small>Next →</small>All guides</a>')+'</div>'
        crumb='<a href="../">Documentation</a><span>/</span><span>'+escape(name)+'</span>'
        page(docs/key,name,key,prefix,intro+'<div class="doc-body">'+body+'</div>'+pagination,crumb,toc)
        for extra,slug in extras:
            extra_links={k:("../" if v=="./" else "../"+v) for k,v in links.items()}
            extra_body,extra_toc=markdown(extra.read_text(encoding="utf-8"),extra_links)
            page(docs/key/slug,title(slug),key,"../../../",'<h1>'+escape(title(slug))+'</h1><p><a href="../">← Back to pack instructions</a></p><div class="doc-body">'+extra_body+'</div>','<a href="../../">Documentation</a><span>/</span><a href="../">'+escape(name)+'</a>',extra_toc)
