# -*- coding: utf-8 -*-
"""
Scraper pour CBRE
"""

import logging
import re
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS
from config.selectors import CBRE_SELECTORS

logger = logging.getLogger(__name__)


class CBREScraper(RequestsScraper):
    """Scraper pour le site CBRE qui hérite de la classe RequestsScraper"""

    def __init__(self, ua_generateur, proxy) -> None:
        super().__init__(ua_generateur, proxy, "CBRE", SITEMAPS["CBRE"])
        self.selectors = CBRE_SELECTORS

    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> None:
        """Méthode de post-traitement surchargée pour les besoins du scraper CBRE

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        # Surcharger la méthode obtenir la reference
        reference_element = soup.find("li", class_="LS breadcrumb-item active")
        reference_element = reference_element.find("span")
        data["reference"] = (
            reference_element.get_text(strip=True) if reference_element else "N/A"
        )
        # Surcharger la méthode obtenir l'actif
        actif_map = {
            "bureaux": "Bureaux",
            "activites": "Locaux d'activité",
            "entrepots": "Entrepots",
        }
        data["actif"] = next(
            (label for key, label in actif_map.items() if key in url), "N/A"
        )
        # Surcharger la méthode obtenir le contrat
        contrat_map = {
            "a-louer": "Location",
            "a-vendre": "Vente",
        }
        data["contrat"] = next(
            (label for key, label in contrat_map.items() if key in url), "N/A"
        )

    def filtre_urls(self, urls: list[str]) -> list[str]:
        """
        Méthode de filtrage surchargée pour les besoins du scraper BNP

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper

        Returns:
            urls_filtrees (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        logger.info("Filtrage des offres CBRE")
        urls_filtrees = []
        pattern = re.compile(
            r"https://immobilier.cbre.fr/offre/(a-louer|a-vendre)/bureaux/(\d+)"
        )
        for url in urls:
            if url.startswith(
                "https://immobilier.cbre.fr/offre/"
            ):  # On filtre les offres bureaux dont l'url commence par cette string
                if "bureaux" in url:
                    match = pattern.match(url)
                    if match and match.group(2)[:2] in DEPARTMENTS_IDF:
                        urls_filtrees.append(url)
                else:
                    urls_filtrees.append(url)
        logger.info(
            f"[{self.name.upper()}] Trouvé {len(urls_filtrees)} URLs filtrées sans bureaux région"
        )
        return urls_filtrees
