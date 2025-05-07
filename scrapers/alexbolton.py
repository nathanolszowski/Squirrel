# -*- coding: utf-8 -*-
"""
Scraper pour Alex Bolton
"""

import logging
import requests
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import SITEMAPS, REQUEST_TIMEOUT, USER_AGENT
from config.selectors import ALEXBOLTON_SELECTORS

logger = logging.getLogger(__name__)

class ALEXBOLTONScraper(RequestsScraper):
    """Scraper pour le site ALEXBOLTON"""
    
    def __init__(self):
        super().__init__("ALEXBOLTON", SITEMAPS["ALEXBOLTON"])
        self.selectors = ALEXBOLTON_SELECTORS# -*- coding: utf-8 -*-

    def scrape_listing(self, url):
        """Scrape une annonce alexbolton"""
        try:
            response = requests.get(url, headers={"User-agent":USER_AGENT.get()}, timeout=REQUEST_TIMEOUT)
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
            logger.error(f"[self.name] Erreur scraping {url}: {e}")
            return None
        
    def filtre_idf_bureaux(self, urls):
        """Filtre les URLs pour supprimer les bureaux hors IDF. FYI : AlexBolton ne fait que du Bureaux IDF"""
        filtered_urls = []
        for url in urls:
            if url.startswith("https://www.alexbolton.fr/annonces/") :
                filtered_urls.append(url)
        logger.info(f"[{self.name.upper()}] Trouvé {len(filtered_urls)} URLs filtrées sans bureaux région")
        return filtered_urls