"""Consolidated site structure: What we do, Sectors, AI hub, Resources hub, case studies, home,
contextual calls to action, redirect stubs. Called from build.py with the build module as `B`."""
import os, re, html
from newsite_content import *
from cases_extra import CASE_EXTRA, NEW_CASES
from content import EXPERTISE, SERVICES, HUB_FAQ
from notes import SERIES, SERIES_BLURB

CASE_ORDER = ["aws-us-east-1-2025", "jaguar-land-rover-2025", "collins-aerospace-2025", "marks-and-spencer-2025",
              "change-healthcare-2024", "crowdstrike-delta-2024", "colonial-pipeline-2021", "norsk-hydro-2019", "tsb-2018"]
CASE_YEAR = {"aws-us-east-1-2025": 2025, "jaguar-land-rover-2025": 2025, "collins-aerospace-2025": 2025, "marks-and-spencer-2025": 2025,
             "change-healthcare-2024": 2024, "crowdstrike-delta-2024": 2024, "colonial-pipeline-2021": 2021, "norsk-hydro-2019": 2019, "tsb-2018": 2018}

def slug(c): return c["path"].split("/")[-1][:-5]

def prepare_cases(B):
    """Add the new cases and the one-line takeaways, and put the cases in display order (newest first)."""
    existing = {slug(c) for c in B.CASES}
    for c in NEW_CASES:
        if slug(c) not in existing: B.CASES.append(c)
    for c in B.CASES:
        x = CASE_EXTRA[slug(c)]
        c["line"], c["monday"], c["tool"] = x["line"], x["monday"], x["tool"]
    B.CASES.sort(key=lambda c: CASE_ORDER.index(slug(c)))

# ---------------------------------------------------------------- labels and links
def label(B, key):
    new = REMAP.get(key)
    if new in ANCHOR_NAMES: return ANCHOR_NAMES[new]
    return B.name_of(key)

def case_by_slug(B, s): return next(c for c in B.CASES if slug(c) == s)

def book_href(B): return B.BOOKING_URL or "contact.html"

def btn(B, r, label_pair, key, cls):
    T, P, E = B.T, B.P, B.E
    if key == "@book":
        if B.BOOKING_URL: return f'<a class="btn {cls}" href="{E(B.BOOKING_URL)}" target="_blank" rel="noopener">{P(label_pair)}</a>'
        key = "contact.html"
    return f'<a class="btn {cls}" href="{r}{key}">{P(label_pair)}</a>'

def ctx_cta(B, r, path):
    """A slim, page-specific call to action instead of the same form on every page."""
    T, P = B.T, B.P
    entry = None
    for key, val in CTX:
        if path == key or (not key.endswith(".html") and path.startswith(key)):
            entry = val; break
    else:
        entry = CTX_DEFAULT
    if entry == "@default": entry = CTX_DEFAULT
    if entry == "@case":
        c = next((c for c in B.CASES if c["path"] == path), None)
        if not c: return ""
        tool_key, tool_label = c["tool"]
        entry = (("Faites le test de lundi sur vos propres chiffres", "Run Monday's check on your own numbers"),
                 ("Les trois vérifications ci-dessus prennent moins d'une heure. Si l'une d'elles échoue, parlons-en.", "The three checks above take under an hour. If one of them fails, let's talk."),
                 [(tool_label, tool_key), (CTX_BOOK, "@book")])
    if entry is None: return ""
    h, p, buttons = entry
    acts = "".join(btn(B, r, lab, key, "primary" if i == 0 else "ghost") for i, (lab, key) in enumerate(buttons))
    return f'''<section class="block" id="next" style="border-top:0;padding-top:24px" data-pagefind-ignore>
      <aside class="ctx" aria-labelledby="ctx-h"><div><h2 id="ctx-h">{P(h)}</h2><p>{P(p)}</p></div><div class="cta-actions">{acts}</div></aside>
    </section>'''

# ---------------------------------------------------------------- nav and footer
def nav_wwd(B):
    return [{"path": f"what-we-do/index.html#{o['id']}", "short": o["name"]} for o in OUTCOMES]

def nav_ind(B):
    feat = [p for p in B.IND if p["path"].split("/")[-1][:-5] in FEATURED_IND]
    return feat + [{"path": "what-we-do/industries.html", "short": ("Tous les secteurs", "All sectors")}]

def footer_html(B, r):
    T, P = B.T, B.P
    li = lambda key, pair: f'<li><a href="{r}{key}">{P(pair)}</a></li>'
    col = lambda title, items: f'<div><h2 class="fh">{P(title)}</h2><ul>{"".join(items)}</ul></div>'
    wwd = col(("Ce que nous faisons", "What we do"), [li(f"what-we-do/index.html#{o['id']}", o["name"]) for o in OUTCOMES] + [li("what-we-do/methodology.html", B.OTHER["what-we-do/methodology.html"])])
    sectors = col(("Secteurs", "Sectors"), [li(p["path"], p["short"]) for p in nav_ind(B)[:-1]] + [li("what-we-do/industries.html", ("Tous les secteurs", "All sectors")), li("what-we-do/regulations.html", B.OTHER["what-we-do/regulations.html"])])
    ai = col(("IA", "AI"), [li("ai/index.html", ("Vue d'ensemble", "Overview")), li("ai/auditor.html", B.AUDITOR["short"]), li("ai/citadel.html", B.CITADEL["short"]), li("ai/vision-questionnaire.html", B.OTHER["ai/vision-questionnaire.html"])])
    learn = col(("Apprendre", "Learn"), [li(k, B.OTHER[k]) for k in ["case-studies/index.html", "insights/index.html", "resources/index.html", "resources/downtime-calculator.html", "resources/glossary.html", "self-assessment.html"]])
    us = col(("FZ Consultation", "FZ Consultation"), [li("contact.html", B.OTHER["contact.html"]), li("partners.html", B.OTHER["partners.html"]), li("search.html", B.OTHER["search.html"])])
    return f'''<footer class="site">
  <div class="wrap fgrid">
    <div class="fbrand">
      <img src="{r}../assets/logo.webp" alt="FZ Consultation" width="160" height="120" class="flogo">
      <p>{T("Résilience d'affaires, sécurité et reprise après sinistre.", "Business resilience, security and disaster recovery.")}</p>
      <p><a href="mailto:{B.EMAIL}">{B.EMAIL}</a></p>
    </div>
    {wwd}{sectors}{ai}{learn}{us}
  </div>
  <div class="wrap fbottom">
    <span>© <span class="year">2026</span> FZ Consultation</span>
    <span class="flegal"><a href="{r}privacy.html">{P(B.OTHER["privacy.html"])}</a><a href="{r}legal.html">{P(B.OTHER["legal.html"])}</a><a href="{r}accessibility.html">{P(B.OTHER["accessibility.html"])}</a><a href="{r}security.html">{P(B.OTHER["security.html"])}</a><a href="{r}governance.html">{P(B.OTHER["governance.html"])}</a></span>
    <span>{T("Europe · Royaume-Uni · Canada · États-Unis", "Europe · UK · Canada · United States")}</span>
  </div>
</footer>'''

# ---------------------------------------------------------------- case cards and pages
def case_cards2(B, r, items=None):
    P, T, ARROW = B.P, B.T, B.ARROW
    out = '<div class="cases">'
    for c in (items or B.CASES):
        out += (f'<a href="{r}{c["path"]}" data-sector="{c["sector"][1].lower()}"><span class="pk">{P(c["sector"])}<span class="yr">· {CASE_YEAR[slug(c)]}</span></span>'
                f'<h3>{P(c["short"])}</h3><span class="line">{P(c["line"])}</span><span class="more">{T("Lire l&#39;analyse et la vérification du lundi", "Read the analysis and the Monday check")} {ARROW}</span></a>')
    return out + "</div>"

def build_cases(B):
    T, P, E, ARROW = B.T, B.P, B.E, B.ARROW
    DISC = ("Analyse fondée uniquement sur des informations publiques. FZ Consultation n'a pas participé à cet incident et n'a aucun lien avec les organisations mentionnées.",
            "Analysis based solely on public information. FZ Consultation was not involved in this incident and has no affiliation with the organizations named.")
    for c in B.CASES:
        r = "../"
        b = B.page_hero(r, [("case-studies/index.html", B.OTHER["case-studies/index.html"]), (c["path"], c["sector"])],
                        (T("Étude de cas · ", "Case study · ") + c["sector"][0], T("Étude de cas · ", "Case study · ") + c["sector"][1]), c["short"], c["summary"])
        b += f'<section class="block" style="border-top:0;padding-top:0"><p class="takeaway"><span>{T("En une phrase", "In one sentence")}</span>{P(c["line"])}</p></section>'
        b += '<section class="facts"><dl>' + "".join(f"<div><dt>{P(k)}</dt><dd>{P(v)}</dd></div>" for k, v in c["facts"]) + "</dl>"
        b += f'<p class="disclaimer">{P(DISC)}</p></section>'
        b += f'<section class="block split"><div><h2>{T("Ce qui s&#39;est passé", "What happened")}</h2></div><ol class="timeline-list">'
        b += "".join(f'<li><span class="when">{P(w)}</span>{P(d, tag="p")}</li>' for w, d in c["timeline"]) + "</ol></section>"
        b += f'<section class="block split"><div><h2>{T("Ce qui a mal tourné", "What went wrong")}</h2>{T("D&#39;après les sources publiques citées plus bas.", "According to the public sources listed below.", tag="p", cls="intro")}</div><div class="cover">'
        b += "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in c["wrong"]) + "</div></section>"
        b += f'<section class="block"><h2>{T("Les leçons pour votre organisation", "Lessons for your organization")}</h2><ol class="lessons">'
        for i, (h, d, link) in enumerate(c["lessons"], 1):
            b += f'<li><span class="ln">{i}</span><div><h3>{P(h)}</h3>{P(d, tag="p")}<a class="textlink" href="{r}{link}">{P(label(B, link))} {ARROW}</a></div></li>'
        b += "</ol></section>"
        tool_key, tool_label = c["tool"]
        b += f'''<section class="block"><div class="monday"><h2>{T("À vérifier lundi matin", "Check on Monday morning")}</h2>
          {T("Trois questions à poser à votre propre organisation cette semaine. Si vous ne pouvez pas répondre à l&#39;une d&#39;elles en cinq minutes, c&#39;est votre première tâche.", "Three questions to put to your own organization this week. If you cannot answer one of them in five minutes, that is your first task.", tag="p", cls="intro")}
          <ol class="mchecks">{"".join(f"<li><span>{P(m)}</span></li>" for m in c["monday"])}</ol>
          <a class="btn primary" href="{r}{tool_key}">{P(tool_label)}</a></div></section>'''
        b += f'<section class="block"><h2>Sources</h2><ul class="sources">' + "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener noreferrer"{B.SRCLANG()}>{E(t)}</a></li>' for t, u in c["sources"]) + "</ul></section>"
        others = [x for x in B.CASES if x is not c][:3]
        b += f'<section class="block"><h2>{T("Autres études de cas", "More case studies")}</h2>{B.link_rows(r, others)}</section>'
        B.page(c["path"], (f'{c["short"][0]} | FZ Consultation', f'{c["short"][1]} | FZ Consultation'), c["summary"], b)
    path = "case-studies/index.html"
    n = len(B.CASES)
    b = B.page_hero("../", [(path, B.OTHER[path])], B.OTHER[path], ("Neuf incidents réels, lus pour ce que vous vérifieriez lundi matin", "Nine real incidents, read for what you would check on Monday morning") if n == 9 else ("Des incidents réels, lus pour ce que vous vérifieriez lundi matin", "Real incidents, read for what you would check on Monday morning"),
        ("Chaque étude s'appuie uniquement sur des sources publiques, se résume en une phrase et se termine par trois vérifications concrètes. Ce ne sont pas des histoires de malchance : ce sont des défaillances que vous pouvez tester chez vous.",
         "Each study rests only on public sources, boils down to one sentence and ends with three concrete checks. These are not stories of bad luck: they are failures you can test for in your own organization."))
    sectors = []
    for c in B.CASES:
        if c["sector"][1].lower() not in [s_[0] for s_ in sectors]: sectors.append((c["sector"][1].lower(), c["sector"]))
    chips = f'<div class="chips" role="group" aria-label="{T("Filtrer par secteur", "Filter by sector")}"><button type="button" class="chip" data-filter="all" aria-pressed="true">{T("Tous", "All")}</button>' + "".join(f'<button type="button" class="chip" data-filter="{k}" aria-pressed="false">{P(v)}</button>' for k, v in sectors) + f'</div><p class="muted chip-status" role="status" aria-live="polite" data-one="{T("1 étude affichée", "1 study shown")}" data-many="{T("{n} études affichées", "{n} studies shown")}"></p>'
    b += f'<section class="block"><h2 class="sr-only">{T("Toutes les études de cas", "All case studies")}</h2>{chips}{case_cards2(B, "../")}<p class="note">{T("Analyses fondées uniquement sur des informations publiques, avec sources. FZ Consultation n&#39;a participé à aucun de ces incidents et n&#39;a aucun lien avec les organisations mentionnées.", "Analyses based solely on public information, with sources. FZ Consultation was not involved in any of these incidents and has no affiliation with the organizations named.")}</p><p><a class="textlink" href="../resources/downtime-calculator.html#benchmarks">{T("Ce que coûte une heure d&#39;interruption", "What an hour of downtime costs")} {ARROW}</a></p></section>'
    latest = latest_note(B)
    if latest:
        b += f'<section class="block"><div class="series"><div><p class="eyebrow">{P(SERIES)}</p><h2>{P(latest["title"])}</h2><p>{P(SERIES_BLURB)}</p></div><a class="btn primary" href="../insights/{latest["slug"]}.html">{T("Lire la note du mois", "Read this month&#39;s note")}</a></div></section>'
    B.page(path, ("Études de cas | FZ Consultation", "Case studies | FZ Consultation"), ("Incidents réels, sources publiques, et trois vérifications à faire lundi matin.", "Real incidents, public sources, and three checks to run on Monday morning."), b)

def latest_note(B):
    notes = sorted([a for a in B.INSIGHTS if a.get("series")], key=lambda a: a["date"], reverse=True)
    return notes[0] if notes else None

# ---------------------------------------------------------------- What we do
def faq_pool(B):
    pool = {}
    for p in list(EXPERTISE) + list(SERVICES):
        for q, a in p["faq"]: pool[q[1]] = (q, a)
    for q, a in HUB_FAQ: pool[q[1]] = (q, a)
    return pool

def build_wwd(B):
    T, P, ARROW = B.T, B.P, B.ARROW
    path = "what-we-do/index.html"; r = "../"
    b = B.page_hero(r, [(path, B.OTHER[path])], B.OTHER[path], WWD_HERO["title"], WWD_HERO["lede"])
    b = b.replace("</section>", f'<ol class="oc-nav" aria-label="{T("Les quatre tâches", "The four jobs")}">' + "".join(
        f'<li><a href="#{o["id"]}"><span class="n">{i:02d}</span>{P(o["name"])}</a></li>' for i, o in enumerate(OUTCOMES, 1)) + "</ol></section>", 1)
    for i, o in enumerate(OUTCOMES, 1):
        b += f'<section class="block outcome" id="{o["id"]}"><div class="oc-head"><span class="oc-n" aria-hidden="true">{i:02d}</span><div><p class="eyebrow">{P(o["name"])}</p><h2>{P(o["title"])}</h2></div></div>'
        b += f'<p class="stance">{P(o["stance"])}</p>'
        if o["id"] == "know":
            phases = [
                (("Entretiens et collecte", "Interviews and discovery"), ("1 à 2 semaines", "1 to 2 weeks"), ("Direction, TI, opérations, fournisseurs", "Leadership, IT, operations, suppliers")),
                (("Analyse", "Analysis"), ("1 semaine", "1 week"), ("Comparaison aux référentiels et à vos cibles", "Comparison to frameworks and your targets")),
                (("Restitution", "Readout"), ("Une demi-journée", "Half a day"), ("Constats et feuille de route pour la direction", "Findings and roadmap for leadership")),
            ]
            b += f'<div class="block" style="border-top:0;padding:0 0 24px">{B.timeline_diagram(phases)}</div>'
        b += '<div class="cover grid2">' + "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in o["do"]) + "</div>"
        b += (f'<div class="oc-foot"><div><h3>{T("Ce que vous recevez", "What you get")}</h3><ul class="checks">' + "".join(f"<li>{P(d)}</li>" for d in o["get"]) + "</ul></div>"
              f'<div><h3>{T("Pour commencer seul", "Start on your own")}</h3><ul class="rows">' + "".join(
                  f'<li><a href="{r}{k}"><span class="rt">{P(lab)}</span>{ARROW}</a></li>' for k, lab in o["start"]) + "</ul></div></div>")
        b += "</section>"
    b += f'<section class="block split"><div><h2>{P(WWD_HOW["title"])}</h2></div>{P(WWD_HOW["big"], tag="p", cls="big")}</section>'
    b += (f'<section class="block"><h2>{T("Aller plus loin", "Go further")}</h2><ul class="rows">'
          f'<li><a href="{r}what-we-do/methodology.html"><span class="rt">{P(B.OTHER["what-we-do/methodology.html"])}</span><span class="rs">{T("Comprendre, planifier, tester, améliorer : le cycle derrière les quatre tâches.", "Understand, plan, test, improve: the cycle behind the four jobs.")}</span>{ARROW}</a></li>'
          f'<li><a href="{r}what-we-do/industries.html"><span class="rt">{P(B.OTHER["what-we-do/industries.html"])}</span><span class="rs">{T("Chaque secteur casse à sa manière.", "Every sector breaks in its own way.")}</span>{ARROW}</a></li>'
          f'<li><a href="{r}what-we-do/regulations.html"><span class="rt">{P(B.OTHER["what-we-do/regulations.html"])}</span><span class="rs">{T("Europe, Royaume-Uni, Canada, États-Unis.", "Europe, UK, Canada, United States.")}</span>{ARROW}</a></li>'
          f'<li><a href="{r}case-studies/index.html"><span class="rt">{P(B.OTHER["case-studies/index.html"])}</span><span class="rs">{T("Des incidents réels et trois vérifications pour lundi matin.", "Real incidents and three checks for Monday morning.")}</span>{ARROW}</a></li></ul></section>')
    pool = faq_pool(B)
    items = [pool[q] for q in WWD_FAQ_QUESTIONS if q in pool]
    b += B.faq(items, ("Questions fréquentes", "Frequently asked questions"))
    B.page(path, ("Ce que nous faisons | FZ Consultation", "What we do | FZ Consultation"),
           ("Savoir, préparer, prouver, rester prêt : les quatre tâches de la résilience d'affaires.", "Know, prepare, prove, stay ready: the four jobs of business resilience."), b)

# ---------------------------------------------------------------- Sectors
def build_sectors(B):
    T, P, ARROW = B.T, B.P, B.ARROW
    WWD = ("what-we-do/index.html", B.OTHER["what-we-do/index.html"])
    path = "what-we-do/industries.html"; r = "../"
    inds = {p["path"].split("/")[-1][:-5]: p for p in B.IND}
    b = B.page_hero(r, [WWD, (path, B.OTHER[path])], B.OTHER[WWD[0]], IND_HUB["title"], IND_HUB["lede"])
    b += f'<section class="block"><h2>{T("En détail", "In depth")}</h2>{B.link_rows(r, [inds[s] for s in FEATURED_IND])}</section>'
    b += f'<section class="block"><h2>{T("En bref", "In brief")}</h2></section>'
    for s in COMPACT_IND:
        p = inds[s]
        b += f'<section class="block ind-compact" id="{s}"><h2>{P(p["short"])}</h2><div class="split" style="border:0;padding:0"><div>{P(p["context"], tag="p", cls="intro")}</div><div class="cover">'
        b += "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in p["risks"][:2]) + "</div></div>"
        b += '<ul class="regtags" style="margin-top:16px">' + "".join(f"<li>{P(x) if isinstance(x, tuple) else x}</li>" for x in p["regs"]) + "</ul>"
        if p["cases"]:
            b += f'<p style="margin-top:16px">' + " &nbsp; ".join(f'<a class="textlink" href="{r}{k}">{P(B.item_of(k)["short"])} {ARROW}</a>' for k in p["cases"][:2]) + "</p>"
        b += "</section>"
    B.page(path, ("Secteurs | FZ Consultation", "Sectors | FZ Consultation"), ("Secteurs que nous accompagnons : trois en détail, cinq en bref.", "Sectors we support: three in depth, five in brief."), b)
    for s in FEATURED_IND:
        ind = inds[s]; ipath = ind["path"]; r = B.rprefix(ipath)
        b = B.page_hero(r, [WWD, (path, B.OTHER[path]), (ipath, ind["short"])], ("Secteur", "Sector"), ind["short"], ind["lede"])
        b += f'<section class="block" style="border-top:0;padding-top:0"><p class="stance">{P(SECTOR_STANCE[s])}</p></section>'
        b += f'<section class="block split"><div><h2>{T("Le contexte", "The context")}</h2>{P(ind["context"], tag="p", cls="intro")}</div><div class="cover">'
        b += "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in ind["risks"]) + "</div></section>"
        b += f'<section class="block split"><div><h2>{T("Référentiels clés", "Key frameworks")}</h2></div><ul class="regtags">' + "".join(f"<li>{P(x) if isinstance(x, tuple) else x}</li>" for x in ind["regs"]) + "</ul></section>"
        if ind["cases"]:
            cs = [case_by_slug(B, k.split("/")[-1][:-5]) for k in ind["cases"]]
            b += f'<section class="block"><h2>{T("À lire en premier", "Read these first")}</h2>{case_cards2(B, r, cs)}</section>'
        others = [inds[x] for x in FEATURED_IND if x != s]
        b += f'<section class="block"><h2>{T("Autres secteurs", "Other sectors")}</h2>{B.link_rows(r, others)}<p><a class="textlink" href="{r}{path}">{T("Tous les secteurs", "All sectors")} {ARROW}</a></p></section>'
        B.page(ipath, (f'{ind["short"][0]} | FZ Consultation', f'{ind["short"][1]} | FZ Consultation'), ind["summary"], b)

# ---------------------------------------------------------------- AI hub
def build_ai_hub(B):
    T, P, E, ARROW = B.T, B.P, B.E, B.ARROW
    path = "ai/index.html"; r = "../"
    b = f"""<section class="phero">{B.crumbs(r, [(path, B.OTHER[path])])}
      <p class="eyebrow">{T("Intelligence artificielle", "Artificial intelligence")}</p>
      <h1>{P(AI_HERO["title"])}</h1>
      <p class="lede">{P(AI_HERO["lede"])}</p>
      <div class="actions"><a class="btn primary" href="{r}ai/auditor.html">FZ AI Auditor</a><a class="btn ghost" href="{r}ai/vision-questionnaire.html">{T("Faire le questionnaire de vision", "Take the vision questionnaire")}</a></div>
    </section>"""
    b += B.auditor_band(r)
    # EU calendar
    b += f'<section class="block" id="eu-ai-act"><h2>{P(AI_EU["title"])}</h2>{P(AI_EU["intro"], tag="p", cls="intro")}<table class="tl-eu"><caption class="sr-only">{P(AI_EU["title"])}</caption><tbody>'
    b += "".join(f'<tr><th scope="row">{P(d)}</th><td>{P(t)}</td></tr>' for d, t in AI_EU["rows"]) + "</tbody></table>"
    b += f'<p class="note">{P(AI_EU["note"])} <a href="{E(AI_EU["src"][1])}" target="_blank" rel="noopener noreferrer"{B.SRCLANG()}>{E(AI_EU["src"][0])}</a></p></section>'
    sections = {p["path"].split("/")[-1][:-5]: p for p in B.AI_PAGES}
    for sid, key in (("strategy", "strategy-adoption"), ("agents", "agents"), ("governance", "governance")):
        p = sections[key]
        b += f'<section class="block outcome" id="{sid}"><h2>{P(p["title"])}</h2><p class="stance">{P(AI_STANCE[sid])}</p>'
        b += f'{P(p["intro"], tag="p", cls="intro")}<div class="cover grid2">' + "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in p["cover"]) + "</div>"
        b += f'<div class="oc-foot"><div><h3>{T("Ce que vous recevez", "What you get")}</h3><ul class="checks">' + "".join(f"<li>{P(d)}</li>" for d in p["deliverables"]) + "</ul></div><div></div></div></section>"
    b += f'<section class="block"><h2>{T("Plateforme et alignement", "Platform and alignment")}</h2>{B.link_rows(r, [B.CITADEL, {"path": "ai/vision-questionnaire.html", "short": B.OTHER["ai/vision-questionnaire.html"], "summary": ("Treize questions pour aligner la direction sur la vision de l\'IA.", "Thirteen questions to align leadership on the AI vision.")}])}</section>'
    b += f'<section class="block split"><div><h2>{T("Pourquoi un cabinet de résilience ?", "Why a resilience firm?")}</h2></div>{T("Les agents IA deviennent des systèmes critiques : ils ont des accès, prennent des décisions et peuvent tomber en panne. Nous les traitons comme tels, avec identités, limites, supervision et plan de reprise dès la conception.", "AI agents are becoming critical systems: they have access, make decisions and can fail. We treat them that way, with identity, limits, monitoring and a recovery plan from the start.", tag="p", cls="big")}</section>'
    faqs = [q for p in B.AI_PAGES for q in p["faq"]]
    b += B.faq(faqs)
    B.page(path, ("Intelligence artificielle | FZ Consultation", "Artificial intelligence | FZ Consultation"), ("Audit d'agents IA, stratégie, agents, gouvernance et Microsoft Foundry Citadel.", "AI agent audit, strategy, agents, governance and Microsoft Foundry Citadel."), b)

# ---------------------------------------------------------------- Resources hub
def tpl_inside(B, t):
    """A short 'what is inside' list drawn from the template's own data."""
    i = B.I()
    if "phases" in t: return [p[0][i] for p in t["phases"]]
    if "columns" in t: return [c[i] for c in t["columns"]][:8]
    if "sections" in t: return [h[i] for h, _ in t["sections"]]
    return []

def build_resources_hub(B):
    import extras
    T, P, E, ARROW = B.T, B.P, B.E, B.ARROW
    path = "resources/index.html"; r = B.rprefix(path)
    b = B.page_hero(r, [(path, B.OTHER[path])], ("Ressources", "Resources"), ("Outils, modèles et lectures", "Tools, templates and reading"),
        ("Des outils gratuits, des modèles à télécharger et des notes pour avancer sur la résilience, même avant de nous appeler.", "Free tools, downloadable templates and notes to make progress on resilience, even before you call us."))
    tools = [
      {"path": "self-assessment.html", "short": ("Auto-évaluation de la résilience", "Resilience self-assessment"), "summary": ("Vingt questions pondérées, un score par domaine et vos priorités.", "Twenty weighted questions, a score by area and your priorities.")},
      {"path": "resources/downtime-calculator.html", "short": B.OTHER["resources/downtime-calculator.html"], "summary": ("Estimez le coût d'un incident, puis comparez avec les repères publics par secteur.", "Estimate the cost of an incident, then compare it with public benchmarks by industry.")},
      {"path": "ai/vision-questionnaire.html", "short": B.OTHER["ai/vision-questionnaire.html"], "summary": ("Treize questions pour aligner votre direction sur votre vision de l'IA.", "Thirteen questions to align your leadership on your AI vision.")},
    ]
    b += f'<section class="block"><h2>{T("Outils interactifs", "Interactive tools")}</h2>{B.link_rows(r, tools)}</section>'
    b += f'<section class="block"><h2>{T("Modèles à télécharger", "Downloadable templates")}</h2>{T("Quatre documents Word modifiables, en français et en anglais, à adapter à votre organisation.", "Four editable Word documents, in French and English, to adapt to your organization.", tag="p", cls="intro")}'
    for t in B.TEMPLATES:
        dl = f'{r}../assets/downloads/{t["slug"]}-{B.LANG}.docx'
        inside = tpl_inside(B, t)
        b += f'<article class="tpl-card" id="{t["slug"]}"><h3>{P(t["title"])}</h3>{P(t["summary"], tag="p")}'
        if inside: b += f'<p class="muted" style="margin-bottom:0">{T("Contenu :", "Inside:")}</p><ul>' + "".join(f"<li>{x}</li>" for x in inside) + "</ul>"
        b += '<div class="cta-actions tpl-actions">'
        if t["slug"] == "ransomware-checklist":
            b += f'<a class="btn primary" href="{r}resources/{t["slug"]}.html">{T("Ouvrir la liste interactive", "Open the interactive checklist")}</a>'
            b += f'<a class="btn ghost" href="{dl}" download>{T("Télécharger (Word)", "Download (Word)")}</a>'
        else:
            b += f'<a class="btn primary" href="{dl}" download>{T("Télécharger (Word, .docx)", "Download (Word, .docx)")}</a>'
        b += "</div></article>"
    b += f'<p class="note">{P(B.TEMPLATE_DISCLAIMER)}</p></section>'
    arts = sorted(B.INSIGHTS, key=lambda a: a["date"], reverse=True)[:3]
    b += f'<section class="block"><h2>{T("À lire", "Reading")}</h2>{B.link_rows(r, [B.item_of(f"insights/{a["slug"]}.html") for a in arts])}<p style="margin-top:20px"><a class="textlink" href="{r}insights/index.html">{T("Tous les articles", "All articles")} {ARROW}</a> &nbsp; <a class="textlink" href="{r}resources/glossary.html">{P(B.OTHER["resources/glossary.html"])} {ARROW}</a></p></section>'
    B.page(path, ('Ressources | FZ Consultation', 'Resources | FZ Consultation'), ("Outils gratuits, modèles à télécharger, glossaire et notes sur la résilience d'affaires.", "Free tools, downloadable templates, glossary and notes on business resilience."), b)

# ---------------------------------------------------------------- Home
def build_home(B):
    T, P, E, ARROW = B.T, B.P, B.E, B.ARROW
    src = open(os.path.join(B.HERE, "home_main.html")).read()
    m = re.search(r'<figure class="timeline">.*?</figure>', src, re.S)
    fig = B.strip_other(m.group(0)) if m else ""
    r = ""
    b = f'''<section class="hero">
      <h1>{P(HOME["h1"])}</h1>
      <p class="lede">{P(HOME["lede"])}</p>
      <div class="actions"><a class="btn primary" href="#worries">{T("Choisir mon inquiétude", "Start with what worries me")}</a><a class="btn ghost" href="case-studies/index.html">{T("Lire les incidents", "Read the incidents")}</a></div>
      {fig}
    </section>
    <section class="block" id="worries"><h2>{P(HOME["worries_h"])}</h2>{P(HOME["worries_i"], tag="p", cls="intro")}<div class="paths">'''
    for w in HOME["worries"]:
        b += f'<article class="path"><h3>{P(w["h"])}</h3><p>{P(w["p"])}</p><ul>'
        for kind, key, lab in w["links"]:
            b += f'<li><a href="{r}{key}"><span class="k">{P(HOME["kinds"][kind])}</span><span>{P(lab)}</span></a></li>'
        b += "</ul></article>"
    b += "</div></section>"
    feat = [case_by_slug(B, s) for s in HOME["featured"]]
    b += f'<section class="block"><h2>{P(HOME["cases_h"])}</h2>{P(HOME["cases_i"], tag="p", cls="intro")}{case_cards2(B, r, feat)}<p style="margin-top:20px"><a class="textlink" href="case-studies/index.html">{T("Les neuf études de cas", "All nine case studies")} {ARROW}</a></p>'
    note = latest_note(B)
    if note:
        b += f'<div class="series" style="margin-top:28px"><div><p class="eyebrow">{P(SERIES)}</p><h3 style="margin:0 0 6px;font-size:1.2rem">{P(note["title"])}</h3><p>{P(note["summary"])}</p></div><a class="btn ghost" href="insights/{note["slug"]}.html">{T("Lire la note", "Read the note")}</a></div>'
    b += "</section>"
    b += f'''<section class="block"><h2>{P(HOME["tools_h"])}</h2><div class="pillars">
      <a href="resources/downtime-calculator.html"><span class="pk">01</span><h3>{T("Calculateur du coût d'une interruption", "Downtime cost calculator")}</h3>{T("Quelques chiffres, un ordre de grandeur. Tout reste dans votre navigateur.", "A few numbers, an order of magnitude. Everything stays in your browser.", tag="p")}<span class="more">{T("Calculer", "Calculate")} {ARROW}</span></a>
      <a href="resources/ransomware-checklist.html"><span class="pk">02</span><h3>{T("Liste de vérification rançongiciel", "Ransomware checklist")}</h3>{T("Cinq phases pour garder la tête froide pendant les premières heures. À imprimer.", "Five phases to keep a clear head through the first hours. Print it.", tag="p")}<span class="more">{T("Ouvrir la liste", "Open the checklist")} {ARROW}</span></a>
      <a href="self-assessment.html"><span class="pk">03</span><h3>{T("Auto-évaluation de la résilience", "Resilience self-assessment")}</h3>{T("Vingt questions, huit minutes, un score par domaine et votre point le plus fragile.", "Twenty questions, eight minutes, a score by area and your most fragile spot.", tag="p")}<span class="more">{T("Commencer", "Start")} {ARROW}</span></a>
    </div></section>'''
    b += f'<section class="block"><h2>{P(HOME["jobs_h"])}</h2>' + B.link_rows(r, [{"path": f"what-we-do/index.html#{o['id']}", "short": o["name"], "summary": o["title"]} for o in OUTCOMES]) + "</section>"
    b += f'<section class="block split"><div><h2>{P(WWD_HOW["title"])}</h2></div>{P(WWD_HOW["big"], tag="p", cls="big")}</section>'
    B.page("index.html", ("FZ Consultation — Résilience, sécurité et reprise après sinistre", "FZ Consultation — Business resilience, security and disaster recovery"),
           ("FZ Consultation aide les organisations à chiffrer ce qu'une panne leur coûterait, à bâtir une reprise qui tient et à la répéter avant le vrai jour.",
            "FZ Consultation helps organizations put a number on what an outage would cost, build recovery that holds, and rehearse it before the real day."), b)

# ---------------------------------------------------------------- redirects and link rewriting
def write_stubs(B):
    """One small noindex page at every retired URL, so old links, bookmarks and search results still land somewhere useful."""
    for lang in B.LANGS:
        B.LANG = lang
        T, E = B.T, B.E
        for old, new in REMAP.items():
            depth = old.count("/")
            r = "../" * depth
            target = r + new
            canon = f"{B.SITE}/{lang}/{new.split('#')[0]}"
            doc = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; base-uri 'self'; object-src 'none'">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url={E(target)}">
<meta name="robots" content="noindex,follow">
<title>{T("Cette page a déménagé", "This page has moved")} | FZ Consultation</title>
<meta name="description" content="{T("Cette page a été regroupée avec une autre. Vous allez être redirigé.", "This page was merged into another. You are being redirected.")}">
<link rel="canonical" href="{canon}">
<style>body{{font-family:system-ui,sans-serif;max-width:560px;margin:15vh auto;padding:0 24px;line-height:1.5;color:#16222E;background:#EEF1F3}}a{{color:#0052B2;font-weight:700}}@media (prefers-color-scheme:dark){{body{{color:#E6ECF3;background:#0E1726}}a{{color:#86B3F0}}}}</style>
</head>
<body><main><h1>{T("Cette page a déménagé", "This page has moved")}</h1>
<p>{T("Son contenu fait maintenant partie d&#39;une page plus complète.", "Its content is now part of a fuller page.")} <a href="{E(target)}">{T("Continuer", "Continue")}</a></p></main></body>
</html>
'''
            full = os.path.join(B.OUT, lang, old)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "w").write(doc)

def rewrite_links(B):
    """Point every internal link at the new location of a retired page (also inside JSON data blocks)."""
    keys = sorted(REMAP, key=len, reverse=True)
    n = 0
    for lang in B.LANGS:
        for dp, dn, fn in os.walk(os.path.join(B.OUT, lang)):
            for f in fn:
                if not f.endswith(".html"): continue
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, os.path.join(B.OUT, lang))
                if rel in REMAP: continue          # the stubs themselves
                s = open(p, encoding="utf-8").read(); o = s
                for k in keys:
                    if k in s: s = s.replace(k, REMAP[k])
                if s != o:
                    open(p, "w", encoding="utf-8").write(s); n += 1
    return n
