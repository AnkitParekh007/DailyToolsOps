import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from build_docs import markdown
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if "id" in attrs: self.ids.add(attrs["id"])
        if tag=="a" and "href" in attrs: self.links.append(attrs["href"])
class DocsTests(unittest.TestCase):
    def test_escaping(self):
        html,toc=markdown("## Heading\n<script>alert(1)</script>\n[click](javascript:alert)\n```sh\n<evil>\n```")
        self.assertNotIn("<script>",html)
        self.assertNotIn('href="javascript:',html)
        self.assertIn("&lt;evil&gt;",html)
        self.assertEqual(toc,[("heading","Heading")])
    def test_docs_and_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"site"
            subprocess.run([sys.executable,str(ROOT/"scripts/build_site.py"),str(out)],check=True,capture_output=True)
            entries=json.loads((out/"catalog.json").read_text())["packs"]
            for item in entries:
                page=out/"docs"/item["id"]/"index.html"
                self.assertTrue(page.is_file())
                text=page.read_text(encoding="utf-8")
                self.assertIn("Copy code",text)
                self.assertIn("Prerequisites",text)
                self.assertIn(item["id"]+"-"+item["version"]+".zip",text)
                self.assertIn('aria-current="page"',text)
            for page in (out/"docs").rglob("index.html"):
                parser=Links(); parser.feed(page.read_text(encoding="utf-8"))
                for href in parser.links:
                    url=urlsplit(href)
                    if url.scheme or url.netloc: continue
                    target=(page.parent/unquote(url.path)).resolve() if url.path else page
                    if target.is_dir(): target=target/"index.html"
                    self.assertTrue(target.is_file(),str(page)+": "+href)
                    if url.fragment and target.suffix==".html":
                        p=Links(); p.feed(target.read_text(encoding="utf-8"))
                        self.assertIn(url.fragment,p.ids,str(page)+": "+href)
