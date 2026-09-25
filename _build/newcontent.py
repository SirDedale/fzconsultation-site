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

# (domain, question, recommendation if weak)
QUIZ = [
 ("bc", ("Vos services essentiels sont-ils identifiés et priorisés, avec l'impact d'une interruption dans le temps ?", "Are your essential services identified and prioritized, with the impact of an interruption over time?"),
        ("Réaliser une analyse d'impact pour savoir quoi rétablir en premier.", "Run a business impact analysis to know what to restore first.")),
 ("bc", ("Avez-vous un plan de continuité qui couvre les personnes, les locaux et les fournisseurs, pas seulement l'informatique ?", "Do you have a continuity plan covering people, sites and suppliers, not just IT?"),
        ("Élargir le plan de continuité au-delà de l'informatique.", "Extend your continuity plan beyond IT.")),
 ("bc", ("Une cellule de crise et des messages types pour les employés, clients et régulateurs sont-ils prêts ?", "Are a crisis team and template messages for staff, customers and regulators ready?"),
        ("Définir la cellule de crise et préparer les communications à l'avance.", "Define the crisis team and prepare communications in advance.")),
 ("dr", ("Des cibles RTO et RPO sont-elles définies et approuvées par la direction ?", "Are RTO and RPO targets defined and approved by leadership?"),
        ("Fixer des cibles RTO et RPO par service, validées par la direction.", "Set RTO and RPO targets per service, signed off by leadership.")),
 ("dr", ("Disposez-vous d'une copie de sauvegarde isolée ou immuable, hors d'atteinte d'un attaquant ?", "Do you keep an isolated or immutable backup copy, out of an attacker's reach?"),
        ("Ajouter une copie de sauvegarde isolée ou immuable.", "Add an isolated or immutable backup copy.")),
 ("dr", ("Avez-vous restauré un système critique complet au cours des 12 derniers mois ?", "Have you restored a complete critical system in the last 12 months?"),
        ("Planifier une restauration complète chronométrée d'un système critique.", "Schedule a full, timed restore of a critical system.")),
 ("sec", ("L'authentification multifacteur est-elle activée sur tous les accès distants et comptes administrateurs ?", "Is multi-factor authentication enabled on all remote access and admin accounts?"),
        ("Généraliser la MFA aux accès distants et aux comptes à privilèges.", "Roll out MFA to all remote and privileged access.")),
 ("sec", ("Avez-vous un plan de réponse aux incidents avec des rôles et des contacts externes à jour ?", "Do you have an incident response plan with roles and up-to-date external contacts?"),
        ("Rédiger un plan de réponse aux incidents et des scénarios types.", "Write an incident response plan and playbooks.")),
 ("sec", ("Votre centre de services vérifie-t-il l'identité avant toute réinitialisation de mot de passe ou de MFA ?", "Does your help desk verify identity before any password or MFA reset?"),
        ("Renforcer la vérification d'identité au centre de services, y compris chez les prestataires.", "Strengthen help desk identity checks, including at service providers.")),
 ("tp", ("Connaissez-vous vos fournisseurs critiques et leur capacité de reprise ?", "Do you know your critical suppliers and their ability to recover?"),
        ("Cartographier les fournisseurs critiques et évaluer leur résilience.", "Map critical suppliers and assess their resilience.")),
 ("tp", ("Les données de vos applications SaaS (Microsoft 365, Google Workspace…) sont-elles sauvegardées de façon indépendante ?", "Is the data in your SaaS applications (Microsoft 365, Google Workspace…) backed up independently?"),
        ("Mettre en place une sauvegarde indépendante des données SaaS.", "Set up an independent backup of SaaS data.")),
 ("tp", ("La direction a-t-elle participé à un exercice de crise au cours des 12 derniers mois ?", "Has leadership taken part in a crisis exercise in the last 12 months?"),
        ("Organiser un exercice sur table avec la direction.", "Run a tabletop exercise with leadership.")),
]

QUIZ_UI = {
 "fr": {"q": "Question", "of": "sur", "next": "Suivant", "prev": "Précédent", "see": "Voir mon résultat", "restart": "Recommencer",
        "overall": "Score global", "by": "Par domaine", "prio": "Vos trois priorités", "learn": "En savoir plus",
        "bands": ["Exposé", "En développement", "Solide"],
        "bandtxt": ["Plusieurs fondations manquent. Un incident sérieux aurait probablement un impact important et durable.",
                    "Les bases existent, mais des écarts importants subsistent, surtout sur ce qui n'a pas été testé.",
                    "Votre organisation est bien préparée. L'enjeu est maintenant de tester régulièrement et de garder les plans à jour."],
        "cta": "Discuter de mes résultats"},
 "en": {"q": "Question", "of": "of", "next": "Next", "prev": "Back", "see": "See my result", "restart": "Start again",
        "overall": "Overall score", "by": "By area", "prio": "Your top three priorities", "learn": "Learn more",
        "bands": ["Exposed", "Developing", "Solid"],
        "bandtxt": ["Several foundations are missing. A serious incident would likely have a large and lasting impact.",
                    "The basics are in place, but significant gaps remain, especially in what hasn't been tested.",
                    "Your organization is well prepared. The focus now is regular testing and keeping plans current."],
        "cta": "Discuss my results"},
}
