# Monthly series: "What this outage teaches" / "Ce que cette panne nous apprend".
# Format of every issue: facts box, what we know, what we do not know yet, what it teaches, a Monday-morning check, sources.
# House rules: only sources that were opened and read; claims attributed; the company's own words in quotes;
# no statement about a named company's dependency unless that company confirmed it.
# Extra block kinds on top of insights.py: ("facts", [(label, value)]), ("check", [item]), ("src", [(title, url)]).

SERIES = ("Ce que cette panne nous apprend", "What this outage teaches")
SERIES_BLURB = ("Une note par mois : ce qui s'est passé, ce que nous ne savons pas encore, ce que cela enseigne, et trois ou quatre vérifications à faire lundi matin. Sources lues, affirmations attribuées.",
                "One note a month: what happened, what we do not know yet, what it teaches, and three or four checks for Monday morning. Sources read, claims attributed.")

NOTES = [
 {
  "slug": "outage-note-2026-10-google-cloud-london",
  "series": True, "issue": 1,
  "date": "2026-10-29", "mins": 3,
  "title": ("Octobre 2026 : une zone de Google Cloud à Londres, environ huit heures",
            "October 2026: one Google Cloud zone in London, about eight hours"),
  "summary": ("Une panne d'alimentation dans une zone de Google Cloud a paralysé des services pendant des heures. Ce que l'on sait, ce que l'on ignore encore, et quoi vérifier lundi.",
              "A power event in one Google Cloud zone took services down for hours. What we know, what we do not know yet, and what to check on Monday."),
  "related": ["case-studies/aws-us-east-1-2025.html", "what-we-do/services/exercises.html", "resources/downtime-calculator.html"],
  "body": [
   ("facts", [
     (("Quand", "When"), ("Impact dès 6 h 08 UTC le 20 octobre 2026 ; « atténué pour la plupart des clients » à 14 h 03 UTC", "Impact from about 06:08 UTC on 20 October 2026; “mitigated for most customers” at 14:03 UTC")),
     (("Où", "Where"), ("europe-west2-b, l'une des trois zones de la région de Londres", "europe-west2-b, one of the three zones of the London region")),
     (("Cause selon Google", "Cause according to Google"), ("« A power event caused an outage within europe-west2-b zone. »", "“A power event caused an outage within europe-west2-b zone.”")),
     (("Services cités", "Services named"), ("BigQuery Data Transfer Service, Cloud Filestore, Cloud Run, App Engine, NetApp Volumes, GKE, Managed Kafka (d'après The Register)", "BigQuery Data Transfer Service, Cloud Filestore, Cloud Run, App Engine, NetApp Volumes, GKE, Managed Kafka (per The Register)")),
     (("Pas encore public", "Not yet public"), ("L'analyse d'incident de Google, promise à la fin de son enquête interne", "Google's incident analysis, promised once its internal investigation is complete")),
   ]),
   ("h", ("Ce que l'on sait", "What we know")),
   ("p", ("Aux premières heures du 20 octobre, un incident d'alimentation électrique a mis hors service une zone de la région londonienne de Google Cloud. L'impact pour les clients a commencé vers 6 h 08 UTC. À 11 h 58 UTC, Google prévoyait, sous réserve, une reprise complète pour 13 h 00 UTC ; à 14 h 03 UTC, il décrivait le problème comme atténué pour la plupart des clients, un très petit nombre restant touchés. Environ huit heures entre le premier impact et « surtout réglé ».",
          "In the early hours of 20 October, a power event took a zone of Google Cloud's London region offline. Customer impact began around 06:08 UTC. At 11:58 UTC Google tentatively projected full recovery by 13:00 UTC, and at 14:03 UTC it described the issue as mitigated for most customers, with a very small number still affected. Roughly eight hours from first impact to “mostly fixed”.")),
   ("p", ("Plusieurs organisations britanniques connues ont été signalées comme touchées, dont Lloyds Bank, HSBC, Royal Mail, Rightmove, DPD, BT, Screwfix et Revolut. Ces signalements viennent de la presse et de sites de suivi des pannes. Dans les sources que nous avons lues, aucune de ces entreprises ne l'avait confirmé, et nous ne savons pas lesquelles dépendaient de la zone touchée.",
          "Several well-known UK organizations were reported as affected, among them Lloyds Bank, HSBC, Royal Mail, Rightmove, DPD, BT, Screwfix and Revolut. Those reports come from the press and outage trackers. In the sources we read, none of those companies had confirmed it, and we do not know which of them depended on the affected zone.")),
   ("h", ("Ce que l'on ignore encore", "What we do not know yet")),
   ("ul", [
     ("La cause au-delà de « incident d'alimentation » : Google a promis une analyse une fois son enquête interne terminée.", "The cause beyond “power event”: Google has promised an analysis once its internal investigation is complete."),
     ("Pourquoi la perte d'une zone a été visible de tant de monde. Google ne parle que d'une zone ; un universitaire cité par The Register parle d'une panne « régionale, centrée sur europe-west2 ».", "Why the loss of one zone was visible to so many. Google speaks of one zone only; an academic quoted by The Register calls it “a regional outage centered on europe-west2”."),
     ("Si les clients touchés avaient une conception multi-zones qui n'a pas basculé, ou une conception à zone unique.", "Whether the affected customers had multi-zone designs that failed to fail over, or single-zone designs."),
   ]),
   ("h", ("Ce que cela enseigne", "What it teaches")),
   ("p", ("Une zone est censée être l'unité que l'on peut perdre. La question utile n'est pas de savoir si Google a failli, mais lesquels de vos services s'en seraient aperçus.",
          "A zone is supposed to be the unit you can lose. The useful question is not whether Google failed, but which of your services would have noticed.")),
   ("ul", [
     ("La perte d'une zone est la défaillance que l'architecture infonuagique promet d'absorber, et la plus souvent non testée. Un service est multi-zones quand il a réellement basculé, pas quand le schéma le dit.", "Losing a zone is the failure cloud architecture promises to absorb, and the one most often untested. A service is multi-zone when it has actually failed over, not when the diagram says so."),
     ("Les services gérés cachent leur zone. Le stockage, les files et les bases que vous n'avez pas placés vous-même sont peut-être à zone unique par défaut. Vérifiez, ne supposez pas.", "Managed services hide their zone. Storage, queues and databases you did not place yourself may be single-zone by default. Check, don't assume."),
     ("Huit heures, c'est long face à une tolérance d'impact. Si vous avez écrit deux heures pour un service de paiement, une panne de zone comme celle-ci la dépasse, sauf si la bascule fonctionne.", "Eight hours is a long time against an impact tolerance. If you wrote two hours for a payments service, a zone-level outage like this one exceeds it unless failover works."),
   ]),
   ("h", ("À vérifier lundi matin", "Check on Monday morning")),
   ("check", [
     ("Listez les services qui tournent dans une seule zone, y compris les services gérés que vous n'avez pas placés vous-même.", "List the services you run in a single zone, including managed ones you did not place yourself."),
     ("Choisissez-en un et faites-le basculer, chronomètre en main. Si vous ne pouvez pas, écrivez pourquoi.", "Pick one and fail it over, stopwatch in hand. If you cannot, write down why."),
     ("Vérifiez que vos outils de surveillance, votre page d'état et vos alertes ne dépendent pas de la zone ou du fournisseur qu'ils surveillent.", "Check that your monitoring, status page and alerts do not live in the same zone or provider they watch."),
     ("Comparez huit heures à la tolérance d'impact que vous avez écrite pour votre service le plus important.", "Compare eight hours with the impact tolerance you wrote down for your most important service."),
   ]),
   ("src", [
     ("The Register: Google Cloud outage (20 October 2026)", "https://www.theregister.com/a/5304160"),
     ("TechRadar: Google Cloud down, live coverage", "https://www.techradar.com/pro/live/google-cloud-down-major-outage-across-europe-hits-big-brands-banking-apps-and-more"),
     ("ThousandEyes: Google Cloud outage analysis, October 20, 2026", "https://www.thousandeyes.com/blog/google-cloud-outage-analysis-october-20-2026"),
   ]),
  ]},
]
