# -*- coding: utf-8 -*-
"""
Scraper pour Alex Bolton
"""

import logging
import httpx
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import SITEMAPS, REQUEST_TIMEOUT
from config.selectors import ALEXBOLTON_SELECTORS

logger = logging.getLogger(__name__)

class ALEXBOLTONScraper(RequestsScraper):
    """Scraper pour le site ALEXBOLTON qui hérite de la classe RequestsScraper"""
    
    def __init__(self, ua_generateur) -> None:
        super().__init__(ua_generateur,"ALEXBOLTON", SITEMAPS["ALEXBOLTON"])
        self.selectors = ALEXBOLTON_SELECTORS# -*- coding: utf-8 -*-

    def scrape_listing(self, url: str) -> dict:
        """
        Scrape une annonce Alexbolton
        
        Args:
            urls (str): Chaîne de caractères représentant l'url à scraper
        Retruns:
            data (dict): Dictionnaire avec les informations de chaque offre scrapée
        """
        try:
            logger.info(f"[{self.name.upper()}] Début du scraping des données pour chacune des offres")
            response = httpx.get(url, headers={"User-agent":self.ua_generateur.get()}, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Déterminer le contrat
            contrat_map = {
                "Loyer": "Location",
                "Prix": "Vente",
            }
            contrat = next((label for key, label in contrat_map.items() if key in self.safe_select_text(soup, self.selectors["contrat"])), "N/A")
            
            # Déterminer l'accroche
            accroche = soup.find("div", class_="col-lg-5 position-relative")
            accroche = accroche.find_all("p")
            accroche = accroche[8].get_text()
            
            # Extraction des données
            data = {
                "confrere" : self.name,
                "url": url,
                "reference" : self.safe_select_text(soup, self.selectors["reference"]),
                "contrat": contrat,
                "actif" : "Bureaux",
                "disponibilite" : self.safe_select_text(soup, self.selectors["disponibilite"]),
                "surface" : self.safe_select_text(soup, self.selectors["surface"]),
                "adresse" : " ".join([self.safe_select_text(soup, self.selectors["nom_immeuble"]),
                                      self.safe_select_text(soup, self.selectors["adresse"])]),
                "contact" : self.safe_select_text(soup, self.selectors["contact"]),
                "accroche" : accroche,
                "amenagements" : self.safe_select_text(soup, self.selectors["amenagements"]),
                "prix_global" : self.safe_select_text(soup, self.selectors["prix_global"])
            }
            return data
            
        except Exception as e:
            logger.error(f"[self.name] Erreur scraping des données pour {url}: {e}")
            return None
        
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

