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

    def post_taitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> dict:
        # Détermine le type de contrat
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
        # Déterminer le type d'actif
        actif_map = {
            "bureau": "Bureaux",
            "local": "Locaux d'activité",
            "entrepot": "Entrepots",
        }
        data["actif"] = next(
            (label for key, label in actif_map.items() if key in url), "N/A"
        )
        # Déterminer l'adresse complète
        adresse = self.safe_select_text(soup, self.selectors["adresse"])
        nom_immeuble = self.safe_select_text(soup, self.selectors["nom_immeuble"])
        data["adresse"] = f"{nom_immeuble} {adresse}".strip()

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
            if "bureau" in url:
                # Check if it contains any department from DEPARTMENTS_IDF
                if not any(
                    f"-{departement}/" in url for departement in DEPARTMENTS_IDF
                ):
                    filtered_urls.append(url)
            else:
                filtered_urls.append(url)
        logger.info(
            f"[{self.name.upper()}] Trouvé {len(filtered_urls)} URLs filtrées sans bureaux région"
        )
        return filtered_urls
