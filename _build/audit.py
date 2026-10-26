#!/usr/bin/env python3
"""Browser audit: serves the built site locally and, for every page in light AND dark mode, runs
axe-core (WCAG 2.0/2.1/2.2 A+AA + best practices), collects console errors and CSP violations, and checks
for horizontal overflow at phone width. Also exercises the interactive states (quiz result, AI vision
result, calculator result, search results, open mega menu, form error state).

Setup (once):   npm install axe-core pagefind   &&   pip install playwright && playwright install chromium
Run:            python3 _build/audit.py [--pages substring] [--langs fr,en] [--no-states]
Exit code 1 if any problem is found. External hosts are blocked during the audit (no network needed)."""
import os, re, sys, json, threading, argparse, functools, http.server, socketserver
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def find_axe():
    for c in (os.environ.get("AXE_PATH"), os.path.join(ROOT, "node_modules/axe-core/axe.min.js"), os.path.join(ROOT, "../node_modules/axe-core/axe.min.js"), "/home/claude/node_modules/axe-core/axe.min.js"):
        if c and os.path.exists(c): return c
    sys.exit("axe-core not found: run `npm install axe-core` (or set AXE_PATH)")

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def end_headers(self):
        self.send_header("Cache-Control", "no-store"); super().end_headers()

def serve():
    handler = functools.partial(Quiet, directory=ROOT)
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler); srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]

AXE_OPTS = {"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]}}
INIT = """window.__csp=[];document.addEventListener('securitypolicyviolation',e=>window.__csp.push(e.violatedDirective+' '+e.blockedURI));"""

def pages_from_sitemap():
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    out = []
    for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
        p = re.sub(r"^https?://[^/]+", "", loc)
        out.append(p + "index.html" if p.endswith("/") else p)
    out += ["/fr/search.html", "/en/search.html", "/404.html", "/index.html"]
    return sorted(set(out))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default=""); ap.add_argument("--langs", default="fr,en"); ap.add_argument("--no-states", action="store_true")
    a = ap.parse_args()
    axe_src = open(find_axe(), encoding="utf-8").read()
    srv, port = serve(); base = f"http://127.0.0.1:{port}"
    langs = a.langs.split(",")
    pages = [p for p in pages_from_sitemap() if a.pages in p and (p.split("/")[1] in langs or p in ("/404.html", "/index.html"))]
    problems = []; counts = {"axe": 0, "console": 0, "csp": 0, "overflow": 0}
    def log(kind, where, msg):
        counts[kind] += 1; problems.append(f"[{kind}] {where}: {msg}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        def new_ctx(scheme, width=1280, height=900):
            ctx = browser.new_context(color_scheme=scheme, viewport={"width": width, "height": height})
            ctx.add_init_script(INIT)
            def route(r):
                u = r.request.url
                if u.startswith(base): r.continue_()
                else: r.abort()
            ctx.route("**/*", route)
            return ctx
        def attach(page, where):
            def on_console(m):
                if m.type in ("error", "warning"):
                    t = m.text
                    if "net::ERR_FAILED" in t or "Failed to load resource" in t and "127.0.0.1" not in t: return   # blocked external hosts
                    log("console", where, f"{m.type}: {t[:200]}")
            page.on("console", on_console)
            page.on("pageerror", lambda e: log("console", where, f"pageerror: {str(e)[:200]}"))
        def run_axe(page, where):
            page.evaluate(axe_src)
            res = page.evaluate("axe.run(document, %s)" % json.dumps(AXE_OPTS))
            for v in res["violations"]:
                nodes = "; ".join((n["target"][0] if n["target"] else "?") for n in v["nodes"][:3])
                log("axe", where, f'{v["id"]} ({v["impact"]}) x{len(v["nodes"])} — {v["help"]} @ {nodes}')
        def csp_check(page, where):
            for v in page.evaluate("window.__csp||[]"): log("csp", where, v)

        for scheme in ("light", "dark"):
            ctx = new_ctx(scheme)
            for p in pages:
                where = f"{p} [{scheme}]"
                pg = ctx.new_page(); attach(pg, where)
                try:
                    pg.goto(base + p, wait_until="load"); pg.wait_for_timeout(120)
                    run_axe(pg, where); csp_check(pg, where)
                except Exception as e:
                    log("console", where, f"load failed: {e}")
                pg.close()
            if not a.no_states:
                for lang in langs:
                    states(ctx, base, lang, scheme, attach, run_axe, csp_check, log)
            ctx.close()
        # phone-width overflow (light only; layout does not depend on scheme)
        ctx = new_ctx("light", 375, 800)
        for p in pages:
            pg = ctx.new_page(); where = f"{p} [375px]"; attach(pg, where)
            try:
                pg.goto(base + p, wait_until="load"); pg.wait_for_timeout(80)
                w = pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                if w[0] > w[1] + 1: log("overflow", where, f"page is {w[0]}px wide in a {w[1]}px viewport")
            except Exception as e:
                log("console", where, f"load failed: {e}")
            pg.close()
        ctx.close(); browser.close()
    srv.shutdown()
    seen = set(); out = []
    for pr in problems:
        if pr not in seen: seen.add(pr); out.append(pr)
    for pr in out: print(pr)
    print(f"\n{len(pages)} pages x light/dark + states: axe={counts['axe']} console={counts['console']} csp={counts['csp']} overflow={counts['overflow']}")
    return 1 if problems else 0

def states(ctx, base, lang, scheme, attach, run_axe, csp_check, log):
    def fresh(path, tag):
        pg = ctx.new_page(); where = f"/{lang}/{path} {tag} [{scheme}]"; attach(pg, where)
        pg.goto(f"{base}/{lang}/{path}", wait_until="load"); return pg, where
    def safe(fn, where):
        try: fn()
        except Exception as e: log("console", where, f"state failed: {str(e)[:200]}")
    # quiz result
    pg, w = fresh("self-assessment.html", "(quiz result)")
    def quiz():
        pg.click("#qs")
        for _ in range(60):
            if pg.query_selector("#qn") is None: break
            pg.check("input[name=a] >> nth=%d" % 1, force=True); pg.click("#qn")
        pg.wait_for_timeout(150); run_axe(pg, w); csp_check(pg, w)
    safe(quiz, w); pg.close()
    # vision result
    pg, w = fresh("ai/vision-questionnaire.html", "(vision result)")
    def vision():
        pg.click("#vs")
        for _ in range(40):
            if pg.query_selector("#vn") is None: break
            pg.check("input[name=v] >> nth=0", force=True); pg.click("#vn")
        pg.wait_for_timeout(150); run_axe(pg, w); csp_check(pg, w)
    safe(vision, w); pg.close()
    # calculator
    pg, w = fresh("resources/downtime-calculator.html", "(calculator result)")
    def calc():
        pg.click("#calc-form button[type=submit]"); pg.wait_for_timeout(100); run_axe(pg, w); csp_check(pg, w)
    safe(calc, w); pg.close()
    # search
    pg, w = fresh("search.html", "(search results)")
    def search():
        pg.fill("#q", "ransomware" if lang == "en" else "rançongiciel"); pg.press("#q", "Enter")
        pg.wait_for_selector("#search-results li", timeout=8000); run_axe(pg, w); csp_check(pg, w)
    safe(search, w); pg.close()
    # mega menu open + form error
    pg, w = fresh("index.html", "(mega menu open)")
    def mega():
        pg.click(".mega-toggle"); pg.wait_for_timeout(80); run_axe(pg, w)
    safe(mega, w); pg.close()
    pg, w = fresh("contact.html", "(form error)")
    def form():
        pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(100); run_axe(pg, w)
    safe(form, w); pg.close()
    pg, w = fresh("case-studies/index.html", "(filter applied)")
    def filt():
        pg.click(".chip >> nth=1"); pg.wait_for_timeout(80); run_axe(pg, w)
    safe(filt, w); pg.close()

if __name__ == "__main__":
    sys.exit(main())
