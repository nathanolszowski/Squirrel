# Squirrel Scrapers

Ce projet est une collection de scrapers pour extraire des données d'annonces immobilières de différents sites de courtiers.

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
│   └── export.py        # Fonctions d'export (JSON, etc.)
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

Pour lancer tous les scrapers :
```bash
python main.py
```

## Fonctionnalités

- Extraction des annonces de bureaux en Île-de-France
- Support de plusieurs sites (BNP, JLL, etc.)
- Export des données en JSON
- Logging détaillé
- Gestion des erreurs robuste

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
