# -*- coding: utf-8 -*-
"""
Configuration globale pour les scrapers
"""

# Départements d'Île-de-France ciblés
DEPARTMENTS_IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]

# Timeouts et délais
REQUEST_TIMEOUT = 5  # secondes
SELENIUM_WAIT_TIME = 10  # secondes

# Configuration Selenium
SELENIUM_OPTIONS = [
    "--headless",
    "--disable-blink-features=AutomationControlled",
    "--disable-gpu",
    "--enable-unsafe-swiftshader",
    "--no-sandbox",
    "start-maximized",
    "--log-level=1",
    "window-size=1920x1080"
]

# URLs des sitemaps
SITEMAPS = {
    "BNP": {"Bureaux" : "https://www.bnppre.fr/sitemaps/bnppre/sitemap-bureaux.xml", 
            "Entrepôt" : "https://www.bnppre.fr/sitemaps/bnppre/sitemap-entrepots.xml", 
            "Locaux" : "https://www.bnppre.fr/sitemaps/bnppre/sitemap-locaux.xml"},
    "JLL": "https://immobilier.jll.fr/sitemap-properties.xml",
    "CBRE": "https://immobilier.cbre.fr/sitemap.xml",
    "ALEXBOLTON" : "https://www.alexbolton.fr/sitemap.xml",
    "CUSHMAN" : "https://immobilier.cushmanwakefield.fr/sitemap.xml",
    "KNIGHTFRANK" : {"Location" : "https://www.knightfrank.fr/resultat?nature=1&localisation=75%7C77%7C78%7C91%7C92%7C93%7C94%7C95%7C&typeOffre=1", 
                    "Vente" : "https://www.knightfrank.fr/resultat?nature=2&localisation=75%7C77%7C78%7C91%7C92%7C93%7C94%7C95%7C&typeOffre=1"},
    "ARTHURLOYD" : "https://www.arthur-loyd.com/sitemap-offer.xml",
    "SAVILLS": "https://livev6-searchapi.savills.com/Data/SearchByUrl"
    # Ajouter les autres sitemaps ici
}

# Mise à jour ou non de la liste des user-agents
USER_AGENT_MAJ = False

# Nom ou chemin du fichier cache des user-agents
FICHIER_CACHE_USER_AGENT = "user_agent.json"
