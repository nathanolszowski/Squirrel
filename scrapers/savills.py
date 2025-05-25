# -*- coding: utf-8 -*-
"""
Scraper pour SAVILLS
"""

import logging
import httpx
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import SITEMAPS, REQUEST_TIMEOUT
#from config.selectors import SAVILLS_SELECTORS

logger = logging.getLogger(__name__)

class SAVILLSScraper(RequestsScraper):
    """Scraper pour le site ARTHURLOYD qui hérite de la classe RequestsScraper"""
    
    def __init__(self, ua_generateur) -> None:
        super().__init__(ua_generateur,"SAVILLS", SITEMAPS["SAVILLS"])
        #self.selectors = SAVILLS_SELECTORS
        self.base_url = "https://search.savills.com"
        self.api_url = "https://livev6-searchapi.savills.com/Data/SearchByUrl"
    
    def get_sitemap_api(self):
        header_search_url = {
            'gpscountrycode': 'fr',
            'gpslanguagecode': 'fr',
            'origin': self.base_url,
            'user-agent': self.ua_generateur.get()
        }
        json_data_search_url = {
            'url': '/fr/fr/liste?SearchList=Id_16+Category_RegionCountyCountry&Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&CommercialSizeUnit=SquareMeter&LandAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10&Page=1',
        }
        response = httpx.get(self.sitemap_url, headers=header_search_url, json=json_data_search_url, timeout=REQUEST_TIMEOUT)
        nb_pages_resultats = response.json()["Results"]["PagingInfo"]["PageCount"]
        ids = []
        for nb in nb_pages_resultats:
            json_data_search_url = {
                'url': f'/fr/fr/liste?SearchList=Id_16+Category_RegionCountyCountry&Tenure=GRS_T_R&SortOrder=SO_PCDD&Currency=EUR&Period=Year&CommercialPropertyType=GRS_CPT_O&Receptions=-1&CommercialSizeUnit=SquareMeter&LandAreaUnit=SquareMeter&AvailableSizeUnit=SquareMeter&Category=GRS_CAT_COM&Shapes=W10&Page={nb}',
            }
            response = httpx.get(self.sitemap_url, headers=header_search_url, json=json_data_search_url, timeout=REQUEST_TIMEOUT)
            properties = response.json()["Results"]["Properties"]
            ids = [prop["ExternalPropertyID"] for prop in properties if "ExternalPropertyID" in prop]
        return ids
           
    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> dict:
        pass
        
    def filtre_idf_bureaux(self, urls: list[str]) -> list[str]:
        """
        Filtre les URLs pour supprimer les bureaux hors IDF

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper
        Returns:
            filtered_urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage
        """
        pass