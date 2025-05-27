# -*- coding: utf-8 -*-
"""
Scraper pour Alex Bolton
"""

import logging
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import SITEMAPS
from config.selectors import ALEXBOLTON_SELECTORS

logger = logging.getLogger(__name__)

class ALEXBOLTONScraper(RequestsScraper):
    """Scraper pour le site ALEXBOLTON qui hérite de la classe RequestsScraper"""
    
    def __init__(self, ua_generateur, proxy) -> None:
        super().__init__(ua_generateur, proxy,"ALEXBOLTON", SITEMAPS["ALEXBOLTON"])
        self.selectors = ALEXBOLTON_SELECTORS# -*- coding: utf-8 -*-

    def post_taitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> dict:
        logger.info("Lancement du post-traitement spécifique à AlexBolton")
        # Déterminer le contrat
        contrat_map = {
            "Loyer": "Location",
            "Prix": "Vente",
        }
        data["contrat"] = next((label for key, label in contrat_map.items() if key in self.safe_select_text(soup, self.selectors["contrat"])), "N/A")
        # Déterminer l'accroche
        accroche = soup.find("div", class_="col-lg-5 position-relative")
        accroche = accroche.find_all("p")
        data["accroche"] = accroche[8].get_text()

    def filtre_idf_bureaux(self, urls: list[str]) -> list[str]:
        """
        Filtre les URLs pour supprimer les bureaux hors IDF. FYI : AlexBolton ne fait que du Bureaux IDF

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper
        Returns:
            filtered_urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        logger.info("Filtrage des offres")
        filtered_urls = []
        for url in urls:
            if url.startswith("https://www.alexbolton.fr/annonces/") :
                filtered_urls.append(url)
        logger.info(f"[{self.name.upper()}] Trouvé {len(filtered_urls)} URLs filtrées sans bureaux région")
        return filtered_urls

