# -*- coding: utf-8 -*-
"""
Scraper pour CUSHMAN
"""

import logging
import re
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS
from config.selectors import CUSHMAN_SELECTORS

logger = logging.getLogger(__name__)

class CUSHMANScraper(RequestsScraper):
    """Scraper pour le site CUSHMAN qui hérite de la classe RequestsScraper"""
    
    def __init__(self, ua_generateur, proxy) -> None:
        super().__init__(ua_generateur, proxy, "CUSHMAN", SITEMAPS["CUSHMAN"])
        self.selectors = CUSHMAN_SELECTORS
        
        
    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> dict:
        logger.info("Lancement du post-traitement spécifique à Cushman")      
        # Déterminer le contrat
        contrat_map = {
            "location": "Location",
            "achat": "Vente"
        }
        data["contrat"] = next((label for key, label in contrat_map.items() if key in url), "N/A")
        # Déterminer l'actif
        actif_map = {
            "Bureaux": "Bureaux",
            "Activités": "Locaux d'activité",
            "Entrepôts": "Entrepots"
            }
        data["actif"] = next((label for key, label in actif_map.items() if key in data["actif"]), "N/A")

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
        pattern = re.compile(r'-\d{5}-\d+[a-zA-Z]*$') # Suffixe de type "-75009-139113AB"
        for url in urls:
            if pattern.search(url):
                if "bureaux" in url:
                    last_segment = url.strip('/').split('/')[-1]
                    part = last_segment.split('-')
                    part = part[-2]
                    if not any(departement in part for departement in DEPARTMENTS_IDF) :
                        filtered_urls.append(url)
                else :
                    filtered_urls.append(url)
        logger.info(f"[{self.name.upper()}] Trouvé {len(filtered_urls)} URLs filtrées sans bureaux région")
        print(filtered_urls)
        return filtered_urls