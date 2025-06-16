# -*- coding: utf-8 -*-
"""
Scraper pour CUSHMAN
"""

import logging
import re
import json
import html
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

    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> None:
        """Méthode de post-traitement surchargée pour les besoins du scraper CUSHMAN

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        # Surcharger la méthode obtenir contrat
        contrat_map = {"location": "Location", "achat": "Vente"}
        data["contrat"] = next(
            (label for key, label in contrat_map.items() if key in url), "N/A"
        )
        # Surcharger la méthode obtenir actif
        actif_map = {
            "bureaux": "Bureaux",
            "Bureaux": "Bureaux",
            "Activités": "Locaux d'activité",
            "Entrepôts": "Entrepots",
            "Coworking": "Bureau équipé",
            "Bureaux privés": "Bureau équipé",
        }
        data["actif"] = next(
            (label for key, label in actif_map.items() if key in data["actif"]), "N/A"
        )
        # Surcharger la méthode obtenir la division
        if "divisibles" in data["surface"]:
            divisible = data["surface"].find("divisibles")
            surface_divisible = data["surface"][:divisible].strip()
            divisibilite = data["surface"][divisible:].strip()
            data["surface"] = surface_divisible
            data["division"] = divisibilite
        else:
            data["division"] = "Non divisible"
        # Surcharger la méthode obtenir l'url image
        parent_image = soup.find("div", class_="c-swiper__slide")
        img_image = parent_image.find("source")
        if img_image and img_image["srcset"]:
            data["url_image"] = img_image["srcset"]

        # Surcharger la méthode obtenir la posititon gps
        div_map = soup.find("div", class_="c-map js-map")
        data_property = div_map.get("data-property")
        decoded_json_str = html.unescape(data_property)
        positions = json.loads(decoded_json_str)
        data["latitude"] = float(positions["address"]["displayedGeolocation"]["lat"])
        data["longitude"] = float(positions["address"]["displayedGeolocation"]["lon"])

    def filtre_urls(self, urls: list[str]) -> list[str]:
        """
        Méthode de filtrage surchargée pour les besoins du scraper CUSHMAN

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper

        Returns:
            urls_filtrees (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        logger.info("Filtrage des offres Cushman & Wakefield")
        urls_filtrees = []
        pattern = re.compile(
            r"-\d{5}-\d+[a-zA-Z]*$"
        )  # Suffixe de type "-75009-139113AB"
        for url in urls:
            if pattern.search(url):
                if "bureaux" in url:
                    last_segment = url.strip("/").split("/")[-1]
                    part = last_segment.split("-")
                    part = part[-2]
                    if any(departement in part for departement in DEPARTMENTS_IDF):
                        urls_filtrees.append(url)
                elif "activites" or "entrepots" in url:
                    urls_filtrees.append(url)
        logger.info(
            f"[{self.name.upper()}] Trouvé {len(urls_filtrees)} URLs filtrées sans bureaux région"
        )
        return urls_filtrees
