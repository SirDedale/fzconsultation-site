#!/usr/bin/env python3
"""Static checks for the generated site. Exit code 1 on any error.
Usage:  python3 _build/check.py            (run from the repo root or anywhere)
Checks: internal links and #anchors, hreflang pairs, page basics (title, description, one h1, lang,
canonical), no inline executable scripts (CSP), JSON/JSON-LD validity, language purity, sitemap,
security.txt expiry, downloads present."""
import os, re, sys, json
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
errors, warnings = [], []
def err(p, m): errors.append(f"{p}: {m}")
def warn(p, m): warnings.append(f"{p}: {m}")

VOID = {"br", "hr", "img", "input", "meta", "link", "source", "wbr", "col", "area", "base", "embed", "track", "param"}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.srcs = set(), [], []
        self.h1 = 0; self.title = ""; self.in_title = False; self.desc = None; self.canonical = None
        self.lang = None; self.hreflangs = {}; self.inline_scripts = 0; self.json_blocks = []
        self._script = None; self.text = []; self._lang_stack = []; self._skip = 0; self.csp = False
        self.main_has_pf = False; self.imgs_no_alt = 0; self.btn_no_name = 0
        self.stack = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "html": self.lang = a.get("lang")
        if tag == "h1": self.h1 += 1
        if tag == "title": self.in_title = True
        if tag == "meta":
            if a.get("name") == "description": self.desc = a.get("content")
            if (a.get("http-equiv") or "").lower() == "content-security-policy": self.csp = True
        if tag == "link":
            if a.get("rel") == "canonical": self.canonical = a.get("href")
            if a.get("rel") == "alternate" and a.get("hreflang"): self.hreflangs[a["hreflang"]] = a.get("href")
            if a.get("rel") in ("stylesheet", "preload", "icon") and a.get("href"): self.srcs.append(a["href"])
        if tag == "a" and a.get("href") is not None: self.links.append(a["href"])
        if tag in ("img", "script") and a.get("src"): self.srcs.append(a["src"])
        if tag == "img" and a.get("alt") is None: self.imgs_no_alt += 1
        if tag == "main" and "data-pagefind-body" in a: self.main_has_pf = True
        if tag == "script":
            t = a.get("type", "")
            if not a.get("src"):
                self._script = (t, [])
                if t not in ("application/json", "application/ld+json"): self.inline_scripts += 1
        if tag in ("script", "style", "noscript"): self._skip += 1
        if tag not in VOID:
            self.stack.append((tag, a.get("lang")))
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag == "script" and self._script:
            self.json_blocks.append((self._script[0], "".join(self._script[1]))); self._script = None
        if tag in ("script", "style", "noscript"): self._skip = max(0, self._skip - 1)
        while self.stack:
            t, _ = self.stack.pop()
            if t == tag: break
    def handle_data(self, d):
        if self.in_title: self.title += d
        if self._script is not None: self._script[1].append(d)
        if self._skip: return
        if any(l and l != self.lang for _, l in self.stack): return   # passages in another language
        self.text.append(d)

def parse(path):
    p = Page(); p.feed(open(path, encoding="utf-8").read()); return p

def site_files():
    for base in ("fr", "en"):
        for dp, dn, fn in os.walk(os.path.join(ROOT, base)):
            for f in fn:
                if f.endswith(".html"): yield os.path.join(dp, f)
    for f in ("index.html", "404.html"): yield os.path.join(ROOT, f)

def resolve(from_file, href):
    """Return filesystem path for an internal href, or None for external/ignored."""
    u = urlparse(href)
    if u.scheme in ("http", "https"):
        if u.netloc in ("fzconsultation.xyz",): path = u.path
        else: return None
    elif u.scheme in ("mailto", "tel", "javascript", "data"): return None
    elif href.startswith("//"): return None
    else: path = u.path
    if not path: return from_file
    path = unquote(path)
    full = os.path.normpath(os.path.join(ROOT, path.lstrip("/")) if path.startswith("/") else os.path.join(os.path.dirname(from_file), path))
    if os.path.isdir(full): full = os.path.join(full, "index.html")
    return full

FR_WORDS = re.compile(r"\b(les|des|vous|pour|avec|dans|votre|nous|une|est)\b", re.I)
EN_WORDS = re.compile(r"\b(the|and|with|your|for|that|this|are|our|you)\b", re.I)

def main():
    pages = {}
    for f in site_files():
        pages[f] = parse(f)
    rel = lambda f: os.path.relpath(f, ROOT)
    for f, p in pages.items():
        r = rel(f)
        if r in ("index.html", "404.html"): continue
        lang = r.split(os.sep)[0]
        if p.lang != lang: err(r, f"html lang={p.lang!r}, expected {lang!r}")
        if not p.title.strip(): err(r, "missing <title>")
        if not p.desc: err(r, "missing meta description")
        if p.h1 != 1: err(r, f"{p.h1} <h1> elements (expected 1)")
        if not p.canonical: err(r, "missing canonical")
        if not p.csp: err(r, "missing Content-Security-Policy meta")
        if p.inline_scripts: err(r, f"{p.inline_scripts} inline executable script(s) (blocked by CSP)")
        if p.imgs_no_alt: err(r, f"{p.imgs_no_alt} <img> without alt attribute")
        for t, body in p.json_blocks:
            try: json.loads(body)
            except Exception as e: err(r, f"invalid {t or 'script'} JSON: {e}")
        # hreflang counterparts
        other = "en" if lang == "fr" else "fr"
        counterpart = os.path.join(ROOT, other, *r.split(os.sep)[1:])
        if not os.path.exists(counterpart): err(r, f"no {other} counterpart")
        # internal links and anchors
        for href in p.links + p.srcs:
            tgt = resolve(f, href)
            if tgt is None: continue
            if not os.path.exists(tgt): err(r, f"broken link/resource: {href}"); continue
            frag = urlparse(href).fragment
            if frag and tgt.endswith(".html"):
                tp = pages.get(tgt) or parse(tgt)
                if frag not in tp.ids: err(r, f"missing anchor #{frag} in {rel(tgt)}")
        # language purity (advisory thresholds)
        text = " ".join(p.text)
        if lang == "fr":
            n = len(EN_WORDS.findall(text))
            if n > 12: warn(r, f"{n} English stopwords in French page (check for untranslated text)")
        else:
            n = len(FR_WORDS.findall(text))
            if n > 12: warn(r, f"{n} French stopwords in English page (check for untranslated text)")
    # sitemap
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
        tgt = resolve(os.path.join(ROOT, "x"), loc)
        if tgt is None or not os.path.exists(tgt): err("sitemap.xml", f"URL not found on disk: {loc}")
    # security.txt
    st = os.path.join(ROOT, ".well-known", "security.txt")
    if not os.path.exists(st): err(".well-known/security.txt", "missing")
    else:
        m = re.search(r"^Expires:\s*(\S+)", open(st).read(), re.M)
        if not m: err("security.txt", "no Expires field")
        else:
            exp = datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))
            days = (exp - datetime.now(timezone.utc)).days
            if days < 0: err("security.txt", f"EXPIRED {-days} days ago: renew SECURITY_EXPIRES in build.py")
            elif days < 45: warn("security.txt", f"expires in {days} days: renew SECURITY_EXPIRES in build.py")
    # downloads
    for slug in ("ransomware-checklist", "rto-rpo-worksheet", "ai-acceptable-use-policy"):
        for l in ("fr", "en"):
            if not os.path.exists(os.path.join(ROOT, "assets", "downloads", f"{slug}-{l}.docx")): err("assets/downloads", f"missing {slug}-{l}.docx")
    # search index present?
    if not os.path.exists(os.path.join(ROOT, "pagefind", "pagefind.js")): warn("pagefind/", "search index not built (run: npx pagefind --site .)")
    for w in warnings: print("WARN ", w)
    for e in errors: print("ERROR", e)
    print(f"\n{len(pages)} pages checked: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
