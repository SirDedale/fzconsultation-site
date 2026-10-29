# Copy for the consolidated pages. Every string is a (fr, en) pair unless noted.
# Voice rule: say what we see go wrong, then what to do. No "we work with you to...".

# Retired page -> new home. build.py writes redirect stubs for each key and rewrites internal links.
REMAP = {
 "what-we-do/expertise/index.html": "what-we-do/index.html",
 "what-we-do/services/index.html": "what-we-do/index.html",
 "what-we-do/expertise/business-continuity.html": "what-we-do/index.html#know",
 "what-we-do/expertise/disaster-recovery.html": "what-we-do/index.html#prepare",
 "what-we-do/expertise/cybersecurity.html": "what-we-do/index.html#prepare",
 "what-we-do/expertise/cloud-resilience.html": "what-we-do/index.html#prepare",
 "what-we-do/services/assessments.html": "what-we-do/index.html#know",
 "what-we-do/services/planning.html": "what-we-do/index.html#prepare",
 "what-we-do/services/exercises.html": "what-we-do/index.html#prove",
 "what-we-do/services/advisory.html": "what-we-do/index.html#stay-ready",
 "what-we-do/industries/technology-saas.html": "what-we-do/industries.html#technology-saas",
 "what-we-do/industries/manufacturing-transport.html": "what-we-do/industries.html#manufacturing-transport",
 "what-we-do/industries/retail.html": "what-we-do/industries.html#retail",
 "what-we-do/industries/professional-services.html": "what-we-do/industries.html#professional-services",
 "what-we-do/industries/public-sector.html": "what-we-do/industries.html#public-sector",
 "ai/strategy-adoption.html": "ai/index.html#strategy",
 "ai/agents.html": "ai/index.html#agents",
 "ai/governance.html": "ai/index.html#governance",
 "resources/cost-of-downtime.html": "resources/downtime-calculator.html#benchmarks",
 "resources/rto-rpo-worksheet.html": "resources/index.html#rto-rpo-worksheet",
 "resources/ai-acceptable-use-policy.html": "resources/index.html#ai-acceptable-use-policy",
 "resources/ai-agent-audit-scorecard.html": "resources/index.html#ai-agent-audit-scorecard",
}
COMPACT_IND = ["technology-saas", "manufacturing-transport", "retail", "professional-services", "public-sector"]
FEATURED_IND = ["financial-services", "healthcare", "energy-utilities"]

# Names for the link text that points at an anchor.
ANCHOR_NAMES = {
 "what-we-do/index.html": ("Ce que nous faisons", "What we do"),
 "what-we-do/index.html#know": ("Savoir : mesurer ce qu'un arrêt coûterait", "Know: measure what stopping would cost"),
 "what-we-do/index.html#prepare": ("Préparer : une reprise qui tient", "Prepare: recovery that holds"),
 "what-we-do/index.html#prove": ("Prouver : répéter avant le vrai jour", "Prove: rehearse before the real day"),
 "what-we-do/index.html#stay-ready": ("Rester prêt : suivre dans la durée", "Stay ready: follow through"),
 "ai/index.html#strategy": ("Stratégie et adoption de l'IA", "AI strategy and adoption"),
 "ai/index.html#agents": ("Conception d'agents IA", "AI agent design"),
 "ai/index.html#governance": ("Gouvernance et risques de l'IA", "AI governance and risk"),
 "resources/downtime-calculator.html#benchmarks": ("Repères de coût par secteur", "Cost benchmarks by industry"),
 "resources/index.html#rto-rpo-worksheet": ("Feuille de travail RTO/RPO", "RTO/RPO worksheet"),
 "resources/index.html#ai-acceptable-use-policy": ("Politique d'utilisation de l'IA", "AI acceptable-use policy"),
 "resources/index.html#ai-agent-audit-scorecard": ("Tableau d'audit d'agents IA", "AI agent audit scorecard"),
}

# ---------------------------------------------------------------- What we do
WWD_HERO = {
 "title": ("Savoir ce que vous perdriez. Le corriger. Le prouver. Continuer de le prouver.", "Know what you'd lose. Fix it. Prove it. Keep proving it."),
 "lede": ("La résilience n'est pas un document. C'est un chiffre que vous avez mesuré en répétition, avant le vrai jour difficile. Voici nos quatre tâches, dans l'ordre où elles servent.",
          "Resilience is not a document. It is a number you measured in a rehearsal, before the real bad day. These are our four jobs, in the order they pay off."),
}

OUTCOMES = [
 {"id": "know",
  "name": ("Savoir", "Know"),
  "title": ("Combien coûterait un arrêt, et à quelle vitesse faut-il repartir ?", "What would stopping cost, and how fast must you restart?"),
  "stance": ("Presque partout, les objectifs de reprise ont été fixés par la TI d'après ce que les systèmes savent faire, pas par l'entreprise d'après ce qu'elle peut supporter. C'est à l'envers, et c'est pourquoi le premier vrai incident casse le plan.",
             "Almost everywhere, recovery targets were set by IT from what the systems can do, not by the business from what it can bear. That is backwards, and it is why the first real incident breaks the plan."),
  "do": [
   (("Analyse d'impact sur les activités", "Business impact analysis"), ("Des entretiens avec ceux qui font tourner les services, pas seulement ceux qui possèdent les serveurs. Résultat : combien de temps chaque service peut s'arrêter avant que les dégâts soient inacceptables.",
                                     "Interviews with the people who run the services, not only those who own the servers. Output: how long each service can stop before the damage is unacceptable.")),
   (("Carte des dépendances et des tiers", "Dependency and third-party map"), ("La panne qui fait mal vient presque toujours d'une dépendance que personne n'avait listée : un fournisseur d'identité, un processeur de paiement, une seule région infonuagique, un outil de sécurité installé partout.",
                                     "The outage that hurts almost always comes from a dependency nobody listed: an identity provider, a payment processor, a single cloud region, a security tool installed everywhere.")),
   (("Cibles RTO et RPO", "RTO and RPO targets"), ("Signées par le responsable d'affaires, avec le coût pour les atteindre à côté du coût de les manquer.", "Signed off by the business owner, with the cost of meeting them next to the cost of missing them.")),
  ],
  "get": [
   ("Rapport de constats et indice de maturité", "Findings report and maturity score"),
   ("Registre des services essentiels et de leurs dépendances", "Register of essential services and dependencies"),
   ("Cibles RTO et RPO approuvées par la direction", "RTO and RPO targets signed off by leadership"),
   ("Feuille de route priorisée et présentation à la direction", "Prioritized roadmap and executive readout"),
  ],
  "start": [("resources/downtime-calculator.html", ("Chiffrer une heure d'arrêt", "Put a number on an hour of downtime")),
            ("resources/rto-rpo-worksheet.html", ("Remplir la feuille RTO/RPO", "Fill in the RTO/RPO worksheet")),
            ("self-assessment.html", ("Faire l'auto-évaluation (8 minutes)", "Take the self-assessment (8 minutes)"))],
 },
 {"id": "prepare",
  "name": ("Préparer", "Prepare"),
  "title": ("Une reprise bâtie pour un mauvais jour, pas pour un bon.", "Recovery built for a bad day, not a good one."),
  "stance": ("Une sauvegarde est une copie. La reprise est une capacité. La plupart des organisations possèdent la première et supposent la seconde.",
             "A backup is a copy. Recovery is a capability. Most organizations own the first and assume the second."),
  "do": [
   (("Architecture de reprise et procédures", "Recovery architecture and runbooks"), ("Des procédures pas à pas, écrites avec ceux qui les exécuteront, et mesurées contre la cible de temps de reprise. Une procédure que seul son auteur sait suivre n'est pas une procédure.",
                                     "Step-by-step runbooks, written with the people who will run them and timed against the recovery target. A runbook only its author can follow is not a runbook.")),
   (("Sauvegardes qui survivent à une attaque", "Backups that survive an attack"), ("Copies isolées ou immuables, comptes d'administration distincts, et une restauration réellement faite par quelqu'un d'autre que la personne qui l'a configurée.",
                                     "Isolated or immutable copies, separate administration accounts, and a restore actually performed by someone other than the person who set it up.")),
   (("Identités et accès à distance", "Identity and remote access"), ("Authentification multifacteur partout où quelque chose est exposé, comptes inactifs supprimés, réinitialisations de mot de passe vérifiées. C'est la porte d'entrée de plusieurs des incidents étudiés sur ce site.",
                                     "Multi-factor authentication wherever anything is exposed, inactive accounts removed, password resets verified. It is the way in for several of the incidents studied on this site.")),
   (("Concentration infonuagique et fournisseurs", "Cloud and vendor concentration"), ("Une seule région, un seul fournisseur, un seul plan de contrôle : que faites-vous quand la page d'état est rouge ? Nous cherchons les points de défaillance uniques et proposons des correctifs proportionnés au risque.",
                                     "One region, one provider, one control plane: what do you do when the status page is red? We look for single points of failure and propose fixes proportionate to the risk.")),
   (("Plans de continuité et de crise", "Continuity and crisis plans"), ("Courts, à jour, utilisables sous pression, et écrits avec vos équipes. Ils couvrent les personnes, les sites, les fournisseurs et la communication, pas seulement l'informatique.",
                                     "Short, current, usable under pressure, and written with your teams. They cover people, sites, suppliers and communication, not only IT.")),
  ],
  "get": [
   ("Stratégie et architecture de reprise, procédures pas à pas", "Recovery strategy and architecture, step-by-step runbooks"),
   ("Liste des points de défaillance uniques, classée par risque", "List of single points of failure, ranked by risk"),
   ("Plan de réponse aux incidents et scénarios", "Incident response plan and playbooks"),
   ("Plans de continuité et de gestion de crise, modèles de communication", "Continuity and crisis management plans, communication templates"),
  ],
  "start": [("resources/ransomware-checklist.html", ("Liste de vérification rançongiciel", "Ransomware checklist")),
            ("insights/backups-are-not-recovery.html", ("Une sauvegarde n'est pas une reprise", "A backup is not a recovery")),
            ("case-studies/aws-us-east-1-2025.html", ("Étude de cas : AWS us-east-1", "Case study: AWS us-east-1"))],
 },
 {"id": "prove",
  "name": ("Prouver", "Prove"),
  "title": ("Ce que vous n'avez pas répété, vous l'avez seulement espéré.", "What you haven't rehearsed, you have only hoped."),
  "stance": ("Le premier test échoue presque toujours. C'est son intérêt : chaque blocage trouvé en exercice est un blocage que vous ne découvrirez pas pendant l'incident.",
             "The first test almost always fails. That is its value: every blocker found in a rehearsal is one you will not discover during the incident."),
  "do": [
   (("Exercices sur table", "Tabletop exercises"), ("La direction et les équipes face à un scénario réaliste de votre secteur, avec un journal de décisions. On y découvre qui décide, qui ne répond pas, et ce que personne n'avait prévu.", "Leadership and teams facing a realistic scenario from your sector, with a decision log. You find out who decides, who does not answer, and what nobody planned for.")),
   (("Tests techniques de restauration et de bascule", "Technical restore and failover tests"), ("Chronométrés, contre la cible, avec la documentation telle qu'elle existe aujourd'hui. Y compris la perte d'une région, pas seulement d'un serveur.", "Timed against the target, using the documentation as it exists today. Including the loss of a region, not only a server.")),
   (("Simulations de crise", "Crisis simulations"), ("La communication sous pression, hors bande : ce que vous dites au personnel, aux clients et aux médias quand vos outils habituels sont inaccessibles.", "Communication under pressure, out of band: what you tell staff, customers and the media when your usual tools are unreachable.")),
  ],
  "get": [
   ("Scénarios et trousse d'exercice", "Scenario and exercise pack"),
   ("Rapport post-exercice", "After-action report"),
   ("Plan de correction priorisé", "Prioritized remediation plan"),
  ],
  "start": [("resources/rto-rpo-worksheet.html", ("Remplir la feuille RTO/RPO", "Fill in the RTO/RPO worksheet")),
            ("case-studies/index.html", ("Lire les incidents et leurs vérifications du lundi", "Read the incidents and their Monday checks"))],
 },
 {"id": "stay-ready",
  "name": ("Rester prêt", "Stay ready"),
  "title": ("La résilience s'use. Planifiez l'usure.", "Resilience decays. Plan for the decay."),
  "stance": ("Les environnements changent plus vite que les plans. Un plan vieux d'un an décrit une entreprise qui n'existe plus.", "Environments change faster than plans. A plan older than a year describes a company that no longer exists."),
  "do": [
   (("Revue trimestrielle de résilience", "Quarterly resilience review"), ("Ce qui a changé, ce qui a cassé en test, ce qui reste ouvert. Un tableau de bord des risques et des actions que la direction lit vraiment.", "What changed, what broke in testing, what is still open. A risk and action dashboard leadership actually reads.")),
   (("Préparation réglementaire", "Regulatory readiness"), ("DORA, NIS2, FCA/PRA, BSIF, SOC 2 : des preuves plutôt que des documents, et un soutien pour les audits et les questionnaires de clients.", "DORA, NIS2, FCA/PRA, OSFI, SOC 2: evidence rather than documents, and support for audits and customer questionnaires.")),
   (("Agents IA : un nouvel audit à chaque changement", "AI agents: re-audit on every change"), ("Un modèle, une consigne ou une permission qui change déplace le rayon d'impact. FZ AI Auditor refait la mesure à chaque changement important.", "A model, prompt or permission change moves the blast radius. FZ AI Auditor re-runs the measurement on every material change.")),
  ],
  "get": [
   ("Revue trimestrielle de résilience", "Quarterly resilience review"),
   ("Tableau de bord des risques et des actions", "Risk and action dashboard"),
   ("Soutien aux audits et aux questionnaires de clients", "Support for audits and customer questionnaires"),
  ],
  "start": [("what-we-do/regulations.html", ("Exigences par région", "Requirements by region")),
            ("ai/auditor.html", ("FZ AI Auditor", "FZ AI Auditor"))],
 },
]

WWD_FAQ_QUESTIONS = [  # English question text -> pulled from the existing FAQs
 "Where should we start?",
 "How are you different from a reseller or integrator?",
 "Aren't our backups enough?",
 "Isn't being in the cloud already disaster recovery?",
 "Do you run penetration tests?",
 "Can exercises be run remotely?",
 "Do you provide legal advice on compliance?",
]

WWD_HOW = {
 "title": ("Comment nous travaillons", "How we work"),
 "big": ("Indépendants, par principe. Nous ne revendons ni logiciels ni matériel, et nous travaillons sur les plateformes que vous avez déjà choisies. Chaque recommandation part de vos besoins, pas du catalogue d'un fournisseur. En français ou en anglais, à distance ou sur place.",
         "Independent, by design. We resell no software or hardware, and we work on the platforms you have already chosen. Every recommendation starts from your needs, not a vendor's catalogue. In French or English, remote or on site."),
}

# ---------------------------------------------------------------- Sectors
SECTOR_STANCE = {
 "financial-services": ("Les régulateurs ne demandent plus si vous avez un plan. Ils demandent si vous avez prouvé que vous restez dans votre tolérance d'impact.",
                        "Regulators no longer ask whether you have a plan. They ask whether you have proved you stay within your impact tolerance."),
 "healthcare": ("À l'hôpital, le plan de panne est un processus papier. S'il n'a pas été répété cette année, vous n'en avez pas.",
                "In a hospital the outage plan is a paper process. If it has not been rehearsed this year, you do not have one."),
 "energy-utilities": ("La vraie question n'est pas « sommes-nous attaqués ? » mais « sur quel critère arrêtons-nous nous-mêmes, et pouvons-nous continuer sans la TI ? »",
                      "The real question is not “are we under attack?” but “on what criterion do we stop ourselves, and can we run without IT?”"),
}
IND_HUB = {
 "title": ("Trois secteurs en détail, cinq en bref", "Three sectors in depth, five in brief"),
 "lede": ("Chaque secteur casse à sa manière. Les trois premiers ont leur page complète ; les autres tiennent en quelques lignes ci-dessous.",
          "Every sector breaks in its own way. The first three have full pages; the others fit in a few lines below."),
}

# ---------------------------------------------------------------- AI
AI_EU = {
 "title": ("Le calendrier du règlement européen sur l'IA a changé", "The EU AI Act calendar has changed"),
 "intro": ("Le « Digital Omnibus » (règlement (UE) 2026/1744) est en vigueur. Voici les dates à retenir, d'après le résumé d'Orrick du 29 juillet 2026. Vérifiez-les avec vos conseillers juridiques et le texte au Journal officiel.",
           "The Digital Omnibus (Regulation (EU) 2026/1744) is in force. These are the dates to know, based on Orrick's 29 July 2026 summary. Check them with your legal advisers and the text in the Official Journal."),
 "rows": [
  (("2 décembre 2026", "2 December 2026"), ("Transparence de l'article 50(2) (contenus synthétiques) pour les systèmes mis sur le marché avant le 2 août 2026 ; nouvelles interdictions de l'article 5 (images intimes non consenties et matériel d'abus sexuel d'enfants).",
                                          "Article 50(2) transparency (synthetic content) for systems placed on the market before 2 August 2026; new Article 5 prohibitions (non-consensual intimate imagery and child sexual abuse material).")),
  (("2 décembre 2027", "2 December 2027"), ("Obligations des systèmes à haut risque de l'annexe III (au lieu du 2 août 2026). Les systèmes déjà sur le marché ne sont visés que s'ils sont substantiellement modifiés après cette date.",
                                          "Obligations for Annex III high-risk systems (instead of 2 August 2026). Systems already on the market are covered only if substantially modified after that date.")),
  (("2 août 2028", "2 August 2028"), ("Obligations des systèmes à haut risque de l'annexe I (produits réglementés). Date limite de la Commission pour l'acte délégué sur les chevauchements sectoriels.", "Obligations for Annex I high-risk systems (regulated products). Deadline for the Commission's delegated act on sector overlaps.")),
  (("2 août 2030", "2 August 2030"), ("Conformité des systèmes d'IA destinés aux autorités publiques.", "Compliance for AI systems intended for public authorities.")),
 ],
 "note": ("Source : Orrick, « EU AI Act Update: Digital Omnibus Finalizes 8 Compliance Changes », 29 juillet 2026. Cette page a été corrigée le 29 octobre 2026 : elle indiquait auparavant un calendrier sans dates.",
          "Source: Orrick, “EU AI Act Update: Digital Omnibus Finalizes 8 Compliance Changes”, 29 July 2026. This page was corrected on 29 October 2026: it previously described the calendar without dates."),
 "src": ("Orrick: EU AI Act Update, Digital Omnibus Finalizes 8 Compliance Changes", "https://www.orrick.com/en/Insights/2026/07/EU-AI-Act-Update-Digital-Omnibus-Finalizes-8-Compliance-Changes"),
}
AI_HERO = {
 "title": ("Les agents agissent à grande échelle. Savez-vous ce qu'ils font ?", "Agents act at scale. Do you know what they are doing?"),
 "lede": ("Presque toutes les organisations savent lister leurs agents IA. Presque aucune ne sait dire, preuves à l'appui, ce qu'ils font, ce qu'ils valent et jusqu'où une seule erreur peut aller. C'est ce que nous mesurons, puis ce que nous aidons à construire et à gouverner.",
          "Almost every organization can list its AI agents. Almost none can say, with evidence, what they do, what they are worth and how far one mistake can go. That is what we measure, and then help build and govern."),
}

# ---------------------------------------------------------------- Home
HOME = {
 "h1": ("Découvrez ce qui casse pendant que ce n'est encore qu'une répétition.", "Find out what breaks while it is still a rehearsal."),
 "lede": ("FZ Consultation aide les organisations d'Europe, du Royaume-Uni, du Canada et des États-Unis à chiffrer ce qu'une panne leur coûterait, à bâtir une reprise qui tient et à la répéter avant le vrai jour.",
          "FZ Consultation helps organizations in Europe, the UK, Canada and the US put a number on what an outage would cost, build recovery that holds, and rehearse it before the real day."),
 "worries_h": ("Qu'est-ce qui vous empêche de dormir ?", "What keeps you up at night?"),
 "worries_i": ("Choisissez l'inquiétude la plus proche de la vôtre. Chacune mène à un incident réel, à un outil gratuit et à ce que nous ferions.", "Pick the worry closest to yours. Each leads to a real incident, a free tool and what we would do."),
 "worries": [
  {"h": ("Un rançongiciel", "Ransomware"),
   "p": ("Si des attaquants verrouillaient vos systèmes ce soir, pourriez-vous restaurer sans payer ?", "If attackers locked your systems tonight, could you restore without paying?"),
   "links": [("case", "case-studies/norsk-hydro-2019.html", ("Norsk Hydro refuse de payer", "Norsk Hydro refuses to pay")),
             ("tool", "resources/ransomware-checklist.html", ("Liste de vérification rançongiciel", "Ransomware checklist")),
             ("service", "what-we-do/index.html#prepare", ("Des sauvegardes qui survivent", "Backups that survive"))]},
  {"h": ("Une panne chez un fournisseur ou un nuage", "A cloud or vendor outage"),
   "p": ("Ce n'est pas votre panne, mais c'est vous qui la payez. Savez-vous de quoi vous dépendez ?", "It is not your outage, but you pay for it. Do you know what you depend on?"),
   "links": [("case", "case-studies/aws-us-east-1-2025.html", ("AWS us-east-1, octobre 2025", "AWS us-east-1, October 2025")),
             ("tool", "resources/downtime-calculator.html", ("Calculateur du coût d'une interruption", "Downtime cost calculator")),
             ("service", "what-we-do/index.html#know", ("Cartographier les dépendances", "Map the dependencies"))]},
  {"h": ("Un régulateur ou un auditeur pose la question", "A regulator or auditor asks"),
   "p": ("DORA, NIS2, FCA/PRA, BSIF. Avez-vous des preuves, ou seulement des documents ?", "DORA, NIS2, FCA/PRA, OSFI. Do you have evidence, or only documents?"),
   "links": [("case", "case-studies/tsb-2018.html", ("TSB : 48,65 M£ d'amende", "TSB: a £48.65m fine")),
             ("tool", "self-assessment.html", ("Auto-évaluation (8 minutes)", "Self-assessment (8 minutes)")),
             ("service", "what-we-do/index.html#stay-ready", ("Des preuves, en continu", "Evidence, continuously"))]},
  {"h": ("Des agents IA en production", "AI agents in production"),
   "p": ("Une erreur d'agent touche tous les cas traités avant que quelqu'un regarde. Savez-vous jusqu'où ?", "An agent error touches every case it handled before someone looked. Do you know how far?"),
   "links": [("case", "insights/three-questions-for-every-ai-agent.html", ("Trois questions pour chaque agent", "Three questions for every agent")),
             ("tool", "resources/ai-agent-audit-scorecard.html", ("Tableau d'audit d'agents IA", "AI agent audit scorecard")),
             ("service", "ai/auditor.html", ("FZ AI Auditor", "FZ AI Auditor"))]},
 ],
 "kinds": {"case": ("Lire", "Read"), "tool": ("Utiliser", "Use"), "service": ("Voir", "See")},
 "cases_h": ("Ce qui s'est vraiment passé, et ce qu'il faut vérifier lundi matin", "What really happened, and what to check on Monday morning"),
 "cases_i": ("Chaque étude de cas repose uniquement sur des sources publiques et se termine par trois vérifications à faire dans votre propre organisation.", "Every case study rests only on public sources and ends with three checks to run in your own organization."),
 "featured": ["aws-us-east-1-2025", "jaguar-land-rover-2025", "marks-and-spencer-2025"],
 "tools_h": ("À essayer aujourd'hui, sans nous appeler", "Try today, without calling us"),
 "jobs_h": ("Quatre tâches, dans cet ordre", "Four jobs, in this order"),
}

# ---------------------------------------------------------------- Contextual calls to action
# (headline, text, [(label_pair, href_key)]) chosen by page path or prefix; first match wins.
CTX_BOOK = ("Réserver 30 minutes", "Book 30 minutes")
CTX = [
 ("index.html", "@default"),
 ("contact.html", None), ("search.html", None), ("privacy.html", None), ("legal.html", None),
 ("accessibility.html", None), ("governance.html", None), ("security.html", None),
 ("self-assessment.html", None), ("resources/glossary.html", None),
 ("what-we-do/index.html", (("Vous ne savez pas par laquelle commencer ?", "Not sure which of the four to start with?"),
     ("L'auto-évaluation prend huit minutes et vous dit quel domaine est votre point le plus fragile. On en parle ensuite, si vous voulez.", "The self-assessment takes eight minutes and tells you which area is your weakest. We can talk about it afterwards, if you like."),
     [(("Faire l'auto-évaluation", "Take the self-assessment"), "self-assessment.html"), (CTX_BOOK, "@book")])),
 ("what-we-do/methodology.html", (("Voyez le cycle à l'œuvre", "See the cycle at work"), ("Les études de cas montrent chaque étape là où elle a manqué.", "The case studies show each step where it was missing."),
     [(("Lire les études de cas", "Read the case studies"), "case-studies/index.html")])),
 ("what-we-do/regulations.html", (("Quelles règles s'appliquent vraiment à vous ?", "Which of these rules really apply to you?"),
     ("Cela dépend de votre rôle, de vos marchés et de vos fournisseurs. Trente minutes suffisent pour faire le tri.", "It depends on your role, your markets and your suppliers. Thirty minutes is enough to sort it out."),
     [(CTX_BOOK, "@book"), (("Faire l'auto-évaluation", "Take the self-assessment"), "self-assessment.html")])),
 ("what-we-do/industries", (("Commencez par l'incident le plus proche de votre secteur", "Start with the incident closest to your sector"),
     ("Chaque étude de cas se termine par trois vérifications à faire lundi matin.", "Every case study ends with three checks for Monday morning."),
     [(("Voir les études de cas", "See the case studies"), "case-studies/index.html"), (CTX_BOOK, "@book")])),
 ("case-studies/index.html", (("Lequel de ces incidents pourrait être le vôtre ?", "Which of these incidents could be yours?"),
     ("L'auto-évaluation vous situe en huit minutes. Ensuite, nous pouvons regarder votre cas précis.", "The self-assessment places you in eight minutes. Then we can look at your specific case."),
     [(("Faire l'auto-évaluation", "Take the self-assessment"), "self-assessment.html"), (CTX_BOOK, "@book")])),
 ("case-studies/", "@case"),
 ("ai/auditor.html", (("Cadrer un audit de vos agents", "Scope an audit of your agents"),
     ("Commencez par le tableau d'audit gratuit : remplissez une ligne par agent. Puis dites-nous ce que vous y avez trouvé.", "Start with the free audit scorecard: fill in one row per agent. Then tell us what you found."),
     [(("Écrire au sujet de FZ AI Auditor", "Write to us about FZ AI Auditor"), "contact.html?topic=auditor"), (("Télécharger le tableau d'audit", "Get the audit scorecard"), "resources/index.html#ai-agent-audit-scorecard")])),
 ("ai/citadel.html", (("Prêt à cadrer votre plateforme ?", "Ready to frame your platform?"), ("Le questionnaire de vision aligne votre direction en sept minutes.", "The vision questionnaire aligns your leadership in seven minutes."),
     [(("Faire le questionnaire de vision", "Take the vision questionnaire"), "ai/vision-questionnaire.html"), (CTX_BOOK, "@book")])),
 ("ai/vision-questionnaire.html", None),
 ("ai/", (("Commencez par la question la plus simple", "Start with the simplest question"),
     ("Combien d'agents avez-vous en production, et qui peut en arrêter un ? Si la réponse prend plus d'une minute, parlons-en.", "How many agents do you have in production, and who can stop one? If answering takes more than a minute, let's talk."),
     [(("Faire le questionnaire de vision", "Take the vision questionnaire"), "ai/vision-questionnaire.html"), (CTX_BOOK, "@book")])),
 ("resources/downtime-calculator.html", (("Ce chiffre est une estimation. Le vrai se mesure.", "That figure is an estimate. The real one is measured."),
     ("Une analyse d'impact sur les activités remplace vos hypothèses par des entretiens et des preuves.", "A business impact analysis replaces your assumptions with interviews and evidence."),
     [(("Voir comment nous le mesurons", "See how we measure it"), "what-we-do/index.html#know"), (CTX_BOOK, "@book")])),
 ("resources/ransomware-checklist.html", (("Une liste ne remplace pas une répétition", "A list is not a rehearsal"), ("Un exercice sur table montre en trois heures ce que la liste ne dit pas.", "A tabletop exercise shows in three hours what the list cannot."),
     [(("Voir les exercices", "See the exercises"), "what-we-do/index.html#prove"), (CTX_BOOK, "@book")])),
 ("resources/", (("Vous avez un modèle. Vous voulez un deuxième avis ?", "You have a template. Want a second opinion?"), ("Envoyez-nous ce que vous avez rempli ; nous vous dirons ce qui manque.", "Send us what you filled in and we will tell you what is missing."),
     [(("Nous écrire", "Write to us"), "contact.html?topic=intro"), (CTX_BOOK, "@book")])),
 ("insights/index.html", (("Un sujet que vous voudriez voir traité ?", "A topic you would like covered?"), ("Dites-le-nous. Les notes mensuelles partent souvent d'une question de lecteur.", "Tell us. The monthly notes often start from a reader's question."),
     [(("Proposer un sujet", "Suggest a topic"), "contact.html?topic=other")])),
 ("insights/", (("Cela ressemble à votre situation ?", "Does this sound like your situation?"), ("Trente minutes suffisent pour dire par où commencer.", "Thirty minutes is enough to say where to start."),
     [(CTX_BOOK, "@book"), (("Faire l'auto-évaluation", "Take the self-assessment"), "self-assessment.html")])),
 ("partners.html", (("Parlons partenariat", "Let's talk partnership"), ("Présentez votre organisation et vos clients ; nous verrons comment nous compléter.", "Tell us about your organization and clients, and we will see how we complement each other."),
     [(("Nous écrire", "Write to us"), "contact.html?topic=partnership")])),
]
CTX_DEFAULT = (("Parlons de votre prochaine panne, avant qu'elle n'arrive", "Let's talk about your next outage before it happens"),
               ("Un premier échange de 30 minutes, sans engagement, en français ou en anglais.", "A free 30-minute intro call, in French or English."),
               [(CTX_BOOK, "@book"), (("Nous écrire", "Write to us"), "contact.html")])

AI_STANCE = {
 "strategy": ("La plupart des organisations n'ont pas trop peu d'idées d'IA. Elles ont trop de pilotes, et aucun moyen de savoir lequel a rapporté quelque chose.",
              "Most organizations do not have too few AI ideas. They have too many pilots, and no way to tell which one paid off."),
 "agents": ("Un agent est un nouvel employé qui a un identifiant et aucun bon sens. Donnez-lui un périmètre, un responsable et un interrupteur d'arrêt.",
            "An agent is a new employee with a login and no common sense. Give it a scope, a manager and an off switch."),
 "governance": ("Une politique que personne ne suit est pire que pas de politique : elle donne l'illusion du contrôle. Gardez-la assez courte pour qu'on la suive.",
                "A policy nobody follows is worse than none: it creates the illusion of control. Keep it short enough to be followed."),
}
