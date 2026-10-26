"""New sections: Resources hub, downtime calculator, templates, glossary, Insights (+RSS),
search, security, accessibility, governance. Called from build.py with the build module as `B`."""
import json, os, re, unicodedata, html
from datetime import datetime
from email.utils import format_datetime
from tools import TEMPLATES, CALC, GLOSSARY, TEMPLATE_DISCLAIMER, RANSOM, RTORPO, AIPOL
from insights import INSIGHTS

MONTHS = {"fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
          "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}

def fmt_date(iso, lang):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MONTHS['fr'][m-1]} {y}" if lang == "fr" else f"{MONTHS['en'][m-1]} {d}, {y}"

def jsondata(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def sort_key(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()

# ------------------------------------------------------------------ helpers
def tpl_path(t): return f"resources/{t['slug']}.html"
def art_path(a): return f"insights/{a['slug']}.html"

def tpl_items():
    return [{"path": tpl_path(t), "short": t["short"], "summary": t["summary"]} for t in TEMPLATES]

def art_items():
    return [{"path": art_path(a), "short": a["title"], "summary": a["summary"]} for a in INSIGHTS]

def build_extras(B):
    build_resources_hub(B); build_calculator(B); build_templates(B); build_glossary(B)
    build_insights(B); build_search(B); build_security(B); build_accessibility(B); build_governance(B)

def hero(B, path, trail_extra, eyebrow, title, lede):
    r = B.rprefix(path)
    trail = trail_extra + [(path, B.OTHER[path])]
    return r, B.page_hero(r, trail, eyebrow, title, lede)

RES = ("resources/index.html", ("Ressources", "Resources"))

# ------------------------------------------------------------------ resources hub
def build_resources_hub(B):
    T, P, ARROW = B.T, B.P, B.ARROW
    path = "resources/index.html"; r = B.rprefix(path)
    b = B.page_hero(r, [(path, B.OTHER[path])], ("Ressources", "Resources"), ("Outils, modèles et lectures", "Tools, templates and reading"),
        ("Des outils gratuits, des modèles à télécharger et des articles pour avancer sur la résilience, même avant de nous appeler.", "Free tools, downloadable templates and articles to make progress on resilience, even before you call us."))
    tools = [
      {"path": "self-assessment.html", "short": ("Auto-évaluation de la résilience", "Resilience self-assessment"), "summary": ("Vingt questions pondérées, un score par domaine et vos priorités.", "Twenty weighted questions, a score by area and your priorities.")},
      {"path": "resources/downtime-calculator.html", "short": B.OTHER["resources/downtime-calculator.html"], "summary": ("Estimez le coût d'un incident en quelques chiffres. Tout reste dans votre navigateur.", "Estimate the cost of an incident from a few numbers. Everything stays in your browser.")},
      {"path": "resources/cost-of-downtime.html", "short": B.OTHER["resources/cost-of-downtime.html"], "summary": ("Repères publics par secteur et incidents réels, avec sources.", "Public benchmarks by industry and real incidents, with sources.")},
      {"path": "ai/vision-questionnaire.html", "short": B.OTHER["ai/vision-questionnaire.html"], "summary": ("Treize questions pour aligner votre direction sur votre vision de l'IA.", "Thirteen questions to align your leadership on your AI vision.")},
    ]
    b += f'<section class="block"><h2>{T("Outils interactifs", "Interactive tools")}</h2>{B.link_rows(r, tools)}</section>'
    b += f'<section class="block"><h2>{T("Modèles à télécharger", "Downloadable templates")}</h2>{T("Trois documents Word modifiables, en français et en anglais, à adapter à votre organisation.", "Three editable Word documents, in French and English, to adapt to your organization.", tag="p", cls="intro")}{B.link_rows(r, tpl_items())}</section>'
    b += f'<section class="block"><h2>{T("À lire", "Reading")}</h2>{B.link_rows(r, art_items()[:3])}<p style="margin-top:20px"><a class="textlink" href="{r}insights/index.html">{T("Tous les articles", "All articles")} {ARROW}</a> &nbsp; <a class="textlink" href="{r}resources/glossary.html">{P(B.OTHER["resources/glossary.html"])} {ARROW}</a></p></section>'
    b += f'<section class="block"><h2>{T("Apprendre des incidents", "Learning from incidents")}</h2>{B.case_cards(r, B.CASES[:3])}<p style="margin-top:20px"><a class="textlink" href="{r}case-studies/index.html">{T("Toutes les études de cas", "All case studies")} {ARROW}</a></p></section>'
    B.page(path, (f'Ressources | FZ Consultation', 'Resources | FZ Consultation'), ("Outils gratuits, modèles à télécharger, glossaire et articles sur la résilience d'affaires.", "Free tools, downloadable templates, glossary and articles on business resilience."), b)

# ------------------------------------------------------------------ calculator
def build_calculator(B):
    T, P, E = B.T, B.P, B.E
    path = "resources/downtime-calculator.html"; r = B.rprefix(path)
    b = B.page_hero(r, [RES, (path, B.OTHER[path])], ("Outil gratuit", "Free tool"), ("Calculateur du coût d'une interruption", "Downtime cost calculator"),
        ("Un ordre de grandeur, calculé à partir de vos propres chiffres, pour savoir ce qu'une heure d'arrêt représente pour vous.", "An order of magnitude, calculated from your own numbers, to see what an hour of downtime means for you."))
    ui = CALC["ui"][B.LANG]
    fields = ""
    for key, label, hint, default in CALC["fields"]:
        h = P(hint)
        hid = f' aria-describedby="h-{key}"' if h else ""
        hp = f'<span class="hint" id="h-{key}">{h}</span>' if h else ""
        fields += f'<label for="f-{key}">{P(label)}{hp}<input id="f-{key}" name="{key}" type="number" inputmode="decimal" min="0" step="any" value="{default}"{hid}></label>'
    cur = f'<label for="f-cur">{ui["currency"]}<select id="f-cur" name="cur"><option value="CAD">CAD $</option><option value="USD">USD $</option><option value="EUR">EUR €</option><option value="GBP">GBP £</option></select></label>'
    data = {"ui": ui, "lang": B.LANG, "defaultCur": "CAD" if B.LANG == "fr" else "USD"}
    b += f'''<section class="block calc-wrap">
      <form id="calc-form" class="cform calc" novalidate>
        <h2>{T("Vos hypothèses", "Your assumptions")}</h2>
        {cur}
        <div class="calc-grid">{fields}</div>
        <div class="calc-actions"><button class="btn primary" type="submit">{ui["calc"]}</button><button class="btn ghost" type="reset">{ui["reset"]}</button></div>
      </form>
      <div class="calc-out" id="calc-out" aria-live="polite" tabindex="-1">
        <p class="muted" id="calc-empty">{T("Les résultats apparaîtront ici.", "Results will appear here.")}</p>
      </div>
      <noscript><p>{T("Ce calculateur nécessite JavaScript.", "This calculator requires JavaScript.")}</p></noscript>
      <script type="application/json" id="calc-data">{jsondata(data)}</script>
    </section>
    <section class="block"><p class="note">{T("Estimation indicative, fondée uniquement sur ce que vous saisissez : elle ne tient pas compte de l'atteinte à la réputation, de la perte de clients à long terme ni des conséquences réglementaires. Vos chiffres ne quittent pas votre navigateur. Pour une valeur fiable, une analyse d'impact sur les activités reste la bonne méthode.", "Indicative estimate based only on what you enter: it does not account for reputational damage, long-term customer loss or regulatory consequences. Your numbers never leave your browser. For a reliable value, a business impact analysis remains the right method.")}</p>
    <p><a class="textlink" href="{r}resources/cost-of-downtime.html">{T("Comparer avec les repères publics par secteur", "Compare with public benchmarks by industry")} {B.ARROW}</a></p></section>'''
    js = f'<script src="{r}../assets/calc.js?v={B.VER}"></script>'
    B.page(path, ("Calculateur du coût d'une interruption | FZ Consultation", "Downtime cost calculator | FZ Consultation"),
           ("Estimez gratuitement le coût d'une interruption d'activité à partir de vos propres chiffres.", "Estimate the cost of a business interruption from your own numbers, for free."), b, extra_js=js)

# ------------------------------------------------------------------ templates
def build_templates(B):
    T, P, E, ARROW = B.T, B.P, B.E, B.ARROW
    for t in TEMPLATES:
        path = tpl_path(t); r = B.rprefix(path)
        i = B.I()
        b = B.page_hero(r, [RES, (path, t["short"])], ("Modèle à télécharger", "Downloadable template"), t["title"], t["lede"])
        dl = f'{r}../assets/downloads/{t["slug"]}-{B.LANG}.docx'
        b += f'''<section class="block split"><div><h2>{T("Comment l'utiliser", "How to use it")}</h2></div><div>{P(t["how"], tag="p", cls="intro")}
          <div class="cta-actions tpl-actions"><a class="btn primary" href="{dl}" download>{T("Télécharger (Word, .docx)", "Download (Word, .docx)")}</a><button class="btn ghost" type="button" data-print>{T("Imprimer cette page", "Print this page")}</button></div></div></section>'''
        if t is RANSOM:
            for title, items in t["phases"]:
                b += f'<section class="block"><h2>{P(title)}</h2><ul class="chk">' + "".join(f'<li><label><input type="checkbox"> <span>{P(it)}</span></label></li>' for it in items) + "</ul></section>"
            b += f'<section class="block"><h2>Sources</h2><ul class="sources">' + "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener noreferrer"{B.SRCLANG()}>{E(n)}</a></li>' for n, u in t["sources"]) + f'</ul>{T("Cette liste s&#39;inspire de bonnes pratiques publiques, dont les guides ci-dessus ; elle n&#39;est ni approuvée ni publiée par ces organismes.", "This list draws on public good practice, including the guides above; it is neither endorsed nor published by those agencies.", tag="p", cls="note")}</section>'
        elif t is RTORPO:
            b += f'<section class="block"><h2>{T("Définitions", "Definitions")}</h2><dl class="defs">' + "".join(f"<div><dt>{P(k)}</dt><dd>{P(v)}</dd></div>" for k, v in t["defs"]) + "</dl></section>"
            head = "".join(f'<th scope="col">{P(c)}</th>' for c in t["columns"])
            ex = "".join(f"<td>{P(c)}</td>" for c in t["example"])
            blank = "<tr>" + "<td></td>" * len(t["columns"]) + "</tr>"
            b += f'''<section class="block"><h2>{T("Le tableau", "The worksheet")}</h2>
              <div class="tscroll" tabindex="0" role="region" aria-label="{T("Tableau RTO / RPO, défilement horizontal possible", "RTO / RPO worksheet, scrolls horizontally")}">
              <table class="wtable"><caption>{T("Première ligne : exemple fictif. Le fichier Word contient le tableau vierge.", "First row: fictional example. The Word file contains the blank worksheet.")}</caption>
              <thead><tr>{head}</tr></thead><tbody><tr class="ex">{ex}</tr>{blank*2}</tbody></table></div></section>'''
            b += f'<section class="block"><h2>{T("Conseils", "Tips")}</h2><div class="cover grid2">' + "".join(f'<div class="citem"><h3>{P(h)}</h3>{P(d, tag="p")}</div>' for h, d in t["tips"]) + "</div></section>"
        else:
            b += f'<section class="block"><h2>{T("Contenu du modèle", "What the template contains")}</h2><ol class="policy">' + "".join(f'<li><h3>{P(h)}</h3>{P(d, tag="p")}</li>' for h, d in t["sections"]) + "</ol></section>"
        b += f'<section class="block"><p class="note">{P(TEMPLATE_DISCLAIMER)}</p></section>'
        rel = [B.item_of(k) for k in t["related"]]
        b += f'<section class="block"><h2>{T("À voir aussi", "Related")}</h2>{B.link_rows(r, rel)}</section>'
        B.page(path, (f'{t["title"][0]} | FZ Consultation', f'{t["title"][1]} | FZ Consultation'), t["summary"], b)

# ------------------------------------------------------------------ glossary
def build_glossary(B):
    T, P, ARROW = B.T, B.P, B.ARROW
    path = "resources/glossary.html"; r = B.rprefix(path); i = B.I()
    terms = sorted(GLOSSARY, key=lambda x: sort_key(x[0][i]))
    letters = sorted({sort_key(t[0][i])[0].upper() for t in terms})
    b = B.page_hero(r, [RES, (path, B.OTHER[path])], ("Ressources", "Resources"), ("Glossaire de la résilience", "Resilience glossary"),
        ("Les termes que l'on rencontre en continuité, reprise après sinistre, cybersécurité et IA, expliqués simplement.", "The terms you meet in continuity, disaster recovery, cybersecurity and AI, explained simply."))
    b += f'<nav class="az" aria-label="{T("Index alphabétique", "Alphabetical index")}">' + "".join(f'<a href="#letter-{l}">{l}</a>' for l in letters) + "</nav>"
    b += '<section class="block">'
    cur = None
    for term, d in terms:
        l = sort_key(term[i])[0].upper()
        if l != cur:
            if cur is not None: b += "</dl></div>"
            b += f'<div class="gl-sec"><h2 id="letter-{l}">{l}</h2><dl class="gloss">'; cur = l
        slug = slugify(term[1])
        b += f'<div class="gl-item" id="term-{slug}"><dt>{P(term)}</dt><dd>{P(d)}</dd></div>'
    b += "</dl></div></section>"
    b += f'<section class="block"><h2>{T("Un terme manque ?", "Missing a term?")}</h2><p><a class="textlink" href="{r}contact.html">{T("Dites-le-nous", "Tell us")} {ARROW}</a></p></section>'
    B.page(path, ("Glossaire de la résilience | FZ Consultation", "Resilience glossary | FZ Consultation"),
           ("Définitions claires : RTO, RPO, BIA, rançongiciel, DORA, NIS2, agent IA et plus.", "Clear definitions: RTO, RPO, BIA, ransomware, DORA, NIS2, AI agent and more."), b)

# ------------------------------------------------------------------ insights
def render_blocks(B, blocks):
    out = ""
    for kind, c in blocks:
        if kind == "h": out += f"<h2>{B.P(c)}</h2>"
        elif kind == "p": out += f"<p>{B.P(c)}</p>"
        elif kind == "ul": out += "<ul>" + "".join(f"<li>{B.P(x)}</li>" for x in c) + "</ul>"
    return out

def build_insights(B):
    T, P, E, ARROW = B.T, B.P, B.E, B.ARROW
    lang = B.LANG
    arts = sorted(INSIGHTS, key=lambda a: a["date"], reverse=True)
    path = "insights/index.html"; r = B.rprefix(path)
    b = B.page_hero(r, [RES, (path, B.OTHER[path])], ("Insights", "Insights"), ("Articles et points de vue", "Articles and perspectives"),
        ("Des textes courts et pratiques sur la reprise, la sécurité et l'IA, sans jargon inutile.", "Short, practical pieces on recovery, security and AI, without needless jargon."))
    b += '<section class="block"><ul class="rows">' + "".join(
        f'<li><a href="{r}{art_path(a)}"><span class="rt">{P(a["title"])}<span class="meta">{fmt_date(a["date"], lang)} · {a["mins"]} min</span></span><span class="rs">{P(a["summary"])}</span>{ARROW}</a></li>' for a in arts) + "</ul>"
    b += f'<p style="margin-top:24px"><a class="textlink" href="{r}insights/feed.xml">{T("S&#39;abonner par flux RSS", "Subscribe via RSS")} {ARROW}</a></p></section>'
    B.page(path, ("Insights | FZ Consultation", "Insights | FZ Consultation"), ("Articles pratiques sur la résilience, la reprise après sinistre, la sécurité et l'IA.", "Practical articles on resilience, disaster recovery, security and AI."), b)
    for a in arts:
        path = art_path(a); r = B.rprefix(path)
        b = B.page_hero(r, [RES, ("insights/index.html", B.OTHER["insights/index.html"]), (path, a["title"])],
                        (f'Insights · {fmt_date(a["date"], "fr")} · {a["mins"]} min', f'Insights · {fmt_date(a["date"], "en")} · {a["mins"]} min'), a["title"], a["summary"])
        b += f'<section class="block prose"><div class="prose-in">{render_blocks(B, a["body"])}</div></section>'
        b += f'<section class="block"><h2>{T("Pour aller plus loin", "Go further")}</h2>{B.link_rows(r, [B.item_of(k) for k in a["related"]])}</section>'
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": P(a["title"]), "description": P(a["summary"]), "datePublished": a["date"], "dateModified": a["date"],
              "inLanguage": lang, "author": {"@type": "Organization", "name": "FZ Consultation", "url": B.SITE}, "publisher": {"@type": "Organization", "name": "FZ Consultation", "url": B.SITE},
              "mainEntityOfPage": B.url_of(lang, path)}
        B.page(path, (f'{a["title"][0]} | FZ Consultation', f'{a["title"][1]} | FZ Consultation'), a["summary"], b, ld=[ld])
    # RSS
    items = ""
    for a in arts:
        dt = datetime.strptime(a["date"], "%Y-%m-%d").replace(hour=9)
        from datetime import timezone
        items += f'<item><title>{html.escape(P(a["title"]))}</title><link>{B.url_of(lang, art_path(a))}</link><guid isPermaLink="true">{B.url_of(lang, art_path(a))}</guid><pubDate>{format_datetime(dt.replace(tzinfo=timezone.utc))}</pubDate><description>{html.escape(P(a["summary"]))}</description></item>'
    feed = f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>FZ Consultation — Insights</title><link>{B.url_of(lang, "insights/index.html")}</link><description>{html.escape(T("Articles sur la résilience d&#39;affaires, la sécurité, la reprise après sinistre et l&#39;IA.", "Articles on business resilience, security, disaster recovery and AI."))}</description><language>{lang}</language><atom:link href="{B.url_of(lang, "insights/feed.xml")}" rel="self" type="application/rss+xml"/>{items}</channel></rss>\n'
    open(os.path.join(B.OUT, lang, "insights", "feed.xml"), "w").write(feed)

# ------------------------------------------------------------------ search
def build_search(B):
    T, P = B.T, B.P
    path = "search.html"; r = ""
    ui = {"fr": {"none": "Aucun résultat pour « {q} ». Essayez d'autres mots ou parcourez les ressources.", "count1": "1 résultat", "countN": "{n} résultats", "loading": "Chargement de la recherche…", "error": "La recherche n'est pas disponible pour le moment. Utilisez le menu pour naviguer.", "prompt": "Saisissez au moins deux caractères.", "more": "Afficher plus de résultats"},
          "en": {"none": "No results for “{q}”. Try other words or browse the resources.", "count1": "1 result", "countN": "{n} results", "loading": "Loading search…", "error": "Search is not available right now. Use the menu to browse.", "prompt": "Enter at least two characters.", "more": "Show more results"}}[B.LANG]
    b = B.page_hero(r, [(path, B.OTHER[path])], ("Recherche", "Search"), ("Rechercher dans le site", "Search the site"),
        ("Trouvez une page, un service, une étude de cas ou un terme du glossaire.", "Find a page, a service, a case study or a glossary term."))
    b += f'''<section class="block search-wrap" data-pf="{r}../pagefind/pagefind.js">
      <form id="search-form" role="search" class="searchbox">
        <label for="q">{T("Votre recherche", "Your search")}</label>
        <div class="sb-row"><input id="q" name="q" type="search" autocomplete="off" enterkeyhint="search"><button class="btn primary" type="submit">{T("Rechercher", "Search")}</button></div>
      </form>
      <p id="search-status" class="muted" role="status" aria-live="polite"></p>
      <ol id="search-results" class="results"></ol>
      <button type="button" id="search-more" class="btn ghost" hidden>{ui["more"]}</button>
      <noscript><p>{T("La recherche nécessite JavaScript.", "Search requires JavaScript.")}</p></noscript>
      <script type="application/json" id="search-data">{jsondata(ui)}</script>
    </section>'''
    js = f'<script type="module" src="{r}../assets/search.js?v={B.VER}"></script>'
    B.page(path, ("Recherche | FZ Consultation", "Search | FZ Consultation"), ("Rechercher dans le site FZ Consultation.", "Search the FZ Consultation site."), b, extra_js=js, noindex=True)

# ------------------------------------------------------------------ security
def build_security(B):
    T, P, E, ARROW, EMAIL = B.T, B.P, B.E, B.ARROW, B.EMAIL
    path = "security.html"; r = ""
    b = B.page_hero(r, [(path, B.OTHER[path])], ("Sécurité", "Security"), ("Comment nous protégeons ce site", "How we protect this site"),
        ("Un cabinet de sécurité doit montrer l'exemple. Voici ce que nous faisons, ce que le site collecte, et comment nous signaler une faille.", "A security firm should lead by example. Here is what we do, what this site collects, and how to report a flaw."))
    s = [
      (("Un site volontairement simple", "A deliberately simple site"), T("Le site est statique : pas de base de données, pas de comptes, pas de système de gestion de contenu à corriger. Il est servi uniquement en HTTPS et ne dépose aucun cookie. Ce que l'on ne déploie pas ne peut pas être attaqué.", "The site is static: no database, no accounts, no content management system to patch. It is served over HTTPS only and sets no cookies. What you do not deploy cannot be attacked.")),
      (("Peu de tiers, tous listés", "Few third parties, all listed"), None),
      (("Mesures techniques", "Technical measures"), "<ul>" + "".join(f"<li>{x}</li>" for x in [
         T("Une politique de sécurité du contenu (CSP) restreint les origines des scripts, des connexions et des ressources, et interdit les scripts intégrés aux pages.", "A Content Security Policy (CSP) restricts the origins of scripts, connections and resources, and forbids scripts embedded in pages."),
         T("La police de caractères est hébergée sur le site : aucune requête vers un service de polices tiers.", "The typeface is hosted on the site itself: no request to a third-party font service."),
         T("L'extension de sécurité DNS (DNSSEC) est activée sur le domaine.", "DNS Security Extensions (DNSSEC) are enabled on the domain."),
         T("Le site publie un fichier security.txt (RFC 9116) pour que les chercheurs sachent à qui écrire.", "The site publishes a security.txt file (RFC 9116) so researchers know whom to contact."),
         T("La recherche s'exécute entièrement dans votre navigateur, sur un index statique : vos requêtes ne sont pas transmises.", "Search runs entirely in your browser against a static index: your queries are not transmitted."),
      ]) + "</ul>"),
      (("Signaler une vulnérabilité", "Report a vulnerability"), T(f'Si vous pensez avoir trouvé une faille, écrivez à <a href="mailto:{EMAIL}">{EMAIL}</a> en décrivant ce que vous avez observé et comment le reproduire. Nous accusons réception dans les cinq jours ouvrables et vous tenons informé de la correction. Nous considérons la recherche de bonne foi qui respecte les règles ci-dessous comme autorisée et n&#39;engagerons pas de poursuites contre vous.', f'If you believe you found a flaw, email <a href="mailto:{EMAIL}">{EMAIL}</a> describing what you saw and how to reproduce it. We acknowledge reports within five business days and keep you informed about the fix. We regard good-faith research that follows the rules below as authorized and will not take legal action against you.')),
      (("Règles de la recherche", "Rules for research"), "<ul>" + "".join(f"<li>{x}</li>" for x in [
         T("Limitez-vous à ce site (fzconsultation.xyz). Les services tiers listés ci-dessus relèvent de leurs propres programmes.", "Stay within this site (fzconsultation.xyz). The third-party services listed above have their own programs."),
         T("N'accédez pas aux données d'autrui, ne les modifiez pas et ne les conservez pas. Arrêtez dès que vous avez démontré le problème.", "Do not access, change or keep other people's data. Stop as soon as you have demonstrated the issue."),
         T("Pas de déni de service, d'hameçonnage ni d'ingénierie sociale visant notre personnel ou nos clients.", "No denial of service, phishing or social engineering against our staff or clients."),
         T("Laissez-nous un délai raisonnable pour corriger avant toute divulgation publique.", "Give us reasonable time to fix before any public disclosure."),
      ]) + "</ul>"),
      (("Hors périmètre", "Out of scope"), T("Les rapports automatisés sans impact démontré, l'absence d'en-têtes HTTP que notre hébergeur ne permet pas de configurer, et les constats sur des services tiers.", "Automated reports with no demonstrated impact, HTTP headers our host does not let us configure, and findings on third-party services.")),
    ]
    b += '<section class="block legal">'
    for h, body in s:
        if body is None:
            rows = [("GitHub Pages", T("Hébergement du site", "Site hosting"), T("Toutes les pages", "All pages")),
                    ("Cloudflare Web Analytics", T("Mesure d'audience agrégée, sans cookies", "Aggregate analytics, no cookies"), T("Toutes les pages", "All pages")),
                    ("Formspree", T("Transmission du formulaire de contact", "Contact form delivery"), T("Uniquement à l'envoi du formulaire", "Only when the form is submitted")),
                    ("Calendly", T("Prise de rendez-vous", "Appointment booking"), T("Uniquement si vous cliquez sur « Réserver »", "Only if you click “Book”")),
                    ("Namecheap", T("Nom de domaine et courriel", "Domain name and email"), T("Hors du site", "Outside the site"))]
            body = f'<div class="tscroll" tabindex="0" role="region" aria-label="{T("Services tiers", "Third-party services")}"><table class="wtable"><thead><tr><th scope="col">{T("Service", "Service")}</th><th scope="col">{T("Rôle", "Role")}</th><th scope="col">{T("Quand", "When")}</th></tr></thead><tbody>' + "".join(f"<tr><td>{a}</td><td>{b_}</td><td>{c}</td></tr>" for a, b_, c in rows) + "</tbody></table></div>"
            body += f'<p>{T("Détails dans notre", "Details in our")} <a href="{r}privacy.html">{T("politique de confidentialité", "privacy policy")}</a>.</p>'
        elif not body.startswith("<"):
            body = f"<p>{body}</p>"
        b += f"<h2>{P(h)}</h2>{body}"
    b += "</section>"
    B.page(path, ("Sécurité du site | FZ Consultation", "Site security | FZ Consultation"), ("Les mesures de sécurité de ce site et la façon de signaler une vulnérabilité.", "The security measures of this site and how to report a vulnerability."), b)

# ------------------------------------------------------------------ accessibility
def build_accessibility(B):
    T, P, EMAIL = B.T, B.P, B.EMAIL
    path = "accessibility.html"; r = ""
    b = B.page_hero(r, [(path, B.OTHER[path])], ("Légal", "Legal"), B.OTHER[path], (f"Dernière mise à jour : {B.UPDATED[0]}", f"Last updated: {B.UPDATED[1]}"))
    S = [
     (("Notre engagement", "Our commitment"), T("FZ Consultation veut que son site soit utilisable par le plus grand nombre, y compris les personnes qui utilisent un lecteur d'écran, naviguent au clavier, agrandissent le texte ou ont besoin d'un fort contraste. Nous visons la conformité aux Règles pour l'accessibilité des contenus Web (WCAG) 2.2, niveau AA.", "FZ Consultation wants its website to be usable by as many people as possible, including people who use a screen reader, navigate by keyboard, enlarge text or need strong contrast. We aim for conformance with the Web Content Accessibility Guidelines (WCAG) 2.2, level AA.")),
     (("Ce que nous avons fait", "What we have done"), "<ul>" + "".join(f"<li>{x}</li>" for x in [
        T("Structure sémantique : titres hiérarchisés, repères de page, lien d'évitement « Aller au contenu ».", "Semantic structure: ordered headings, page landmarks, a “Skip to content” link."),
        T("Navigation complète au clavier, avec indicateur de focus visible ; la touche Échap ferme les menus.", "Full keyboard navigation with a visible focus indicator; the Escape key closes menus."),
        T("Thèmes clair et sombre, avec un sélecteur manuel en plus du réglage de votre système, et contrastes de couleur vérifiés.", "Light and dark themes, with a manual switch in addition to your system setting, and checked colour contrast."),
        T("Respect de la préférence « réduire les animations » et du zoom ou de l'agrandissement du texte du navigateur.", "Respect for the “reduce motion” preference and for browser zoom or text enlargement."),
        T("Formulaires avec étiquettes explicites, messages d'état annoncés aux technologies d'assistance et champ anti-pourriel invisible pour les personnes.", "Forms with explicit labels, status messages announced to assistive technology and an anti-spam field hidden from people."),
        T("Les diagrammes ont une alternative textuelle ou une liste équivalente ; la langue des passages en langue étrangère est indiquée.", "Diagrams have a text alternative or an equivalent list; the language of passages in another language is marked."),
        T("Le site est disponible en français et en anglais, avec un sélecteur de langue sur chaque page.", "The site is available in French and English, with a language switch on every page."),
     ]) + "</ul>"),
     (("Comment nous avons vérifié", "How we checked"), T("Les pages sont testées automatiquement avec l'outil axe-core, en thèmes clair et sombre, ainsi que dans les états de résultats des outils interactifs, à chaque modification. Ce contrôle automatique ne détecte qu'une partie des problèmes. Nous n'avons pas encore fait tester le site par des personnes utilisant des technologies d'assistance ; c'est une étape que nous prévoyons.", "Pages are tested automatically with the axe-core tool, in light and dark themes and in the result states of the interactive tools, on every change. Automated checks detect only part of all issues. We have not yet had the site tested by people using assistive technology; this is a step we plan to take.")),
     (("Limites connues", "Known limitations"), "<ul>" + "".join(f"<li>{x}</li>" for x in [
        T("Les liens vers des sites externes (sources, réservation) mènent à des pages dont nous ne contrôlons pas l'accessibilité.", "Links to external sites (sources, booking) lead to pages whose accessibility we do not control."),
        T("Les modèles Word téléchargeables ne sont pas encore validés avec le vérificateur d'accessibilité d'Office.", "The downloadable Word templates have not yet been validated with Office's accessibility checker."),
        T("Certains termes techniques et noms de normes sont en anglais, avec leur explication en français dans le glossaire.", "Some technical terms and standard names are in English, with explanations in the glossary."),
     ]) + "</ul>"),
     (("Nous écrire", "Contact us"), T(f'Si un contenu vous est inaccessible, ou si vous avez une suggestion, écrivez-nous à <a href="mailto:{EMAIL}">{EMAIL}</a> en indiquant la page et le problème rencontré, ainsi que l&#39;outil que vous utilisez si vous le souhaitez. Nous répondons dans les cinq jours ouvrables et proposons une alternative accessible dans la mesure du possible.', f'If any content is inaccessible to you, or if you have a suggestion, email <a href="mailto:{EMAIL}">{EMAIL}</a> with the page and the problem, and the tool you use if you wish. We reply within five business days and offer an accessible alternative where possible.')),
    ]
    b += '<section class="block legal">' + "".join(f"<h2>{P(h)}</h2>{body if body.startswith('<') else '<p>'+body+'</p>'}" for h, body in S) + "</section>"
    B.page(path, ("Accessibilité | FZ Consultation", "Accessibility | FZ Consultation"), ("Notre engagement et nos mesures d'accessibilité numérique.", "Our digital accessibility commitment and measures."), b)

# ------------------------------------------------------------------ governance
def build_governance(B):
    T, P, EMAIL, ARROW = B.T, B.P, B.EMAIL, B.ARROW
    path = "governance.html"; r = ""
    b = B.page_hero(r, [(path, B.OTHER[path])], ("Transparence", "Transparency"), B.OTHER[path],
        ("Comment nous choisissons nos sources, révisons nos contenus et corrigeons nos erreurs.", "How we choose our sources, review our content and fix our mistakes."))
    S = [
     (("Indépendance", "Independence"), T("Nous ne revendons ni logiciels ni matériel. Les plateformes citées le sont pour décrire notre expertise ; leur mention n'implique aucun partenariat officiel.", "We resell no software or hardware. Platforms are named to describe our expertise; naming them implies no official partnership.")),
     (("Sources et preuves", "Sources and evidence"), T("Les études de cas et les chiffres de coût d'interruption reposent uniquement sur des sources publiques, citées en bas de chaque page. Nous distinguons les faits rapportés des estimations, et nous indiquons lorsqu'un chiffre est une estimation d'analyste ou d'enquête. Les chiffres varient selon la méthode : ce sont des ordres de grandeur.", "Case studies and downtime-cost figures rely solely on public sources, cited at the bottom of each page. We distinguish reported facts from estimates, and we say when a figure is an analyst or survey estimate. Figures vary with method: they are orders of magnitude.")),
     (("Révision des contenus", "Content review"), T("Nous visons une révision de chaque page au moins une fois par an, et plus tôt lorsqu'une réglementation ou un fait cité change. Lorsqu'une page a fait l'objet d'une révision de ses sources, la date de révision est affichée sous son titre.", "We aim to review each page at least once a year, and sooner when a regulation or a cited fact changes. When a page has had its sources reviewed, the review date is shown under its title.")),
     (("Politique de correction", "Corrections policy"), T(f'Si vous relevez une erreur, écrivez à <a href="mailto:{EMAIL}">{EMAIL}</a>. Nous vérifions auprès de la source, corrigeons rapidement, et consignons toute correction substantielle dans le journal ci-dessous.', f'If you spot an error, email <a href="mailto:{EMAIL}">{EMAIL}</a>. We check against the source, fix it promptly, and record any substantive correction in the log below.')),
     (("Journal des corrections", "Corrections log"), "<ul><li><strong>" + fmt_date("2026-10-26", B.LANG) + ".</strong> " + T("Page « Coût des interruptions » : chiffres d'Amazon Prime Day 2018, de Southwest Airlines et du secteur manufacturier revérifiés auprès des sources et corrigés ; sources remplacées par des sources primaires.", "“Cost of downtime” page: figures for Amazon Prime Day 2018, Southwest Airlines and the manufacturing sector re-checked against sources and corrected; sources replaced with primary ones.") + "</li></ul>"),
     (("Protection des renseignements", "Privacy practices"), T(f'Nous tenons un registre interne des traitements de renseignements personnels et supprimons les échanges avec les prospects au plus tard trois ans après le dernier contact. Voir la <a href="{r}privacy.html">politique de confidentialité</a>.', f'We keep an internal register of personal-information processing and delete exchanges with prospects no later than three years after the last contact. See the <a href="{r}privacy.html">privacy policy</a>.')),
    ]
    b += '<section class="block legal">' + "".join(f"<h2>{P(h)}</h2>{body if body.startswith('<') else '<p>'+body+'</p>'}" for h, body in S) + "</section>"
    B.page(path, ("Gouvernance et corrections | FZ Consultation", "Governance and corrections | FZ Consultation"), ("Sources, révision des contenus et politique de correction de FZ Consultation.", "FZ Consultation's sources, content review and corrections policy."), b)
