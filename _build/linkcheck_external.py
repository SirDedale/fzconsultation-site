#!/usr/bin/env python3
"""Checks that every external link in the built site still resolves (HTTP status < 400).
Run monthly in CI (see .github/workflows/checks.yml) - it needs normal internet access.
Some publishers block automated requests (403/429); those are reported as WARN, not errors,
so review them by hand. Exit code 1 only for definite failures (404/410, DNS errors, timeouts twice)."""
import os, re, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SKIP_HOSTS = ("fzconsultation.xyz", "calendly.com", "formspree.io", "static.cloudflareinsights.com", "cloudflareinsights.com")
UA = "Mozilla/5.0 (compatible; fz-linkcheck/1.0; +https://fzconsultation.xyz/en/governance.html)"

def collect():
    urls = {}
    for base in ("fr", "en"):
        for dp, _, fn in os.walk(os.path.join(ROOT, base)):
            for f in fn:
                if not f.endswith(".html"): continue
                txt = open(os.path.join(dp, f), encoding="utf-8").read()
                for u in re.findall(r'href="(https?://[^"#]+)', txt):
                    if any(h in u for h in SKIP_HOSTS): continue
                    urls.setdefault(u.replace("&amp;", "&"), set()).add(os.path.relpath(os.path.join(dp, f), ROOT))
    return urls

def probe(u):
    last = None
    for attempt in range(2):
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(u, method=method, headers={"User-Agent": UA, "Accept": "*/*"})
                with urllib.request.urlopen(req, timeout=20) as r: return u, r.status, None
            except urllib.error.HTTPError as e:
                last = (u, e.code, str(e))
                if e.code in (403, 405, 429, 999): continue
                if e.code >= 400 and method == "GET": return last
            except Exception as e:
                last = (u, None, str(e))
        time.sleep(2)
    return last

def main():
    urls = collect(); bad = []; warn = []
    with ThreadPoolExecutor(8) as ex:
        for u, code, msg in ex.map(probe, urls):
            if code and code < 400: continue
            (warn if code in (403, 429, 999) else bad).append((u, code, msg))
    for u, c, m in warn: print(f"WARN  {c} {u}  (blocked for bots? check by hand) <- {sorted(urls[u])[0]}")
    for u, c, m in bad: print(f"ERROR {c or 'ERR'} {u}  {m or ''} <- {sorted(urls[u])[0]}")
    print(f"\n{len(urls)} external links: {len(bad)} broken, {len(warn)} to review by hand")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
