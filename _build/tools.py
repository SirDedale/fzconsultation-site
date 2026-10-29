# Content for the Resources section: templates, glossary, downtime-calculator labels.
# Everything is a (fr, en) pair. Templates are general-purpose starting points, not legal advice.

TEMPLATE_DISCLAIMER = ("Modèle général fourni comme point de départ. Adaptez-le à votre organisation et faites-le valider par vos conseillers juridiques, de conformité et de sécurité avant usage. Il ne constitue pas un avis juridique.",
                       "General-purpose template provided as a starting point. Adapt it to your organization and have it reviewed by your legal, compliance and security advisers before use. It is not legal advice.")

# ---------------- Ransomware response checklist ----------------
RANSOM = {
 "slug": "ransomware-checklist",
 "title": ("Liste de vérification : réponse à un rançongiciel", "Checklist: responding to ransomware"),
 "short": ("Liste de vérification rançongiciel", "Ransomware checklist"),
 "summary": ("Une liste en cinq phases pour garder la tête froide pendant les premières heures d'une attaque par rançongiciel.", "A five-phase checklist to keep a clear head during the first hours of a ransomware attack."),
 "lede": ("À imprimer et à ranger avec votre plan d'intervention, hors de vos systèmes habituels. Elle suppose que vos systèmes principaux peuvent être inaccessibles.", "Print it and keep it with your response plan, outside your usual systems. It assumes your main systems may be unavailable."),
 "how": ("Utilisez cette liste comme aide-mémoire, pas comme plan complet. Les décisions de fond (payer ou non, notifier qui, redémarrer quand) appartiennent à votre direction, avec vos conseillers juridiques et votre assureur. Préparez les coordonnées à l'avance : en pleine crise, personne ne retrouve un numéro de téléphone.",
         "Use this list as a memory aid, not a complete plan. The big decisions (whether to pay, who to notify, when to restart) belong to your leadership, with your legal advisers and insurer. Prepare the contact details in advance: in the middle of a crisis, nobody finds a phone number."),
 "phases": [
  (("1. Dans la première heure : contenir", "1. In the first hour: contain"), [
    ("Isolez les appareils touchés du réseau (débranchez le câble, coupez le Wi-Fi) sans les éteindre, afin de préserver les preuves en mémoire.", "Isolate affected devices from the network (unplug the cable, disable Wi-Fi) without powering them off, to preserve evidence in memory."),
    ("Désactivez les comptes compromis et, si nécessaire, coupez les accès à distance (VPN, bureau à distance).", "Disable compromised accounts and, if needed, cut remote access (VPN, remote desktop)."),
    ("Protégez les sauvegardes : déconnectez-les ou verrouillez-les avant qu'elles ne soient chiffrées ou effacées.", "Protect backups: disconnect or lock them before they are encrypted or deleted."),
    ("Activez votre équipe de crise et ouvrez un journal horodaté de chaque constat et décision.", "Activate your crisis team and open a time-stamped log of every finding and decision."),
    ("Communiquez hors bande (téléphone, messagerie personnelle) : supposez que votre courriel et votre clavardage sont lus par l'attaquant.", "Communicate out of band (phone, personal messaging): assume the attacker can read your email and chat."),
  ]),
  (("2. Dans les 24 premières heures : évaluer", "2. Within 24 hours: assess"), [
    ("Identifiez ce qui est touché : systèmes, données, sites, fournisseurs et clients concernés.", "Identify what is affected: systems, data, sites, suppliers and customers involved."),
    ("Repérez le point d'entrée probable et vérifiez si des données ont été copiées avant le chiffrement (double extorsion).", "Find the likely entry point and check whether data was copied before encryption (double extortion)."),
    ("Faites un instantané de ce qui est touché (images disques, journaux) avant toute remise en état.", "Take a snapshot of what is affected (disk images, logs) before any rebuild."),
    ("Prévenez votre assureur cyber et votre cabinet juridique ; respectez les délais de déclaration de votre police.", "Notify your cyber insurer and your legal counsel; respect the reporting deadlines in your policy."),
    ("Faites appel à une équipe d'intervention sur incident, interne ou externe, si vous n'avez pas l'expertise.", "Bring in an incident response team, internal or external, if you lack the expertise."),
  ]),
  (("3. Décisions et notifications", "3. Decisions and notifications"), [
    ("Signalez l'incident aux autorités policières et aux organismes de cybersécurité compétents de votre pays.", "Report the incident to law enforcement and the competent cybersecurity agencies in your country."),
    ("Déterminez les obligations de notification : régulateurs, personnes touchées, clients, partenaires (DORA, NIS2, RGPD, Loi 25, règles sectorielles).", "Determine notification duties: regulators, affected individuals, customers, partners (DORA, NIS2, GDPR, Law 25, sector rules)."),
    ("Consignez la décision sur la rançon : qui décide, sur quelle base, avec quels conseils. Vérifiez au préalable les risques de sanctions.", "Record the ransom decision: who decides, on what basis, with what advice. Check sanctions exposure first."),
    ("Préparez une communication unique et factuelle pour le personnel, les clients et les médias.", "Prepare a single, factual communication for staff, customers and the media."),
  ]),
  (("4. Reprise", "4. Recovery"), [
    ("Rebâtissez à partir de sources saines : images validées, sauvegardes testées et analysées avant restauration.", "Rebuild from clean sources: validated images, backups tested and scanned before restoration."),
    ("Réinitialisez tous les identifiants (comptes de service, administrateurs, clés d'accès) avant de reconnecter quoi que ce soit.", "Reset all credentials (service accounts, administrators, access keys) before reconnecting anything."),
    ("Restaurez par ordre de priorité d'affaires, en vous appuyant sur vos analyses d'impact et vos objectifs de reprise (RTO/RPO).", "Restore in business-priority order, based on your impact analysis and recovery objectives (RTO/RPO)."),
    ("Surveillez de près les systèmes restaurés : l'attaquant peut avoir laissé des accès persistants.", "Monitor restored systems closely: the attacker may have left persistent access."),
  ]),
  (("5. Après l'incident", "5. After the incident"), [
    ("Tenez un retour d'expérience sans reproche dans les deux à quatre semaines suivantes.", "Hold a blameless review within two to four weeks."),
    ("Corrigez la cause racine et les écarts constatés (accès, segmentation, sauvegardes, détection).", "Fix the root cause and the gaps found (access, segmentation, backups, detection)."),
    ("Mettez à jour le plan d'intervention, les coordonnées et les scénarios d'exercice.", "Update the response plan, the contact details and the exercise scenarios."),
    ("Planifiez un exercice qui rejoue le scénario pour confirmer que les correctifs fonctionnent.", "Schedule an exercise that replays the scenario to confirm the fixes work."),
  ]),
 ],
 "sources": [
  ("CISA — #StopRansomware Guide", "https://www.cisa.gov/stopransomware/ransomware-guide"),
  ("NCSC (UK) — Mitigating malware and ransomware attacks", "https://www.ncsc.gov.uk/guidance/mitigating-malware-and-ransomware-attacks"),
 ],
 "related": ["what-we-do/expertise/cybersecurity.html", "what-we-do/services/exercises.html"],
}

# ---------------- RTO / RPO worksheet ----------------
RTORPO = {
 "slug": "rto-rpo-worksheet",
 "title": ("Feuille de travail RTO / RPO", "RTO / RPO worksheet"),
 "short": ("Feuille de travail RTO / RPO", "RTO / RPO worksheet"),
 "summary": ("Un tableau pour fixer, service par service, le temps de reprise et la perte de données que l'entreprise peut tolérer.", "A table to set, service by service, the recovery time and data loss the business can tolerate."),
 "lede": ("Commencez par la tolérance de l'entreprise, pas par la technologie : la bonne cible se décide avec les responsables d'affaires.", "Start from what the business can tolerate, not from the technology: the right target is set with business owners."),
 "how": ("Remplissez une ligne par service d'affaires important. Demandez à son responsable : « Après combien de temps d'arrêt les dégâts deviennent-ils inacceptables ? Combien de données récentes peut-on perdre ? » Comparez ensuite avec ce que vos systèmes savent réellement faire, mesuré lors d'un test, pas lu dans une brochure.",
         "Fill in one row per important business service. Ask its owner: \"After how long a stoppage does the damage become unacceptable? How much recent data can we afford to lose?\" Then compare with what your systems can really do, measured in a test, not read in a brochure."),
 "defs": [
  (("RTO", "RTO"), ("Recovery Time Objective : durée maximale visée entre l'interruption et le retour du service.", "Recovery Time Objective: the target maximum time between the interruption and the service coming back.")),
  (("RPO", "RPO"), ("Recovery Point Objective : ancienneté maximale des données restaurées, donc la perte de données acceptée.", "Recovery Point Objective: the maximum age of restored data, hence the data loss accepted.")),
  (("MTPD", "MTPD"), ("Durée maximale d'interruption tolérable : au-delà, la survie de l'activité est menacée. Le RTO doit rester nettement en dessous.", "Maximum Tolerable Period of Disruption: beyond it, the viability of the activity is threatened. The RTO must stay well below it.")),
 ],
 "columns": [
  ("Service d'affaires", "Business service"), ("Responsable", "Owner"), ("Coût d'une heure d'arrêt", "Cost of one hour down"),
  ("MTPD", "MTPD"), ("RTO cible", "Target RTO"), ("RPO cible", "Target RPO"),
  ("RTO testé", "Tested RTO"), ("RPO réel", "Actual RPO"), ("Dépendances", "Dependencies"), ("Écart et action", "Gap and action"),
 ],
 "example": [
  ("Paiement en ligne", "Online payment"), ("Directrice du commerce", "Head of e-commerce"), ("45 000 $", "$45,000"),
  ("8 h", "8 h"), ("2 h", "2 h"), ("15 min", "15 min"),
  ("6 h", "6 h"), ("24 h", "24 h"), ("Base de données, passerelle de paiement, DNS", "Database, payment gateway, DNS"),
  ("Écart de 4 h sur le RTO et de 23 h 45 sur le RPO : répliquer la base et automatiser le basculement.", "4 h gap on RTO and 23 h 45 on RPO: replicate the database and automate failover."),
 ],
 "tips": [
  (("Cibles par niveaux", "Tier your targets"), ("Quatre niveaux (par exemple critique, important, utile, différable) suffisent. Un RTO différent pour chaque système est impossible à tester et à financer.", "Four tiers (for example critical, important, useful, deferrable) are enough. A different RTO for every system is impossible to test and to fund.")),
  (("Mesurez, ne devinez pas", "Measure, don't guess"), ("Une colonne « testé » vide est une réponse en soi : elle indique que l'objectif n'a jamais été démontré.", "An empty \"tested\" column is an answer in itself: it shows the objective has never been demonstrated.")),
  (("Suivez les dépendances", "Follow dependencies"), ("Un service ne reprend pas plus vite que le plus lent de ses composants : identité, DNS, réseau, fournisseurs.", "A service cannot recover faster than the slowest of its parts: identity, DNS, network, suppliers.")),
  (("Revoyez chaque année", "Review yearly"), ("Une nouvelle application, un changement de fournisseur ou une fusion déplacent les cibles. Revoyez-les au moins une fois par an.", "A new application, a supplier change or a merger shifts the targets. Review them at least once a year.")),
 ],
 "related": ["what-we-do/expertise/disaster-recovery.html", "resources/downtime-calculator.html"],
}

# ---------------- AI acceptable-use policy ----------------
AIPOL = {
 "slug": "ai-acceptable-use-policy",
 "title": ("Modèle de politique d'utilisation acceptable de l'IA", "AI acceptable-use policy template"),
 "short": ("Politique d'utilisation de l'IA", "AI acceptable-use policy"),
 "summary": ("Un modèle de politique en douze sections pour encadrer l'usage de l'IA générative et des agents par le personnel.", "A twelve-section policy template to govern staff use of generative AI and agents."),
 "lede": ("Une base à personnaliser pour dire clairement aux équipes ce qui est permis, ce qui est interdit et qui est responsable.", "A base to customize so teams know clearly what is allowed, what is not and who is accountable."),
 "how": ("Les passages entre crochets sont à remplir ou à adapter. Faites valider le texte par vos services juridique, des ressources humaines et de la sécurité. Une politique que personne ne lit ne protège rien : accompagnez-la d'une courte formation et d'une liste d'outils approuvés tenue à jour.",
         "Passages in square brackets are to be completed or adapted. Have the text reviewed by your legal, human resources and security teams. A policy nobody reads protects nothing: pair it with short training and a maintained list of approved tools."),
 "sections": [
  (("Objet et portée", "Purpose and scope"), ("Cette politique encadre l'utilisation d'outils d'intelligence artificielle, y compris l'IA générative et les agents autonomes, par le personnel, les sous-traitants et les stagiaires de [Nom de l'organisation], dans le cadre de leur travail.", "This policy governs the use of artificial intelligence tools, including generative AI and autonomous agents, by the staff, contractors and interns of [Organization name] in the course of their work.")),
  (("Définitions", "Definitions"), ("« Outil d'IA » : tout service ou logiciel qui génère du contenu, formule des recommandations ou prend des décisions à partir de modèles d'apprentissage. « Agent » : outil d'IA qui exécute des actions (envoyer, modifier, acheter, déployer) sans validation à chaque étape.", "\"AI tool\": any service or software that generates content, makes recommendations or takes decisions using learned models. \"Agent\": an AI tool that carries out actions (send, change, purchase, deploy) without approval at each step.")),
  (("Outils approuvés", "Approved tools"), ("Seuls les outils inscrits au [registre des outils d'IA approuvés] peuvent être utilisés avec des données de l'organisation. Toute nouvelle demande passe par [le responsable désigné] avant utilisation.", "Only tools listed in the [register of approved AI tools] may be used with the organization's data. Any new request goes through [the designated owner] before use.")),
  (("Données permises et interdites", "Permitted and prohibited data"), ("Il est interdit de saisir dans un outil non approuvé : renseignements personnels, données de clients, secrets commerciaux, code source confidentiel, informations financières non publiques, identifiants et clés d'accès. Les données de classification [interne] peuvent être utilisées uniquement dans les outils approuvés pour ce niveau.", "It is prohibited to enter into an unapproved tool: personal information, customer data, trade secrets, confidential source code, non-public financial information, credentials and access keys. Data classified [internal] may be used only in tools approved for that level.")),
  (("Supervision humaine et responsabilité", "Human oversight and accountability"), ("Vous restez responsable de tout contenu ou toute décision issus de l'IA que vous utilisez. Vérifiez les faits, les sources et les chiffres avant diffusion. Aucune décision ayant un effet important sur une personne (embauche, crédit, discipline, santé) ne peut être prise uniquement par un outil d'IA.", "You remain accountable for any AI-generated content or decision you use. Check facts, sources and figures before sharing. No decision with a significant effect on a person (hiring, credit, discipline, health) may be made solely by an AI tool.")),
  (("Agents et automatisation", "Agents and automation"), ("Chaque agent a un propriétaire nommé, une identité distincte, des accès réduits au strict nécessaire, une journalisation de ses actions et un moyen de l'arrêter rapidement. Les actions irréversibles ou à fort impact exigent une approbation humaine.", "Every agent has a named owner, a distinct identity, access limited to what is strictly necessary, logging of its actions and a way to stop it quickly. Irreversible or high-impact actions require human approval.")),
  (("Transparence", "Transparency"), ("Indiquez quand un contenu a été produit ou substantiellement modifié par l'IA lorsque cela peut influencer la confiance de son destinataire, et lorsque la loi ou un contrat l'exige. Informez les clients lorsqu'ils interagissent avec un agent plutôt qu'avec une personne.", "Disclose when content was produced or substantially altered by AI where this may affect the recipient's trust, and where law or contract requires it. Tell customers when they are interacting with an agent rather than a person.")),
  (("Propriété intellectuelle", "Intellectual property"), ("Ne soumettez pas de contenu protégé par le droit d'auteur dont vous n'avez pas les droits. Vérifiez les conditions d'utilisation des contenus générés avant de les utiliser dans des livrables destinés aux clients.", "Do not submit copyrighted content you have no right to use. Check the terms of use for generated content before using it in client deliverables.")),
  (("Fournisseurs et tiers", "Vendors and third parties"), ("Avant d'approuver un outil, vérifiez où les données sont traitées et conservées, si elles servent à entraîner les modèles, les certifications du fournisseur et ses engagements en cas d'incident.", "Before approving a tool, check where data is processed and stored, whether it is used to train models, the vendor's certifications and its commitments in case of an incident.")),
  (("Signalement des incidents", "Incident reporting"), ("Signalez immédiatement à [adresse ou service] toute fuite de données, tout comportement inattendu d'un agent ou tout contenu inapproprié produit par un outil. Le signalement de bonne foi ne donne lieu à aucune sanction.", "Immediately report to [address or team] any data leak, unexpected agent behavior or inappropriate content produced by a tool. Good-faith reporting leads to no penalty.")),
  (("Formation", "Training"), ("Chaque personne suit une formation sur cette politique à l'embauche puis [chaque année].", "Everyone completes training on this policy at onboarding and then [every year].")),
  (("Application", "Enforcement"), ("Le non-respect de cette politique peut entraîner des mesures allant jusqu'à la fin de l'emploi ou du contrat, selon la gravité et conformément à la loi applicable.", "Non-compliance with this policy may lead to measures up to termination of employment or contract, depending on severity and in line with applicable law.")),
  (("Révision", "Review"), ("Cette politique est revue au moins [tous les six mois] et après tout incident important ou changement réglementaire. Propriétaire : [fonction]. Version : [numéro]. Date : [date].", "This policy is reviewed at least [every six months] and after any significant incident or regulatory change. Owner: [role]. Version: [number]. Date: [date].")),
 ],
 "related": ["ai/governance.html", "ai/citadel.html"],
}

AISCORE = {
 "slug": "ai-agent-audit-scorecard",
 "title": ("Tableau de bord d'audit d'un agent IA", "AI agent audit scorecard"),
 "short": ("Tableau de bord d'audit d'agent IA", "AI agent audit scorecard"),
 "summary": ("Un tableau pour suivre, agent par agent, la fidélité au périmètre, la valeur réalisée et le rayon d'impact, et le refaire chaque trimestre.", "A table to track, agent by agent, scope fidelity, value realized and blast radius, and to re-run every quarter."),
 "lede": ("La version allégée de la méthode de FZ AI Auditor, pour que votre équipe fasse un premier état des lieux et le répète.", "A lightweight version of the FZ AI Auditor method, so your team can take a first inventory and repeat it."),
 "how": ("Remplissez une ligne par agent ou automatisation déployé. Appuyez chaque colonne sur des preuves (journaux, traces, factures, échantillons revus) plutôt que sur le document de conception. Les cotes ci-dessous sont un exemple : adaptez les seuils à votre tolérance au risque. Refaites le tableau chaque trimestre et à chaque changement de modèle, consigne ou permission.", "Fill in one row per deployed agent or automation. Back every column with evidence (logs, traces, invoices, reviewed samples) rather than the design document. The ratings below are an example: adapt the thresholds to your risk tolerance. Re-run the table every quarter and whenever a model, prompt or permission changes."),
 "defs_title": ("Grille de cotation du rayon d'impact (exemple)", "Blast-radius rating grid (example)"),
 "defs": [
  (("Faible", "Low"), ("Erreurs réversibles, peu de cas touchés, détection le jour même.", "Reversible errors, few cases touched, detection the same day.")),
  (("Modéré", "Moderate"), ("Erreurs réversibles mais nombreuses, ou détection en quelques jours. Correction coûteuse sans être critique.", "Reversible but numerous errors, or detection within days. Costly to correct but not critical.")),
  (("Élevé", "High"), ("Erreurs partiellement irréversibles, ou touchant clients, argent ou obligations réglementaires, avec détection lente.", "Partly irreversible errors, or errors touching customers, money or regulatory obligations, with slow detection.")),
  (("Critique", "Critical"), ("Erreurs irréversibles ou touchant la sécurité, des montants importants ou la conformité, à volume élevé, avec détection incertaine. Exige validation humaine, déploiement progressif et interrupteur d'arrêt testé.", "Irreversible errors, or errors affecting safety, large sums or compliance, at high volume, with uncertain detection. Requires human approval, staged rollout and a tested kill switch.")),
 ],
 "columns": [
  ("Agent / automatisation", "Agent / automation"), ("Responsable", "Owner"), ("Périmètre : autorisé contre observé", "Scope: authorized vs observed"),
  ("Dérive (aucune / mineure / importante)", "Drift (none / minor / material)"), ("Coût mensuel", "Monthly cost"), ("Valeur évitée mensuelle", "Monthly value displaced"),
  ("Exactitude vs référence humaine", "Accuracy vs human baseline"), ("Gravité du pire cas · réversible ?", "Worst-case severity · reversible?"), ("Délai de détection", "Time to detect"),
  ("Cote de rayon d'impact", "Blast-radius rating"), ("Écart de confinement", "Containment gap"), ("Prochaine revue", "Next review"),
 ],
 "example": [
  ("Agent de tri des courriels clients", "Customer email triage agent"), ("Responsable du soutien", "Support lead"), ("Autorisé : classer et suggérer. Observé : envoie aussi des réponses automatiques", "Authorized: classify and suggest. Observed: also sends auto-replies"),
  ("Importante", "Material"), ("4 000 $", "$4,000"), ("9 000 $", "$9,000"), ("92 % (n = 200) contre 96 % humain", "92% (n = 200) vs 96% human"),
  ("Moyenne · en partie irréversible", "Medium · partly irreversible"), ("3 jours", "3 days"), ("Élevée", "High"), ("Pas de validation avant envoi ni d'interrupteur testé", "No approval before sending or tested kill switch"), ("Dans 3 mois ou au prochain changement", "In 3 months or at next change"),
 ],
 "tips": [
  (("Commencez par l'inventaire", "Start with the inventory"), ("Incluez les agents adoptés par les équipes sans passer par la TI.", "Include agents teams adopted without going through IT.")),
  (("Mesurez la valeur", "Measure value"), ("Remplacez les estimations par les coûts réels et un échantillon revu à la main.", "Replace estimates with real costs and a hand-reviewed sample.")),
  (("Cotez le pire cas", "Rate the worst case"), ("Jugez le rayon d'impact sur ce qui peut mal tourner au volume réel, pas sur la moyenne.", "Rate blast radius by what can go wrong at real volume, not by the average.")),
  (("Comparez les contrôles à la cote", "Match controls to the rating"), ("Notez l'écart entre les contrôles existants et ceux qu'exige la cote.", "Record the gap between existing controls and those the rating requires.")),
 ],
 "related": ["ai/auditor.html", "ai/governance.html"],
}

TEMPLATES = [RANSOM, RTORPO, AIPOL, AISCORE]

# ---------------- Calculator labels ----------------
CALC = {
 "fields": [
  ("revenue", ("Revenus générés par heure d'activité", "Revenue generated per operating hour"), ("Revenu annuel divisé par les heures d'activité. Laissez à 0 si le service ne génère pas directement de revenus.", "Annual revenue divided by operating hours. Leave at 0 if the service does not directly generate revenue."), 20000),
  ("lost_pct", ("Part des revenus réellement perdue (%)", "Share of revenue actually lost (%)"), ("Une partie des ventes se reporte à plus tard. Estimez la part définitivement perdue.", "Part of sales is deferred rather than lost. Estimate the share permanently lost."), 60),
  ("staff", ("Personnes empêchées de travailler", "People unable to work"), ("", ""), 80),
  ("rate", ("Coût horaire chargé moyen par personne", "Average fully loaded hourly cost per person"), ("Salaire, avantages et frais généraux.", "Salary, benefits and overheads."), 55),
  ("idle_pct", ("Part du temps réellement improductive (%)", "Share of time actually unproductive (%)"), ("Les équipes contournent une partie de la panne : 100 % est rarement réaliste.", "Teams work around part of an outage: 100% is rarely realistic."), 70),
  ("hours", ("Durée de l'interruption (heures)", "Outage duration (hours)"), ("", ""), 8),
  ("penalty", ("Pénalités contractuelles et crédits de service", "Contractual penalties and service credits"), ("Montant total pour l'incident.", "Total for the incident."), 25000),
  ("recovery", ("Coûts de reprise et d'intervention", "Recovery and response costs"), ("Experts externes, heures supplémentaires, matériel de remplacement.", "External experts, overtime, replacement hardware."), 40000),
 ],
 "ui": {
  "fr": {"currency": "Devise (affichage seulement)", "calc": "Calculer", "reset": "Réinitialiser", "total": "Coût estimé de l'incident", "per_hour": "Soit environ {x} par heure d'interruption", "rev": "Revenus perdus", "prod": "Productivité perdue", "pen": "Pénalités et crédits", "rec": "Reprise et intervention",
         "what_if": "Et si l'interruption durait moins longtemps ?", "what_if_t": "Chaque heure gagnée sur la reprise vaut environ {x}. Réduire la durée de {a} h à {b} h économiserait environ {y}.", "invalid": "Entrez des nombres positifs.", "chart": "Répartition du coût estimé"},
  "en": {"currency": "Currency (display only)", "calc": "Calculate", "reset": "Reset", "total": "Estimated cost of the incident", "per_hour": "About {x} per hour of downtime", "rev": "Lost revenue", "prod": "Lost productivity", "pen": "Penalties and credits", "rec": "Recovery and response",
         "what_if": "What if the outage were shorter?", "what_if_t": "Every hour saved on recovery is worth about {x}. Cutting the duration from {a} h to {b} h would save about {y}.", "invalid": "Enter positive numbers.", "chart": "Breakdown of the estimated cost"},
 },
}

# ---------------- Glossary ----------------
GLOSSARY = [
 (("RTO (objectif de temps de reprise)", "RTO (Recovery Time Objective)"), ("Durée maximale visée entre le début d'une interruption et le retour du service à un niveau acceptable.", "The target maximum time between the start of an interruption and the service returning to an acceptable level.")),
 (("RPO (objectif de point de reprise)", "RPO (Recovery Point Objective)"), ("Ancienneté maximale des données que l'on accepte de perdre, mesurée en temps : un RPO de 15 minutes signifie qu'on tolère de perdre au plus les 15 dernières minutes.", "The maximum age of data you accept to lose, measured in time: a 15-minute RPO means you can lose at most the last 15 minutes.")),
 (("MTPD (durée maximale d'interruption tolérable)", "MTPD (Maximum Tolerable Period of Disruption)"), ("Durée au-delà de laquelle l'interruption d'une activité menace la survie de l'organisation. Le RTO doit être inférieur.", "The duration beyond which an activity's interruption threatens the organization's viability. The RTO must be lower.")),
 (("BIA (analyse d'impact sur les activités)", "BIA (Business Impact Analysis)"), ("Démarche qui identifie les activités essentielles, leurs dépendances et l'impact d'une interruption dans le temps, pour fixer les priorités de reprise.", "A process that identifies essential activities, their dependencies and the impact of disruption over time, to set recovery priorities.")),
 (("PCA / continuité des activités", "BCP / business continuity"), ("Ensemble des mesures et plans qui permettent de poursuivre les activités essentielles pendant et après une perturbation.", "The measures and plans that keep essential activities running during and after a disruption.")),
 (("PRA / reprise après sinistre", "DRP / disaster recovery"), ("Volet technique qui rétablit les systèmes informatiques et les données après une panne ou un sinistre.", "The technical side that restores IT systems and data after an outage or disaster.")),
 (("Résilience opérationnelle", "Operational resilience"), ("Capacité à fournir ses services importants malgré une perturbation, et à s'en remettre dans les limites de tolérance fixées.", "The ability to deliver important services despite disruption, and to recover within the tolerances set.")),
 (("Tolérance d'impact", "Impact tolerance"), ("Niveau maximal de perturbation d'un service important que l'organisation est prête à accepter, notion centrale des règles britanniques de résilience opérationnelle.", "The maximum level of disruption to an important service the organization is willing to accept, central to UK operational resilience rules.")),
 (("Service d'affaires important", "Important business service"), ("Service dont l'interruption causerait un préjudice intolérable aux clients ou à l'intégrité du marché.", "A service whose disruption would cause intolerable harm to customers or to market integrity.")),
 (("Rançongiciel", "Ransomware"), ("Logiciel malveillant qui chiffre les données ou bloque l'accès aux systèmes pour exiger une rançon, souvent combiné à un vol de données.", "Malware that encrypts data or blocks access to systems to demand a ransom, often combined with data theft.")),
 (("Double extorsion", "Double extortion"), ("Tactique où l'attaquant chiffre les données et menace aussi de les publier si la rançon n'est pas payée.", "A tactic where the attacker encrypts data and also threatens to publish it if the ransom is not paid.")),
 (("Règle 3-2-1", "3-2-1 rule"), ("Garder trois copies des données, sur deux types de supports, dont une hors site. On la complète souvent par une copie immuable ou isolée.", "Keep three copies of data, on two types of media, one of them off-site. It is often completed with an immutable or isolated copy.")),
 (("Sauvegarde immuable", "Immutable backup"), ("Copie qui ne peut être modifiée ni supprimée pendant une période définie, même par un administrateur, ce qui la protège des rançongiciels.", "A copy that cannot be altered or deleted for a defined period, even by an administrator, which protects it from ransomware.")),
 (("Bascule (failover)", "Failover"), ("Transfert du service vers un site ou un système de secours lorsque le principal tombe en panne.", "Switching the service to a standby site or system when the primary one fails.")),
 (("Site de reprise", "Recovery site"), ("Emplacement de secours (chaud, tiède ou froid selon sa disponibilité) où l'on relance les systèmes après un sinistre.", "A backup location (hot, warm or cold depending on readiness) where systems are restarted after a disaster.")),
 (("Exercice sur table", "Tabletop exercise"), ("Simulation en salle où l'équipe déroule un scénario d'incident et discute de ses décisions, sans manipuler les systèmes.", "A discussion-based simulation where the team walks through an incident scenario and talks through its decisions without touching systems.")),
 (("Test de reprise", "Recovery test"), ("Essai réel de restauration de systèmes et de données pour mesurer les RTO et RPO obtenus.", "A real trial of restoring systems and data to measure the RTO and RPO achieved.")),
 (("Zéro confiance (Zero Trust)", "Zero Trust"), ("Principe selon lequel aucun utilisateur ni appareil n'est approuvé d'office : chaque accès est vérifié, avec des droits réduits au minimum.", "A principle where no user or device is trusted by default: every access is verified, with rights limited to the minimum.")),
 (("Moindre privilège", "Least privilege"), ("Accorder à chaque personne ou système uniquement les accès nécessaires à sa tâche.", "Granting each person or system only the access needed for its task.")),
 (("Authentification multifacteur (MFA)", "Multi-factor authentication (MFA)"), ("Vérification de l'identité avec au moins deux preuves de nature différente, comme un mot de passe et une clé matérielle ou un code.", "Verifying identity with at least two different kinds of proof, such as a password plus a hardware key or code.")),
 (("Clé d'accès (passkey)", "Passkey"), ("Méthode de connexion sans mot de passe reposant sur la cryptographie à clé publique et résistante à l'hameçonnage.", "A passwordless sign-in method based on public-key cryptography that resists phishing.")),
 (("DORA", "DORA"), ("Règlement européen sur la résilience opérationnelle numérique du secteur financier, applicable depuis janvier 2025.", "EU regulation on digital operational resilience for the financial sector, applicable since January 2025.")),
 (("NIS2", "NIS2"), ("Directive européenne qui relève les exigences de cybersécurité pour les entités essentielles et importantes.", "EU directive raising cybersecurity requirements for essential and important entities.")),
 (("Chaîne d'approvisionnement logicielle", "Software supply chain"), ("Ensemble des composants, bibliothèques et fournisseurs dont dépend un logiciel ; un maillon compromis peut toucher tous ses utilisateurs.", "All the components, libraries and vendors a piece of software depends on; one compromised link can affect all its users.")),
 (("Risque lié aux tiers", "Third-party risk"), ("Risque qu'une panne, une faille ou une faillite chez un fournisseur perturbe vos propres services.", "The risk that an outage, flaw or failure at a supplier disrupts your own services.")),
 (("Risque de concentration", "Concentration risk"), ("Dépendance excessive à un seul fournisseur, une seule région ou une seule technologie.", "Excessive dependence on a single supplier, region or technology.")),
 (("Agent IA", "AI agent"), ("Système d'IA qui poursuit un objectif en enchaînant des actions (appeler des outils, écrire, déployer) avec peu ou pas de validation humaine à chaque étape.", "An AI system that pursues a goal by chaining actions (calling tools, writing, deploying) with little or no human approval at each step.")),
 (("Injection de consignes (prompt injection)", "Prompt injection"), ("Attaque qui glisse des instructions dans un contenu lu par une IA pour détourner son comportement.", "An attack that slips instructions into content read by an AI to hijack its behavior.")),
 (("Hallucination", "Hallucination"), ("Réponse d'un modèle d'IA qui paraît plausible mais est fausse ou inventée.", "An AI model output that sounds plausible but is false or made up.")),
 (("IA de l'ombre (shadow AI)", "Shadow AI"), ("Usage d'outils d'IA par le personnel sans l'approbation ni la connaissance de l'organisation.", "Staff use of AI tools without the organization's approval or knowledge.")),
 (("Gouvernance de l'IA", "AI governance"), ("Politiques, rôles, inventaires et contrôles qui encadrent le développement et l'usage de l'IA dans l'organisation.", "The policies, roles, inventories and controls that frame how AI is built and used in the organization.")),
 (("Microsoft Foundry Citadel", "Microsoft Foundry Citadel"), ("Architecture de référence publiée par Microsoft pour gouverner la plateforme d'IA d'entreprise : voir notre page dédiée.", "A reference architecture published by Microsoft for governing an enterprise AI platform: see our dedicated page.")),
]
