# -*- coding: utf-8 -*-
"""
Scraper pour BNP Paribas Real Estate
"""

import logging
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS
from config.selectors import BNP_SELECTORS

logger = logging.getLogger(__name__)


class BNPScraper(RequestsScraper):
    """Scraper pour le site BNP Paribas Real Estate qui hérite de la classe RequestsScraper"""

    def __init__(self, ua_generateur, proxy) -> None:
        super().__init__(ua_generateur, proxy, "BNP", SITEMAPS["BNP"])
        self.selectors = BNP_SELECTORS

    def post_taitement_hook(
        self, data: dict, soup: BeautifulSoup, url: str
    ) -> dict[str]:
        """Méthode de post-traitement surchargée pour les besoins du scraper de BNP

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper

        Returns:
            dict[str]: Représente les données de l'offre à scraper après modification spécifique pour un scraper
        """
        # Surcharger la méthode obtenir contrat
        if "a-louer" in url:
            data["contrat"] = "Location"
            data["prix_global"] = self.safe_select_text(
                soup, self.selectors["loyer_global"]
            )
        elif "a-vendre" in url:
            data["contrat"] = "Vente"
            data["prix_global"] = self.safe_select_text(
                soup, self.selectors["prix_global"]
            )
        else:
            data["contrat"] = "N/A"
        # Surcharger la méthode obtenir l'actif
        actif_map = {
            "bureau": "Bureaux",
            "local": "Locaux d'activité",
            "entrepot": "Entrepots",
        }
        data["actif"] = next(
            (label for key, label in actif_map.items() if key in url), "N/A"
        )
        # Surcharger la méthode obtenir l'adresse
        adresse = self.safe_select_text(soup, self.selectors["adresse"])
        nom_immeuble = self.safe_select_text(soup, self.selectors["nom_immeuble"])
        data["adresse"] = f"{nom_immeuble} {adresse}".strip()

    def filtre_urls(self, urls: list[str]) -> list[str]:
        """
        Méthode de filtrage surchargée pour les besoins du scraper BNP

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper

        Returns:
            urls_filtrees (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        logger.info("Filtrage des offres BNP")
        urls_filtrees = []
        for url in urls:
            if "bureau" in url:
                # Regarde si contient les départements IDF
                if not any(
                    f"-{departement}/" in url for departement in DEPARTMENTS_IDF
                ):
                    urls_filtrees.append(url)
            else:
                urls_filtrees.append(url)
        logger.info(
            f"[{self.name.upper()}] Trouvé {len(urls_filtrees)} URLs filtrées sans bureaux région"
        )
        return urls_filtrees
