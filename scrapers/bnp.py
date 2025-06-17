# -*- coding: utf-8 -*-
"""
Scraper pour BNP Paribas Real Estate
"""

import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
from core.requests_scraper import RequestsScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS
from config.selectors import BNP_SELECTORS

logger = logging.getLogger(__name__)


class BNPScraper(RequestsScraper):
    """Scraper pour le site BNP Paribas Real Estate qui hérite de la classe RequestsScraper"""

    def __init__(self, ua_generateur, proxy) -> None:
        super().__init__(ua_generateur, proxy, "BNP", SITEMAPS["BNP"])
        self.selectors = BNP_SELECTORS

    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> None:
        """Méthode de post-traitement surchargée pour les besoins du scraper de BNP

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
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
            "coworking": "Bureau équipé",
        }
        data["actif"] = next(
            (label for key, label in actif_map.items() if key in url), "N/A"
        )
        # Surcharger la méthode obtenir l'adresse
        adresse = self.safe_select_text(soup, self.selectors["adresse"])
        nom_immeuble = self.safe_select_text(soup, self.selectors["nom_immeuble"])
        data["adresse"] = f"{nom_immeuble} {adresse}".strip()

        # Surcharger la méthode obtenir l'url image
        parent_image = soup.find("div", class_="img-container")
        if parent_image:
            img_image = parent_image.find("img")
            if img_image and img_image["data-lazy"]:
                url_image = urljoin("https://www.bnppre.fr", img_image["data-lazy"])
                data["url_image"] = url_image
        else:
            data["url_image"] = None

        # Surcharger la méthode obtenir la position gps
        script = soup.find("script", string=re.compile(r"var geocode"))
        if script:
            match = re.search(r"var geocode\s*=\s*(\{.*?\});", script.string, re.DOTALL)

            if match:
                geocode_json = match.group(1)
                geocode = json.loads(geocode_json)

                # Extraire la localisation
                location = geocode["results"][0]["geometry"]["location"]
                data["latitude"] = float(location["lat"])
                data["longitude"] = float(location["lng"])
        else:
            data["latitude"] = 48.866669
            data["longitude"] = 2.33333

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
                if any(f"-{departement}/" in url for departement in DEPARTMENTS_IDF):
                    urls_filtrees.append(url)
            else:
                urls_filtrees.append(url)
        logger.info(
            f"[{self.name.upper()}] Trouvé {len(urls_filtrees)} URLs filtrées sans bureaux région"
        )
        return urls_filtrees
