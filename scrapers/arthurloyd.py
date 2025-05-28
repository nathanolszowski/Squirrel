# -*- coding: utf-8 -*-
"""
Scraper pour ARTHURLOYD
"""

import logging
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import SITEMAPS
from config.selectors import ARTHURLOYD_SELECTORS

logger = logging.getLogger(__name__)


class ARTHURLOYDScraper(RequestsScraper):
    """Scraper pour le site ARTHURLOYD qui hérite de la classe RequestsScraper"""

    def __init__(self, ua_generateur, proxy) -> None:
        super().__init__(ua_generateur, proxy, "ARTHURLOYD", SITEMAPS["ARTHURLOYD"])
        self.selectors = ARTHURLOYD_SELECTORS

    def post_traitement_hook(
        self, data: dict, soup: BeautifulSoup, url: str
    ) -> dict[str]:
        """Méthode de post-traitement surchargée pour les besoins du scraper AlexBolton

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper

        Returns:
            dict[str]: Représente les données de l'offre à scraper après modification spécifique pour un scraper
        """
        # Surcharger la méthode obtenir contrat
        contrat_map = {
            "location": "Location",
            "vente": "Vente",
        }
        data["contrat"] = next(
            (label for key, label in contrat_map.items() if key in url), "N/A"
        )
        # Surcharger la méthode obtenir l'actif
        actif_map = {
            "bureau": "Bureaux",
            "activite-entrepots": "Locaux d'activité",
            "logistique": "Entrepots",
        }
        data["actif"] = next(
            (label for key, label in actif_map.items() if key in url), "N/A"
        )
        # Surcharger la méthode obtenir l'adresse
        data["adresse"] = (
            f"{self.safe_select_text(soup, self.selectors["titre"])}, {data["adresse"]}"
        )

    def filtre_urls(self, urls: list[str]) -> list[str]:
        """
        Filtre les URLs pour supprimer les bureaux hors IDF

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper

        Returns:
            urls_filtrees (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        logger.info("Filtrage des urls Arthur Loyd")
        motifs_url = [
            "bureau-location/ile-de-france/",
            "bureau-vente/ile-de-france/",
            "locaux-activite-entrepots-location/",
            "locaux-activite-entrepots-vente/",
            "logistique-location/",
            "logistique-vente/",
        ]
        urls_filtrees = [
            url for url in urls if any(motif in url for motif in motifs_url)
        ]
        logger.info(
            f"[{self.name.upper()}] Trouvé {len(urls_filtrees)} URLs filtrées sans bureaux région avec la logistique et l'activité"
        )
        return urls_filtrees
