# New page content. (fr, en) pairs.

QUIZ_DOMAINS = {
 "bc": (("Continuité des activités", "Business continuity"), "what-we-do/expertise/business-continuity.html"),
 "dr": (("Reprise après sinistre", "Disaster recovery"), "what-we-do/expertise/disaster-recovery.html"),
 "sec": (("Cybersécurité", "Cybersecurity"), "what-we-do/expertise/cybersecurity.html"),
 "tp": (("Tiers, nuage et exercices", "Third parties, cloud and exercises"), "what-we-do/expertise/cloud-resilience.html"),
}

QUIZ_OPTIONS = [
 ("Non", "No"),
 ("Partiellement", "Partly"),
 ("Oui", "Yes"),
 ("Oui, testé ou revu cette année", "Yes, tested or reviewed this year"),
]

QUIZ_INDUSTRIES = [
 ("Services financiers", "Financial services"), ("Santé", "Healthcare"), ("Technologie et SaaS", "Technology and SaaS"),
 ("Manufacture, transport et logistique", "Manufacturing, transport and logistics"), ("Énergie et services publics", "Energy and utilities"),
 ("Commerce de détail", "Retail"), ("Services professionnels", "Professional services"), ("Secteur public et OBNL", "Public sector and non-profits"),
 ("Autre", "Other"),
]
QUIZ_SIZES = [
 ("Moins de 50 employés", "Under 50 employees"), ("50 à 250 employés", "50 to 250 employees"),
 ("250 à 1 000 employés", "250 to 1,000 employees"), ("Plus de 1 000 employés", "Over 1,000 employees"),
]

# (domain, question, weight 1|2)
QUIZ = [
 ("bc", ("Vos services essentiels sont-ils identifiés et priorisés, avec l'impact d'une interruption dans le temps ?", "Are your essential services identified and prioritized, with the impact of an interruption over time?"), 2),
 ("bc", ("Avez-vous un plan de continuité qui couvre les personnes, les locaux et les fournisseurs, pas seulement l'informatique ?", "Do you have a continuity plan covering people, sites and suppliers, not just IT?"), 2),
 ("bc", ("Une cellule de crise et des messages types pour les employés, clients et régulateurs sont-ils prêts ?", "Are a crisis team and template messages for staff, customers and regulators ready?"), 1),
 ("bc", ("Vos fournisseurs critiques ont-ils été identifiés, avec un plan si l'un d'eux tombe en panne ?", "Have your critical suppliers been identified, with a plan if one of them fails?"), 1),
 ("bc", ("Vos plans de continuité ont-ils été mis à jour au cours des 12 derniers mois ?", "Have your continuity plans been updated in the last 12 months?"), 1),
 ("dr", ("Des cibles RTO et RPO sont-elles définies et approuvées par la direction ?", "Are RTO and RPO targets defined and approved by leadership?"), 2),
 ("dr", ("Disposez-vous d'une copie de sauvegarde isolée ou immuable, hors d'atteinte d'un attaquant ?", "Do you keep an isolated or immutable backup copy, out of an attacker's reach?"), 2),
 ("dr", ("Avez-vous restauré un système critique complet au cours des 12 derniers mois ?", "Have you restored a complete critical system in the last 12 months?"), 2),
 ("dr", ("Savez-vous, système par système, dans quel ordre les rétablir après une panne majeure ?", "Do you know, system by system, the order to restore them in after a major outage?"), 1),
 ("dr", ("Votre stratégie de reprise couvre-t-elle vos environnements sur site et infonuagiques ?", "Does your recovery strategy cover both on-premises and cloud environments?"), 1),
 ("sec", ("L'authentification multifacteur est-elle activée sur tous les accès distants et comptes administrateurs ?", "Is multi-factor authentication enabled on all remote access and admin accounts?"), 2),
 ("sec", ("Avez-vous un plan de réponse aux incidents avec des rôles et des contacts externes à jour ?", "Do you have an incident response plan with roles and up-to-date external contacts?"), 2),
 ("sec", ("Votre centre de services vérifie-t-il l'identité avant toute réinitialisation de mot de passe ou de MFA ?", "Does your help desk verify identity before any password or MFA reset?"), 1),
 ("sec", ("Vos systèmes exposés à Internet sont-ils corrigés selon un calendrier régulier ?", "Are your internet-facing systems patched on a regular schedule?"), 1),
 ("sec", ("Savez-vous quels comptes ont des droits d'administrateur sur votre annuaire ou vos systèmes critiques ?", "Do you know which accounts hold admin rights on your directory or critical systems?"), 1),
 ("tp", ("Connaissez-vous vos fournisseurs critiques et leur capacité de reprise ?", "Do you know your critical suppliers and their ability to recover?"), 1),
 ("tp", ("Les données de vos applications SaaS (Microsoft 365, Google Workspace…) sont-elles sauvegardées de façon indépendante ?", "Is the data in your SaaS applications (Microsoft 365, Google Workspace…) backed up independently?"), 2),
 ("tp", ("La direction a-t-elle participé à un exercice de crise au cours des 12 derniers mois ?", "Has leadership taken part in a crisis exercise in the last 12 months?"), 2),
 ("tp", ("Avez-vous une stratégie de sortie si un fournisseur infonuagique majeur devenait indisponible ?", "Do you have an exit strategy if a major cloud provider became unavailable?"), 1),
 ("tp", ("Vos exercices ou tests se terminent-ils par un plan de correction suivi jusqu'à sa réalisation ?", "Do your exercises or tests end with a remediation plan that gets followed through?"), 1),
]

# Narrative shown for the weakest domain in the results (2-3 sentences, no per-question hard sell).
QUIZ_NARRATIVE = {
 "bc": ("La continuité des activités semble être votre point le plus fragile. C'est souvent la zone la moins visible au quotidien, jusqu'à ce qu'une interruption touche autre chose que l'informatique : un site, un fournisseur, ou simplement la coordination entre équipes.",
        "Business continuity looks like your most fragile area. It's often the least visible day to day, until an interruption touches something other than IT: a site, a supplier, or simply coordination between teams."),
 "dr": ("La reprise après sinistre semble être votre point le plus fragile. Des sauvegardes qui existent sans jamais avoir été restaurées, ou des cibles de reprise qui n'ont jamais été validées par la direction, sont des lacunes courantes qui ne se révèlent que le jour où elles comptent.",
        "Disaster recovery looks like your most fragile area. Backups that exist but have never been restored, or recovery targets that have never been signed off by leadership, are common gaps that only surface on the day they matter."),
 "sec": ("La cybersécurité semble être votre point le plus fragile. Dans la plupart des incidents que nous avons étudiés, la porte d'entrée était simple à corriger a posteriori : un accès sans MFA, un compte oublié, un centre de services trop confiant.",
         "Cybersecurity looks like your most fragile area. In most incidents we've studied, the way in was simple to fix in hindsight: access without MFA, a forgotten account, a help desk too quick to trust."),
 "tp": ("Vos tiers, votre nuage et vos exercices semblent être votre point le plus fragile. Une organisation peut avoir de bons plans sur papier et rester exposée si elle n'a jamais vérifié ses fournisseurs critiques ou jamais testé ces plans en conditions réelles.",
        "Your third parties, cloud and exercises look like your most fragile area. An organization can have solid plans on paper and still be exposed if it has never checked its critical suppliers or never tested those plans under real conditions."),
}

QUIZ_UI = {
 "fr": {"intro_title": "Avant de commencer", "org_industry": "Votre secteur", "org_size": "Taille de votre organisation",
        "org_optional": "Ces deux réponses sont facultatives ; elles nous aident à mettre votre résultat en contexte.",
        "start": "Commencer", "q": "Question", "of": "sur", "next": "Suivant", "prev": "Précédent", "see": "Voir mon résultat", "restart": "Recommencer",
        "overall": "Score global", "by": "Par domaine", "narrative_title": "Ce que montrent vos réponses",
        "bands": ["Exposé", "En développement", "Solide"],
        "bandtxt": ["Plusieurs fondations manquent. Un incident sérieux aurait probablement un impact important et durable.",
                    "Les bases existent, mais des écarts importants subsistent, surtout sur ce qui n'a pas été testé.",
                    "Votre organisation est bien préparée. L'enjeu est maintenant de tester régulièrement et de garder les plans à jour."],
        "context_lede": "Pour une organisation de votre taille dans le secteur", "context_mid": ", une heure d'interruption se chiffre souvent en dizaines ou centaines de milliers de dollars.",
        "context_link": "Voir les ordres de grandeur par secteur",
        "no_single": "Il n'y a pas de recette unique ici : la meilleure prochaine étape dépend de contraintes que ce questionnaire ne connaît pas — votre budget, vos échéances réglementaires, ce qui s'est déjà passé chez vous.",
        "cta": "Discuter de mes résultats avec nous", "print": "Imprimer", "copy": "Copier le résumé", "copied": "Copié"},
 "en": {"intro_title": "Before you start", "org_industry": "Your industry", "org_size": "Size of your organization",
        "org_optional": "Both answers are optional; they help us put your result in context.",
        "start": "Start", "q": "Question", "of": "of", "next": "Next", "prev": "Back", "see": "See my result", "restart": "Start again",
        "overall": "Overall score", "by": "By area", "narrative_title": "What your answers show",
        "bands": ["Exposed", "Developing", "Solid"],
        "bandtxt": ["Several foundations are missing. A serious incident would likely have a large and lasting impact.",
                    "The basics are in place, but significant gaps remain, especially in what hasn't been tested.",
                    "Your organization is well prepared. The focus now is regular testing and keeping plans current."],
        "context_lede": "For an organization your size in the", "context_mid": " sector, one hour of interruption often runs into the tens or hundreds of thousands of dollars.",
        "context_link": "See the order of magnitude by industry",
        "no_single": "There's no single recipe here: the best next step depends on constraints this questionnaire doesn't know — your budget, your regulatory deadlines, what has already happened to you.",
        "cta": "Discuss my results with us", "print": "Print", "copy": "Copy the summary", "copied": "Copied"},
}
