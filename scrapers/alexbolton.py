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
        super().__init__(ua_generateur, proxy, "ALEXBOLTON", SITEMAPS["ALEXBOLTON"])
        self.selectors = ALEXBOLTON_SELECTORS

    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> None:
        """Méthode de post-traitement surchargée pour les besoins du scraper AlexBolton

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        data["actif"] = "Bureaux"
        # Surcharger la méthode obtenir contrat
        contrat_map = {
            "Loyer": "Location",
            "Prix": "Vente",
        }
        data["contrat"] = next(
            (
                label
                for key, label in contrat_map.items()
                if key in self.safe_select_text(soup, self.selectors["contrat"])
            ),
            "N/A",
        )
        # Surcharger la méthode obtenir accroche
        accroche = soup.find("div", class_="col-lg-5 position-relative")
        accroche = accroche.find_all("p")
        data["accroche"] = accroche[8].get_text()

        # Surcharger la méthode obtenir url image
        img = soup.find("img", class_="listing-header-photo-img u-z-index-1 d-md-none")
        if img and img.get("src"):
            data["url_image"] = img["src"]

        # # Surcharger la méthode obtenir latitude et longitude
        position_div = soup.find("div", id="listing-map-target")
        if position_div:
            data["latitude"] = position_div.get("data-latitude")
            data["longitude"] = position_div.get("data-longitude")

    def filtre_urls(self, urls: list[str]) -> list[str]:
        """
        Méthode de filtrage surchargée pour les besoins du scraper AlexBolton. FYI : AlexBolton ne fait que du Bureaux IDF

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper

        Returns:
            urls_filtrees (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        logger.info("Filtrage des offres AlexBolton")
        urls_filtrees = []
        for url in urls:
            if url.startswith(
                "https://www.alexbolton.fr/annonces/"
            ):  # On filtre les offres bureaux dont l'url commence par cette string
                urls_filtrees.append(url)
        logger.info(
            f"[{self.name.upper()}] Trouvé {len(urls_filtrees)} URLs filtrées sans bureaux région"
        )
        return urls_filtrees
