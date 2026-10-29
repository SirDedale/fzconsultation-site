"""FZ Consultation site generator.
Builds separate /fr/ and /en/ versions of every page, plus root redirect, 404, sitemap and robots.
Edit the CONFIG block, then run:  python3 build.py
"""
import os, re, html, json, shutil, sys, hashlib
from content import *
from cases import CASES
from newcontent import *
from industries import IND
from ai import *
from partners import *
from downtime import *
from auditor import AUDITOR
from tools import TEMPLATES, GLOSSARY
from insights import INSIGHTS
import extras, sys, hashlib
import newsite
from newsite_content import REMAP, ANCHOR_NAMES
from tools import TEMPLATE_DISCLAIMER

# ================= CONFIG =================
SITE = "https://fzconsultation.xyz"
EMAIL = "contact@fzconsultation.xyz"
BOOKING_URL = "https://calendly.com/fabien-mariou"  # Calendly link; leave "" to hide the booking button
FORMSPREE_ID = "mkjgvpwo"       # e.g. "abcdwxyz" from formspree.io; leave "" and the form opens the visitor's email app instead
CF_ANALYTICS_TOKEN = "b23a07ee11d3441f89c969fc2c62f224"   # Cloudflare Web Analytics token; leave "" for no analytics
UPDATED = ("29 octobre 2026", "October 29, 2026")
REVIEWED = {  # pages whose sources were re-checked; shown under the page title. ISO dates.
    "resources/downtime-calculator.html": "2026-10-26",
}
SECURITY_EXPIRES = "2027-09-30T00:00:00Z"   # security.txt must be renewed before this date (RFC 9116)
# ==========================================

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..") if os.path.basename(HERE) == "_build" else os.path.join(HERE, "site2")
LANGS = ["fr", "en"]
LANG = "fr"
PAGES = []  # (lang-independent path) for sitemap

def I(): return 0 if LANG == "fr" else 1
def SRCLANG(): return ' lang="en"' if LANG == "fr" else ""   # source titles are in English
def T(fr, en, tag=None, cls=""):
    txt = fr if LANG == "fr" else en
    if not tag: return txt
    c = f' class="{cls}"' if cls else ""
    return f"<{tag}{c}>{txt}</{tag}>"
def P(pair, **k): return T(pair[0], pair[1], **k)
def E(s): return html.escape(s, quote=True)

ARROW = '<svg class="arr" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

OTHER = {
 "what-we-do/index.html": ("Ce que nous faisons", "What we do"),
 "what-we-do/expertise/index.html": ("Expertise", "Expertise"),
 "what-we-do/services/index.html": ("Services", "Services"),
 "what-we-do/methodology.html": ("Méthodologie", "Methodology"),
 "what-we-do/industries.html": ("Secteurs", "Industries"),
 "what-we-do/regulations.html": ("Réglementation", "Regulations"),
 "case-studies/index.html": ("Études de cas", "Case studies"),
 "self-assessment.html": ("Auto-évaluation", "Self-assessment"),
 "contact.html": ("Nous joindre", "Contact"),
 "privacy.html": ("Politique de confidentialité", "Privacy policy"),
 "legal.html": ("Mentions légales", "Legal notice"),
 "ai/index.html": ("Intelligence artificielle", "Artificial intelligence"),
 "partners.html": ("Écosystème et partenariats", "Ecosystem and partnerships"),
 "resources/cost-of-downtime.html": ("Coût des interruptions", "Cost of downtime"),
 "ai/vision-questionnaire.html": ("Questionnaire de vision IA", "AI vision questionnaire"),
 "resources/index.html": ("Ressources", "Resources"),
 "resources/downtime-calculator.html": ("Calculateur du coût d'une interruption", "Downtime cost calculator"),
 "resources/glossary.html": ("Glossaire", "Glossary"),
 "insights/index.html": ("Insights", "Insights"),
 "search.html": ("Recherche", "Search"),
 "security.html": ("Sécurité du site", "Site security"),
 "accessibility.html": ("Accessibilité", "Accessibility"),
 "governance.html": ("Gouvernance et corrections", "Governance and corrections"),
}
for _t in TEMPLATES: OTHER[f"resources/{_t['slug']}.html"] = _t["short"]
for _a in INSIGHTS: OTHER[f"insights/{_a['slug']}.html"] = _a["title"]
_EXTRA_ITEMS = ([{"path": f"resources/{t['slug']}.html", "short": t["short"], "summary": t["summary"]} for t in TEMPLATES] +
                [{"path": f"insights/{a['slug']}.html", "short": a["title"], "summary": a["summary"]} for a in INSIGHTS])
fmt_date = extras.fmt_date
AI_ALL = [AUDITOR] + AI_PAGES + [CITADEL]
def name_of(key):
    new = REMAP.get(key)
    if new in ANCHOR_NAMES: return ANCHOR_NAMES[new]
    for p in EXPERTISE + SERVICES + IND + AI_ALL + CASES:
        if p["path"] == key: return p["short"]
    return OTHER[key]
def item_of(key):
    new = REMAP.get(key)
    extra = next((p for p in _EXTRA_ITEMS if p["path"] == key), None)
    if new in ANCHOR_NAMES:
        return {"path": key, "short": ANCHOR_NAMES[new], "summary": extra["summary"] if extra else ("", "")}
    for p in EXPERTISE + SERVICES + IND + AI_ALL + CASES + _EXTRA_ITEMS:
        if p["path"] == key: return p
    return {"path": key, "short": OTHER[key], "summary": ("", "")}

def url_of(lang, path):
    p = path[:-len("index.html")] if path.endswith("index.html") else path
    return f"{SITE}/{lang}/{p}"

# ---------------- layout ----------------
def header(r, current):
    other = "en" if LANG == "fr" else "fr"
    def a(key, pair, cls=""):
        cur = ' aria-current="page"' if key == current else ""
        c = f' class="{cls}"' if cls else ""
        return f'<a href="{r}{key}"{c}{cur}>{P(pair)}</a>'
    col = lambda title_key, items: (
        f'<div class="mcol"><a class="mhead" href="{r}{title_key}">{P(OTHER[title_key])} {ARROW}</a><ul>' +
        "".join(f'<li>{a(p["path"], p["short"])}</li>' for p in items) + "</ul></div>")
    approach = ('<div class="mcol"><span class="mhead plain">' + T("Approche", "Approach") + '</span><ul>' +
        "".join(f'<li>{a(k, OTHER[k])}</li>' for k in ["what-we-do/methodology.html", "what-we-do/regulations.html", "self-assessment.html", "resources/downtime-calculator.html"]) +
        f'</ul><a class="mall" href="{r}what-we-do/index.html">{T("Voir tout ce que nous faisons", "View everything we do")} {ARROW}</a></div>')
    fr_cur = ' aria-current="true"' if LANG == "fr" else ""
    en_cur = ' aria-current="true"' if LANG == "en" else ""
    fr_href = f"{r}../fr/{current}" if LANG == "en" else f"{r}{current}"
    en_href = f"{r}../en/{current}" if LANG == "fr" else f"{r}{current}"
    return f'''<a class="skip" href="#main">{T("Aller au contenu", "Skip to content")}</a>
<header class="site">
  <div class="wrap bar">
    <a class="brand" href="{r}index.html" aria-label="FZ Consultation">
      <img class="mark" src="{r}../assets/mark.webp" alt="" width="40" height="29">
      <span class="word">Consultation</span>
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="{T("Menu", "Menu")}">
      <span class="bars" aria-hidden="true"></span><span class="mt-label">{T("Menu", "Menu")}</span>
    </button>
    <nav id="primary-nav" class="primary" aria-label="{T("Navigation principale", "Main navigation")}">
      <div class="has-mega">
        <button class="mega-toggle" type="button" aria-expanded="false" aria-controls="mega">{T("Ce que nous faisons", "What we do")}{CHEV}</button>
        <div class="mega" id="mega">
          <div class="wrap mega-grid">
            {col("what-we-do/index.html", newsite.nav_wwd(sys.modules[__name__]))}
            {col("what-we-do/industries.html", newsite.nav_ind(sys.modules[__name__]))}
            {approach}
          </div>
        </div>
      </div>
      {a("ai/index.html", ("IA", "AI"))}
      {a("case-studies/index.html", ("Études de cas", "Case studies"))}
      {a("resources/index.html", ("Ressources", "Resources"))}
      {a("contact.html", ("Nous joindre", "Contact us"), "nav-cta")}
      <div class="nav-tools">
        <a href="{r}search.html">{T("Rechercher dans le site", "Search the site")}</a>
        <button class="theme-toggle txt" type="button" data-label-light="{T("Passer au thème clair", "Switch to light theme")}" data-label-dark="{T("Passer au thème sombre", "Switch to dark theme")}">{T("Changer de thème", "Change theme")}</button>
      </div>
    </nav>
    <div class="hdr-tools">
      <a class="icon-btn" href="{r}search.html" aria-label="{T("Rechercher", "Search")}"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 13l4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></a>
      <button class="icon-btn theme-toggle" type="button" data-label-light="{T("Passer au thème clair", "Switch to light theme")}" data-label-dark="{T("Passer au thème sombre", "Switch to dark theme")}" aria-label="{T("Changer de thème", "Change theme")}"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 3.5a6.5 6.5 0 0 1 0 13z" fill="currentColor"/></svg></button>
    </div>
    <nav class="lang" aria-label="Langue / Language">
      <a href="{fr_href}" hreflang="fr" data-lang="fr"{fr_cur}>FR</a>
      <a href="{en_href}" hreflang="en" data-lang="en"{en_cur}>EN</a>
    </nav>
  </div>
</header>'''

def cta_block(r, path=""):
    book = (f'<a class="btn signal" href="{E(BOOKING_URL)}" target="_blank" rel="noopener">{T("Réserver un appel de 30 minutes", "Book a 30-minute call")}</a>' if BOOKING_URL else "")
    selfassess = "" if path == "self-assessment.html" else f'<a class="btn outline-light" href="{r}self-assessment.html">{T("Faire l&#39;auto-évaluation", "Take the self-assessment")}</a>'
    return f'''<section class="block" id="contact" style="border-top:0;padding-top:24px" data-pagefind-ignore>
      <div class="contact">
        <div class="contact-top">
          <h2>{T("Parlons de votre prochaine panne, avant qu'elle n'arrive.", "Let's talk about your next outage before it happens.")}</h2>
          <p>{T("Un premier échange de 30 minutes, sans engagement, pour faire le point sur vos risques et vos priorités.", "A free 30-minute intro call to review your risks and priorities.")}</p>
          <div class="cta-actions">{book}{selfassess}</div>
        </div>
        <form class="cform mini" id="contact-form" data-endpoint="{"https://formspree.io/f/" + E(FORMSPREE_ID) if FORMSPREE_ID else ""}" data-email="{EMAIL}" novalidate>
          <h3>{T("Nous écrire", "Send us a message")}</h3>
          <label>{T("Nom", "Name")} <span aria-hidden="true">*</span><input name="name" autocomplete="name" required></label>
          <label>{T("Courriel", "Email")} <span aria-hidden="true">*</span><input name="email" type="email" autocomplete="email" required></label>
          <label>{T("Message", "Message")} <span aria-hidden="true">*</span><textarea name="message" rows="3" required></textarea></label>
          <input type="hidden" name="_subject" value="{T("Nouveau message — site FZ Consultation", "New message — FZ Consultation website")}">
          <label class="hp" aria-hidden="true">Website<input name="_gotcha" tabindex="-1" autocomplete="off"></label>
          <label class="consent"><input type="checkbox" name="consent" required> <span>{T("J&#39;accepte que mes informations soient utilisées pour répondre à ma demande, conformément à la", "I agree that my information will be used to respond to my request, in line with the")} <a href="{r}privacy.html">{T("politique de confidentialité", "privacy policy")}</a>.</span></label>
          <button class="btn signal" type="submit">{T("Envoyer", "Send")}</button>
          <p class="fstatus" role="status" aria-live="polite" data-ok="{T("Merci, votre message a bien été envoyé. Nous vous répondrons rapidement.", "Thank you, your message has been sent. We will get back to you shortly.")}" data-err="{T("L&#39;envoi a échoué. Écrivez-nous directement à", "Sending failed. Please email us directly at")} {EMAIL}." data-missing="{T("Merci de remplir les champs obligatoires et d&#39;accepter la politique de confidentialité.", "Please fill in the required fields and accept the privacy policy.")}" data-mailto="{T("Votre application de courriel va s&#39;ouvrir avec votre message.", "Your email app will open with your message.")}"></p>
        </form>
      </div>
    </section>'''

def footer(r):
    return newsite.footer_html(sys.modules[__name__], r)

CSP = ("default-src 'self'; script-src 'self' 'wasm-unsafe-eval' https://static.cloudflareinsights.com; "
       "style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; "
       "connect-src 'self' https://formspree.io https://cloudflareinsights.com; "
       "form-action 'self' https://formspree.io; base-uri 'self'; object-src 'none'")
_LD = {"crumbs": None, "faq": None}

def json_ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"

def page(path, title, desc, body, extra_head="", extra_js="", ld=None, noindex=False):
    depth = path.count("/") + 1          # +1 for the /fr or /en folder
    r = "../" * (depth - 1)              # link prefix to this language's root
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{url_of(l, path)}">' for l in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    analytics = (f'<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "{E(CF_ANALYTICS_TOKEN)}"}}\'></script>' if CF_ANALYTICS_TOKEN else "")
    ttl, dsc = P(title), P(desc)
    # structured data
    blocks = list(ld or [])
    if _LD["crumbs"]:
        trail = _LD["crumbs"]
        items = [{"@type": "ListItem", "position": 1, "name": T("Accueil", "Home"), "item": url_of(LANG, "index.html")}]
        for n, (key, pair) in enumerate(trail, 2):
            items.append({"@type": "ListItem", "position": n, "name": P(pair), "item": url_of(LANG, key)})
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if _LD["faq"]:
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": re.sub(r"<[^>]+>", "", P(q)), "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", P(a))}} for q, a in _LD["faq"]]})
    if path == "index.html":
        blocks.append({"@context": "https://schema.org", "@type": "Organization", "name": "FZ Consultation", "url": SITE, "logo": f"{SITE}/assets/logo.webp",
                       "email": EMAIL, "description": dsc, "areaServed": ["Europe", "United Kingdom", "Canada", "United States"], "knowsLanguage": ["fr", "en"]})
        blocks.append({"@context": "https://schema.org", "@type": "WebSite", "name": "FZ Consultation", "url": url_of(LANG, "index.html"), "inLanguage": LANG})
    _LD["crumbs"] = None; _LD["faq"] = None
    ld_html = "".join(json_ld(x) for x in blocks)
    reviewed = ""
    if path in REVIEWED:
        reviewed = f'<p class="reviewed">{T("Sources révisées le", "Sources reviewed on")} <time datetime="{REVIEWED[path]}">{fmt_date(REVIEWED[path], LANG)}</time></p>'
        body = body.replace("</section>", "</section>" + reviewed, 1)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    rss = f'<link rel="alternate" type="application/rss+xml" title="FZ Consultation — Insights" href="{r}insights/feed.xml">'
    doc = f'''<!DOCTYPE html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(ttl)}</title>
<meta name="description" content="{E(dsc)}">
{robots}
<link rel="canonical" href="{url_of(LANG, path)}">
{alt}
<meta property="og:type" content="website">
<meta property="og:site_name" content="FZ Consultation">
<meta property="og:title" content="{E(ttl)}">
<meta property="og:description" content="{E(dsc)}">
<meta property="og:url" content="{url_of(LANG, path)}">
<meta property="og:image" content="{SITE}/assets/og-{LANG}.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{"fr_FR" if LANG == "fr" else "en_US"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}../assets/mark.webp" type="image/webp">
<link rel="preload" href="{r}../assets/fonts/schibsted-grotesk.woff2" as="font" type="font/woff2" crossorigin>
{rss}
<script src="{r}../assets/theme.js?v={VER}"></script>
<link rel="stylesheet" href="{r}../assets/site.css?v={VER}">
{extra_head}{ld_html}{analytics}
</head>
<body>
{header(r, path)}
<main id="main"{"" if noindex else " data-pagefind-body"}>
  <div class="wrap">
{body}
{newsite.ctx_cta(sys.modules[__name__], r, path)}
  </div>
</main>
{footer(r)}
<script src="{r}../assets/site.js?v={VER}"></script>
{extra_js}
</body>
</html>
'''
    full = os.path.join(OUT, LANG, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(doc)
    if LANG == "fr" and not noindex: PAGES.append(path)
    return r

import math
def hub_diagram(center, nodes, size=420, pad=110):
    cx = cy = size/2 + pad; R = size*0.34; nr = size*0.115
    vb = size + pad*2
    parts = [f'<svg class="hubdiag" viewBox="0 0 {vb} {vb}" role="img" aria-label="{E(P(center))}">']
    N = len(nodes)
    coords = []
    for k in range(N):
        ang = -math.pi/2 + k*2*math.pi/N
        x, y = cx + R*math.cos(ang), cy + R*math.sin(ang)
        coords.append((x, y, ang))
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" class="hd-line"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{size*0.185}" class="hd-center"/>')
    parts.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" class="hd-clabel">{E(P(center))}</text>')
    for k, (label, sub) in enumerate(nodes):
        x, y, ang = coords[k]
        parts.append(f'<circle cx="{x}" cy="{y}" r="{nr}" class="hd-node"/>')
        parts.append(f'<text x="{x}" y="{y-4}" text-anchor="middle" dominant-baseline="middle" class="hd-num">{k+1:02d}</text>')
        cosA, sinA = math.cos(ang), math.sin(ang)
        if abs(cosA) < 0.35:
            anchor_pos = "middle"; lx = x; ly = y + nr + 22 if sinA > 0 else y - nr - 14
        elif cosA > 0:
            anchor_pos = "start"; lx = x + nr + 12; ly = y + nr + 20 if sinA > 0.35 else (y - nr - 14 if sinA < -0.35 else y + 5)
        else:
            anchor_pos = "end"; lx = x - nr - 12; ly = y + nr + 20 if sinA > 0.35 else (y - nr - 14 if sinA < -0.35 else y + 5)
        parts.append(f'<text x="{lx}" y="{ly}" text-anchor="{anchor_pos}" class="hd-label">{E(P(label))}</text>')
    parts.append('</svg>')
    return '<div class="hubdiag-wrap">' + "".join(parts) + '</div>'

def timeline_diagram(phases, size_w=1040, size_h=190):
    n = len(phases); parts = [f'<svg class="tldiag" viewBox="0 0 {size_w} {size_h}" role="img" aria-label="timeline">']
    y = 70; x0, x1 = 130, size_w-130
    parts.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" class="td-axis"/>')
    for k, (label, dur, desc) in enumerate(phases):
        x = x0 + (x1-x0) * k/(n-1) if n > 1 else (x0+x1)/2
        parts.append(f'<circle cx="{x}" cy="{y}" r="9" class="td-dot"/>')
        parts.append(f'<text x="{x}" y="{y-22}" text-anchor="middle" class="td-dur">{E(P(dur))}</text>')
        parts.append(f'<text x="{x}" y="{y+34}" text-anchor="middle" class="td-label">{E(P(label))}</text>')
        for i, line in enumerate(wrap_text(P(desc), 26)):
            parts.append(f'<text x="{x}" y="{y+54+i*16}" text-anchor="middle" class="td-desc">{E(line)}</text>')
    parts.append('</svg>')
    svg_html = '<div class="tldiag-wrap">' + "".join(parts) + '</div>'
    mobile = '<ol class="tldiag-mobile">' + "".join(
        f'<li><span class="tdm-dur">{E(P(dur))}</span><strong>{E(P(label))}</strong><span class="tdm-desc">{E(P(desc))}</span></li>'
        for label, dur, desc in phases) + '</ol>'
    return svg_html + mobile

def wrap_text(text, width):
    words = text.split(); lines = []; cur = ""
    for w in words:
        if len(cur) + len(w) + 1 <= width: cur = (cur + " " + w).strip()
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines[:3]

def crumbs(r, trail):
    _LD["crumbs"] = trail
    items = [f'<li><a href="{r}index.html">{T("Accueil", "Home")}</a></li>']
    for key, pair in trail[:-1]:
        items.append(f'<li><a href="{r}{key}">{P(pair)}</a></li>')
    items.append(f'<li aria-current="page">{P(trail[-1][1])}</li>')
    return f'<nav class="crumbs" data-pagefind-ignore aria-label="{T("Fil d&#39;Ariane", "Breadcrumb")}"><ol>{"".join(items)}</ol></nav>'

def rprefix(path): return "../" * path.count("/")

def page_hero(r, trail, eyebrow, title, lede):
    return f'''<section class="phero">
      {crumbs(r, trail)}
      <p class="eyebrow">{P(eyebrow)}</p>
      <h1>{P(title)}</h1>
      <p class="lede">{P(lede)}</p>
    </section>'''

def link_rows(r, items):
    return '<ul class="rows">' + "".join(
        f'<li><a href="{r}{p["path"]}"><span class="rt">{P(p["short"])}</span><span class="rs">{P(p["summary"])}</span>{ARROW}</a></li>'
        for p in items) + "</ul>"

def faq(items, title=("Questions fréquentes", "Frequently asked questions")):
    _LD["faq"] = items
    return (f'<section class="block"><h2>{P(title)}</h2><div class="faq">' +
        "".join(f'<details><summary>{P(q)}</summary><div>{P(a, tag="p")}</div></details>' for q, a in items) +
        "</div></section>")

def case_cards(r, items=None):
    return '<div class="cases">' + "".join(
        f'<a href="{r}{c["path"]}" data-sector="{c["sector"][1].lower()}"><span class="pk">{P(c["sector"])}</span><h3>{P(c["short"])}</h3>{P(c["summary"], tag="p")}<span class="more">{T("Lire l&#39;analyse", "Read the analysis")} {ARROW}</span></a>'
        for c in (items or CASES)) + "</div>"

def quiz_band(r):
    return f'''<section class="block"><div class="band">
      <div><p class="eyebrow">{T("Gratuit · 5 minutes", "Free · 5 minutes")}</p>
      <h2>{T("Quel est votre niveau de résilience ?", "How resilient is your organization?")}</h2>
      {T("Douze questions pour obtenir un score par domaine et vos trois priorités. Vos réponses restent dans votre navigateur.", "Twelve questions for a score by area and your top three priorities. Your answers stay in your browser.", tag="p")}</div>
      <a class="btn primary" href="{r}self-assessment.html">{T("Commencer l'auto-évaluation", "Start the self-assessment")}</a>
    </div></section>'''

# ---------------- pages ----------------
def build_lang():
    WWD = ("what-we-do/index.html", OTHER["what-we-do/index.html"])

    # methodology
    path = "what-we-do/methodology.html"; r = "../"
    b = page_hero(r, [WWD, (path, OTHER[path])], OTHER[WWD[0]], ("Notre méthodologie", "Our methodology"),
        ("Un cycle simple, répété jusqu'à ce que la reprise devienne une routine plutôt qu'une improvisation.", "A simple cycle, repeated until recovery becomes routine rather than improvisation."))
    b += f'<section class="block">{hub_diagram(("Résilience", "Resilience"), [(t, d) for t, d, outs in METHOD])}</section>'
    b += f'<section class="block"><h2 class="sr-only">{T("Les étapes du cycle", "The phases of the cycle")}</h2><ol class="phases">'
    for i, (t, d, outs) in enumerate(METHOD, 1):
        b += f'<li><div class="pn">{i:02d}</div><div><h3>{P(t)}</h3>{P(d, tag="p")}<p class="outs"><strong>{T("Livrables", "Outputs")}</strong> ' + " · ".join(P(o) for o in outs) + "</p></div></li>"
    b += "</ol></section>"
    b += f'<section class="block"><h2>{T("Nos principes", "Our principles")}</h2><div class="cover grid2">' + "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in PRINCIPLES) + "</div></section>"
    page(path, ("Méthodologie | FZ Consultation", "Methodology | FZ Consultation"), ("Comprendre, planifier, tester, améliorer.", "Understand, plan, test, improve."), b)

    newsite.build_sectors(sys.modules[__name__])
    r = "../"

    # regulations
    path = "what-we-do/regulations.html"
    b = page_hero(r, [WWD, (path, OTHER[path])], OTHER[WWD[0]], ("Réglementation et référentiels", "Regulations and frameworks"),
        ("Nous alignons nos travaux sur les exigences de chaque marché où vous opérez.", "We align our work with the requirements of each market you operate in."))
    b += '<section class="block">'
    for region, items in REG:
        b += f'<div class="regrow"><h2 class="regh">{P(region)}</h2><dl>'
        for k, d in items:
            b += f"<div><dt>{P(k) if isinstance(k, tuple) else k}</dt><dd>{P(d)}</dd></div>"
        b += "</dl></div>"
    b += f'<p class="note">{T("FZ Consultation fournit des conseils opérationnels et techniques, et non des avis juridiques. Les exigences évoluent : vérifiez toujours leur portée exacte pour votre organisation.", "FZ Consultation provides operational and technical advice, not legal advice. Requirements change: always confirm their exact scope for your organization.")}</p></section>'
    page(path, ("Réglementation | FZ Consultation", "Regulations | FZ Consultation"), ("Référentiels et exigences par région.", "Frameworks and requirements by region."), b)

    newsite.build_cases(sys.modules[__name__])

    newsite.build_wwd(sys.modules[__name__])

    # contact
    path = "contact.html"; r = ""
    book = (f'<a class="btn primary" href="{E(BOOKING_URL)}" target="_blank" rel="noopener">{T("Choisir un créneau", "Pick a time")}</a>' if BOOKING_URL
            else f'<p class="muted">{T("Proposez-nous quelques créneaux dans votre message et nous vous confirmerons un horaire.", "Suggest a few time slots in your message and we will confirm one.")}</p>')
    subjects = [("intro", ("Premier échange", "Intro call")), ("assessment", ("Évaluation", "Assessment")), ("dr", ("Reprise après sinistre", "Disaster recovery")), ("cyber", ("Cybersécurité", "Cybersecurity")), ("exercise", ("Exercice ou test", "Exercise or test")), ("ai", ("Intelligence artificielle", "Artificial intelligence")), ("auditor", ("Audit d'agents IA (FZ AI Auditor)", "AI agent audit (FZ AI Auditor)")), ("partnership", ("Partenariat", "Partnership")), ("other", ("Autre", "Other"))]
    b = page_hero(r, [(path, OTHER[path])], ("Contact", "Contact"), ("Parlons de votre situation", "Let's talk about your situation"),
        ("Un premier échange de 30 minutes, sans engagement, en français ou en anglais.", "A free 30-minute intro call, in French or English."))
    b += f'''<section class="block contact-grid">
      <div class="side">
        <h2>{T("Réserver un appel", "Book a call")}</h2>{book}
        <h2>{T("Avant l'appel", "Before the call")}</h2>
        <p class="muted">{T("L'auto-évaluation prend cinq minutes et donne une bonne base de discussion.", "The self-assessment takes five minutes and gives us a good starting point.")}</p>
        <p><a class="textlink" href="{r}self-assessment.html">{T("Faire l'auto-évaluation", "Take the self-assessment")} {ARROW}</a></p>
      </div>
      <form class="cform" id="contact-form" data-endpoint="{"https://formspree.io/f/" + E(FORMSPREE_ID) if FORMSPREE_ID else ""}" data-email="{EMAIL}" novalidate>
        <h2>{T("Nous écrire", "Send us a message")}</h2>
        <div class="row2">
          <label>{T("Nom", "Name")} <span aria-hidden="true">*</span><input name="name" autocomplete="name" required></label>
          <label>{T("Courriel", "Email")} <span aria-hidden="true">*</span><input name="email" type="email" autocomplete="email" required></label>
        </div>
        <div class="row2">
          <label>{T("Organisation", "Organization")}<input name="organization" autocomplete="organization"></label>
          <label>{T("Sujet", "Topic")}<select name="topic">{"".join(f'<option data-key="{k}">{P(v)}</option>' for k, v in subjects)}</select></label>
        </div>
        <label>{T("Message", "Message")} <span aria-hidden="true">*</span><textarea name="message" rows="6" required></textarea></label>
        <input type="hidden" name="_subject" value="{T("Nouveau message — site FZ Consultation", "New message — FZ Consultation website")}">
        <label class="hp" aria-hidden="true">Website<input name="_gotcha" tabindex="-1" autocomplete="off"></label>
        <label class="consent"><input type="checkbox" name="consent" required> <span>{T("J'accepte que mes informations soient utilisées pour répondre à ma demande, conformément à la", "I agree that my information will be used to respond to my request, in line with the")} <a href="{r}privacy.html">{T("politique de confidentialité", "privacy policy")}</a>.</span></label>
        <button class="btn primary" type="submit">{T("Envoyer", "Send")}</button>
        <p class="fstatus" role="status" aria-live="polite" data-ok="{T("Merci, votre message a bien été envoyé. Nous vous répondrons rapidement.", "Thank you, your message has been sent. We will get back to you shortly.")}" data-err="{T("L'envoi a échoué. Écrivez-nous directement à", "Sending failed. Please email us directly at")} {EMAIL}." data-missing="{T("Merci de remplir les champs obligatoires et d'accepter la politique de confidentialité.", "Please fill in the required fields and accept the privacy policy.")}" data-mailto="{T("Votre application de courriel va s'ouvrir avec votre message.", "Your email app will open with your message.")}"></p>
      </form>
    </section>'''
    page(path, ("Nous joindre | FZ Consultation", "Contact | FZ Consultation"), ("Réservez un premier échange de 30 minutes ou écrivez-nous.", "Book a 30-minute intro call or send us a message."), b)

    # self-assessment
    path = "self-assessment.html"
    qdata = {
        "domains": {k: {"name": P(v[0]), "href": v[1]} for k, v in QUIZ_DOMAINS.items()},
        "options": [P(o) for o in QUIZ_OPTIONS],
        "questions": [{"d": d, "q": P(q), "w": w} for d, q, w in QUIZ],
        "industries": [P(x) for x in QUIZ_INDUSTRIES],
        "sizes": [P(x) for x in QUIZ_SIZES],
        "narrative": {k: P(v) for k, v in QUIZ_NARRATIVE.items()},
        "ui": QUIZ_UI[LANG],
    }
    b = page_hero(r, [(path, OTHER[path])], ("Gratuit · 8 minutes", "Free · 8 minutes"), ("Auto-évaluation de la résilience", "Resilience self-assessment"),
        ("Vingt questions pondérées sur la continuité, la reprise, la sécurité et vos tiers, avec le contexte de votre secteur. Vous obtenez un score par domaine sous forme de diagramme, et une lecture de votre point le plus fragile.", "Twenty weighted questions on continuity, recovery, security and third parties, with context from your industry. You get a score by area as a diagram, and a read on your most fragile spot."))
    b += f'''<section class="block quiz-wrap">
      <div id="quiz" class="quiz" aria-live="polite"></div>
      <noscript><p>{T("Cette auto-évaluation nécessite JavaScript.", "This self-assessment requires JavaScript.")}</p></noscript>
      <p class="note">{T("Vos réponses, y compris votre secteur et la taille de votre organisation, sont traitées uniquement dans votre navigateur. Elles ne sont ni envoyées ni enregistrées. Ce résultat est indicatif et ne remplace pas une évaluation complète.", "Your answers, including your industry and organization size, are processed only in your browser. They are never sent or stored. This result is indicative and does not replace a full assessment.")}</p>
    </section>'''
    js = f'<script type="application/json" id="quiz-data" data-root="{r}">{extras.jsondata(qdata)}</script><script src="{r}../assets/quiz.js?v={VER}"></script>'
    page(path, ("Auto-évaluation de la résilience | FZ Consultation", "Resilience self-assessment | FZ Consultation"),
         ("Évaluez gratuitement la résilience de votre organisation en huit minutes.", "Assess your organization's resilience in eight minutes, for free."), b, extra_js=js)

    build_ai()
    newsite.build_ai_hub(sys.modules[__name__])
    build_partners()

    extras.build_extras(sys.modules[__name__])

    # privacy
    build_privacy(); build_legal()

    # home
    newsite.build_home(sys.modules[__name__])

def ai_band(r):
    return f"""<section class="block"><div class="band ai">
      <div><p class="eyebrow">{T("Intelligence artificielle", "Artificial intelligence")}</p>
      <h2>{T("Adopter l'IA vite, sans perdre le contrôle", "Adopt AI fast, without losing control")}</h2>
      {T("Vision, agents, gouvernance, audit et plateforme Microsoft Foundry Citadel : nous appliquons à l'IA la même exigence de résilience.", "Vision, agents, governance, audit and the Microsoft Foundry Citadel platform: we apply the same resilience discipline to AI.", tag="p")}</div>
      <a class="btn primary" href="{r}ai/index.html">{T("Découvrir notre offre IA", "Explore our AI services")}</a>
    </div></section>"""

def resources_band(r):
    latest = sorted(INSIGHTS, key=lambda a: a["date"], reverse=True)[0]
    return f"""<section class="block"><h2>{T("Ressources gratuites", "Free resources")}</h2>
      <div class="pillars">
      <a href="{r}resources/downtime-calculator.html"><span class="pk">01</span><h3>{T("Calculateur du coût d'une interruption", "Downtime cost calculator")}</h3>{T("Estimez en quelques chiffres ce qu'une heure d'arrêt vous coûte.", "Estimate from a few numbers what an hour of downtime costs you.", tag="p")}<span class="more">{T("Calculer", "Calculate")} {ARROW}</span></a>
      <a href="{r}resources/index.html"><span class="pk">02</span><h3>{T("Modèles à télécharger", "Downloadable templates")}</h3>{T("Liste rançongiciel, feuille RTO/RPO et politique d'utilisation de l'IA.", "Ransomware checklist, RTO/RPO worksheet and AI acceptable-use policy.", tag="p")}<span class="more">{T("Voir les ressources", "Browse resources")} {ARROW}</span></a>
      <a href="{r}insights/{latest["slug"]}.html"><span class="pk">03</span><h3>{P(latest["title"])}</h3>{P(latest["summary"], tag="p")}<span class="more">{T("Lire l'article", "Read the article")} {ARROW}</span></a>
      </div></section>"""

def auditor_band(r):
    return f"""<section class="block"><div class="band auditor">
      <div><p class="eyebrow">{T("Nouveau · FZ AI Auditor", "New · FZ AI Auditor")}</p>
      <h2>{T("Vos agents IA font-ils ce qu'ils devraient, et valent-ils ce qu'ils coûtent ?", "Are your AI agents doing what they should, and are they worth what they cost?")}</h2>
      {T("Un audit avec preuves du périmètre, de la valeur réalisée et du rayon d'impact des agents déployés.", "An evidence-based audit of the scope, value realized and blast radius of your deployed agents.", tag="p")}</div>
      <a class="btn primary" href="{r}ai/auditor.html">{T("Découvrir FZ AI Auditor", "Explore FZ AI Auditor")}</a>
    </div></section>"""

def build_ai():
    WWD = ("ai/index.html", OTHER["ai/index.html"])
    # citadel
    c = CITADEL; r = "../"
    b = page_hero(r, [WWD, (c["path"], c["short"])], ("IA · Plateforme", "AI · Platform"), c["title"], c["lede"])
    b += f'<section class="block split"><div><h2>{T("Qu&#39;est-ce que Citadel ?", "What is Citadel?")}</h2></div>{P(c["what"], tag="p", cls="big")}</section>'
    b += hub_diagram(("Citadel", "Citadel"), [(("Gouvernance", "Governance"), ""), (("Opérations", "Operations"), ""), (("Identité", "Identity"), ""), (("Sécurité", "Security"), "")])
    b += f'<section class="block"><h2>{T("Quatre couches de gouvernance", "Four layers of governance")}</h2><ol class="layers">' + "".join(f'<li><span class="lnum">{i}</span><div><h3>{P(h)}</h3>{P(d, tag="p")}</div></li>' for i, (h, d) in enumerate(c["layers"], 1)) + "</ol></section>"
    b += f'<section class="block"><h2>{T("Pourquoi c&#39;est utile", "Why it matters")}</h2><div class="cover grid2">' + "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in c["why"]) + "</div></section>"
    b += f'<section class="block"><h2>{T("Notre accompagnement Citadel", "How we help with Citadel")}</h2><ol class="phases">' + "".join(f'<li><div class="pn">{i:02d}</div><div><h3>{P(h)}</h3>{P(d, tag="p")}</div></li>' for i, (h, d) in enumerate(c["our"], 1)) + "</ol>"
    b += f'<p style="margin-top:28px"><a class="btn primary" href="{r}ai/vision-questionnaire.html">{T("Commencer par le questionnaire de vision", "Start with the vision questionnaire")}</a></p></section>'
    b += f'<section class="block"><h2>Sources</h2><ul class="sources">' + "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener noreferrer"{SRCLANG()}>{E(t)}</a></li>' for t, u in c["sources"]) + f'</ul>{P(c["note"], tag="p", cls="note")}</section>'
    page(c["path"], ("Microsoft Foundry Citadel | FZ Consultation", "Microsoft Foundry Citadel | FZ Consultation"), c["summary"], b)
    # vision questionnaire
    path = "ai/vision-questionnaire.html"
    data = {"questions": [{"id": q["id"], "type": q["type"], "pillar": q.get("pillar"), "q": P(q["q"]), "opts": [P(o) for o in q["opts"]]} for q in VISION],
            "pillars": {k: {"name": P(v[0]), "href": v[1], "rec": P(v[2])} for k, v in VISION_PILLARS.items()},
            "ui": VISION_UI[LANG], "phrases": VISION_PHRASES[LANG], "email": EMAIL}
    b = page_hero(r, [WWD, (path, OTHER[path])], ("IA · 7 minutes", "AI · 7 minutes"), ("Questionnaire de vision IA", "AI vision questionnaire"),
        ("Treize questions pour formuler votre vision, mesurer votre maturité sur cinq piliers et savoir par où commencer.", "Thirteen questions to frame your vision, measure readiness across five pillars and know where to start."))
    b += f"""<section class="block split"><div><h2>{T("Aligner l&#39;équipe", "Align the team")}</h2></div>{T("Demandez à chaque membre de la direction de remplir le questionnaire séparément, puis comparez les synthèses. Les écarts entre les réponses sont le meilleur point de départ pour l&#39;atelier de vision.", "Ask each member of leadership to complete the questionnaire separately, then compare the summaries. The gaps between answers are the best starting point for the vision workshop.", tag="p", cls="big")}</section>
    <section class="block quiz-wrap"><div id="vision" class="quiz" aria-live="polite"></div>
      <noscript><p>{T("Ce questionnaire nécessite JavaScript.", "This questionnaire requires JavaScript.")}</p></noscript>
      {T("Vos réponses restent dans votre navigateur. Elles ne nous sont transmises que si vous choisissez de nous envoyer la synthèse.", "Your answers stay in your browser. They are only sent to us if you choose to email us the summary.", tag="p", cls="note")}
    </section>"""
    js = f'<script type="application/json" id="vision-data" data-root="{r}">{extras.jsondata(data)}</script><script src="{r}../assets/vision.js?v={VER}"></script>'
    page(path, ("Questionnaire de vision IA | FZ Consultation", "AI vision questionnaire | FZ Consultation"), ("Formulez votre vision de l'IA et mesurez votre maturité.", "Frame your AI vision and measure your readiness."), b, extra_js=js)

def build_partners():
    path = "partners.html"; r = ""
    card = lambda n, d: f'<div class="citem"><h3>{n}</h3>{P(d, tag="p")}</div>'
    b = page_hero(r, [(path, OTHER[path])], ("Partenariats", "Partnerships"), ("Tous les nuages, publics et privés", "Every cloud, public and private"),
        ("Nous travaillons sur les plateformes que vous avez choisies, sans vous en imposer une. Et nous collaborons avec ceux qui servent les mêmes clients.", "We work on the platforms you have chosen, without pushing one on you. And we team up with those who serve the same clients."))
    b += f'<section class="block split"><div><h2>{T("Indépendants de toute plateforme", "Platform-independent")}</h2></div>{T("La plupart des organisations combinent plusieurs nuages publics et une infrastructure privée. Les récents changements de licences dans la virtualisation ont aussi poussé beaucoup d&#39;entre elles à revoir leur plateforme. Notre rôle : que vos services restent disponibles, quel que soit l&#39;endroit où ils tournent.", "Most organizations combine several public clouds with private infrastructure. Recent virtualization licensing changes have also pushed many of them to reconsider their platform. Our role: keep your services available, wherever they run.", tag="p", cls="big")}</section>'
    b += f'<section class="block"><h2>{T("Nuages publics", "Public clouds")}</h2><div class="cover grid2">' + "".join(card(n, d) for n, d in PUBLIC) + "</div></section>"
    b += f'<section class="block"><h2>{T("Nuage privé et hybride", "Private and hybrid cloud")}</h2><div class="cover grid2">' + "".join(card(n, d) for n, d in PRIVATE) + "</div></section>"
    b += f'<section class="block"><h2>{T("Ce que nous faisons entre les plateformes", "What we do across platforms")}</h2><div class="cover grid2">' + "".join(card(P(h), d) for h, d in CROSS) + f'</div><p><a class="textlink" href="{r}what-we-do/expertise/cloud-resilience.html">{P(name_of("what-we-do/expertise/cloud-resilience.html"))} {ARROW}</a></p></section>'
    b += f'<section class="block"><h2>{T("Devenir partenaire", "Partner with us")}</h2>{T("Nous travaillons avec les acteurs qui servent les mêmes clients que nous.", "We work with organizations that serve the same clients as we do.", tag="p", cls="intro")}<div class="pillars">' + "".join(f'<div class="pcard"><span class="pk">0{i}</span><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for i, (h, d) in enumerate(WAYS, 1)) + "</div></section>"
    b += f'<section class="block split"><div><h2>{T("Modes de collaboration", "Ways to work together")}</h2></div><div class="cover">' + "".join(card(P(h), d) for h, d in MODELS) + f'</div></section>'
    b += f'<section class="block"><div class="band ai"><div><h2>{T("Parlons partenariat", "Let&#39;s talk partnership")}</h2>{T("Présentez-nous votre organisation et vos clients : nous verrons ensemble comment nous compléter.", "Tell us about your organization and clients, and we will see together how we can complement each other.", tag="p")}</div><a class="btn primary" href="{r}contact.html">{T("Nous écrire", "Send us a message")}</a></div>'
    b += f'{T("Les plateformes citées le sont pour décrire notre expertise ; leur mention n&#39;implique pas un partenariat officiel avec leurs éditeurs. Toutes les marques appartiennent à leurs propriétaires respectifs.", "Platforms are named to describe our expertise; naming them does not imply an official partnership with their vendors. All trademarks belong to their respective owners.", tag="p", cls="note")}</section>'
    page(path, ("Écosystème et partenariats | FZ Consultation", "Ecosystem and partnerships | FZ Consultation"), ("Résilience sur tous les nuages publics et privés, et partenariats avec intégrateurs, éditeurs et cabinets.", "Resilience across every public and private cloud, and partnerships with integrators, vendors and firms."), b)

def downtime_sections(r):
    b = f'<section class="block" id="benchmarks"><h2>{T("Repères de coût publics", "Public cost benchmarks")}</h2>{T("Des ordres de grandeur publics, par secteur, et des incidents réels pour donner une idée concrète de l&#39;enjeu.", "Public benchmarks, by industry, and real incidents to give a concrete sense of what&#39;s at stake.", tag="p", cls="intro")}<div class="dt-bench">'
    for h, d, src in BENCH_GENERAL:
        b += f'<div class="dt-b"><strong>{P(h)}</strong> {P(d)} <sup><a href="#dt-src-{src}">[{src+1}]</a></sup></div>'
    b += "</div></section>"
    b += f'<section class="block"><h2>{T("Par secteur", "By industry")}</h2><div class="dt-table"><div class="dt-row dt-head"><span>{T("Secteur", "Industry")}</span><span>{T("Ordre de grandeur", "Order of magnitude")}</span><span>{T("Contexte", "Context")}</span></div>'
    for row in BY_INDUSTRY:
        b += f'<div class="dt-row"><span class="dt-i">{P(row["industry"])}</span><span class="dt-r">{P(row["range"])}</span><span class="dt-n">{P(row["note"])} <sup><a href="#dt-src-{row["src"]}">[{row["src"]+1}]</a></sup></span></div>'
    b += "</div></section>"
    b += f'<section class="block"><h2>{T("Incidents réels", "Real incidents")}</h2><div class="dt-cards">'
    for inc in INCIDENTS:
        link = f'{r}{inc["case"]}' if inc["case"] else None
        srcnote = f' <sup><a href="#dt-src-{inc["src"]}">[{inc["src"]+1}]</a></sup>' if inc["src"] is not None else ""
        b += f'<div class="dt-card"><span class="pk">{P(inc["sector"])}</span><h3>{P(inc["name"])}</h3><p>{P(inc["fact"])}</p><p class="dt-cost">{P(inc["cost"])}{srcnote}</p>'
        if link: b += f'<a class="textlink" href="{link}">{T("Lire l&#39;étude de cas", "Read the case study")} {ARROW}</a>'
        b += "</div>"
    b += "</div></section>"
    b += f'<section class="block"><p class="note">{P(METHOD_NOTE)}</p></section>'
    b += f'<section class="block"><h2>Sources</h2><ol class="sources" id="dt-sources">'
    for i, (t, u) in enumerate(SOURCES):
        b += f'<li id="dt-src-{i}"><a href="{E(u)}" target="_blank" rel="noopener noreferrer"{SRCLANG()}>{E(t)}</a></li>'
    b += "</ol></section>"
    return b

def TODO(fr, en): return f'<mark class="todo">[{T("À compléter", "To complete")} : {T(fr, en)}]</mark>' if LANG == "fr" else f'<mark class="todo">[To complete: {en}]</mark>'

def build_privacy():
    path = "privacy.html"; r = ""
    S = []
    S.append((("Qui sommes-nous", "Who we are"),
      T(f"Le responsable du traitement est FZ Consultation. Pour toute question sur vos renseignements personnels, écrivez à <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. ",
        f"The data controller is FZ Consultation. For any question about your personal information, email <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. ") +
      T("La personne responsable de la protection des renseignements personnels est : ", "The person in charge of the protection of personal information is: ") +
      f"Fabien Mariou, <a href=\"mailto:{EMAIL}\">{EMAIL}</a>."))
    items = [
      (T("Messages que vous nous envoyez", "Messages you send us"),
       T("Nom, courriel, organisation et contenu du message, lorsque vous nous écrivez par courriel ou par le formulaire. Nous les utilisons uniquement pour vous répondre et assurer le suivi de votre demande.",
         "Name, email, organization and message content, when you email us or use the form. We use them only to reply and follow up on your request."))]
    if FORMSPREE_ID:
        items.append((T("Formulaire de contact", "Contact form"), T("Le formulaire est transmis par Formspree, qui nous relaie votre message.", "The form is delivered by Formspree, which forwards your message to us.")))
    if BOOKING_URL:
        items.append((T("Prise de rendez-vous", "Booking"), T("Si vous réservez un appel, l'outil de réservation traite votre nom, votre courriel et le créneau choisi.", "If you book a call, the booking tool processes your name, email and chosen time.")))
    if CF_ANALYTICS_TOKEN:
        items.append((T("Mesure d'audience", "Analytics"), T("Nous utilisons Cloudflare Web Analytics, qui mesure la fréquentation de façon agrégée, sans cookies et sans profil individuel.", "We use Cloudflare Web Analytics, which measures traffic in aggregate, without cookies or individual profiles.")))
    items += [
      (T("Hébergement", "Hosting"), T("Le site est hébergé par GitHub Pages. Comme tout hébergeur, GitHub peut enregistrer l'adresse IP des visiteurs à des fins de sécurité.", "The site is hosted on GitHub Pages. Like any host, GitHub may log visitors' IP addresses for security purposes.")),
      (T("Auto-évaluation", "Self-assessment"), T("Vos réponses sont traitées uniquement dans votre navigateur et ne nous sont jamais transmises.", "Your answers are processed only in your browser and are never sent to us.")),
      (T("Questionnaire de vision IA", "AI vision questionnaire"), T("Vos réponses restent dans votre navigateur. Elles ne nous parviennent que si vous choisissez de nous envoyer la synthèse par courriel.", "Your answers stay in your browser. They only reach us if you choose to email us the summary.")),
      (T("Préférences d'affichage", "Display preferences"), T("Votre choix de langue et de thème (clair, sombre ou automatique) est conservé dans le stockage local de votre navigateur, et n'est jamais transmis. Nous n'utilisons aucun cookie.", "Your language and theme choice (light, dark or automatic) is kept in your browser's local storage and never transmitted. We use no cookies.")),
      (T("Recherche et calculateur", "Search and calculator"), T("La recherche utilise un index statique et s'exécute dans votre navigateur : vos requêtes ne sont pas transmises. Les chiffres saisis dans le calculateur ne quittent pas votre navigateur.", "Search uses a static index and runs in your browser: your queries are not transmitted. Numbers entered in the calculator never leave your browser.")),
    ]
    S.append((("Renseignements que nous recueillons", "Information we collect"), "<ul>" + "".join(f"<li><strong>{h}.</strong> {d}</li>" for h, d in items) + "</ul>"))
    S.append((("Bases légales", "Legal bases"), T("Nous traitons vos renseignements sur la base de votre consentement ou de notre intérêt légitime à répondre aux demandes qui nous sont adressées et à assurer la sécurité du site.",
        "We process your information on the basis of your consent or our legitimate interest in responding to requests and keeping the site secure.")))
    S.append((("Conservation", "Retention"), T("Nous conservons les échanges avec les prospects jusqu'à trois ans après le dernier contact, puis nous les supprimons, sauf si une relation d'affaires en cours ou une obligation légale exige une conservation plus longue.",
        "We keep exchanges with prospective clients for up to three years after the last contact, then delete them, unless an ongoing business relationship or a legal obligation requires longer retention.")))
    S.append((("Prestataires et transferts hors de votre pays", "Service providers and transfers outside your country"), T("Certains prestataires (hébergement et, le cas échéant, formulaire, réservation ou mesure d'audience) sont situés aux États-Unis. Ces transferts reposent sur des garanties appropriées, comme les clauses contractuelles types ou le cadre de protection des données UE–États-Unis lorsqu'il s'applique. Nous ne vendons ni ne louons vos renseignements.",
        "Some providers (hosting and, where applicable, form, booking or analytics) are located in the United States. These transfers rely on appropriate safeguards, such as standard contractual clauses or the EU–U.S. Data Privacy Framework where it applies. We never sell or rent your information.")))
    S.append((("Vos droits", "Your rights"), T(f"Selon la loi qui s'applique à vous (RGPD, RGPD du Royaume-Uni, Loi 25 au Québec, LPRPDE au Canada ou autres), vous pouvez demander l'accès à vos renseignements, leur rectification, leur suppression ou leur portabilité, vous opposer à leur traitement, en limiter l'usage et retirer votre consentement. Écrivez à <a href=\"mailto:{EMAIL}\">{EMAIL}</a> ; nous répondons dans un délai de 30 jours.",
        f"Depending on the law that applies to you (GDPR, UK GDPR, Quebec's Law 25, Canada's PIPEDA or others), you can request access to your information, correction, deletion or portability, object to or restrict its processing, and withdraw your consent. Email <a href=\"mailto:{EMAIL}\">{EMAIL}</a>; we respond within 30 days.")))
    S.append((("Plaintes", "Complaints"), T("Vous pouvez aussi vous adresser à une autorité de contrôle : la CNIL en France, l'ICO au Royaume-Uni, la Commission d'accès à l'information du Québec, le Commissariat à la protection de la vie privée du Canada, ou l'autorité de votre pays.",
        "You can also contact a supervisory authority: the CNIL in France, the ICO in the UK, Quebec's Commission d'accès à l'information, the Office of the Privacy Commissioner of Canada, or the authority in your country.")))
    S.append((("Sécurité", "Security"), T("Le site est servi uniquement en HTTPS et ne dépose aucun cookie. Nous limitons l'accès aux messages reçus aux personnes qui en ont besoin.", "The site is served only over HTTPS and sets no cookies. Access to messages we receive is limited to those who need it.")))
    S.append((("Modifications", "Changes"), T("Nous pouvons mettre à jour cette politique. La date de dernière mise à jour figure en haut de la page.", "We may update this policy. The date of the last update appears at the top of the page.")))
    b = page_hero(r, [(path, OTHER[path])], ("Légal", "Legal"), OTHER[path], (f"Dernière mise à jour : {UPDATED[0]}", f"Last updated: {UPDATED[1]}"))
    b += '<section class="block legal">' + "".join(f"<h2>{P(h)}</h2><div>{body}</div>" for h, body in S) + "</section>"
    page(path, ("Politique de confidentialité | FZ Consultation", "Privacy policy | FZ Consultation"), ("Comment FZ Consultation traite vos renseignements personnels.", "How FZ Consultation handles your personal information."), b)

def build_legal():
    path = "legal.html"; r = ""
    S = [
     (("Éditeur du site", "Site publisher"),
      f"<p>FZ Consultation — {T('entreprise individuelle', 'sole proprietorship')}<br>621 rue Massena<br>Greenfield Park (Québec) J4V 1E3<br>Canada<br>{T('Numéro d’entreprise du Québec (NEQ)', 'Quebec Enterprise Number (NEQ)')}{T(' : ', ': ')}1181466344<br>{T('Courriel', 'Email')}{T(' : ', ': ')}<a href=\"mailto:{EMAIL}\">{EMAIL}</a></p>"),
     (("Directeur de la publication", "Publication director"), "<p>Fabien Mariou</p>"),
     (("Hébergement", "Hosting"), "<p>GitHub, Inc. — 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, " + T("États-Unis", "United States") + " — <a href=\"https://github.com\" rel=\"noopener\">github.com</a></p>"),
     (("Propriété intellectuelle", "Intellectual property"), "<p>" + T("Le contenu de ce site (textes, logo, graphismes) appartient à FZ Consultation, sauf mention contraire. Toute reproduction sans autorisation est interdite. La police Schibsted Grotesk est utilisée sous licence SIL Open Font License 1.1.",
        "The content of this site (text, logo, graphics) belongs to FZ Consultation unless stated otherwise. Reproduction without permission is prohibited. The Schibsted Grotesk font is used under the SIL Open Font License 1.1.") + "</p>"),
     (("Études de cas", "Case studies"), "<p>" + T("Les études de cas analysent des incidents publics à partir de sources publiques citées. FZ Consultation n'a participé à aucun de ces incidents et n'a aucun lien avec les organisations mentionnées. Les marques citées appartiennent à leurs propriétaires respectifs.",
        "The case studies analyze public incidents using cited public sources. FZ Consultation was not involved in any of these incidents and has no affiliation with the organizations named. Trademarks mentioned belong to their respective owners.") + "</p>"),
     (("Responsabilité", "Liability"), "<p>" + T("Les informations publiées sont fournies à titre général et ne constituent ni un avis juridique ni une recommandation adaptée à votre situation. Les liens vers des sites externes sont fournis pour information ; nous ne sommes pas responsables de leur contenu.",
        "Published information is general in nature and is neither legal advice nor a recommendation tailored to your situation. Links to external sites are provided for information; we are not responsible for their content.") + "</p>"),
     (("Données personnelles", "Personal data"), f'<p>{T("Voir notre", "See our")} <a href="{r}privacy.html">{T("politique de confidentialité", "privacy policy")}</a>.</p>'),
    ]
    b = page_hero(r, [(path, OTHER[path])], ("Légal", "Legal"), OTHER[path], ("Informations sur l'éditeur et l'hébergeur du site.", "Information about the site's publisher and host."))
    b += '<section class="block legal">' + "".join(f"<h2>{P(h)}</h2>{body}" for h, body in S) + "</section>"
    page(path, ("Mentions légales | FZ Consultation", "Legal notice | FZ Consultation"), ("Mentions légales de FZ Consultation.", "FZ Consultation legal notice."), b)

def strip_other(fragment):
    other = "en" if LANG == "fr" else "fr"
    pat = re.compile(r'<(\w+)((?:(?!>)[^\n])*?)\slang="' + other + r'"([^>]*)>.*?</\1>', re.S)
    prev = None
    while prev != fragment:
        prev = fragment; fragment = pat.sub("", fragment)
    return re.sub(r'\slang="' + LANG + '"', "", fragment)

REG = [
 (("Union européenne", "European Union"), [
   ("DORA", ("Règlement sur la résilience opérationnelle numérique du secteur financier, en application depuis janvier 2025 : gestion des risques TIC, tests, incidents et prestataires tiers.", "Digital Operational Resilience Act for the financial sector, applicable since January 2025: ICT risk management, testing, incidents and third-party providers.")),
   ("NIS2", ("Directive sur la cybersécurité des entités essentielles et importantes, transposée dans le droit de chaque État membre.", "Directive on cybersecurity for essential and important entities, transposed into each member state's law.")),
   ("ISO 22301 · ISO/IEC 27001 · ISO/IEC 42001", ("Normes internationales de continuité des activités, de sécurité de l'information et de management des systèmes d'IA.", "International standards for business continuity, information security and AI management systems.")),
   (("Règlement sur l'IA (modifié par le « Digital Omnibus »)", "AI Act (as amended by the Digital Omnibus)"), ("Règlement (UE) 2024/1689, modifié par le règlement (UE) 2026/1744 : obligations des systèmes à haut risque de l'annexe III à partir du 2 décembre 2027 (au lieu du 2 août 2026), de l'annexe I à partir du 2 août 2028, et des systèmes destinés aux autorités publiques au plus tard le 2 août 2030. Transparence de l'article 50(2) et nouvelles interdictions de l'article 5 : 2 décembre 2026. Voir le détail sur la page IA.", "Regulation (EU) 2024/1689, amended by Regulation (EU) 2026/1744: obligations for Annex III high-risk systems from 2 December 2027 (instead of 2 August 2026), for Annex I from 2 August 2028, and for systems intended for public authorities by 2 August 2030. Article 50(2) transparency and the new Article 5 prohibitions: 2 December 2026. Details on the AI page."))]),
 (("Royaume-Uni", "United Kingdom"), [
   ("FCA / PRA", ("Règles de résilience opérationnelle : services d'affaires importants, seuils de tolérance d'impact et scénarios de test.", "Operational resilience rules: important business services, impact tolerances and scenario testing.")),
   ("Cyber Essentials", ("Programme gouvernemental de mesures de sécurité de base, souvent exigé dans les marchés publics.", "Government-backed scheme for baseline security controls, often required in public contracts."))]),
 (("Canada", "Canada"), [
   ("BSIF / OSFI B-13", ("Ligne directrice sur la gestion des risques liés aux technologies et au cyberrisque.", "Guideline on technology and cyber risk management.")),
   ("BSIF / OSFI E-21", ("Ligne directrice sur la résilience opérationnelle et la gestion du risque opérationnel.", "Guideline on operational resilience and operational risk management.")),
   ("BSIF / OSFI E-23", ("Ligne directrice sur la gestion du risque de modèle, y compris les modèles d'IA et d'apprentissage automatique ; en vigueur le 1er mai 2027.", "Guideline on model risk management, including AI and machine-learning models; effective May 1, 2027.")),
   (("Loi 25 (Québec)", "Law 25 (Quebec)"), ("Protection des renseignements personnels, y compris la gestion et la déclaration des incidents de confidentialité.", "Personal information protection, including handling and reporting of privacy incidents."))]),
 (("États-Unis", "United States"), [
   ("NIST CSF 2.0", ("Cadre de cybersécurité de référence : gouverner, identifier, protéger, détecter, répondre, rétablir.", "Reference cybersecurity framework: govern, identify, protect, detect, respond, recover.")),
   ("NIST SP 800-34", ("Guide de planification de la contingence des systèmes d'information.", "Contingency planning guide for information systems.")),
   ("SR 11-7", ("Orientation de la Réserve fédérale et de l'OCC sur la gestion du risque de modèle dans les institutions financières.", "Federal Reserve and OCC guidance on model risk management at financial institutions.")),
   ("NIST AI RMF 1.0", ("Cadre de gestion des risques de l'IA : gouverner, cartographier, mesurer et gérer.", "AI risk management framework: govern, map, measure and manage.")),
   ("SOC 2", ("Rapport d'assurance sur les contrôles, souvent demandé par les clients des entreprises SaaS.", "Assurance report on controls, often requested by customers of SaaS companies."))]),
]

def root_files():
    import base64
    redirect_js = "(function(){var l=null;try{l=localStorage.getItem(\"fz-lang\")}catch(e){}if(l!==\"fr\"&&l!==\"en\")l=(navigator.language||\"fr\").toLowerCase().indexOf(\"fr\")===0?\"fr\":\"en\";location.replace(l+\"/\"+location.search+location.hash)})();"
    sha = "sha256-" + base64.b64encode(hashlib.sha256(redirect_js.encode()).digest()).decode()
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}/{l}/">' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    open(os.path.join(OUT, "index.html"), "w").write(f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FZ Consultation</title>
<meta name="description" content="Résilience d'affaires, sécurité et reprise après sinistre. Business resilience, security and disaster recovery.">
<link rel="canonical" href="{SITE}/">
{alt}
<link rel="icon" href="assets/mark.webp" type="image/webp">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src '{sha}'; style-src 'unsafe-inline'; base-uri 'self'; object-src 'none'">
<script>{redirect_js}</script>
<style>body{{font-family:system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0;background:#EEF1F3;color:#16222E}}a{{color:#0052B2;font-weight:700;margin:0 12px}}</style>
</head>
<body><p><a href="fr/">Français</a> · <a href="en/">English</a></p></body>
</html>
''')
    open(os.path.join(OUT, "404.html"), "w").write('''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self'; base-uri 'self'; object-src 'none'">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page introuvable · Page not found | FZ Consultation</title><meta name="robots" content="noindex">
<link rel="icon" href="/assets/mark.webp" type="image/webp">
<style>@font-face{font-family:"SG";src:url(/assets/fonts/schibsted-grotesk.woff2) format("woff2");font-weight:400 900}
body{font-family:"SG",system-ui,sans-serif;margin:0;min-height:100vh;display:grid;place-items:center;background:#EEF1F3;color:#16222E;padding:24px}
main{max-width:560px}img{height:48px}h1{font-size:2.2rem;margin:24px 0 8px}p{color:#56656F}a{color:#0052B2;font-weight:700}
@media (prefers-color-scheme:dark){body{background:#0E1726;color:#E6ECF3}p{color:#9AA8BA}a{color:#86B3F0}img{filter:brightness(0) invert(1)}}</style></head>
<body><main><img src="/assets/mark.webp" alt="FZ Consultation">
<h1>Page introuvable</h1><p>Cette page n'existe pas ou a été déplacée. <a href="/fr/">Retour à l'accueil</a></p>
<h1 lang="en">Page not found</h1><p lang="en">This page doesn't exist or has moved. <a href="/en/">Back to home</a></p></main></body></html>
''')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = []
    for p in PAGES:
        for l in LANGS:
            links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{x}" href="{url_of(x, p)}"/>' for x in LANGS)
            urls.append(f"  <url>\n    <loc>{url_of(l, p)}</loc>{links}\n  </url>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(OUT, "CNAME"), "w").write(SITE.split("//")[1] + "\n")
    os.makedirs(os.path.join(OUT, ".well-known"), exist_ok=True)
    open(os.path.join(OUT, ".well-known", "security.txt"), "w").write(
        f"Contact: mailto:{EMAIL}\nExpires: {SECURITY_EXPIRES}\nPreferred-Languages: fr, en\nCanonical: {SITE}/.well-known/security.txt\nPolicy: {SITE}/en/security.html\n")
    open(os.path.join(OUT, "_config.yml"), "w").write("# Jekyll settings used by GitHub Pages branch deploys.\n# .well-known must be included explicitly, otherwise Jekyll skips dot-folders.\ninclude:\n  - .well-known\nexclude:\n  - _build\n  - .github\n  - node_modules\n  - README.md\n")

if __name__ == "__main__":
    import hashlib
    import make_docs
    make_docs.main(os.path.join(OUT, "assets", "downloads"))
    h = hashlib.md5()
    for f in ("site.css", "site.js", "quiz.js", "vision.js", "theme.js", "calc.js", "search.js"):
        h.update(open(os.path.join(OUT, "assets", f), "rb").read())
    VER = h.hexdigest()[:8]
    for d in LANGS:
        shutil.rmtree(os.path.join(OUT, d), ignore_errors=True)
    newsite.prepare_cases(sys.modules[__name__])
    for LANG in LANGS:
        build_lang()
    newsite.write_stubs(sys.modules[__name__])
    print('links rewritten in', newsite.rewrite_links(sys.modules[__name__]), 'files')
    root_files()
    print("built", len(PAGES), "pages x", len(LANGS), "languages ->", os.path.abspath(OUT))
