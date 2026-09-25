# AI section. (fr, en) pairs.

AI_PAGES = [
 {
  "path": "ai/strategy-adoption.html",
  "short": ("Stratégie et adoption de l'IA", "AI strategy and adoption"),
  "summary": ("Aligner la direction sur une vision, choisir les bons cas d'usage et accompagner les équipes.", "Align leadership on a vision, choose the right use cases and bring teams along."),
  "title": ("Stratégie et adoption de l'IA", "AI strategy and adoption"),
  "lede": ("Passer des essais dispersés à une adoption qui produit des résultats mesurables.", "Move from scattered experiments to adoption that delivers measurable results."),
  "intro": ("La plupart des organisations utilisent déjà l'IA, souvent sans le savoir. Nous partons de votre vision et de vos contraintes pour choisir quelques cas d'usage à forte valeur, puis nous accompagnons leur adoption réelle par les équipes.",
            "Most organizations already use AI, often without knowing it. We start from your vision and constraints to choose a few high-value use cases, then support their real adoption by teams."),
  "cover": [
    (("Atelier de vision", "Vision workshop"), ("Aligner la direction sur les objectifs, les limites et le niveau d'autonomie acceptable.", "Align leadership on goals, limits and the acceptable level of autonomy.")),
    (("Portefeuille de cas d'usage", "Use case portfolio"), ("Évaluer la valeur, la faisabilité et le risque de chaque idée pour choisir les premières.", "Score each idea on value, feasibility and risk to choose the first ones.")),
    (("Feuille de route", "Roadmap"), ("Séquencer pilotes, fondations de données et gouvernance sur 12 à 18 mois.", "Sequence pilots, data foundations and governance over 12 to 18 months.")),
    (("Adoption et formation", "Adoption and training"), ("Former les équipes, créer une communauté de pratique et mesurer l'usage.", "Train teams, build a community of practice and measure usage.")),
  ],
  "deliverables": [("Énoncé de vision IA validé par la direction", "AI vision statement approved by leadership"), ("Portefeuille de cas d'usage priorisé", "Prioritized use case portfolio"), ("Feuille de route sur 12 à 18 mois", "12- to 18-month roadmap"), ("Plan de formation et indicateurs d'adoption", "Training plan and adoption metrics")],
  "faq": [(("Par où commencer ?", "Where should we start?"), ("Par notre questionnaire de vision : il prépare l'atelier et fait ressortir les écarts entre les attentes des participants.", "With our vision questionnaire: it prepares the workshop and surfaces gaps between participants' expectations."))],
  "related": ["ai/vision-questionnaire.html", "ai/governance.html"],
 },
 {
  "path": "ai/agents.html",
  "short": ("Conception d'agents IA", "AI agent design and build"),
  "summary": ("Concevoir et construire des agents utiles, supervisés et sûrs.", "Design and build agents that are useful, supervised and safe."),
  "title": ("Conception et création d'agents IA", "AI agent design and build"),
  "lede": ("Des agents qui font gagner du temps, avec des limites claires et un humain aux bons endroits.", "Agents that save time, with clear limits and a human in the right places."),
  "intro": ("Un agent n'est pas un simple assistant : il agit dans vos systèmes. Nous concevons chaque agent avec son périmètre, ses outils, ses droits d'accès, ses points de validation humaine et ses indicateurs, puis nous l'évaluons avant la mise en production.",
            "An agent is not just an assistant: it acts in your systems. We design each agent with its scope, tools, access rights, human approval points and metrics, then evaluate it before production."),
  "cover": [
    (("Conception", "Design"), ("Tâches, outils, données accessibles et niveau d'autonomie, définis avec les métiers.", "Tasks, tools, accessible data and autonomy level, defined with the business.")),
    (("Construction", "Build"), ("Développement sur la plateforme de votre choix, dont Microsoft Foundry et Copilot Studio.", "Development on the platform of your choice, including Microsoft Foundry and Copilot Studio.")),
    (("Évaluation et tests", "Evaluation and testing"), ("Jeux de tests, tests d'attaque par injection de requêtes et mesure de la qualité.", "Test sets, prompt injection testing and quality measurement.")),
    (("Mise en production", "Production"), ("Identité propre à chaque agent, journalisation, supervision et plan de retour arrière.", "A dedicated identity per agent, logging, monitoring and a rollback plan.")),
  ],
  "deliverables": [("Fiche de conception de l'agent", "Agent design brief"), ("Agent fonctionnel et documenté", "Working, documented agent"), ("Rapport d'évaluation et de sécurité", "Evaluation and security report"), ("Procédures d'exploitation et de désactivation", "Operating and shutdown procedures")],
  "faq": [(("Un agent peut-il agir seul ?", "Can an agent act on its own?"), ("Oui, dans des limites définies. Nous recommandons de commencer par des agents qui proposent et d'accroître l'autonomie à mesure que la confiance se construit.", "Yes, within defined limits. We recommend starting with agents that propose actions and increasing autonomy as trust builds."))],
  "related": ["ai/citadel.html", "ai/governance.html"],
 },
 {
  "path": "ai/governance.html",
  "short": ("Gouvernance et risques de l'IA", "AI governance and risk"),
  "summary": ("Politique, inventaire, classification des risques et conformité réglementaire.", "Policy, inventory, risk classification and regulatory compliance."),
  "title": ("Gouvernance, risques et conformité de l'IA", "AI governance, risk and compliance"),
  "lede": ("Encadrer l'IA sans freiner l'innovation.", "Govern AI without slowing innovation."),
  "intro": ("La gouvernance de l'IA prolonge ce que vous faites déjà en sécurité et en gestion des risques. Nous mettons en place un cadre proportionné : ce qui est permis, ce qui doit être approuvé et comment surveiller les usages.",
            "AI governance extends what you already do in security and risk management. We set up a proportionate framework: what is allowed, what needs approval and how usage is monitored."),
  "cover": [
    (("Politique d'utilisation", "Acceptable use policy"), ("Règles claires pour les employés, les données et les outils autorisés.", "Clear rules for staff, data and approved tools.")),
    (("Inventaire et IA non autorisée", "Inventory and shadow AI"), ("Recenser les outils et agents utilisés, officiels ou non.", "List the tools and agents in use, official or not.")),
    (("Classification des risques", "Risk classification"), ("Classer les usages selon le règlement européen sur l'IA et vos propres critères.", "Classify use cases under the EU AI Act and your own criteria.")),
    (("Système de management", "Management system"), ("Aligner le cadre sur ISO/IEC 42001 et le NIST AI RMF.", "Align the framework with ISO/IEC 42001 and the NIST AI RMF.")),
  ],
  "deliverables": [("Politique d'utilisation de l'IA", "AI acceptable use policy"), ("Registre des systèmes d'IA", "AI system register"), ("Méthode de classification et d'approbation", "Classification and approval method"), ("Feuille de route de conformité", "Compliance roadmap")],
  "faq": [(("Le règlement européen sur l'IA nous concerne-t-il ?", "Does the EU AI Act apply to us?"),
           ("S'il vous concerne dépend de votre rôle (fournisseur ou utilisateur) et de vos usages, y compris hors de l'UE si vos systèmes y sont utilisés. Ses obligations s'appliquent progressivement ; nous vous aidons à faire l'inventaire et la classification, en lien avec vos conseillers juridiques.",
            "Whether it applies depends on your role (provider or deployer) and your use cases, including outside the EU if your systems are used there. Its obligations phase in over time; we help with inventory and classification, alongside your legal advisers."))],
  "related": ["ai/citadel.html", "ai/strategy-adoption.html"],
 },
]

CITADEL = {
 "path": "ai/citadel.html",
 "short": ("Microsoft Foundry Citadel", "Microsoft Foundry Citadel"),
 "summary": ("Une plateforme de gouvernance pour déployer des agents IA à grande échelle sur Azure.", "A governance platform for deploying AI agents at scale on Azure."),
 "title": ("Microsoft Foundry Citadel", "Microsoft Foundry Citadel"),
 "lede": ("Gouverner vos agents IA sur Azure dès le premier jour, avec une architecture de référence éprouvée.", "Govern your AI agents on Azure from day one, with a proven reference architecture."),
 "what": ("Citadel est une architecture de référence open source publiée par Microsoft pour gouverner l'IA et les agents sur Azure. Elle repose sur un modèle en étoile : un point de contrôle central applique les règles, tandis que chaque équipe développe ses agents dans son propre environnement, à l'intérieur de garde-fous communs.",
          "Citadel is an open-source reference architecture published by Microsoft for governing AI and agents on Azure. It uses a hub-and-spoke model: a central control point enforces the rules, while each team builds its agents in its own environment, inside shared guardrails."),
 "layers": [
   (("Couche 1 — Hub de gouvernance", "Layer 1 — Governance hub"), ("Une passerelle IA centrale sur Azure API Management : contrôle d'accès, détection de données personnelles, sécurité du contenu, suivi des coûts et de l'usage par équipe.", "A central AI gateway on Azure API Management: access control, personal data detection, content safety, cost and usage tracking per team.")),
   (("Couche 2 — Opérations des agents", "Layer 2 — Agent operations"), ("Des environnements par équipe sur Microsoft Foundry, avec traces d'exécution, évaluations et tests d'attaque.", "Per-team environments on Microsoft Foundry, with execution traces, evaluations and red-teaming.")),
   (("Couche 3 — Identité des agents", "Layer 3 — Agent identity"), ("Chaque agent reçoit une identité gérée dans Microsoft Entra ID, avec un responsable humain et un cycle de vie.", "Each agent gets a managed identity in Microsoft Entra ID, with a human owner and a lifecycle.")),
   (("Couche 4 — Sécurité", "Layer 4 — Security fabric"), ("Protection contre les menaces et gouvernance des données avec Microsoft Defender et Purview.", "Threat protection and data governance with Microsoft Defender and Purview.")),
 ],
 "why": [
   (("Des pilotes qui atteignent la production", "Pilots that reach production"), ("Les blocages de sécurité et de conformité sont réglés une fois, au niveau de la plateforme.", "Security and compliance blockers are solved once, at platform level.")),
   (("Des coûts maîtrisés", "Controlled costs"), ("Chaque appel à un modèle est attribué à une équipe et à un budget.", "Every model call is attributed to a team and a budget.")),
   (("Une autonomie encadrée", "Autonomy within guardrails"), ("Les équipes innovent vite sans créer d'IA non autorisée.", "Teams move fast without creating shadow AI.")),
 ],
 "our": [
   (("Évaluation de préparation", "Readiness assessment"), ("Zone d'atterrissage Azure, identités, réseau, quotas de modèles et exigences de gouvernance.", "Azure landing zone, identity, networking, model quotas and governance requirements.")),
   (("Conception et politiques", "Design and policies"), ("Adapter l'architecture à vos risques : règles de la passerelle, contrats d'accès, classification des données.", "Adapt the architecture to your risks: gateway rules, access contracts, data classification.")),
   (("Déploiement et intégration", "Deployment and onboarding"), ("Mise en place du hub et d'un premier environnement d'agents, avec vos équipes Azure.", "Deploy the hub and a first agent environment, with your Azure teams.")),
   (("Résilience de la plateforme IA", "AI platform resilience"), ("Bascule entre régions, plan de reprise et exploitation : notre cœur de métier appliqué à l'IA.", "Cross-region failover, recovery plan and operations: our core expertise applied to AI.")),
 ],
 "note": ("Citadel est un projet open source de Microsoft, en évolution rapide. FZ Consultation est indépendant et n'est pas affilié à Microsoft. Microsoft, Azure, Entra, Defender, Purview et Foundry sont des marques de Microsoft.",
          "Citadel is a fast-evolving open-source project from Microsoft. FZ Consultation is independent and not affiliated with Microsoft. Microsoft, Azure, Entra, Defender, Purview and Foundry are Microsoft trademarks."),
 "sources": [
   ("Azure-Samples — Foundry Citadel Platform (GitHub)", "https://github.com/Azure-Samples/foundry-citadel-platform"),
   ("Azure-Samples — Citadel Governance Hub / AI Hub Gateway (GitHub)", "https://github.com/Azure-Samples/ai-hub-gateway-solution-accelerator"),
   ("Microsoft Tech Community — Operationalizing enterprise AI with the Citadel architecture", "https://techcommunity.microsoft.com/blog/azurearchitectureblog/building-on-ai-landing-zones-operationalizing-enterprise-ai-with-the-citadel-arc/4551078"),
 ],
}

# ---- Vision questionnaire ----
# type: "multi" (summary only), "single" (with pillar score 0..3 by option index), "choice" (summary only, single)
VISION = [
 {"id": "goals", "type": "multi", "q": ("Qu'attendez-vous d'abord de l'IA ?", "What do you want from AI first?"),
  "opts": [("Productivité interne", "Internal productivity"), ("Expérience client", "Customer experience"), ("Nouveaux produits ou services", "New products or services"), ("Réduction des coûts", "Lower costs"), ("Maîtrise des risques et conformité", "Risk and compliance control")]},
 {"id": "areas", "type": "multi", "q": ("Dans quels domaines ?", "In which areas?"),
  "opts": [("Service client", "Customer service"), ("Opérations", "Operations"), ("Finance", "Finance"), ("Ressources humaines", "Human resources"), ("TI et développement", "IT and development"), ("Ventes et marketing", "Sales and marketing"), ("Juridique et conformité", "Legal and compliance")]},
 {"id": "autonomy", "type": "choice", "q": ("Jusqu'où voulez-vous que vos agents IA aillent ?", "How far should your AI agents go?"),
  "opts": [("Répondre aux questions et assister", "Answer questions and assist"), ("Préparer des actions qu'un humain approuve", "Prepare actions a human approves"), ("Agir seuls dans des limites définies", "Act on their own within set limits")]},
 {"id": "horizon", "type": "choice", "q": ("Sur quel horizon voulez-vous des premiers résultats ?", "When do you want first results?"),
  "opts": [("D'ici 3 mois", "Within 3 months"), ("D'ici 6 à 12 mois", "Within 6 to 12 months"), ("Au-delà de 12 mois", "Beyond 12 months")]},
 {"id": "cloud", "type": "choice", "q": ("Quelle est votre plateforme infonuagique principale ?", "What is your main cloud platform?"),
  "opts": [("Microsoft Azure", "Microsoft Azure"), ("AWS", "AWS"), ("Google Cloud", "Google Cloud"), ("Plusieurs", "Several"), ("Surtout sur site", "Mostly on-premises")]},
 {"id": "stage", "type": "single", "pillar": "strategy", "q": ("Où en êtes-vous aujourd'hui avec l'IA ?", "Where are you with AI today?"),
  "opts": [("Aucun usage", "No use yet"), ("Usage individuel d'outils publics", "Individual use of public tools"), ("Projets pilotes", "Pilot projects"), ("Solutions en production", "Solutions in production")]},
 {"id": "sponsor", "type": "single", "pillar": "strategy", "q": ("L'IA a-t-elle un parrain à la direction ?", "Does AI have an executive sponsor?"),
  "opts": [("Non", "No"), ("Un intérêt informel", "Informal interest"), ("Un parrain désigné", "A named sponsor"), ("Parrain, budget et indicateurs", "Sponsor, budget and metrics")]},
 {"id": "data", "type": "single", "pillar": "data", "q": ("Vos données sont-elles prêtes pour l'IA ?", "Is your data ready for AI?"),
  "opts": [("Dispersées et mal connues", "Scattered and poorly known"), ("Connues mais cloisonnées", "Known but siloed"), ("Sources clés documentées, accès contrôlés", "Key sources documented, access controlled"), ("Gouvernées, classifiées et exploitables", "Governed, classified and usable")]},
 {"id": "policy", "type": "single", "pillar": "governance", "q": ("Avez-vous une politique d'utilisation de l'IA ?", "Do you have an AI acceptable use policy?"),
  "opts": [("Non", "No"), ("En cours de rédaction", "Being drafted"), ("Approuvée", "Approved"), ("Approuvée, formée et suivie", "Approved, trained and monitored")]},
 {"id": "inventory", "type": "single", "pillar": "governance", "q": ("Savez-vous quels outils et agents d'IA sont utilisés chez vous ?", "Do you know which AI tools and agents are used in your organization?"),
  "opts": [("Non", "No"), ("En partie", "Partly"), ("Oui, un inventaire existe", "Yes, there is an inventory"), ("Inventaire et processus d'approbation", "Inventory and approval process")]},
 {"id": "reg", "type": "single", "pillar": "governance", "q": ("Avez-vous évalué vos usages au regard de la réglementation, comme le règlement européen sur l'IA ?", "Have you assessed your use cases against regulation, such as the EU AI Act?"),
  "opts": [("Non", "No"), ("Nous en avons conscience", "We are aware of it"), ("Évaluation partielle", "Partial assessment"), ("Classification formelle", "Formal classification")]},
 {"id": "gateway", "type": "single", "pillar": "platform", "q": ("Les appels aux modèles d'IA passent-ils par un point de contrôle central ?", "Do calls to AI models go through a central control point?"),
  "opts": [("Non, chaque équipe gère ses clés", "No, each team manages its own keys"), ("Quelques contrôles", "Some controls"), ("Une passerelle pour une partie des usages", "A gateway for some uses"), ("Passerelle centrale, identités, suivi des coûts", "Central gateway, identity, cost tracking")]},
 {"id": "skills", "type": "single", "pillar": "people", "q": ("Vos équipes sont-elles formées à l'IA ?", "Are your teams trained in AI?"),
  "opts": [("Non", "No"), ("Quelques passionnés", "A few enthusiasts"), ("Un programme a commencé", "A program has started"), ("Formation large et communauté de pratique", "Broad training and a community of practice")]},
]

VISION_PILLARS = {
 "strategy": (("Stratégie", "Strategy"), "ai/strategy-adoption.html", ("Organiser un atelier de vision et bâtir un portefeuille de cas d'usage.", "Run a vision workshop and build a use case portfolio.")),
 "data": (("Données", "Data"), "ai/strategy-adoption.html", ("Documenter et classifier les sources de données des premiers cas d'usage.", "Document and classify data sources for the first use cases.")),
 "governance": (("Gouvernance", "Governance"), "ai/governance.html", ("Adopter une politique d'utilisation et un inventaire des usages de l'IA.", "Adopt an acceptable use policy and an inventory of AI use.")),
 "platform": (("Plateforme", "Platform"), "ai/citadel.html", ("Centraliser l'accès aux modèles derrière une passerelle gouvernée.", "Put model access behind a governed central gateway.")),
 "people": (("Personnes", "People"), "ai/strategy-adoption.html", ("Lancer un programme de formation et une communauté de pratique.", "Launch a training program and a community of practice.")),
}

VISION_UI = {
 "fr": {"start": "Commencer", "org": "Nom de votre organisation (facultatif)", "next": "Suivant", "prev": "Précédent", "see": "Voir la synthèse", "q": "Question", "of": "sur",
        "multi": "Plusieurs choix possibles", "vision": "Votre énoncé de vision (brouillon)", "readiness": "Maturité par pilier", "reco": "Nos recommandations",
        "caution": "Vous visez des agents autonomes alors que la gouvernance est encore à construire : commencez par des agents qui préparent des actions approuvées par un humain.",
        "citadel": "Votre plateforme est Azure : l'architecture Microsoft Foundry Citadel est un bon point de départ pour gouverner vos agents.",
        "send": "Nous envoyer la synthèse", "copy": "Copier", "copied": "Copié", "print": "Imprimer", "restart": "Recommencer", "learn": "En savoir plus",
        "tpl": "D'ici {h}, {o} veut utiliser l'IA pour {g}, en priorité dans {a}. Nos agents devront {x}, sur {c}.",
        "orgdef": "notre organisation", "and": "et", "none": "à préciser", "subject": "Questionnaire de vision IA"},
 "en": {"start": "Start", "org": "Your organization's name (optional)", "next": "Next", "prev": "Back", "see": "See the summary", "q": "Question", "of": "of",
        "multi": "Select all that apply", "vision": "Your vision statement (draft)", "readiness": "Readiness by pillar", "reco": "Our recommendations",
        "caution": "You are aiming for autonomous agents while governance is still being built: start with agents that prepare actions a human approves.",
        "citadel": "Your platform is Azure: the Microsoft Foundry Citadel architecture is a good starting point for governing your agents.",
        "send": "Send us the summary", "copy": "Copy", "copied": "Copied", "print": "Print", "restart": "Start again", "learn": "Learn more",
        "tpl": "Within {h}, {o} wants to use AI for {g}, starting with {a}. Our agents should {x}, on {c}.",
        "orgdef": "our organization", "and": "and", "none": "to be defined", "subject": "AI vision questionnaire"},
}

VISION_PHRASES = {
 "fr": {"horizon": ["3 mois", "6 à 12 mois", "plus de 12 mois"],
        "autonomy": ["répondre aux questions et assister les équipes", "préparer des actions qu'un humain approuve", "agir seuls dans des limites définies"],
        "cloud": ["Microsoft Azure", "AWS", "Google Cloud", "plusieurs plateformes infonuagiques", "une infrastructure surtout sur site"]},
 "en": {"horizon": ["3 months", "6 to 12 months", "more than 12 months"],
        "autonomy": ["answer questions and assist teams", "prepare actions a human approves", "act on their own within set limits"],
        "cloud": ["Microsoft Azure", "AWS", "Google Cloud", "several cloud platforms", "mostly on-premises infrastructure"]},
}
