"""FZ Consultation site generator.
Builds separate /fr/ and /en/ versions of every page, plus root redirect, 404, sitemap and robots.
Edit the CONFIG block, then run:  python3 build.py
"""
import os, re, html, json, shutil
from content import *
from cases import CASES
from newcontent import *
from industries import IND
from ai import *
from partners import *

# ================= CONFIG =================
SITE = "https://fzconsultation.xyz"
EMAIL = "contact@fzconsultation.xyz"
BOOKING_URL = ""          # e.g. your Cal.com or Calendly link; leave "" to hide the booking button
FORMSPREE_ID = "mkjgvpwo"       # e.g. "abcdwxyz" from formspree.io; leave "" and the form opens the visitor's email app instead
CF_ANALYTICS_TOKEN = ""   # Cloudflare Web Analytics token; leave "" for no analytics
UPDATED = ("25 septembre 2026", "September 25, 2026")
# ==========================================

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..") if os.path.basename(HERE) == "_build" else os.path.join(HERE, "site2")
LANGS = ["fr", "en"]
LANG = "fr"
PAGES = []  # (lang-independent path) for sitemap

def I(): return 0 if LANG == "fr" else 1
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
 "ai/vision-questionnaire.html": ("Questionnaire de vision IA", "AI vision questionnaire"),
}
def name_of(key):
    for p in EXPERTISE + SERVICES + IND + AI_PAGES + [CITADEL] + CASES:
        if p["path"] == key: return p["short"]
    return OTHER[key]
def item_of(key):
    for p in EXPERTISE + SERVICES + IND + AI_PAGES + [CITADEL] + CASES:
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
        "".join(f'<li>{a(k, OTHER[k])}</li>' for k in ["what-we-do/methodology.html", "what-we-do/regulations.html", "case-studies/index.html", "partners.html", "self-assessment.html"]) +
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
            {col("what-we-do/expertise/index.html", EXPERTISE)}
            {col("what-we-do/services/index.html", SERVICES)}
            {col("what-we-do/industries.html", IND)}
            {approach}
          </div>
        </div>
      </div>
      {a("ai/index.html", ("IA", "AI"))}
      {a("case-studies/index.html", ("Études de cas", "Case studies"))}
      {a("self-assessment.html", ("Auto-évaluation", "Self-assessment"))}
      {a("contact.html", ("Nous joindre", "Contact us"), "nav-cta")}
    </nav>
    <nav class="lang" aria-label="Langue / Language">
      <a href="{fr_href}" hreflang="fr" data-lang="fr"{fr_cur}>FR</a>
      <a href="{en_href}" hreflang="en" data-lang="en"{en_cur}>EN</a>
    </nav>
  </div>
</header>'''

def cta_block(r, path=""):
    book = (f'<a class="btn signal" href="{E(BOOKING_URL)}" target="_blank" rel="noopener">{T("Réserver un appel de 30 minutes", "Book a 30-minute call")}</a>' if BOOKING_URL else "")
    return f'''<section class="block" id="contact" style="border-top:0;padding-top:24px">
      <div class="contact">
        <h2>{T("Parlons de votre prochaine panne, avant qu'elle n'arrive.", "Let's talk about your next outage before it happens.")}</h2>
        <p>{T("Un premier échange de 30 minutes, sans engagement, pour faire le point sur vos risques et vos priorités.", "A free 30-minute intro call to review your risks and priorities.")}</p>
        <div class="cta-actions">{book}<a class="btn light" href="{r}contact.html">{T("Nous écrire", "Send us a message")}</a>{"" if path == "self-assessment.html" else f'<a class="btn outline-light" href="{r}self-assessment.html">{T("Faire l&#39;auto-évaluation", "Take the self-assessment")}</a>'}</div>
        <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
    </section>'''

def footer(r):
    li = lambda key, pair: f'<li><a href="{r}{key}">{P(pair)}</a></li>'
    return f'''<footer class="site">
  <div class="wrap fgrid">
    <div class="fbrand">
      <img src="{r}../assets/logo.webp" alt="FZ Consultation" width="160" height="120" class="flogo">
      <p>{T("Résilience d'affaires, sécurité et reprise après sinistre.", "Business resilience, security and disaster recovery.")}</p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div><h3>{T("Expertise", "Expertise")}</h3><ul>{"".join(li(p["path"], p["short"]) for p in EXPERTISE)}</ul></div>
    <div><h3>{T("Services", "Services")}</h3><ul>{"".join(li(p["path"], p["short"]) for p in SERVICES)}</ul></div>
    <div><h3>{T("IA", "AI")}</h3><ul>{"".join(li(p["path"], p["short"]) for p in AI_PAGES + [CITADEL])}{li("ai/vision-questionnaire.html", OTHER["ai/vision-questionnaire.html"])}</ul></div>
    <div><h3>{T("Secteurs", "Industries")}</h3><ul>{"".join(li(p["path"], p["short"]) for p in IND)}</ul></div>
    <div><h3>{T("Ressources", "Resources")}</h3><ul>{"".join(li(k, OTHER[k]) for k in ["case-studies/index.html", "partners.html", "what-we-do/methodology.html", "what-we-do/regulations.html", "self-assessment.html", "contact.html"])}</ul></div>
  </div>
  <div class="wrap fbottom">
    <span>© <span class="year">2026</span> FZ Consultation</span>
    <span class="flegal"><a href="{r}privacy.html">{P(OTHER["privacy.html"])}</a><a href="{r}legal.html">{P(OTHER["legal.html"])}</a></span>
    <span>{T("Europe · Royaume-Uni · Canada · États-Unis", "Europe · UK · Canada · United States")}</span>
  </div>
</footer>'''

def page(path, title, desc, body, extra_head="", extra_js=""):
    depth = path.count("/") + 1          # +1 for the /fr or /en folder
    r = "../" * (depth - 1)              # link prefix to this language's root
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{url_of(l, path)}">' for l in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    analytics = (f'<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "{E(CF_ANALYTICS_TOKEN)}"}}\'></script>' if CF_ANALYTICS_TOKEN else "")
    ttl, dsc = P(title), P(desc)
    doc = f'''<!DOCTYPE html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(ttl)}</title>
<meta name="description" content="{E(dsc)}">
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
<link rel="stylesheet" href="{r}../assets/site.css?v={VER}">
{extra_head}{analytics}
</head>
<body>
{header(r, path)}
<main id="main">
  <div class="wrap">
{body}
{cta_block(r, path) if path != "contact.html" else ""}
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
    if LANG == "fr": PAGES.append(path)
    return r

def crumbs(r, trail):
    items = [f'<li><a href="{r}index.html">{T("Accueil", "Home")}</a></li>']
    for key, pair in trail[:-1]:
        items.append(f'<li><a href="{r}{key}">{P(pair)}</a></li>')
    items.append(f'<li aria-current="page">{P(trail[-1][1])}</li>')
    return f'<nav class="crumbs" aria-label="{T("Fil d&#39;Ariane", "Breadcrumb")}"><ol>{"".join(items)}</ol></nav>'

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
    return (f'<section class="block"><h2>{P(title)}</h2><div class="faq">' +
        "".join(f'<details><summary>{P(q)}</summary><div>{P(a, tag="p")}</div></details>' for q, a in items) +
        "</div></section>")

def case_cards(r, items=None):
    return '<div class="cases">' + "".join(
        f'<a href="{r}{c["path"]}"><span class="pk">{P(c["sector"])}</span><h3>{P(c["short"])}</h3>{P(c["summary"], tag="p")}<span class="more">{T("Lire l&#39;analyse", "Read the analysis")} {ARROW}</span></a>'
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

    # detail pages
    def detail(p, section_key):
        r = rprefix(p["path"])
        trail = [WWD, (section_key, OTHER[section_key]), (p["path"], p["short"])]
        b = page_hero(r, trail, OTHER[section_key], p["title"], p["lede"])
        b += f'<section class="block split"><div><h2>{T("Ce que nous couvrons", "What we cover")}</h2>{P(p["intro"], tag="p", cls="intro")}</div><div class="cover">'
        b += "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in p["cover"]) + "</div></section>"
        b += f'<section class="block split"><div><h2>{T("Ce que vous recevez", "What you get")}</h2></div><ul class="checks">'
        b += "".join(f'<li>{P(d)}</li>' for d in p["deliverables"]) + "</ul></section>"
        b += faq(p["faq"])
        rel = [next((x for x in EXPERTISE + SERVICES if x["path"] == k), None) or {"path": k, "short": OTHER[k], "summary": ("", "")} for k in p["related"]]
        b += f'<section class="block"><h2>{T("À voir aussi", "Related")}</h2>{link_rows(r, rel)}</section>'
        page(p["path"], (f'{p["title"][0]} | FZ Consultation', f'{p["title"][1]} | FZ Consultation'), p["summary"], b)
    for p in EXPERTISE: detail(p, "what-we-do/expertise/index.html")
    for p in SERVICES: detail(p, "what-we-do/services/index.html")

    def hub(path, title, lede, items, intro):
        r = rprefix(path)
        b = page_hero(r, [WWD, (path, OTHER[path])], OTHER[WWD[0]], title, lede)
        b += f'<section class="block">{P(intro, tag="p", cls="intro")}{link_rows(r, items)}</section>'
        page(path, (f'{title[0]} | FZ Consultation', f'{title[1]} | FZ Consultation'), lede, b)
    hub("what-we-do/expertise/index.html", ("Nos domaines d'expertise", "Our areas of expertise"),
        ("De la continuité des activités à la cybersécurité, tout ce qui permet à votre organisation de tenir le coup.", "From business continuity to cybersecurity, everything that keeps your organization standing."),
        EXPERTISE, ("Quatre domaines complémentaires. La plupart des mandats en combinent plusieurs, car une panne touche rarement un seul domaine.", "Four complementary areas. Most engagements combine several, because an outage rarely stays in one area."))
    hub("what-we-do/services/index.html", ("Nos services", "Our services"),
        ("Des mandats ciblés ou un accompagnement continu, selon votre maturité et vos échéances.", "Focused engagements or ongoing support, depending on your maturity and deadlines."),
        SERVICES, ("Chaque service peut être pris seul ou enchaîné avec les autres, en suivant notre méthodologie.", "Each service can be taken on its own or combined with the others, following our methodology."))

    # methodology
    path = "what-we-do/methodology.html"; r = "../"
    b = page_hero(r, [WWD, (path, OTHER[path])], OTHER[WWD[0]], ("Notre méthodologie", "Our methodology"),
        ("Un cycle simple, répété jusqu'à ce que la reprise devienne une routine plutôt qu'une improvisation.", "A simple cycle, repeated until recovery becomes routine rather than improvisation."))
    b += '<section class="block"><ol class="phases">'
    for i, (t, d, outs) in enumerate(METHOD, 1):
        b += f'<li><div class="pn">{i:02d}</div><div><h3>{P(t)}</h3>{P(d, tag="p")}<p class="outs"><strong>{T("Livrables", "Outputs")}</strong> ' + " · ".join(P(o) for o in outs) + "</p></div></li>"
    b += "</ol></section>"
    b += f'<section class="block"><h2>{T("Nos principes", "Our principles")}</h2><div class="cover grid2">' + "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in PRINCIPLES) + "</div></section>"
    page(path, ("Méthodologie | FZ Consultation", "Methodology | FZ Consultation"), ("Comprendre, planifier, tester, améliorer.", "Understand, plan, test, improve."), b)

    # industries hub + detail pages
    path = "what-we-do/industries.html"
    b = page_hero(r, [WWD, (path, OTHER[path])], OTHER[WWD[0]], ("Secteurs d'activité", "Industries"),
        ("Chaque secteur a ses propres risques, contraintes et attentes réglementaires.", "Every sector has its own risks, constraints and regulatory expectations."))
    b += f'<section class="block">{link_rows(r, IND)}</section>'
    b += f'<section class="block"><h2>{T("Leçons tirées d&#39;incidents publics", "Lessons from public incidents")}</h2>{case_cards(r)}</section>'
    page(path, ("Secteurs | FZ Consultation", "Industries | FZ Consultation"), ("Secteurs que nous accompagnons.", "Industries we support."), b)
    for ind in IND:
        r = rprefix(ind["path"])
        b = page_hero(r, [WWD, (path, OTHER[path]), (ind["path"], ind["short"])], ("Secteur", "Industry"), ind["short"], ind["lede"])
        b += f'<section class="block split"><div><h2>{T("Le contexte", "The context")}</h2>{P(ind["context"], tag="p", cls="intro")}</div><div class="cover">'
        b += "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in ind["risks"]) + "</div></section>"
        b += f'<section class="block split"><div><h2>{T("Référentiels clés", "Key frameworks")}</h2></div><ul class="regtags">' + "".join(f"<li>{P(x) if isinstance(x, tuple) else x}</li>" for x in ind["regs"]) + f'</ul></section>'
        b += f'<section class="block"><h2>{T("Exemples de mandats", "Example engagements")}</h2>{T("Ces scénarios illustrent le type de travail que nous réalisons dans ce secteur. Ils ne décrivent pas des clients réels.", "These scenarios illustrate the kind of work we do in this sector. They do not describe real clients.", tag="p", cls="intro")}<div class="engs">'
        for e in ind["engagements"]:
            b += f'<article class="eng"><h3>{P(e["t"])}</h3><dl><div><dt>{T("Situation", "Situation")}</dt><dd>{P(e["ctx"])}</dd></div><div><dt>{T("Ce que nous faisons", "What we do")}</dt><dd>{P(e["work"])}</dd></div><div><dt>{T("Résultat attendu", "Expected outcome")}</dt><dd>{P(e["out"])}</dd></div></dl></article>'
        b += "</div></section>"
        if ind["cases"]:
            b += f'<section class="block"><h2>{T("Études de cas liées", "Related case studies")}</h2>{link_rows(r, [item_of(k) for k in ind["cases"]])}</section>'
        b += f'<section class="block"><h2>{T("Autres secteurs", "Other industries")}</h2>{link_rows(r, [x for x in IND if x is not ind][:3])}</section>'
        page(ind["path"], (f'{ind["short"][0]} | FZ Consultation', f'{ind["short"][1]} | FZ Consultation'), ind["summary"], b)
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

    # case studies
    DISC = ("Analyse fondée uniquement sur des informations publiques. FZ Consultation n'a pas participé à cet incident et n'a aucun lien avec les organisations mentionnées.",
            "Analysis based solely on public information. FZ Consultation was not involved in this incident and has no affiliation with the organizations named.")
    for c in CASES:
        r = "../"
        b = page_hero(r, [("case-studies/index.html", OTHER["case-studies/index.html"]), (c["path"], c["sector"])],
                      (T("Étude de cas · ", "Case study · ") + c["sector"][0], T("Étude de cas · ", "Case study · ") + c["sector"][1]), c["short"], c["summary"])
        b += '<section class="facts"><dl>' + "".join(f"<div><dt>{P(k)}</dt><dd>{P(v)}</dd></div>" for k, v in c["facts"]) + "</dl>"
        b += f'<p class="disclaimer">{P(DISC)}</p></section>'
        b += f'<section class="block split"><div><h2>{T("Ce qui s&#39;est passé", "What happened")}</h2></div><ol class="timeline-list">'
        b += "".join(f'<li><span class="when">{P(w)}</span>{P(d, tag="p")}</li>' for w, d in c["timeline"]) + "</ol></section>"
        b += f'<section class="block split"><div><h2>{T("Ce qui a mal tourné", "What went wrong")}</h2>{T("D&#39;après les sources publiques citées plus bas.", "According to the public sources listed below.", tag="p", cls="intro")}</div><div class="cover">'
        b += "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in c["wrong"]) + "</div></section>"
        b += f'<section class="block"><h2>{T("Les leçons pour votre organisation", "Lessons for your organization")}</h2><ol class="lessons">'
        for i, (h, d, link) in enumerate(c["lessons"], 1):
            b += f'<li><span class="ln">{i}</span><div><h3>{P(h)}</h3>{P(d, tag="p")}<a class="textlink" href="{r}{link}">{P(name_of(link))} {ARROW}</a></div></li>'
        b += "</ol></section>"
        b += f'<section class="block"><h2>Sources</h2><ul class="sources">' + "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener noreferrer">{E(t)}</a></li>' for t, u in c["sources"]) + "</ul></section>"
        b += f'<section class="block"><h2>{T("Autres études de cas", "More case studies")}</h2>{link_rows(r, [x for x in CASES if x is not c][:3])}</section>'
        page(c["path"], (f'{c["short"][0]} | FZ Consultation', f'{c["short"][1]} | FZ Consultation'), c["summary"], b)
    path = "case-studies/index.html"
    b = page_hero("../", [(path, OTHER[path])], OTHER[path], ("Leçons tirées d'incidents publics", "Lessons from public incidents"),
        ("Des incidents réels et documentés en finance, en énergie et dans le commerce de détail, et ce qu'ils enseignent sur la résilience.", "Real, documented incidents in finance, energy and retail, and what they teach about resilience."))
    b += f'<section class="block">{case_cards("../")}<p class="note">{T("Analyses fondées uniquement sur des informations publiques, avec sources. FZ Consultation n&#39;a participé à aucun de ces incidents et n&#39;a aucun lien avec les organisations mentionnées.", "Analyses based solely on public information, with sources. FZ Consultation was not involved in any of these incidents and has no affiliation with the organizations named.")}</p></section>'
    b += quiz_band("../")
    page(path, ("Études de cas | FZ Consultation", "Case studies | FZ Consultation"), ("Leçons tirées d'incidents publics.", "Lessons from public incidents."), b)

    # what we do hub
    path = "what-we-do/index.html"; r = "../"
    b = f'''<section class="phero">
      {crumbs(r, [(path, OTHER[path])])}
      <p class="eyebrow">{T("Ce que nous faisons", "What we do")}</p>
      <h1>{T("Résilience d'affaires, de la stratégie à la preuve", "Business resilience, from strategy to proof")}</h1>
      <p class="lede">{T("Nous aidons les organisations à identifier ce qui compte, à se préparer aux interruptions et à démontrer qu'elles peuvent s'en remettre.", "We help organizations identify what matters, prepare for disruption and prove they can recover from it.")}</p>
    </section>
    <section class="block"><h2>{T("Des capacités pour chaque étape", "Capabilities for every stage")}</h2>
    <div class="pillars">
      <a href="{r}what-we-do/expertise/index.html"><span class="pk">01</span><h3>{T("Notre expertise", "Our expertise")}</h3>{T("Continuité, reprise après sinistre, cybersécurité et résilience infonuagique.", "Continuity, disaster recovery, cybersecurity and cloud resilience.", tag="p")}<span class="more">{T("Explorer l'expertise", "Explore expertise")} {ARROW}</span></a>
      <a href="{r}what-we-do/methodology.html"><span class="pk">02</span><h3>{T("Notre méthodologie", "Our methodology")}</h3>{T("Comprendre, planifier, tester, améliorer : un cycle qui produit des résultats mesurables.", "Understand, plan, test, improve: a cycle that produces measurable results.", tag="p")}<span class="more">{T("Découvrir la méthodologie", "See the methodology")} {ARROW}</span></a>
      <a href="{r}what-we-do/services/index.html"><span class="pk">03</span><h3>{T("Nos services", "Our services")}</h3>{T("Évaluations, planification, exercices et accompagnement continu.", "Assessments, planning, exercises and ongoing advisory.", tag="p")}<span class="more">{T("Voir les services", "See services")} {ARROW}</span></a>
    </div></section>
    <section class="block split"><div><h2>{T("Indépendants, par principe", "Independent by design")}</h2></div><div>{T("Nous ne revendons ni logiciels ni matériel. Chaque recommandation part de vos besoins, pas du catalogue d'un fournisseur. Vous gardez la liberté de choisir vos outils et de changer d'avis.", "We resell no software or hardware. Every recommendation starts from your needs, not a vendor's catalogue. You stay free to choose your tools and to change your mind.", tag="p", cls="big")}</div></section>
    <section class="block"><h2>{T("Secteurs que nous accompagnons", "Industries we support")}</h2>
      <ul class="tags">{"".join(f'<li><a href="{r}{p["path"]}">{P(p["short"])}</a></li>' for p in IND)}</ul>
      <p><a class="textlink" href="{r}what-we-do/industries.html">{T("Voir tous les secteurs", "View all industries")} {ARROW}</a></p>
    </section>
    <section class="block"><h2>{T("Quatre marchés, deux langues", "Four markets, two languages")}</h2>
      {T("Europe, Royaume-Uni, Canada et États-Unis. Nous alignons nos travaux sur DORA, NIS2, les règles FCA/PRA, les lignes directrices du BSIF, NIST et SOC 2.", "Europe, the UK, Canada and the United States. We align our work with DORA, NIS2, FCA/PRA rules, OSFI guidelines, NIST and SOC 2.", tag="p", cls="intro")}
      <p><a class="textlink" href="{r}what-we-do/regulations.html">{T("Réglementation par région", "Regulations by region")} {ARROW}</a></p>
    </section>
    {ai_band(r)}
    <section class="block"><h2>{T("Leçons tirées d'incidents publics", "Lessons from public incidents")}</h2>{case_cards(r)}</section>
    {quiz_band(r)}
    {faq(HUB_FAQ, ("Vous avez des questions ? Nous avons des réponses.", "Still have questions? We have answers."))}'''
    page(path, ("Ce que nous faisons | FZ Consultation", "What we do | FZ Consultation"),
         ("Expertise, méthodologie et services en résilience d'affaires, sécurité et reprise après sinistre.", "Expertise, methodology and services in business resilience, security and disaster recovery."), b)

    # contact
    path = "contact.html"; r = ""
    book = (f'<a class="btn primary" href="{E(BOOKING_URL)}" target="_blank" rel="noopener">{T("Choisir un créneau", "Pick a time")}</a>' if BOOKING_URL
            else f'<p class="muted">{T("Proposez-nous quelques créneaux dans votre message et nous vous confirmerons un horaire.", "Suggest a few time slots in your message and we will confirm one.")}</p>')
    subjects = [("Premier échange", "Intro call"), ("Évaluation", "Assessment"), ("Reprise après sinistre", "Disaster recovery"), ("Cybersécurité", "Cybersecurity"), ("Exercice ou test", "Exercise or test"), ("Intelligence artificielle", "Artificial intelligence"), ("Partenariat", "Partnership"), ("Autre", "Other")]
    b = page_hero(r, [(path, OTHER[path])], ("Contact", "Contact"), ("Parlons de votre situation", "Let's talk about your situation"),
        ("Un premier échange de 30 minutes, sans engagement, en français ou en anglais.", "A free 30-minute intro call, in French or English."))
    b += f'''<section class="block contact-grid">
      <div class="side">
        <h2>{T("Réserver un appel", "Book a call")}</h2>{book}
        <h2>{T("Par courriel", "By email")}</h2><p><a class="textlink" href="mailto:{EMAIL}">{EMAIL}</a></p>
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
          <label>{T("Sujet", "Topic")}<select name="topic">{"".join(f"<option>{P(s)}</option>" for s in subjects)}</select></label>
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
        "questions": [{"d": d, "q": P(q), "rec": P(rec)} for d, q, rec in QUIZ],
        "ui": QUIZ_UI[LANG],
    }
    b = page_hero(r, [(path, OTHER[path])], ("Gratuit · 5 minutes", "Free · 5 minutes"), ("Auto-évaluation de la résilience", "Resilience self-assessment"),
        ("Douze questions sur la continuité, la reprise, la sécurité et vos tiers. Vous obtenez un score par domaine et vos trois priorités.", "Twelve questions on continuity, recovery, security and third parties. You get a score by area and your top three priorities."))
    b += f'''<section class="block quiz-wrap">
      <div id="quiz" class="quiz" aria-live="polite"></div>
      <noscript><p>{T("Cette auto-évaluation nécessite JavaScript.", "This self-assessment requires JavaScript.")}</p></noscript>
      <p class="note">{T("Vos réponses sont traitées uniquement dans votre navigateur. Elles ne sont ni envoyées ni enregistrées. Ce résultat est indicatif et ne remplace pas une évaluation complète.", "Your answers are processed only in your browser. They are never sent or stored. This result is indicative and does not replace a full assessment.")}</p>
    </section>'''
    js = f'<script>window.QUIZ={json.dumps(qdata, ensure_ascii=False)};window.QUIZ_ROOT="{r}";</script><script src="{r}../assets/quiz.js?v={VER}"></script>'
    page(path, ("Auto-évaluation de la résilience | FZ Consultation", "Resilience self-assessment | FZ Consultation"),
         ("Évaluez gratuitement la résilience de votre organisation en cinq minutes.", "Assess your organization's resilience in five minutes, for free."), b, extra_js=js)

    build_ai()
    build_partners()

    # privacy
    build_privacy(); build_legal()

    # home
    build_home()

def ai_band(r):
    return f"""<section class="block"><div class="band ai">
      <div><p class="eyebrow">{T("Intelligence artificielle", "Artificial intelligence")}</p>
      <h2>{T("Adopter l'IA vite, sans perdre le contrôle", "Adopt AI fast, without losing control")}</h2>
      {T("Vision, agents, gouvernance et plateforme Microsoft Foundry Citadel : nous appliquons à l'IA la même exigence de résilience.", "Vision, agents, governance and the Microsoft Foundry Citadel platform: we apply the same resilience discipline to AI.", tag="p")}</div>
      <a class="btn primary" href="{r}ai/index.html">{T("Découvrir notre offre IA", "Explore our AI services")}</a>
    </div></section>"""

def build_ai():
    WWD = ("ai/index.html", OTHER["ai/index.html"])
    # detail pages
    for p in AI_PAGES:
        r = rprefix(p["path"])
        b = page_hero(r, [WWD, (p["path"], p["short"])], ("IA", "AI"), p["title"], p["lede"])
        b += f'<section class="block split"><div><h2>{T("Ce que nous couvrons", "What we cover")}</h2>{P(p["intro"], tag="p", cls="intro")}</div><div class="cover">'
        b += "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in p["cover"]) + "</div></section>"
        b += f'<section class="block split"><div><h2>{T("Ce que vous recevez", "What you get")}</h2></div><ul class="checks">' + "".join(f'<li>{P(d)}</li>' for d in p["deliverables"]) + "</ul></section>"
        b += faq(p["faq"])
        b += f'<section class="block"><h2>{T("À voir aussi", "Related")}</h2>{link_rows(r, [item_of(k) for k in p["related"]])}</section>'
        page(p["path"], (f'{p["title"][0]} | FZ Consultation', f'{p["title"][1]} | FZ Consultation'), p["summary"], b)
    # citadel
    c = CITADEL; r = "../"
    b = page_hero(r, [WWD, (c["path"], c["short"])], ("IA · Plateforme", "AI · Platform"), c["title"], c["lede"])
    b += f'<section class="block split"><div><h2>{T("Qu&#39;est-ce que Citadel ?", "What is Citadel?")}</h2></div>{P(c["what"], tag="p", cls="big")}</section>'
    b += f'<section class="block"><h2>{T("Quatre couches de gouvernance", "Four layers of governance")}</h2><ol class="layers">' + "".join(f'<li><span class="lnum">{i}</span><div><h3>{P(h)}</h3>{P(d, tag="p")}</div></li>' for i, (h, d) in enumerate(c["layers"], 1)) + "</ol></section>"
    b += f'<section class="block"><h2>{T("Pourquoi c&#39;est utile", "Why it matters")}</h2><div class="cover grid2">' + "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in c["why"]) + "</div></section>"
    b += f'<section class="block"><h2>{T("Notre accompagnement Citadel", "How we help with Citadel")}</h2><ol class="phases">' + "".join(f'<li><div class="pn">{i:02d}</div><div><h3>{P(h)}</h3>{P(d, tag="p")}</div></li>' for i, (h, d) in enumerate(c["our"], 1)) + "</ol>"
    b += f'<p style="margin-top:28px"><a class="btn primary" href="{r}ai/vision-questionnaire.html">{T("Commencer par le questionnaire de vision", "Start with the vision questionnaire")}</a></p></section>'
    b += f'<section class="block"><h2>Sources</h2><ul class="sources">' + "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener noreferrer">{E(t)}</a></li>' for t, u in c["sources"]) + f'</ul>{P(c["note"], tag="p", cls="note")}</section>'
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
    js = f'<script>window.VISION={json.dumps(data, ensure_ascii=False)};window.VISION_ROOT="{r}";</script><script src="{r}../assets/vision.js?v={VER}"></script>'
    page(path, ("Questionnaire de vision IA | FZ Consultation", "AI vision questionnaire | FZ Consultation"), ("Formulez votre vision de l'IA et mesurez votre maturité.", "Frame your AI vision and measure your readiness."), b, extra_js=js)
    # hub
    path = "ai/index.html"; r = "../"
    b = f"""<section class="phero">{crumbs(r, [(path, OTHER[path])])}
      <p class="eyebrow">{T("Intelligence artificielle", "Artificial intelligence")}</p>
      <h1>{T("Adopter l&#39;IA vite, sans perdre le contrôle", "Adopt AI fast, without losing control")}</h1>
      <p class="lede">{T("De la vision à la production : stratégie, agents, gouvernance et plateforme, avec la même exigence de résilience que pour vos systèmes critiques.", "From vision to production: strategy, agents, governance and platform, with the same resilience discipline as your critical systems.")}</p>
      <div class="actions"><a class="btn primary" href="{r}ai/vision-questionnaire.html">{T("Faire le questionnaire de vision", "Take the vision questionnaire")}</a><a class="btn ghost" href="{r}ai/citadel.html">Microsoft Foundry Citadel</a></div>
    </section>
    <section class="block"><h2>{T("Nos services IA", "Our AI services")}</h2>{link_rows(r, AI_PAGES + [CITADEL])}</section>
    <section class="block"><h2>{T("Notre démarche", "Our approach")}</h2><ol class="phases">
      <li><div class="pn">01</div><div><h3>{T("Aligner", "Align")}</h3>{T("Questionnaire de vision, puis atelier avec la direction pour fixer objectifs, limites et priorités.", "Vision questionnaire, then a leadership workshop to set goals, limits and priorities.", tag="p")}</div></li>
      <li><div class="pn">02</div><div><h3>{T("Encadrer", "Govern")}</h3>{T("Politique, inventaire, classification des risques et plateforme gouvernée comme Citadel.", "Policy, inventory, risk classification and a governed platform such as Citadel.", tag="p")}</div></li>
      <li><div class="pn">03</div><div><h3>{T("Construire", "Build")}</h3>{T("Premiers agents conçus, évalués et mis en production avec supervision humaine.", "First agents designed, evaluated and put into production with human oversight.", tag="p")}</div></li>
      <li><div class="pn">04</div><div><h3>{T("Déployer à l&#39;échelle", "Scale")}</h3>{T("Formation, mesure de la valeur, résilience de la plateforme et extension à d&#39;autres équipes.", "Training, value measurement, platform resilience and roll-out to more teams.", tag="p")}</div></li>
    </ol></section>
    <section class="block split"><div><h2>{T("Pourquoi un cabinet de résilience ?", "Why a resilience firm?")}</h2></div>{T("Les agents IA deviennent des systèmes critiques : ils ont des accès, prennent des décisions et peuvent tomber en panne. Nous les traitons comme tels, avec identités, limites, supervision et plan de reprise dès la conception.", "AI agents are becoming critical systems: they have access, make decisions and can fail. We treat them that way, with identity, limits, monitoring and a recovery plan from the start.", tag="p", cls="big")}</section>"""
    page(path, ("Intelligence artificielle | FZ Consultation", "Artificial intelligence | FZ Consultation"), ("Stratégie IA, agents, gouvernance et Microsoft Foundry Citadel.", "AI strategy, agents, governance and Microsoft Foundry Citadel."), b)

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

def TODO(fr, en): return f'<mark class="todo">[{T("À compléter", "To complete")} : {T(fr, en)}]</mark>' if LANG == "fr" else f'<mark class="todo">[To complete: {en}]</mark>'

def build_privacy():
    path = "privacy.html"; r = ""
    S = []
    S.append((("Qui sommes-nous", "Who we are"),
      T(f"Le responsable du traitement est FZ Consultation. Pour toute question sur vos renseignements personnels, écrivez à <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. ",
        f"The data controller is FZ Consultation. For any question about your personal information, email <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. ") +
      T("La personne responsable de la protection des renseignements personnels est : ", "The person in charge of the protection of personal information is: ") +
      TODO("titre de la personne responsable, par ex. « Directeur général »", "title of the person in charge, e.g. “Managing Director”") + "."))
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
      (T("Préférence de langue", "Language preference"), T("Votre choix de langue est conservé dans le stockage local de votre navigateur. Nous n'utilisons aucun cookie.", "Your language choice is kept in your browser's local storage. We use no cookies.")),
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
      f"<p>FZ Consultation — {TODO('forme juridique', 'legal form')}<br>{TODO('adresse postale', 'postal address')}<br>{TODO('numéro d’immatriculation (SIREN/RCS ou NEQ)', 'registration number (e.g. SIREN/RCS, NEQ or Companies House)')}<br>{T('Courriel', 'Email')} : <a href=\"mailto:{EMAIL}\">{EMAIL}</a></p>"),
     (("Directeur de la publication", "Publication director"), f"<p>{TODO('nom du directeur de la publication', 'name of the publication director')}</p>"),
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

def build_home():
    main = open(os.path.join(HERE, "home_main.html")).read()
    main = re.sub(r'<div class="portrait"><img src="data:[^"]+"', '<div class="portrait"><img src="../assets/logo.webp"', main)
    main = re.sub(r'\s*<section class="block" id="contact".*?</section>', "", main, flags=re.S)
    main = main.replace('<div class="wrap">', "", 1).rstrip()
    if main.endswith("</div>"): main = main[:-6]
    main = strip_other(main)
    links = {("Évaluation de la résilience", "Resilience assessment"): "what-we-do/services/assessments.html",
             ("Plan de reprise après sinistre", "Disaster recovery planning"): "what-we-do/expertise/disaster-recovery.html",
             ("Tests et exercices", "Testing and exercises"): "what-we-do/services/exercises.html",
             ("Bonnes pratiques de sécurité", "Security best practices"): "what-we-do/expertise/cybersecurity.html"}
    for pair, key in links.items():
        t = P(pair)
        pat = re.compile(r'(<h3><span>' + re.escape(t) + r'</span></h3>.*?</ul>)', re.S)
        main = pat.sub(lambda m: m.group(1) + f'\n          <a class="textlink" href="{key}">{T("En savoir plus", "Learn more")} {ARROW}</a>', main, count=1)
    main = main.replace('href="#contact"', 'href="contact.html"')
    main = main.replace('<a class="btn ghost" href="#services">', '<a class="btn ghost" href="what-we-do/index.html">')
    main = main.replace(f'<span>{T("Voir les services", "See services")}</span>', f'<span>{T("Ce que nous faisons", "What we do")}</span>')
    main = main.replace('</ol>\n    </section>', f'</ol>\n      <p style="margin-top:40px"><a class="textlink" href="what-we-do/methodology.html">{T("Découvrir la méthodologie", "See the methodology")} {ARROW}</a></p>\n    </section>', 1)
    main = main.replace('<p class="note">', f'<p style="margin-top:24px"><a class="textlink" href="what-we-do/regulations.html">{T("Réglementation par région", "Regulations by region")} {ARROW}</a></p>\n      <p class="note">', 1)
    main = main.replace(f'<h2><span>Services</span></h2>', f'<h2><span>{T("Ce que nous faisons", "What we do")}</span></h2>', 1)
    main = main.replace('<section class="block" id="approche">', ai_band("") + quiz_band("") + '\n    <section class="block" id="approche">', 1)
    page("index.html", ("FZ Consultation — Résilience, sécurité et reprise après sinistre", "FZ Consultation — Business resilience, security and disaster recovery"),
         ("FZ Consultation aide les organisations à se préparer aux pannes, cyberattaques et sinistres, et à reprendre leurs activités dans les délais que l'entreprise peut se permettre.",
          "FZ Consultation helps organizations prepare for outages, cyberattacks and disasters, and recover within the time the business can afford."), main)

REG = [
 (("Union européenne", "European Union"), [
   ("DORA", ("Règlement sur la résilience opérationnelle numérique du secteur financier, en application depuis janvier 2025 : gestion des risques TIC, tests, incidents et prestataires tiers.", "Digital Operational Resilience Act for the financial sector, applicable since January 2025: ICT risk management, testing, incidents and third-party providers.")),
   ("NIS2", ("Directive sur la cybersécurité des entités essentielles et importantes, transposée dans le droit de chaque État membre.", "Directive on cybersecurity for essential and important entities, transposed into each member state's law.")),
   ("ISO 22301 · ISO/IEC 27001", ("Normes internationales de continuité des activités et de sécurité de l'information.", "International standards for business continuity and information security."))]),
 (("Royaume-Uni", "United Kingdom"), [
   ("FCA / PRA", ("Règles de résilience opérationnelle : services d'affaires importants, seuils de tolérance d'impact et scénarios de test.", "Operational resilience rules: important business services, impact tolerances and scenario testing.")),
   ("Cyber Essentials", ("Programme gouvernemental de mesures de sécurité de base, souvent exigé dans les marchés publics.", "Government-backed scheme for baseline security controls, often required in public contracts."))]),
 (("Canada", "Canada"), [
   ("BSIF / OSFI B-13", ("Ligne directrice sur la gestion des risques liés aux technologies et au cyberrisque.", "Guideline on technology and cyber risk management.")),
   ("BSIF / OSFI E-21", ("Ligne directrice sur la résilience opérationnelle et la gestion du risque opérationnel.", "Guideline on operational resilience and operational risk management.")),
   (("Loi 25 (Québec)", "Law 25 (Quebec)"), ("Protection des renseignements personnels, y compris la gestion et la déclaration des incidents de confidentialité.", "Personal information protection, including handling and reporting of privacy incidents."))]),
 (("États-Unis", "United States"), [
   ("NIST CSF 2.0", ("Cadre de cybersécurité de référence : gouverner, identifier, protéger, détecter, répondre, rétablir.", "Reference cybersecurity framework: govern, identify, protect, detect, respond, recover.")),
   ("NIST SP 800-34", ("Guide de planification de la contingence des systèmes d'information.", "Contingency planning guide for information systems.")),
   ("SOC 2", ("Rapport d'assurance sur les contrôles, souvent demandé par les clients des entreprises SaaS.", "Assurance report on controls, often requested by customers of SaaS companies."))]),
]

def root_files():
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
<script>(function(){{var l=null;try{{l=localStorage.getItem("fz-lang")}}catch(e){{}}if(l!=="fr"&&l!=="en")l=(navigator.language||"fr").toLowerCase().indexOf("fr")===0?"fr":"en";location.replace(l+"/"+location.search+location.hash)}})();</script>
<style>body{{font-family:system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0;background:#EEF1F3;color:#16222E}}a{{color:#0052B2;font-weight:700;margin:0 12px}}</style>
</head>
<body><p><a href="fr/">Français</a> · <a href="en/">English</a></p></body>
</html>
''')
    open(os.path.join(OUT, "404.html"), "w").write('''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
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

if __name__ == "__main__":
    import hashlib
    h = hashlib.md5()
    for f in ("site.css", "site.js", "quiz.js", "vision.js"):
        h.update(open(os.path.join(OUT, "assets", f), "rb").read())
    VER = h.hexdigest()[:8]
    for d in LANGS:
        shutil.rmtree(os.path.join(OUT, d), ignore_errors=True)
    for LANG in LANGS:
        build_lang()
    root_files()
    print("built", len(PAGES), "pages x", len(LANGS), "languages ->", os.path.abspath(OUT))
