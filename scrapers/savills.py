# -*- coding: utf-8 -*-
"""
Scraper pour SAVILLS
"""

import logging
import httpx
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import SITEMAPS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class SAVILLSScraper(RequestsScraper):
    """Scraper pour le site SAVILLS qui hérite de la classe RequestsScraper"""
    
    def __init__(self, ua_generateur) -> None:
        super().__init__(ua_generateur,"SAVILLS", SITEMAPS["SAVILLS"])

        self.base_url = "https://search.savills.com"
        self.api_url = "https://livev6-searchapi.savills.com/Data/SearchByUrl"
        self.property_url = "https://search.savills.com/fr/fr/bien-immobilier-details/"
    
    def get_sitemap_api(self):
        header_search_url = {
            'gpscountrycode': 'fr',
            'gpslanguagecode': 'fr',
            'origin': self.base_url,
            'user-agent': self.ua_generateur.get()
        }
        liste = []
        for actif, url in self.sitemap_url.items():
            page = 1
            pages_resultats = 1
            while page <= pages_resultats:
                params = f"{url}&Page={page}"
                params_url = {
                    'url': params,
                }
                try:
                    response = httpx.post(self.api_url, headers=header_search_url, json=params_url, timeout=REQUEST_TIMEOUT)
                except Exception as e:
                    logger.error(f"[{self.name}] Erreur scraping des données pour {url}: {e}")
                    return None
                pages_resultats = response.json()["Results"]["PagingInfo"]["PageCount"]
                properties = response.json()["Results"]["Properties"]
                
                for property in properties:
                    prop = {
                        "confrere" : self.name,
                        "url" : self.property_url + property["ExternalPropertyIDFormatted"],
                        "reference" : property["ExternalPropertyIDFormatted"],
                        "actif": property["PropertyTypes"]["Caption"],
                        "disponibilite": "",
                        "surface": property["SizeFormatted"],
                        "adresse" : property["AddressLine2"],
                        "contact": property["PrimaryAgent"]["AgentName"],
                        "accroche" : property["LongDescription"]["Body"],
                        "amenagements": "",
                        "prix_global": property["DisplayPriceText"]
                    }
                    liste.append(prop)
                page += 1
        return liste
        
    def filtre_idf_bureaux(self, urls: list[str]) -> list[str]:
        """
        Filtre les URLs pour supprimer les bureaux hors IDF

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper
        Returns:
            filtered_urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage
        """
        pass