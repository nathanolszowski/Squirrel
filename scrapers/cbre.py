# -*- coding: utf-8 -*-
"""
Scraper pour CBRE
"""

import logging
import httpx
import re
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS, REQUEST_TIMEOUT, USER_AGENT
from config.selectors import CBRE_SELECTORS

logger = logging.getLogger(__name__)

class CBREScraper(RequestsScraper):
    """Scraper pour le site CBRE qui hérite de la classe RequestsScraper"""
    
    def __init__(self) -> None:
        super().__init__("CBRE", SITEMAPS["CBRE"])
        self.selectors = CBRE_SELECTORS
           
    def scrape_listing(self, url: str) -> dict:
        """
        Scrape une annonce CBRE
        
        Args:
            urls (str): Chaîne de caractères représentant l'url à scraper
        Retruns:
            data (dict[str]): Dictionnaire de chaînes de caractères avec les informations de chaque offre scrapée
        """
        try:
            logger.info(f"[{self.name.upper()}] Début du scraping des données pour chacune des offres")
            response = httpx.get(url, headers={"User-agent":USER_AGENT.get()}, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Déterminer le contrat
            contrat_map = {
                "a-louer": "Location",
                "a-vendre": "Vente",
            }
            contrat = next((label for key, label in contrat_map.items() if key in url), "N/A")
                
            # Déterminer l'actif
            actif_map = {
                "bureaux": "Bureaux",
                "activites": "Locaux d'activité",
                "entrepots": "Entrepots"
            }
            actif = next((label for key, label in actif_map.items() if key in url), "N/A")
            
            # Déterminer la référence
            reference_element = soup.find('li', class_='LS breadcrumb-item active')
            reference_element = reference_element.find("span")
            reference = reference_element.get_text(strip=True) if reference_element else "N/A"
            
            # Extraction des données
            data = {
                "confrere" : self.name,
                "url": url,
                "reference" : reference,
                "contrat": contrat,
                "actif" : actif,
                "disponibilite" :self.safe_select_text(soup, self.selectors["disponibilite"]),
                "surface" : self.safe_select_text(soup, self.selectors["surface"]),
                "division" : self.safe_select_text(soup, self.selectors["division"]),
                "adresse" : self.safe_select_text(soup, self.selectors["adresse"]),
                "contact" : self.safe_select_text(soup, self.selectors["contact"]),
                "accroche" : self.safe_select_text(soup, self.selectors["accroche"]),
                "amenagements" : " ".join([self.safe_select_text(soup, self.selectors["amenagements"]),
                                           self.safe_select_text(soup, self.selectors["prestations"])]),
                "prix_global" : self.safe_select_text(soup, self.selectors["prix_global"])
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
        pattern = re.compile(r"https://immobilier.cbre.fr/offre/(a-louer|a-vendre)/bureaux/(\d+)")
        for url in urls:
            if url.startswith("https://immobilier.cbre.fr/offre/"):
                if "bureaux" in url:
                    match = pattern.match(url)
                    if match and match.group(2)[:2] in DEPARTMENTS_IDF:
                        filtered_urls.append(url)
                else:
                    filtered_urls.append(url)
        logger.info(f"[{self.name.upper()}] Trouvé {len(filtered_urls)} URLs filtrées sans bureaux région")
        return filtered_urls
