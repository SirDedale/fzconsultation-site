# Insights (articles). Evergreen, no statistics that would need a source.
# Blocks: ("h", (fr,en)) heading, ("p", (fr,en)) paragraph, ("ul", [(fr,en),...]) list.

INSIGHTS = [
 {
  "slug": "backups-are-not-recovery",
  "date": "2026-10-26", "mins": 4,
  "title": ("Une sauvegarde n'est pas une reprise", "A backup is not a recovery"),
  "summary": ("Avoir des copies de ses données ne prouve pas qu'on peut relancer l'entreprise. Ce qu'il faut vraiment tester.", "Having copies of your data does not prove you can restart the business. What you actually need to test."),
  "related": ["what-we-do/expertise/disaster-recovery.html", "resources/rto-rpo-worksheet.html"],
  "body": [
   ("p", ("Presque toutes les organisations ont des sauvegardes. Beaucoup moins ont déjà restauré un environnement complet, dans l'ordre, avec le personnel qui devrait le faire un jour de crise. La différence entre les deux est la différence entre une copie et une capacité.", "Almost every organization has backups. Far fewer have ever restored a whole environment, in order, with the people who would have to do it on a bad day. The gap between the two is the gap between a copy and a capability.")),
   ("h", ("Ce qu'une sauvegarde ne dit pas", "What a backup does not tell you")),
   ("ul", [
     ("Combien de temps la restauration prendra réellement, de bout en bout, y compris l'identité, le réseau et les applications qui en dépendent.", "How long restoration will really take, end to end, including identity, network and the applications that depend on them."),
     ("Si les données restaurées sont cohérentes et utilisables par l'application, pas seulement présentes sur un disque.", "Whether restored data is consistent and usable by the application, not just present on a disk."),
     ("Si la sauvegarde elle-même survivrait à une attaque : copies isolées ou immuables, comptes d'administration distincts.", "Whether the backup itself would survive an attack: isolated or immutable copies, separate administration accounts."),
     ("Si quelqu'un d'autre que la personne qui l'a configurée sait la restaurer.", "Whether anyone other than the person who set it up knows how to restore it."),
   ]),
   ("h", ("Un test simple pour commencer", "A simple test to start with")),
   ("p", ("Choisissez un service important. Fixez un objectif de temps de reprise avec son responsable d'affaires. Puis chronométrez une restauration dans un environnement séparé, avec la documentation telle qu'elle existe aujourd'hui. Notez tout ce qui a bloqué : un mot de passe introuvable, une dépendance oubliée, une étape qui n'était écrite nulle part.", "Pick one important service. Set a recovery time objective with its business owner. Then time a restoration in a separate environment, using the documentation as it exists today. Write down everything that got stuck: a missing password, a forgotten dependency, a step that was written down nowhere.")),
   ("p", ("Le premier test échoue presque toujours, et c'est précisément son intérêt. Chaque blocage trouvé en exercice est un blocage que vous n'aurez pas à découvrir pendant un incident.", "The first test almost always fails, and that is exactly its value. Every blocker found in an exercise is one you will not have to discover during an incident.")),
   ("h", ("À retenir", "Takeaways")),
   ("p", ("Mesurez la reprise, pas la sauvegarde. Refaites le test après chaque changement important, et gardez le résultat : c'est la preuve que vos objectifs sont réalistes.", "Measure recovery, not backup. Repeat the test after every significant change, and keep the result: it is the evidence that your objectives are realistic.")),
  ]},
 {
  "slug": "setting-rto-rpo",
  "date": "2026-10-26", "mins": 4,
  "title": ("Fixer ses RTO et RPO : partir de l'affaire, pas des serveurs", "Setting RTO and RPO: start from the business, not the servers"),
  "summary": ("Comment choisir des objectifs de reprise réalistes, que les responsables d'affaires comprennent et que la TI peut tenir.", "How to choose realistic recovery objectives that business owners understand and IT can meet."),
  "related": ["resources/rto-rpo-worksheet.html", "resources/downtime-calculator.html"],
  "body": [
   ("p", ("Les objectifs de reprise sont souvent fixés par la TI, d'après ce que les systèmes savent faire. C'est l'inverse qu'il faut : l'entreprise dit ce qu'elle peut supporter, puis on regarde ce que cela coûte d'y arriver.", "Recovery objectives are often set by IT, based on what the systems can do. It should be the other way round: the business says what it can bear, then you look at what it costs to get there.")),
   ("h", ("Trois questions pour chaque service", "Three questions for each service")),
   ("ul", [
     ("Après combien de temps d'arrêt les dégâts deviennent-ils inacceptables : clients perdus, obligations manquées, sécurité des personnes ?", "After how long a stoppage does the damage become unacceptable: lost customers, missed obligations, safety of people?"),
     ("Combien de données récentes peut-on perdre, et peut-on les ressaisir à la main ?", "How much recent data can we lose, and can we re-enter it by hand?"),
     ("Que se passe-t-il pendant l'arrêt : existe-t-il un mode dégradé, un processus manuel ?", "What happens during the outage: is there a degraded mode, a manual process?"),
   ]),
   ("h", ("Le coût est le levier de la discussion", "Cost is the lever of the conversation")),
   ("p", ("Un RTO de quinze minutes n'a pas le même prix qu'un RTO de huit heures. Mettre un chiffre sur le coût d'une heure d'arrêt, même approximatif, transforme une discussion technique en décision d'investissement. Notre calculateur d'ordre de grandeur peut servir de point de départ.", "A fifteen-minute RTO does not cost the same as an eight-hour one. Putting a number on the cost of an hour of downtime, even a rough one, turns a technical discussion into an investment decision. Our order-of-magnitude calculator can be a starting point.")),
   ("h", ("Pièges fréquents", "Common pitfalls")),
   ("ul", [
     ("Tout classer « critique » : si tout est prioritaire, rien ne l'est, et le budget ne suit pas.", "Labelling everything \"critical\": if everything is a priority, nothing is, and the budget will not follow."),
     ("Oublier les dépendances : un service ne repart pas avant l'identité, le DNS ou le réseau dont il dépend.", "Forgetting dependencies: a service does not restart before the identity, DNS or network it relies on."),
     ("Ne jamais mesurer : un objectif jamais testé est une hypothèse.", "Never measuring: an objective that has never been tested is an assumption."),
   ]),
   ("p", ("Fixez des niveaux simples, faites-les valider par la direction, puis testez les services du niveau le plus élevé en premier.", "Set simple tiers, get them approved by leadership, then test the highest-tier services first.")),
  ]},
 {
  "slug": "ai-agents-need-recovery-plans",
  "date": "2026-10-26", "mins": 4,
  "title": ("Les agents IA ont aussi besoin d'un plan de reprise", "AI agents need a recovery plan too"),
  "summary": ("Dès qu'un agent agit au nom de l'organisation, il devient un système critique. Cinq questions à se poser avant la mise en production.", "As soon as an agent acts on the organization's behalf, it becomes a critical system. Five questions to ask before going live."),
  "related": ["ai/agents.html", "ai/governance.html", "resources/ai-acceptable-use-policy.html"],
  "body": [
   ("p", ("Un assistant qui rédige un brouillon est un outil. Un agent qui envoie des courriels, modifie des dossiers ou déclenche des paiements est un acteur de votre système d'information, avec des accès, des erreurs possibles et des pannes. Il mérite la même rigueur que n'importe quel système critique.", "An assistant that drafts text is a tool. An agent that sends emails, edits records or triggers payments is an actor in your information system, with access, possible mistakes and outages. It deserves the same rigor as any critical system.")),
   ("h", ("Cinq questions avant la mise en production", "Five questions before going live")),
   ("ul", [
     ("Qui en est le propriétaire, et qui peut l'arrêter immédiatement ?", "Who owns it, and who can stop it immediately?"),
     ("À quoi a-t-il accès ? Les droits sont-ils réduits au strict nécessaire, avec une identité qui lui est propre ?", "What can it access? Are its rights limited to what is strictly necessary, with an identity of its own?"),
     ("Quelles actions sont irréversibles, et lesquelles exigent l'approbation d'une personne ?", "Which actions are irreversible, and which require a person's approval?"),
     ("Peut-on reconstituer ce qu'il a fait ? Journaux, traces des décisions et des sources consultées.", "Can we reconstruct what it did? Logs, traces of decisions and of sources consulted."),
     ("Que fait l'entreprise si l'agent ou la plateforme qui l'héberge tombe en panne ? Existe-t-il un mode manuel ?", "What does the business do if the agent or its hosting platform goes down? Is there a manual fallback?"),
   ]),
   ("h", ("Les nouveaux risques à prévoir", "New risks to plan for")),
   ("p", ("Au-delà des pannes classiques, les agents introduisent des risques propres : des instructions cachées dans un document ou une page web peuvent détourner leur comportement (injection de consignes), et une réponse plausible mais fausse peut déclencher une action réelle. Les limites d'accès et la validation humaine des actions sensibles sont vos meilleures protections.", "Beyond ordinary outages, agents bring their own risks: instructions hidden in a document or web page can hijack their behavior (prompt injection), and a plausible but wrong answer can trigger a real action. Access limits and human approval of sensitive actions are your best protections.")),
   ("h", ("Par où commencer", "Where to start")),
   ("p", ("Inventoriez les outils et agents déjà utilisés, y compris ceux que le personnel a adoptés sans en parler. Adoptez une politique d'utilisation claire, puis traitez chaque agent en production comme un service du plan de continuité : avec un propriétaire, un objectif de reprise et un test.", "Inventory the tools and agents already in use, including those staff adopted without telling anyone. Adopt a clear usage policy, then treat each production agent as a service in the continuity plan: with an owner, a recovery objective and a test.")),
  ]},
]
