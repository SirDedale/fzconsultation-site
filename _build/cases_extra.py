# Additions to the case studies: a one-line takeaway and a "Monday-morning check" for every case,
# plus three new cases (2025) built only from sources that were opened and read on 2026-10-29.
# Every string is a (fr, en) pair. Links are site paths; build.py rewrites retired paths to their new home.

CASE_EXTRA = {
 "tsb-2018": {
  "line": ("Une date de mise en service est une décision, pas un plan : TSB a planifié à rebours depuis la date, et ses clients en ont payé le prix.",
           "A go-live date is a decision, not a plan: TSB worked backwards from the date, and its customers paid for it."),
  "monday": [
   ("Prenez votre prochain grand changement. Chaque phase a-t-elle été estimée avant que la date soit fixée ?", "Take your next big change. Was each phase estimated before the date was fixed?"),
   ("Existe-t-il un retour arrière que vous avez réellement répété, sur tous les centres de données ?", "Is there a rollback you have actually rehearsed, across every data centre?"),
   ("Demandez à votre fournisseur TI le plus critique, même interne, des preuves de test plutôt que des assurances.", "Ask your most critical IT supplier, even an internal one, for test evidence rather than reassurance."),
  ],
  "tool": ("what-we-do/services/exercises.html", ("Répéter un retour arrière", "Rehearse a rollback")),
 },
 "colonial-pipeline-2021": {
  "line": ("Un mot de passe VPN sans second facteur a suffi à arrêter un oléoduc : l'entreprise ne pouvait pas prouver que le côté opérationnel était sain.",
           "One VPN password without a second factor was enough to stop a pipeline: the company could not show that the operational side was safe."),
  "monday": [
   ("Listez chaque accès à distance (VPN, bureau à distance, portails). Lesquels n'exigent pas l'authentification multifacteur ?", "List every remote access path (VPN, remote desktop, portals). Which ones do not require multi-factor authentication?"),
   ("Désactivez les comptes inactifs, surtout ceux qui ont un accès VPN.", "Disable inactive accounts, especially those with VPN access."),
   ("Si vos systèmes TI étaient isolés demain, vos opérations pourraient-elles continuer, et selon quel critère décideriez-vous d'arrêter ?", "If your IT systems were isolated tomorrow, could operations continue, and on what criterion would you decide to stop?"),
  ],
  "tool": ("resources/ransomware-checklist.html", ("La liste de vérification rançongiciel", "The ransomware checklist")),
 },
 "marks-and-spencer-2025": {
  "line": ("Les attaquants sont entrés par le service d'assistance d'un tiers : votre processus de réinitialisation de mot de passe est une porte d'entrée.",
           "The attackers came in through a third party's help desk: your password-reset process is a front door."),
  "monday": [
   ("Que vérifie votre service d'assistance, et celui de votre fournisseur, avant de réinitialiser un mot de passe ou un second facteur ?", "What does your help desk, and your provider's, check before resetting a password or a second factor?"),
   ("Si les commandes, les paiements et les stocks tombaient ensemble, quelle est la procédure manuelle, et qui l'a déjà essayée ?", "If orders, payments and stock failed together, what is the manual procedure, and who has tried it?"),
   ("Dans quel ordre vos services reviendraient-ils, et cet ordre est-il écrit ?", "In what order would your services come back, and is that order written down?"),
  ],
  "tool": ("resources/downtime-calculator.html", ("Chiffrer une semaine sans ventes en ligne", "Put a number on a week without online sales")),
 },
 "change-healthcare-2024": {
  "line": ("La politique exigeait l'authentification multifacteur ; un portail faisait exception. Vérifiez, ne supposez pas.",
           "Policy required multi-factor authentication; one portal was the exception. Verify, don't assume."),
  "monday": [
   ("Testez chaque point d'accès exposé : exige-t-il vraiment un second facteur, y compris les systèmes hérités d'une acquisition ?", "Test every exposed access point: does it really enforce a second factor, including systems inherited through an acquisition?"),
   ("Quel fournisseur intermédiaire arrêterait votre activité s'il tombait, et quel est votre plan de rechange ?", "Which intermediary, if it went down, would stop your business, and what is your fallback?"),
   ("Pourriez-vous restaurer sans payer ? Quand avez-vous restauré pour la dernière fois, en vrai ?", "Could you restore without paying? When did you last restore for real?"),
  ],
  "tool": ("self-assessment.html", ("Mesurer votre dépendance aux tiers", "Measure your third-party dependence")),
 },
 "norsk-hydro-2019": {
  "line": ("Hydro n'a pas payé : elle a produit à la main et dit la vérité. Le mode manuel doit exister avant l'attaque.",
           "Hydro did not pay: it produced by hand and told the truth. The manual mode has to exist before the attack."),
  "monday": [
   ("Pour votre service le plus important, où est la procédure papier, et à quand remonte sa dernière répétition ?", "For your most important service, where is the paper procedure, and when was it last rehearsed?"),
   ("Savez-vous reconstruire votre annuaire (Active Directory ou équivalent) à partir de zéro, et combien de temps cela prendrait ?", "Can you rebuild your directory (Active Directory or equivalent) from scratch, and how long would it take?"),
   ("Qui parlerait aux clients et aux marchés dans la première heure, avec quel texte prêt ?", "Who would speak to customers and markets in the first hour, with what prepared text?"),
  ],
  "tool": ("resources/ransomware-checklist.html", ("La liste de vérification rançongiciel", "The ransomware checklist")),
 },
 "crowdstrike-delta-2024": {
  "line": ("Ce n'était pas une attaque : une mise à jour déployée partout en même temps a suffi. Votre outil de sécurité est aussi un point de défaillance unique.",
           "It was not an attack: one update deployed everywhere at once was enough. Your security tool is also a single point of failure."),
  "monday": [
   ("Quels logiciels reçoivent des mises à jour automatiques sur tout votre parc en même temps, sans déploiement progressif ?", "Which software receives automatic updates across your whole estate at once, with no staged rollout?"),
   ("Où sont vos clés de récupération (BitLocker, par exemple), et pourriez-vous y accéder si votre réseau était à terre ?", "Where are your recovery keys (BitLocker, for example), and could you reach them if your network were down?"),
   ("Après le retour des systèmes, combien de temps pour reprogrammer équipes, stocks ou rendez-vous ?", "Once systems are back, how long to reschedule crews, stock or appointments?"),
  ],
  "tool": ("resources/rto-rpo-worksheet.html", ("La feuille de travail RTO/RPO", "The RTO/RPO worksheet")),
 },
 # --- the three new cases below carry their own extras
 "aws-us-east-1-2025": {
  "line": ("Un enregistrement DNS vide dans une région : quatorze heures et demie de perturbation. Le coupable n'était pas un serveur, c'était l'automatisation.",
           "One empty DNS record in one region: fourteen and a half hours of disruption. The culprit was not a server, it was automation."),
  "monday": [
   ("Quels services de votre organisation dépendent d'une seule région infonuagique, y compris pour l'identité, les files de messages ou la configuration ?", "Which of your services depend on a single cloud region, including for identity, queues or configuration?"),
   ("Si la console de votre fournisseur et son support étaient inaccessibles, comment joindriez-vous vos équipes et vos clients ?", "If your provider's console and support were unreachable, how would you reach your teams and customers?"),
   ("Avez-vous déjà simulé la perte d'une région, pas seulement d'un serveur, en mesurant le temps réel de reprise ?", "Have you ever simulated losing a region, not just a server, and timed the real recovery?"),
  ],
  "tool": ("resources/downtime-calculator.html", ("Chiffrer une journée de panne infonuagique", "Put a number on a day of cloud outage")),
 },
 "jaguar-land-rover-2025": {
  "line": ("Une cyberattaque sur un constructeur est une panne pour des milliers de fournisseurs : l'État a dû garantir un prêt de 1,5 G£.",
           "A cyberattack on one manufacturer is an outage for thousands of suppliers: the government had to guarantee a £1.5bn loan."),
  "monday": [
   ("Quels systèmes votre production ne peut-elle pas contourner, et pourriez-vous les isoler sans arrêter l'usine ?", "Which systems can your production not run without, and could you isolate them without stopping the plant?"),
   ("Avez-vous préparé un redémarrage par étapes : ce qui revient en premier, en deuxième, et qui l'autorise ?", "Have you prepared a staged restart: what comes back first, second, and who authorizes it?"),
   ("Combien de semaines vos fournisseurs clés tiendraient-ils si vous arrêtiez de les commander ? Le savez-vous, ou le supposez-vous ?", "How many weeks could your key suppliers last if you stopped ordering? Do you know, or are you assuming?"),
  ],
  "tool": ("resources/downtime-calculator.html", ("Chiffrer un arrêt de production de plusieurs semaines", "Put a number on a multi-week production stop")),
 },
 "collins-aerospace-2025": {
  "line": ("Un seul fournisseur de logiciel d'enregistrement, quatre aéroports en mode papier. Le plan B manuel n'a pas été conçu pour un week-end de pointe.",
           "One check-in software vendor, four airports on paper. The manual plan B was not designed for a peak weekend."),
  "monday": [
   ("Quelles plateformes partagées avec d'autres clients de votre fournisseur arrêteraient votre activité d'un seul coup ?", "Which platforms shared with your vendor's other customers could stop your business in one blow?"),
   ("Votre mode manuel tient-il à pleine charge, un jour de pointe ? Combien de personnes de plus faut-il ?", "Does your manual mode hold at full volume on a peak day? How many extra people does it need?"),
   ("Avant de reconstruire, comment sauriez-vous que l'attaquant n'est plus dans le système ?", "Before you rebuild, how would you know the attacker is no longer in the system?"),
  ],
  "tool": ("resources/ransomware-checklist.html", ("La liste de vérification rançongiciel", "The ransomware checklist")),
 },
}

NEW_CASES = [
 {
  "path": "case-studies/aws-us-east-1-2025.html",
  "sector": ("Infonuagique", "Cloud"),
  "short": ("AWS us-east-1 : un enregistrement DNS vide, une journée de pannes en cascade", "AWS us-east-1: one empty DNS record, a day of cascading failures"),
  "summary": ("Monde, octobre 2025. Une condition de concurrence dans l'automatisation DNS de DynamoDB prive la région d'une adresse, et de nombreux services tombent avec elle.",
              "Worldwide, October 2025. A race condition in DynamoDB's DNS automation leaves a region without an address, and many services fall with it."),
  "facts": [
    (("Secteur", "Sector"), ("Infonuagique, tous secteurs", "Cloud infrastructure, all sectors")),
    (("Région", "Region"), ("us-east-1 (Virginie du Nord)", "us-east-1 (N. Virginia)")),
    (("Date", "Date"), ("19–20 octobre 2025", "19–20 October 2025")),
    (("Durée de l'événement", "Event window"), ("Environ 14 h 30, de 23 h 48 (HAP) à 14 h 20 (HAP)", "About 14.5 hours, from 11:48 PM to 2:20 PM PDT")),
    (("Cause selon AWS", "Cause according to AWS"), ("Condition de concurrence latente dans la gestion DNS de DynamoDB", "A latent race condition in DynamoDB's DNS management")),
  ],
  "timeline": [
    (("19 oct., 23 h 48 (HAP)", "19 Oct, 11:48 PM PDT"), ("Les appels à l'API DynamoDB échouent en us-east-1 : clients et services AWS ne peuvent plus ouvrir de nouvelles connexions.",
                                 "DynamoDB API calls start failing in us-east-1: customers and AWS services cannot open new connections.")),
    (("20 oct., 0 h 38", "20 Oct, 12:38 AM"), ("AWS identifie l'état DNS de DynamoDB comme source du problème.", "AWS identifies DynamoDB's DNS state as the source.")),
    (("2 h 25 – 2 h 40", "2:25 – 2:40 AM"), ("Toutes les informations DNS sont rétablies ; les enregistrements en cache expirent et les clients se reconnectent. DynamoDB est de retour, après environ 2 h 52.",
                                 "All DNS information is restored; cached records expire and customers reconnect. DynamoDB is back after about 2 hours 52 minutes.")),
    (("2 h 25 – 10 h 36", "2:25 – 10:36 AM"), ("Le lancement d'instances EC2 continue d'échouer pendant des heures après le retour de DynamoDB.", "EC2 instance launches keep failing for hours after DynamoDB has recovered.")),
    (("5 h 30 – 14 h 09", "5:30 AM – 2:09 PM"), ("Les répartiteurs de charge réseau (NLB) renvoient des erreurs de connexion, à cause d'échecs de vérification de santé.", "Network Load Balancers return connection errors because of health-check failures.")),
    (("20 oct., 14 h 20", "20 Oct, 2:20 PM"), ("Fin de l'événement selon AWS. Certains clusters Redshift restent altérés jusqu'au 21 octobre.", "End of the event according to AWS. Some Redshift clusters stay impaired until 21 October.")),
  ],
  "wrong": [
    (("Une automatisation qui se défait elle-même", "Automation that undid itself"), ("Selon AWS, deux « Enactors » DNS se sont croisés : l'un, en retard, a appliqué un ancien plan après un plan plus récent ; le nettoyage a ensuite supprimé l'ancien plan et retiré toutes les adresses du point d'accès régional. Le système, incohérent, a exigé une intervention manuelle.",
                                  "According to AWS, two DNS Enactors collided: a delayed one applied an old plan after a newer one, and the cleanup then deleted the old plan and removed every address of the regional endpoint. The system was left inconsistent and needed manual intervention.")),
    (("Le correctif n'était que la moitié de la reprise", "The fix was only half of the recovery"), ("Une fois le DNS rétabli à 2 h 25, le lancement d'instances EC2 a échoué jusqu'à 10 h 36 et les erreurs NLB ont duré jusqu'à 14 h 09. La reprise d'un service en amont ne règle pas ses dépendants.",
                                  "Once DNS was restored at 2:25 AM, EC2 launches kept failing until 10:36 AM and NLB errors lasted until 2:09 PM. Recovering an upstream service does not recover its dependents.")),
    (("Les outils pour réagir étaient dans la zone touchée", "The tools to respond were inside the blast radius"), ("Les connexions à la console AWS par utilisateurs IAM ont échoué pendant plus d'une heure et demie et l'accès aux dossiers du Centre de support a été bloqué pendant près de trois heures.",
                                  "IAM user sign-in to the AWS console failed for over an hour and a half, and access to Support Center cases was blocked for almost three hours.")),
  ],
  "lessons": [
    (("Trouvez votre dépendance régionale cachée", "Find your hidden regional dependency"), ("Beaucoup de services « globaux » reposent en réalité sur une région. Cartographiez-les avant la panne.", "Many “global” services quietly depend on one region. Map them before the outage."), "what-we-do/services/assessments.html"),
    (("Testez la panne du fournisseur, pas seulement la vôtre", "Test the provider's failure, not just yours"), ("Simulez la perte d'une région et chronométrez la reprise réelle, avec les dépendances en cascade.", "Simulate losing a region and time the real recovery, cascading dependencies included."), "what-we-do/services/exercises.html"),
    (("Gardez un canal hors bande", "Keep an out-of-band channel"), ("Prévoyez comment joindre équipes, clients et fournisseur quand vos outils habituels sont inaccessibles.", "Plan how to reach teams, customers and your provider when your usual tools are unreachable."), "resources/ransomware-checklist.html"),
  ],
  "sources": [
    ("AWS: Summary of the Amazon DynamoDB Service Disruption in the Northern Virginia (US-EAST-1) Region", "https://aws.amazon.com/message/101925"),
  ],
 },
 {
  "path": "case-studies/jaguar-land-rover-2025.html",
  "sector": ("Industrie", "Manufacturing"),
  "short": ("Jaguar Land Rover : des semaines d'usines à l'arrêt, un prêt garanti par l'État", "Jaguar Land Rover: weeks of idle factories and a state-backed loan"),
  "summary": ("Royaume-Uni, 2025. Une cyberattaque arrête la production pendant des semaines et touche plus de 5 000 organisations de la chaîne d'approvisionnement.",
              "UK, 2025. A cyberattack stops production for weeks and reaches over 5,000 organisations across the supply chain."),
  "facts": [
    (("Secteur", "Sector"), ("Construction automobile", "Automotive manufacturing")),
    (("Pays", "Country"), ("Royaume-Uni", "United Kingdom")),
    (("Date", "Date"), ("Confirmée le 2 septembre 2025", "Confirmed on 2 September 2025")),
    (("Durée", "Duration"), ("Production arrêtée pendant des semaines, reprise progressive début octobre 2025", "Production stopped for weeks, restarted in stages from early October 2025")),
    (("Coût estimé", "Estimated cost"), ("1,9 G£ pour l'économie britannique (fourchette 1,6–2,1 G£), selon le Cyber Monitoring Centre", "£1.9bn to the UK economy (range £1.6–2.1bn), according to the Cyber Monitoring Centre")),
  ],
  "timeline": [
    (("2 septembre 2025", "2 September 2025"), ("JLR confirme un incident de cybersécurité, indique avoir pris des mesures immédiates pour en limiter l'impact et déclare que ses activités de vente et de production sont « fortement perturbées ».",
                                  "JLR confirms a cyber incident, says it took immediate action to mitigate the impact, and states that its retail and production activities are “severely disrupted”.")),
    (("Semaines suivantes", "Following weeks"), ("L'assemblage est suspendu à Solihull et Halewood ; l'usine de moteurs de Wolverhampton est touchée ; les concessionnaires ne peuvent plus traiter de commandes (selon la presse spécialisée).",
                                  "Assembly is suspended at Solihull and Halewood; the Wolverhampton engine plant is affected; dealers cannot process new orders (according to trade press).")),
    (("Dans les semaines qui suivent", "In the weeks that follow"), ("Le gouvernement britannique annonce un prêt de 1,5 G£ à JLR, en grande partie garanti par UK Export Finance.", "The UK government announces a £1.5bn loan to JLR, largely guaranteed by UK Export Finance.")),
    (("Début octobre 2025", "Early October 2025"), ("La production reprend progressivement.", "Production restarts gradually.")),
    (("Fin octobre 2025", "Late October 2025"), ("Le Cyber Monitoring Centre estime le coût à 1,9 G£ et classe l'événement en catégorie 3, qualifiant l'attaque d'événement cyber le plus coûteux pour l'économie britannique.",
                                  "The Cyber Monitoring Centre estimates the cost at £1.9bn and rates the event Category 3, calling it the most economically damaging cyber event to hit the UK.")),
  ],
  "wrong": [
    (("Une production qui ne tenait pas sans ses systèmes", "A production line that could not run without its systems"), ("Selon les comptes rendus, le confinement a consisté à désactiver des systèmes centraux, et l'usine n'a pas pu fonctionner sans eux pendant des semaines. Le mode dégradé, s'il existait, n'a pas suffi.",
                                  "According to reports, containment meant switching off core systems, and the plants could not run without them for weeks. A degraded mode, if one existed, was not enough.")),
    (("Une panne qui devient celle de toute la chaîne", "An outage that becomes the whole chain's outage"), ("Le CMC compte plus de 5 000 organisations britanniques touchées, des fournisseurs aux transports et à la vente. L'État a dû garantir un prêt de 1,5 G£ à l'entreprise.",
                                  "The CMC counts over 5,000 UK organisations affected, from suppliers to transport and retail. The government had to guarantee a £1.5bn loan to the company.")),
    (("Des identifiants comme porte d'entrée (revendication)", "Credentials as the way in (a claim)"), ("Le groupe Scattered Lapsus$ Hunters a affirmé avoir utilisé des identifiants Atlassian Jira volés, obtenus par logiciels malveillants et hameçonnage. Cette affirmation provient des attaquants et n'est pas confirmée par JLR.",
                                  "The Scattered Lapsus$ Hunters group claimed it used stolen Atlassian Jira credentials, obtained through malware and phishing. This claim comes from the attackers and is not confirmed by JLR.")),
  ],
  "lessons": [
    (("Sachez ce que la production ne peut pas contourner", "Know what production cannot run without"), ("Listez les systèmes sans lesquels la ligne s'arrête et décidez à l'avance si on peut les isoler sans arrêter l'usine.", "List the systems the line cannot run without and decide in advance whether they can be isolated without stopping the plant."), "what-we-do/services/assessments.html"),
    (("Répétez un redémarrage par étapes", "Rehearse a staged restart"), ("Fixez l'ordre de retour des systèmes et qui l'autorise, puis essayez-le avant l'incident.", "Set the order in which systems return and who authorizes it, then try it before the incident."), "what-we-do/services/exercises.html"),
    (("Protégez les identifiants des outils internes", "Protect credentials to internal tools"), ("Authentification multifacteur et revue des accès sur les outils de développement et de gestion, pas seulement sur la messagerie.", "Multi-factor authentication and access reviews on engineering and project tools, not just on email."), "what-we-do/expertise/cybersecurity.html"),
  ],
  "sources": [
    ("Teiss: Cyberattack on Jaguar Land Rover costs the UK £1.9 billion, says the CMC", "https://www.teiss.co.uk/news/cyberattack-on-jaguar-land-rover-costs-company-19-billion-says-cmc-16607"),
    ("Security Affairs: Cyberattack on Jaguar Land Rover inflicts $2.5B loss on UK economy", "https://securityaffairs.com/183733/security/cyberattack-on-jaguar-land-rover-inflicts-2-5b-loss-on-uk-economy.html"),
    ("Automotive Manufacturing Solutions: JLR shuts IT systems, halts UK plant production after cyberattack", "https://www.automotivemanufacturingsolutions.com/news/jlr-shuts-it-systems-halts-uk-plant-production-after-cyberattack/661733"),
  ],
 },
 {
  "path": "case-studies/collins-aerospace-2025.html",
  "sector": ("Transport aérien", "Aviation"),
  "short": ("Collins Aerospace : un seul logiciel d'enregistrement, quatre aéroports en mode papier", "Collins Aerospace: one check-in system, four airports on paper"),
  "summary": ("Europe, septembre 2025. Un rançongiciel touche un logiciel d'enregistrement partagé et force Heathrow, Bruxelles, Berlin et Dublin à passer en mode manuel.",
              "Europe, September 2025. Ransomware hits a shared check-in system and forces Heathrow, Brussels, Berlin and Dublin onto manual processes."),
  "facts": [
    (("Secteur", "Sector"), ("Aéroports et compagnies aériennes", "Airports and airlines")),
    (("Portée", "Scope"), ("Heathrow, Bruxelles, Berlin Brandebourg, Dublin", "Heathrow, Brussels, Berlin Brandenburg, Dublin")),
    (("Date", "Date"), ("À partir du vendredi 19 septembre 2025, en soirée", "From the evening of Friday 19 September 2025")),
    (("Nature", "Nature"), ("Rançongiciel sur un logiciel de traitement des passagers, confirmé par l'ENISA", "Ransomware on passenger-processing software, confirmed by ENISA")),
    (("Fournisseur", "Vendor"), ("Collins Aerospace (RTX)", "Collins Aerospace (RTX)")),
  ],
  "timeline": [
    (("Vendredi 19 septembre, soir", "Friday 19 September, evening"), ("L'enregistrement et le dépôt des bagages deviennent indisponibles dans plusieurs aéroports européens.", "Check-in and baggage drop become unavailable at several European airports.")),
    (("Samedi 20 septembre", "Saturday 20 September"), ("Des médias évoquent un rançongiciel ; Collins parle seulement d'une « attaque liée à la cybersécurité » et ne confirme pas.", "Media report ransomware; Collins refers only to a “cyber-related attack” and does not confirm.")),
    (("Week-end", "Weekend"), ("Les aéroports émettent des cartes d'embarquement à la main ; à Berlin, un marathon de plus de 55 000 participants aggrave la situation. Heathrow est toujours en reprise dimanche.", "Airports issue boarding passes by hand; in Berlin, a marathon with over 55,000 participants worsens the situation. Heathrow is still recovering on Sunday.")),
    (("Lundi 22 septembre", "Monday 22 September"), ("L'ENISA confirme qu'il s'agit d'un rançongiciel visant le logiciel MUSE de Collins. Bruxelles demande aux compagnies d'annuler 140 de ses 276 vols au départ prévus ce jour-là ; Dublin reste perturbé.",
                                 "ENISA confirms ransomware targeting Collins's MUSE software. Brussels asks airlines to cancel 140 of its 276 scheduled outbound flights for the day; Dublin remains disrupted.")),
  ],
  "wrong": [
    (("Un fournisseur, plusieurs aéroports", "One vendor, several airports"), ("Une plateforme partagée par des clients différents est un point de défaillance commun : une seule compromission a touché plusieurs aéroports à la fois.", "A platform shared by different customers is a common point of failure: one compromise hit several airports at once.")),
    (("Un mode manuel pas conçu pour la pointe", "A manual mode not built for peak volume"), ("Les cartes d'embarquement ont été faites à la main, avec retards et annulations à la clé. Un mode dégradé existe ; la question est à quel volume il tient.", "Boarding passes were written by hand, with delays and cancellations. A degraded mode existed; the question is at what volume it holds.")),
    (("Reconstruire avec l'attaquant encore présent", "Rebuilding with the attacker still present"), ("Selon le compte rendu de TechRepublic, Heathrow a indiqué que plus de 1 000 ordinateurs pouvaient être touchés et que Collins avait constaté la présence des pirates au moment de reconstruire le système.", "According to TechRepublic's report, Heathrow said over 1,000 computers could have been affected and that Collins found the hackers were still present when it tried to rebuild the system.")),
  ],
  "lessons": [
    (("Cartographiez les plateformes partagées", "Map shared platforms"), ("Identifiez les fournisseurs dont la panne arrêterait votre activité et ce que vous feriez ce jour-là.", "Identify the vendors whose outage would stop your business and what you would do that day."), "what-we-do/services/assessments.html"),
    (("Répétez le mode manuel à pleine charge", "Rehearse manual mode at full load"), ("Un exercice en période de pointe montre combien de personnes il faut, et ce qui casse.", "A peak-period exercise shows how many people it takes, and what breaks."), "what-we-do/services/exercises.html"),
    (("Évincez avant de reconstruire", "Evict before you rebuild"), ("Confirmez que l'attaquant n'est plus là avant de restaurer, sinon vous recommencez.", "Confirm the attacker is gone before restoring, or you start over."), "resources/ransomware-checklist.html"),
  ],
  "sources": [
    ("TechRepublic: Ransomware Attack Disrupted Airports Across Europe, Cyber Agency Confirms", "https://www.techrepublic.com/article/news-eu-airport-ransomware/"),
    ("heise online: EU cyber authority confirms ransomware attack on airport software (in German)", "https://heise.de/-10666179"),
  ],
 },
]
