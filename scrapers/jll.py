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

    def __init__(self, ua_generateur, proxy) -> None:
        super().__init__(ua_generateur, proxy, "JLL", SITEMAPS["JLL"])
        self.selectors = JLL_SELECTORS

    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> None:
        """Méthode de post-traitement surchargée pour les besoins du scraper JLL

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraperr
        """
        # Surcharger la méthode obtenir contrat
        contrat_map = {
            "a-louer": "Location",
            "a-vendre": "Vente",
        }
        data["contrat"] = next(
            (label for key, label in contrat_map.items() if key in url), "N/A"
        )
        # Surcharger la méthode obtenir le contrat
        actif_map = {
            "bureaux": "Bureaux",
            "local-activite": "Locaux d'activité",
            "entrepot": "Entrepots",
        }
        data["actif"] = next(
            (label for key, label in actif_map.items() if key in url), "N/A"
        )

    def filtre_urls(self, urls: list[str]) -> list[str]:
        """
        Méthode de filtrage surchargée pour les besoins du scraper JLL

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper

        Returns:
            urls_filtrees (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        logger.info("Filtrage des offres JLL")
        urls_filtrees = []
        for url in urls:
            if url.startswith("https://immobilier.jll.fr/location") or url.startswith(
                "https://immobilier.jll.fr/vente"
            ):
                if "bureaux" in url:
                    last_segment = url.strip("/").split("/")[-1]
                    part = last_segment.split("-")
                    part = part[-2]
                    if not any(departement in part for departement in DEPARTMENTS_IDF):
                        urls_filtrees.append(url)
                else:
                    urls_filtrees.append(url)
        logger.info(
            f"[{self.name.upper()}] Trouvé {len(urls_filtrees)} URLs filtrées sans bureaux région"
        )
        return urls_filtrees
