# -*- coding: utf-8 -*-
"""
Scraper pour CUSHMAN
"""

import logging
import requests
import re
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS, REQUEST_TIMEOUT
from config.selectors import CUSHMAN_SELECTORS

logger = logging.getLogger(__name__)

class CUSHMANScraper(RequestsScraper):
    """Scraper pour le site CUSHMAN"""
    
    def __init__(self):
        super().__init__("CUSHMAN", SITEMAPS["CUSHMAN"])
        self.selectors = CUSHMAN_SELECTORS
        
        
    def scrape_listing(self, url):
        """Scrape une annonce CUSHMAN"""
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Déterminer le contrat
            contrat_map = {
                "location": "Location",
                "achat": "Vente"
            }
            contrat = next((label for key, label in contrat_map.items() if key in url), "N/A")
            # Déterminer l'actif
            actif_map = {
                "Bureaux": "Bureaux",
                "Activités": "Locaux d'activité",
                "Entrepôts": "Entrepots"
            }
            actif = next((label for key, label in actif_map.items() if key in self.safe_select_text(soup, self.selectors["actif"])), "N/A")
            
            # Extraction des données
            data = {
                "confrere" : self.name,
                "url": url,
                "reference" : self.safe_select_text(soup, self.selectors["reference"]),
                "contrat": contrat,
                "actif" : actif,
                "disponibilite" : self.safe_select_text(soup, self.selectors["disponibilite"]),
                "surface" : self.safe_select_text(soup, self.selectors["surface"]),
                "adresse" : self.safe_select_text(soup, self.selectors["adresse"]),
                "contact" : self.safe_select_text(soup, self.selectors["contact"]),
                "accroche" : self.safe_select_text(soup, self.selectors["accroche"]),
                "amenagements" : re.sub(r'(?<!^)([A-Z])', r' \1', self.safe_select_text(soup, self.selectors["amenagements"])),
                "prix_global" : self.safe_select_text(soup, self.selectors["prix_global"])
            }
            return data
            
        except Exception as e:
            logger.error(f"[self.name] Erreur scraping {url}: {e}")
            return None

    def filtre_idf_bureaux(self, urls):
        """Filtre les URLs pour supprimer les bureaux hors IDF"""
        filtered_urls = []
        for url in urls:
            if url.startswith("https://immobilier.cushmanwakefield.fr/location") or url.startswith("https://immobilier.cushmanwakefield.fr/achat"):
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