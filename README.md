# Squirrel Scrapers

Ce projet est une collection de scrapers pour extraire des données d'annonces immobilières de différents sites d'Agence.
Il permet d'avoir une vue du marché complète pour le bureaux en Île-de-France, locaux d'activités et entrepôts en France.
Liste des sites d'agences disponibles :
- CBRE
- BNP
- JLL
- AlexBolton
- Cushman & Wakefield
- Knight Frank
- ArthurLoyd

## Etat du projet et amélioration à venir

1. Priorité 1 :
- Implémenter les scrapers dans la liste des plus grosses agences (Savills, Immprove ex-Evolis)
- Gérer les doublons d'offres :
   - ajout des données de localisation si disponibles (long/lat)
   - comparer lat/long, adresse, accroche, titre et surface totale
- Modifier le cache d'user-agent pour qu'il ne prenne que les browsers chrome/mozilla/opéra (quelques erreurs objectification en UserAgent)
- Travail sur la détéctabilité du scraper en fonction du besoin : cookies, TLSfingerprint, Timing de requêtes et Javascriptfingerprint

2. Priorité 2 :
- Système de cache pour éviter de re-scraper les mêmes pages trop souvent ?
- Mise en place de retry mechanisms pour les requêtes échouées
- Repérage d'un trop grand nombre de N/A sur certaines valeurs pour surveiller la présence du bon sélecteur
- Travail sur les offres de coworking

3. Priorité 3 :
- Travail sur la factorisation du code et la vitesse de scraping
- Parallélisation des scraping avec asyncio ou multiprocessing (asyncio + aiohttp)
- Tests unitaires et d'intégration ?
- Documentation détaillée du code avec docstrings
- Barre de progression des traitements

## Structure du projet

```
test_squirrel/
├── config/
│   ├── settings.py      # Configuration globale
│   └── selectors.py     # Sélecteurs CSS par site
├── core/
│   ├── base_scraper.py      # Classe de base abstraite
│   ├── selenium_scraper.py  # Base pour scrapers Selenium
│   └── requests_scraper.py  # Base pour scrapers Requests
├── scrapers/
│   ├── bnp.py
│   ├── jll.py
│   └── ...
├── utils/
│   └── export.py             # Fonctions d'export JSON (créé un nouveau dossier exports à la racine)
│   └── user_agent.py         # Générateur d'user-agents
│   └── logging_config        # Initialisation du logger (créé un nouveau dossier logs à la racine)
└── main.py             # Point d'entrée
```

## Installation

1. Créer un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

Pour lancer tous les scrapers (par défaut lance l'analyse pour les 5 premiers urls) :
```bash
python main.py
```

Format de sortie JSON :
```
{
   "confrere": "BNP",
   "url": "https://bnppre.fr/a-vendre/local-activite/seine-et-marne-77/croissy-beaubourg-77183/vente-local-activite-1110-m2-non-divisible-OVACT2423977.html",
   "reference": "Référence : OVACT2423977",
   "contrat": "Vente",
   "actif": "Locaux d'activité",
   "disponibilite": "Immédiate",
   "surface": "1 111 m²",
   "division": "N/A",
   "adresse": "N/A 77183 Croissy-Beaubourg",
   "contact": "Baptiste Quilgars",
   "accroche": "BNP PARIBAS REAL ESTATE vous propose, à la Vente, une cellule d'activité avec bureaux d'accompagnement, en bon état, disponible à Croissy-Beaubourg.",
   "amenagements": "L'essentiel à retenirDisponibilité :ImmédiateCharge au sol Rdc :2,00 tonne(s)/m²Porte d'accès plain-pied :3HauteursHauteur sous poutre :5,00 mètre(s)Accès véhiculesAccessibilité type véhicules :Tous porteursEquipementsCharge au sol Rdc :2,00 tonne(s)/m²Climatisation :Réversible dans la partie BureauxEclairage Bureaux :Luminaires encastrésEclairage naturel :SkydomesFaux plafond :OuiFenêtres :OuiPorte d'accès plain-pied :3Sol bureaux :ParquetSols du bâtiment :BétonSource chauffage :Electrique 2 AérothermesType / Etat du bâtimentEtat de l'immeuble :Etat d'usagePrestations de serviceParking :35 PlacesSécurité :Contrôle d'accès - PortailAménagementsAménagement des bureaux :CloisonnésLocaux sociaux :SanitairesSanitaires :Oui",
   "prix_global": "1 700 000 €"
}
```

## Fonctionnalités

- Extraction des annonces de bureaux en Île-de-France, locaux d'activités et logistique en France
- Support de plusieurs sites d'annonces (BNP, JLL, etc.)
- Export des données en JSON
- Logging détaillé
- Gestion des user-agents

## Ajouter un nouveau scraper

1. Créer un nouveau fichier dans le dossier `scrapers/`
2. Hériter de `RequestsScraper` ou `SeleniumScraper`
3. Implémenter la méthode `scrape_listing()`
4. Ajouter les sélecteurs dans `config/selectors.py`
5. Ajouter le sitemap dans `config/settings.py`
6. Instancier le scraper dans `main.py`

## Maintenance

- Les sélecteurs CSS sont centralisés dans `config/selectors.py`
- La configuration globale est dans `config/settings.py`
- Les logs permettent de suivre l'exécution et diagnostiquer les erreurs
