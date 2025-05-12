# -*- coding: utf-8 -*-
"""
Scraper pour BNP Paribas Real Estate
"""

import logging
import httpx
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS, REQUEST_TIMEOUT, USER_AGENT
from config.selectors import BNP_SELECTORS

logger = logging.getLogger(__name__)

class BNPScraper(RequestsScraper):
    """Scraper pour le site BNP Paribas Real Estate qui hérite de la classe RequestsScraper"""
    
    def __init__(self) -> None:
        super().__init__("BNP", SITEMAPS["BNP"])
        self.selectors = BNP_SELECTORS

    def scrape_listing(self, url: str) -> dict:
        """
        Scrape une annonce BNP
        
        Args:
            urls (str): Chaîne de caractères représentant l'url à scraper
        Retruns:
            data (dict): Dictionnaire avec les informations de chaque offre scrapée
        """
        try:
            logger.info(f"[{self.name.upper()}] Début du scraping des données pour chacune des offres")
            response = httpx.get(url, headers={"User-agent":USER_AGENT.get()}, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Détermine le type de contrat
            if 'a-louer' in url:
                contrat = "Location"
                prix_global = self.safe_select_text(soup, self.selectors["loyer_global"])
            elif "a-vendre" in url:
                contrat = "Vente"
                prix_global = self.safe_select_text(soup, self.selectors["prix_global"])
            else:
                contrat = "N/A"
                
            # Déterminer le type d'actif
            actif_map = {
                "bureau": "Bureaux",
                "local": "Locaux d'activité",
                "entrepot": "Entrepots"
            }
                
            actif = next((label for key, label in actif_map.items() if key in url), "N/A")
                
            # Déterminer l'adresse complète
            adresse = self.safe_select_text(soup, self.selectors["adresse"])
            nom_immeuble = self.safe_select_text(soup, self.selectors["nom_immeuble"])
            adresse_complete = f"{nom_immeuble} {adresse}".strip()
            
            # Extraction des données
            data = {
                "confrere" : self.name,
                "url": url,
                "reference": self.safe_select_text(soup, self.selectors["reference"]),
                "contrat": contrat,
                "actif" : actif,
                "disponibilite" :self.safe_select_text(soup, self.selectors["disponibilite"]),
                "surface" : self.safe_select_text(soup, self.selectors["surface"]),
                "division" : self.safe_select_text(soup, self.selectors["division"]),
                "adresse" : adresse_complete,
                "contact" : self.safe_select_text(soup, self.selectors["contact"]),
                "accroche" : self.safe_select_text(soup, self.selectors["accroche"]),
                "amenagements" : self.safe_select_text(soup, self.selectors["amenagements"]),
                "prix_global" : prix_global
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
            if "bureau" in url:
                # Check if it contains any department from DEPARTMENTS_IDF
                if not any(f"-{departement}/" in url for departement in DEPARTMENTS_IDF):
                    filtered_urls.append(url)
            else:
                filtered_urls.append(url)
        logger.info(f"[{self.name.upper()}] Trouvé {len(filtered_urls)} URLs filtrées sans bureaux région")
        return filtered_urls