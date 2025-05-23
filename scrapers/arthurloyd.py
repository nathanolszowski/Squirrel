# -*- coding: utf-8 -*-
"""
Scraper pour ARTHURLOYD
"""

import logging
import re
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS
from config.selectors import ARTHURLOYD_SELECTORS

logger = logging.getLogger(__name__)

class ARTHURLOYDScraper(RequestsScraper):
    """Scraper pour le site CBRE qui hérite de la classe RequestsScraper"""
    
    def __init__(self, ua_generateur) -> None:
        super().__init__(ua_generateur,"CBRE", SITEMAPS["ARTHURLOYD"])
        self.selectors = ARTHURLOYD_SELECTORS
           
    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> dict:
        pass
        
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
        pattern = re.compile(r"https://immobilier.cbre.fr/offre/(a-louer|a-vendre)/bureaux/(\d+)")
        for url in urls:
            if url.startswith("https://immobilier.cbre.fr/offre/"):
                if "bureaux" in url:
                    match = pattern.match(url)
                    if match and match.group(2)[:2] in DEPARTMENTS_IDF:
                        filtered_urls.append(url)
                else:
                    filtered_urls.append(url)
        logger.info(f"[{self.name.upper()}] Trouvé {len(filtered_urls)} URLs filtrées sans bureaux région")
        return filtered_urls