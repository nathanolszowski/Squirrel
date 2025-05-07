# -*- coding: utf-8 -*-
"""
Configuration globale pour les scrapers
"""
from utils.user_agent import Rotator
from utils.liste_user_agent import verifier_user_agents

# Départements d'Île-de-France ciblés
DEPARTMENTS_IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]

# Timeouts et délais
REQUEST_TIMEOUT = 5  # secondes
SELENIUM_WAIT_TIME = 5  # secondes

# Configuration Selenium
SELENIUM_OPTIONS = [
    "--headless",
    "--disable-blink-features=AutomationControlled",
    "--disable-gpu",
    "--no-sandbox",
    "start-maximized",
    "--log-level=1",
    "window-size=1920x1080"
]

# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36
USER_AGENT = Rotator(verifier_user_agents())


# URLs des sitemaps
SITEMAPS = {
    "BNP": {"Bureaux" : "https://bnppre.fr/sitemaps/bnppre/sitemap-bureaux.xml", 
            "Entrepôt" : "https://bnppre.fr/sitemaps/bnppre/sitemap-entrepots.xml", 
            "Locaux" : "https://bnppre.fr/sitemaps/bnppre/sitemap-locaux.xml"},
    "JLL": "https://immobilier.jll.fr/sitemap-properties.xml",
    "CBRE": "https://immobilier.cbre.fr/sitemap.xml",
    "ALEXBOLTON" : "https://www.alexbolton.fr/sitemap.xml",
    "CUSHMAN" : "https://immobilier.cushmanwakefield.fr/sitemap.xml"
    # Ajouter les autres sitemaps ici
}
