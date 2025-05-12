# -*- coding: utf-8 -*-
"""
Scraper pour JLL
"""

import logging
import time
from bs4 import BeautifulSoup
from core.selenium_scraper import SeleniumScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS, SELENIUM_WAIT_TIME
from config.selectors import JLL_SELECTORS


logger = logging.getLogger(__name__)

class JLLScraper(SeleniumScraper):
    """Scraper pour le site JLL qui hérite de la classe SeleniumScraper"""
    
    def __init__(self) -> None:
        super().__init__("JLL", SITEMAPS["JLL"])
        self.selectors = JLL_SELECTORS
     
    def scrape_listing(self, url: str) -> dict:
        """
        Scrape une annonce JLL
        
        Args:
            urls (str): Chaîne de caractères représentant l'url à scraper
        Retruns:
            data (dict): Dictionnaire avec les informations de chaque offre scrapée
        """
        try:
            logger.info(f"[{self.name.upper()}] Début du scraping des données pour chacune des offres")
            self.driver.get(url)
            time.sleep(SELENIUM_WAIT_TIME)
            
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            # Détermine le type de contrat

            contrat_map = {
                "a-louer": "Location",
                "a-vendre": "Vente",
            }
            contrat = next((label for key, label in contrat_map.items() if key in url), "N/A")
            
            # Déterminer le type d'actif
            actif_map = {
                "bureaux": "Bureaux",
                "local-activite": "Locaux d'activité",
                "entrepot": "Entrepots"
            }
            actif = next((label for key, label in actif_map.items() if key in url), "N/A")   
                
            # Extraction des données
            data = {
                "confrere" : self.name,
                "url": url,
                "reference": self.safe_select_text(soup, self.selectors["reference"]),
                "contrat": contrat,
                "actif": actif,
                "disponibilite": self.safe_select_text(soup, self.selectors["disponibilite"]),
                "surface": self.safe_select_text(soup, self.selectors["surface"]),
                "division": self.safe_select_text(soup, self.selectors["division"]),
                "adresse_complete": self.safe_select_text(soup, self.selectors["adresse"]),
                "contact": self.safe_select_text(soup, self.selectors["contact"]),
                "accroche": self.safe_select_text(soup, self.selectors["accroche"]),
                "amenagements": self.safe_select_text(soup, self.selectors["amenagements"]),
                "prix_global": self.safe_select_text(soup, self.selectors["prix_global"])
            }
            return data
            
        except Exception as e:
            logger.error(f"[self.name] Erreur scraping des données pour {url}: {e}")
            return None

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
            if url.startswith("https://immobilier.jll.fr/location") or url.startswith("https://immobilier.jll.fr/vente") :
                if "bureaux" in url:
                    last_segment = url.strip('/').split('/')[-1]
                    part = last_segment.split('-')
                    part = part[-2]
                    if not any(departement in part for departement in DEPARTMENTS_IDF) :
                        filtered_urls.append(url)
                else :
                    filtered_urls.append(url)
        logger.info(f"[{self.name.upper()}] Trouvé {len(filtered_urls)} URLs filtrées sans bureaux région")
        return filtered_urls