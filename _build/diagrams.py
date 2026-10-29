# Hand-drawn SVG diagrams for the AI pages.
#  - citadel_diagram: a layered architecture (fortress) showing the request path through the four Citadel layers.
#  - auditor_diagram: four instrument panels (scope, value, blast radius, containment) on dark cards, deliberately unlike the Citadel.
# All text goes through B.T / B.E so both languages work. Motion is CSS-only and switched off for prefers-reduced-motion.

def citadel_diagram(B):
    T, E = B.T, B.E
    t = lambda fr, en: T(fr, en)
    def chip(x, y, w, label):
        return f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" class="cd-chip"/><text x="{x+w/2}" y="{y+17}" text-anchor="middle" class="cd-chiptxt">{label}</text>'
    def card(x, y, w, h, title, sub, chips, cls=""):
        wc = 'cd-l4' if cls == 'cd-l4' else ''
        o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="cd-card {cls}"/>'
        o += f'<text x="{x+18}" y="{y+28}" class="cd-h {wc}">{title}</text><text x="{x+18}" y="{y+47}" class="cd-sub {wc}">{sub}</text>'
        cx, cy = x + 18, y + 62
        for lab, w2 in chips:
            if cx + w2 > x + w - 12: cx = x + 18; cy += 32
            o += chip(cx, cy, w2, lab); cx += w2 + 8
        return o
    s = []
    s.append(f'<svg class="citdiag" viewBox="0 0 1000 704" role="img" aria-labelledby="cd-t cd-d">')
    s.append(f'<title id="cd-t">{t("Architecture en couches de Citadel", "Layered architecture of Citadel")}</title>')
    s.append(f'<desc id="cd-d">{t("Les applications et agents passent par une passerelle IA gouvernée, au-dessus des opérations d&#39;agents et de l&#39;identité, sur un socle de sécurité, avant d&#39;atteindre les modèles, les outils et les données.", "Applications and agents pass through a governed AI gateway, above agent operations and identity, on a security foundation, before reaching models, tools and data.")}</desc>')
    s.append('<defs><marker id="cd-ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1l8 4-8 4z" class="cd-arhead"/></marker></defs>')
    # consumers
    s.append(f'<text x="500" y="22" text-anchor="middle" class="cd-eyebrow">{t("Qui appelle", "Who calls")}</text>')
    for i, (fr, en) in enumerate([("Applications métier", "Business apps"), ("Agents", "Agents"), ("Copilotes", "Copilots")]):
        x = 150 + i * 240
        s.append(f'<rect x="{x}" y="34" width="200" height="40" rx="8" class="cd-ext"/><text x="{x+100}" y="59" text-anchor="middle" class="cd-exttxt">{t(fr, en)}</text>')
        s.append(f'<path d="M{x+100} 76V96" class="cd-flow" marker-end="url(#cd-ar)"/>')
    # fortress with battlements
    bx, by, bw = 40, 112, 920
    merl = "".join(f'<rect x="{bx+10+i*46}" y="{by-14}" width="30" height="16" class="cd-merl"/>' for i in range(20))
    s.append(merl)
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="470" rx="6" class="cd-wall"/>')
    s.append(f'<text x="{bx+22}" y="{by+30}" class="cd-fort">CITADEL</text>')
    s.append(f'<text x="{bx+bw-22}" y="{by+30}" text-anchor="end" class="cd-sub">{t("Plan de contrôle de l&#39;IA", "AI control plane")}</text>')
    # layer 1 gateway
    s.append(card(70, 158, 860, 126, t("Couche 1 · Hub de gouvernance", "Layer 1 · Governance hub"), t("Passerelle IA centrale (Azure API Management)", "Central AI gateway (Azure API Management)"),
        [(t("Contrôle d&#39;accès", "Access control"), 140), (t("Détection de données personnelles", "Personal data detection"), 230), (t("Sûreté du contenu", "Content safety"), 150), (t("Coûts et usage", "Cost and usage"), 130), (t("Limites de débit", "Rate limits"), 120)], "cd-l1"))
    # layers 2 & 3
    s.append(card(70, 304, 420, 142, t("Couche 2 · Opérations des agents", "Layer 2 · Agent operations"), t("Environnements par équipe (Foundry)", "Per-team environments (Foundry)"),
        [(t("Traces", "Traces"), 70), (t("Évaluations", "Evaluations"), 110), (t("Red-teaming", "Red-teaming"), 110)], "cd-l2"))
    s.append(card(510, 304, 420, 142, t("Couche 3 · Identité des agents", "Layer 3 · Agent identity"), t("Identité gérée (Microsoft Entra ID)", "Managed identity (Microsoft Entra ID)"),
        [(t("Responsable humain", "Human owner"), 140), (t("Cycle de vie", "Lifecycle"), 100), (t("Moindre privilège", "Least privilege"), 130)], "cd-l3"))
    # layer 4 foundation
    s.append(card(70, 466, 860, 96, t("Couche 4 · Socle de sécurité", "Layer 4 · Security fabric"), t("Protection contre les menaces et gouvernance des données", "Threat protection and data governance"),
        [], "cd-l4"))
    s.append(chip(612, 506, 150, "Microsoft Defender") + chip(772, 506, 140, "Microsoft Purview"))
    # internal arrows
    
    # outbound
    s.append(f'<text x="500" y="696" text-anchor="middle" class="cd-eyebrow">{t("Ce qui est appelé", "What is called")}</text>')
    for i, (fr, en) in enumerate([("Modèles", "Models"), ("Outils", "Tools"), ("Données", "Data")]):
        x = 150 + i * 240
        s.append(f'<path d="M{x+100} 584V624" class="cd-flow" marker-end="url(#cd-ar)"/>')
        s.append(f'<rect x="{x}" y="636" width="200" height="40" rx="8" class="cd-ext"/><text x="{x+100}" y="661" text-anchor="middle" class="cd-exttxt">{t(fr, en)}</text>')
    s.append('</svg>')
    return '<figure class="cit-wrap">' + "".join(s) + f'<figcaption>{t("Le chemin d&#39;un appel : rien n&#39;atteint un modèle, un outil ou une donnée sans traverser la passerelle, et chaque couche laisse une trace.", "The path of a call: nothing reaches a model, tool or dataset without crossing the gateway, and every layer leaves a trace.")}</figcaption></figure>'


def auditor_diagram(B):
    T, E = B.T, B.E
    t = lambda fr, en: T(fr, en)
    def panel(n, title, q, body, cap):
        return (f'<div class="aud-panel"><div class="aud-top"><span class="aud-n">{n}</span><span class="aud-tag">{t("Illustratif", "Illustrative")}</span></div>'
                f'<h3>{title}</h3><p class="aud-q">{q}</p>{body}<p class="aud-cap">{cap}</p></div>')
    # 1 scope: authorized vs observed
    scope = ('<svg viewBox="0 0 260 150" role="img" aria-label="' + t("Deux cercles : périmètre autorisé et comportement observé, avec une zone de dérive", "Two circles: authorized scope and observed behavior, with a drift zone") + '">'
             '<circle cx="100" cy="75" r="58" class="au-auth"/><circle cx="150" cy="75" r="58" class="au-obs"/>'
             f'<text x="60" y="78" text-anchor="middle" class="au-t">{t("Autorisé", "Authorized")}</text>'
             f'<text x="198" y="78" text-anchor="middle" class="au-t warn">{t("Dérive", "Drift")}</text>'
             f'<text x="125" y="78" text-anchor="middle" class="au-t dim">{t("Conforme", "In scope")}</text>'
             f'<text x="100" y="12" text-anchor="middle" class="au-s">{t("Conçu", "Designed")}</text><text x="150" y="146" text-anchor="middle" class="au-s">{t("Observé en production", "Observed in production")}</text></svg>')
    # 2 value: bars
    value = ('<svg viewBox="0 0 260 150" role="img" aria-label="' + t("Barres comparant le coût d&#39;exploitation et le coût évité, avec une ligne de référence humaine", "Bars comparing running cost and cost avoided, with a human baseline line") + '">'
             '<line x1="20" y1="128" x2="250" y2="128" class="au-axis"/>'
             '<rect x="40" y="58" width="56" height="70" class="au-bar a"/><rect x="120" y="28" width="56" height="100" class="au-bar b"/><rect x="200" y="78" width="40" height="50" class="au-bar c"/>'
             '<line x1="20" y1="48" x2="250" y2="48" class="au-base"/>'
             f'<text x="22" y="41" class="au-s">{t("Référence humaine", "Human baseline")}</text>'
             f'<text x="68" y="143" text-anchor="middle" class="au-s">{t("Coût", "Cost")}</text><text x="148" y="143" text-anchor="middle" class="au-s">{t("Évité", "Avoided")}</text><text x="220" y="143" text-anchor="middle" class="au-s">{t("Qualité", "Quality")}</text></svg>')
    # 3 blast radius: rings
    blast = ('<svg viewBox="0 0 260 150" role="img" aria-label="' + t("Anneaux concentriques : cas touchés, gravité, délai de détection", "Concentric rings: cases touched, severity, time to detect") + '">'
             '<circle cx="130" cy="75" r="68" class="au-ring r3"/><circle cx="130" cy="75" r="46" class="au-ring r2"/><circle cx="130" cy="75" r="24" class="au-ring r1"/><circle cx="130" cy="75" r="5" class="au-dot"/>'
             f'<text x="130" y="21" text-anchor="middle" class="au-s">{t("Détection", "Detection")}</text><text x="130" y="43" text-anchor="middle" class="au-s">{t("Gravité", "Severity")}</text><text x="130" y="65" text-anchor="middle" class="au-s on">{t("Cas", "Cases")}</text></svg>')
    # 4 containment: controls vs required
    rows = [(t("Arrêt d&#39;urgence", "Kill switch"), True), (t("Revue par échantillon", "Sampled review"), True), (t("Déploiement progressif", "Staged rollout"), False), (t("Responsable humain", "Human owner"), True)]
    ctl = '<svg viewBox="0 0 260 150" role="img" aria-label="' + t("Liste de contrôles, dont un manquant", "Control checklist with one missing") + '">'
    for i, (lab, ok) in enumerate(rows):
        y = 14 + i * 34
        ctl += f'<rect x="10" y="{y}" width="240" height="26" rx="6" class="au-row"/>'
        ctl += (f'<circle cx="28" cy="{y+13}" r="8" class="au-ok"/><path d="M24 {y+13}l3 3 6-6" class="au-tick"/>' if ok else f'<circle cx="28" cy="{y+13}" r="8" class="au-miss"/><path d="M24.5 {y+9.5}l7 7M31.5 {y+9.5}l-7 7" class="au-tick"/>')
        ctl += f'<text x="46" y="{y+17}" class="au-t sm{"" if ok else " warn"}">{lab}</text>'
    ctl += '</svg>'
    out = '<div class="aud-grid">'
    out += panel("01", t("Fidélité au périmètre", "Scope fidelity"), t("Que fait l&#39;agent, comparé à ce qu&#39;on l&#39;a autorisé à faire ?", "What does the agent do, compared with what it was allowed to do?"), scope, t("Source : traces d&#39;exécution et journaux, pas le document de conception.", "Source: execution traces and logs, not the design document."))
    out += panel("02", t("Valeur réalisée", "Value realized"), t("Combien coûte-t-il à exploiter, et que fait-il vraiment économiser ?", "What does it cost to run, and what does it really save?"), value, t("Coût d&#39;exploitation, coût évité et qualité face à une référence humaine.", "Running cost, cost avoided and quality against a human baseline."))
    out += panel("03", t("Rayon d&#39;impact", "Blast radius"), t("S&#39;il se trompe, jusqu&#39;où cela va-t-il, et pendant combien de temps ?", "If it is wrong, how far does it go, and for how long?"), blast, t("Nombre de cas, gravité de chacun, délai avant qu&#39;on s&#39;en aperçoive.", "Number of cases, severity of each, time before anyone notices."))
    out += panel("04", t("Adéquation du confinement", "Containment fit"), t("Les contrôles en place correspondent-ils à ce que le risque exige ?", "Do the controls in place match what the risk demands?"), ctl, t("Chaque contrôle est vérifié, pas supposé.", "Each control is verified, not assumed."))
    return out + '</div>'
