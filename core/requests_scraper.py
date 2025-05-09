# -*- coding: utf-8 -*-
"""
Classe de base pour les scrapers utilisant requests
"""

import logging
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from config.settings import REQUEST_TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)

class RequestsScraper(BaseScraper):
    """Classe de base pour les scrapers utilisant requests et qui hérite de la classe abstraite BaseScraper"""
    
    def get_sitemap_xml(self) -> list:
        """
        Récupère les URLs depuis le ou les sitemaps XML
        
        Returns:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper
        """
        logger.info("Récupération des urls depuis la sitemap principale")
        try:
            urls = []
            if isinstance(self.sitemap_url, dict):
                for actif, url in self.sitemap_url.items():
                    response = requests.get(url, headers={"User-agent":USER_AGENT.get()}, timeout=REQUEST_TIMEOUT)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, "xml")
                    
                    # Récupérer toutes les URLs du sitemap
                    urls.extend([url.find("loc").text for url in soup.find_all("url")])
                logger.info(f"[{self.name}] Trouvé {len(urls)} URLs dans les sitemaps")
            else:
                response = requests.get(self.sitemap_url, headers={"User-agent":USER_AGENT.get()}, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "xml")
                    
                # Récupérer toutes les URLs du sitemap
                urls = [url.find("loc").text for url in soup.find_all("url")]
                logger.info(f"[{self.name}] Trouvé {len(urls)} URLs dans le sitemap")
            return urls
    
        except Exception as e:
            logger.error(f"[{self.name}] Erreur lors de la récupération du sitemap {self.sitemap_url}: {e}")
            return None
    
    def scrape_listing(self, url: str) -> None:
        """
        Scrape une annonce individuelle
        
        Cette méthode doit être surchargée par les classes enfants
        pour implémenter la logique spécifique à chaque site
        """
        raise NotImplementedError("Les sous-classes doivent implémentées la méthode scrape_listing()")
