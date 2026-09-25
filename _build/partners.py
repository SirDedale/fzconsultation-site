# Partners / ecosystem page. Naming a platform does not imply a formal partnership.
PUBLIC = [
 ("Microsoft Azure", ("Zones et régions, Azure Site Recovery et Azure Backup, gouvernance de l'IA avec Citadel.", "Zones and regions, Azure Site Recovery and Azure Backup, AI governance with Citadel.")),
 ("Amazon Web Services (AWS)", ("Architectures multizones et multirégions, AWS Elastic Disaster Recovery, AWS Backup, pilier fiabilité du Well-Architected Framework.", "Multi-AZ and multi-region architectures, AWS Elastic Disaster Recovery, AWS Backup, the Well-Architected reliability pillar.")),
 ("Google Cloud", ("Conception régionale, service Backup and DR, résilience des charges de données et d'IA.", "Regional design, the Backup and DR service, resilience for data and AI workloads.")),
 ("Oracle Cloud Infrastructure", ("Résilience des bases Oracle, réplication et reprise des applications critiques.", "Resilience for Oracle databases, replication and recovery of critical applications.")),
]
PRIVATE = [
 ("VMware by Broadcom", ("Reprise de site, protection contre les rançongiciels et évaluation des options après les changements de licences.", "Site recovery, ransomware protection and assessing options after the licensing changes.")),
 ("Nutanix", ("Reprise intégrée à la plateforme, réplication entre sites et vers le nuage public.", "Built-in platform recovery, replication between sites and to the public cloud.")),
 ("Red Hat OpenShift", ("Résilience des conteneurs et des machines virtuelles, sauvegarde et reprise des applications.", "Resilience for containers and virtual machines, application backup and recovery.")),
 ("Microsoft Azure Local", ("Infrastructure hybride sur site gérée depuis Azure, pour les données qui doivent rester chez vous.", "Hybrid on-premises infrastructure managed from Azure, for data that must stay on site.")),
 ("HPE GreenLake", ("Nuage privé en mode service : continuité, sauvegarde et reprise intégrées.", "Private cloud as a service: built-in continuity, backup and recovery.")),
 ("Dell APEX", ("Infrastructure en mode service, stockage et protection des données sur site et hybride.", "Infrastructure as a service, storage and data protection on-premises and hybrid.")),
]
CROSS = [
 (("Reprise d'un nuage à l'autre", "Cross-cloud recovery"), ("Rétablir un service chez un autre fournisseur ou sur site quand une région ou un fournisseur tombe.", "Restore a service on another provider or on-premises when a region or provider fails.")),
 (("Plans de sortie et risque de concentration", "Exit plans and concentration risk"), ("Des stratégies de sortie testables, comme l'exigent DORA et les régulateurs financiers.", "Testable exit strategies, as DORA and financial regulators require.")),
 (("Migrations sans interruption", "Migrations without disruption"), ("Changer de plateforme de virtualisation ou de nuage avec un plan de retour arrière éprouvé.", "Change virtualization or cloud platform with a proven rollback plan.")),
 (("Gouvernance hybride de l'IA", "Hybrid AI governance"), ("Un même cadre de contrôle pour les modèles hébergés dans le nuage et sur site.", "One control framework for models hosted in the cloud and on-premises.")),
]
WAYS = [
 (("Éditeurs et fournisseurs infonuagiques", "Cloud and technology vendors"), ("Nous aidons vos clients à concevoir, tester et prouver la résilience de ce qu'ils déploient sur votre plateforme.", "We help your customers design, test and prove the resilience of what they deploy on your platform.")),
 (("Intégrateurs et fournisseurs de services gérés", "Integrators and managed service providers"), ("Nous apportons une expertise en continuité, reprise, sécurité et gouvernance de l'IA, en codélivrance ou en sous-traitance.", "We bring continuity, recovery, security and AI governance expertise, through co-delivery or subcontracting.")),
 (("Cabinets de conseil et d'avocats", "Consulting and law firms"), ("Vous couvrez le juridique ou la stratégie ; nous couvrons l'opérationnel et le technique, pour une réponse complète à vos clients.", "You cover legal or strategy; we cover operations and technology, for a complete answer to your clients.")),
]
MODELS = [(("Recommandation", "Referral"), ("Nous nous recommandons mutuellement lorsque le besoin dépasse notre périmètre.", "We refer clients to each other when a need falls outside our scope.")),
          (("Codélivrance", "Co-delivery"), ("Une équipe commune sur un mandat, chacun sur son expertise.", "A joint team on an engagement, each on its own expertise.")),
          (("Sous-traitance", "Subcontracting"), ("Nous intervenons sous votre marque, selon vos méthodes.", "We work under your brand, following your methods."))]
