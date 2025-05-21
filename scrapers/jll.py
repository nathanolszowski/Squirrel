# -*- coding: utf-8 -*-
"""
Scraper pour JLL
"""

import logging
from bs4 import BeautifulSoup
from core.selenium_scraper import SeleniumScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS
from config.selectors import JLL_SELECTORS


logger = logging.getLogger(__name__)

class JLLScraper(SeleniumScraper):
    """Scraper pour le site JLL qui hérite de la classe SeleniumScraper"""
    
    def __init__(self, ua_generateur) -> None:
        super().__init__(ua_generateur,"JLL", SITEMAPS["JLL"])
        self.selectors = JLL_SELECTORS
     
    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> dict:
        logger.info("Lancement du post-traitement spécifique à JLL") 
        # Détermine le type de contrat
        contrat_map = {
            "a-louer": "Location",
            "a-vendre": "Vente",
        }
        data["contrat"] = next((label for key, label in contrat_map.items() if key in url), "N/A")
        # Déterminer le type d'actif
        actif_map = {
            "bureaux": "Bureaux",
            "local-activite": "Locaux d'activité",
            "entrepot": "Entrepots"
        }
        data["actif"] = next((label for key, label in actif_map.items() if key in url), "N/A")   

    def filtre_idf_bureaux(self, urls: list[str]) -> list[str]:
        """
        Filtre les URLs pour supprimer les bureaux hors IDF

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper
        Returns:
            filtered_urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        logger.info("Filtrage des offres")
        filtered_urls = []
        for url in urls:
            if url.startswith("https://immobilier.jll.fr/location") or url.startswith("https://immobilier.jll.fr/vente") :
                if "bureaux" in url:
                    last_segment = url.strip('/').split('/')[-1]
                    part = last_segment.split('-')
                    part = part[-2]
                    if not any(departement in part for departement in DEPARTMENTS_IDF) :
                        filtered_urls.append(url)
                else :
                    filtered_urls.append(url)
        logger.info(f"[{self.name.upper()}] Trouvé {len(filtered_urls)} URLs filtrées sans bureaux région")
        return filtered_urls