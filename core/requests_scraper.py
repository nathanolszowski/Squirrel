# -*- coding: utf-8 -*-
"""
Classe de base pour les scrapers utilisant requests
"""

import logging
import httpx
from typing import List
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from config.settings import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class RequestsScraper(BaseScraper):
    """Classe de base pour les scrapers utilisant requests et qui hérite de la classe abstraite BaseScraper"""
    
    def get_sitemap_xml(self) -> List[str]:
        """
        Récupère les URLs depuis le ou les sitemaps XML en surchageant la méthode de la classe abstraite BaseScraper
        
        Returns:
            urls (List[str]): Liste de chaînes de caractères représentant les urls à scraper
        """
        logger.info("Récupération des urls depuis la ou les sitemaps XML")
        try:
            urls = []
            if isinstance(self.sitemap_url, dict):
                for actif, url in self.sitemap_url.items():
                    response = httpx.get(url, headers={"User-agent":self.ua_generateur.get()}, timeout=REQUEST_TIMEOUT)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, "xml")
                    
                    # Récupérer toutes les URLs du sitemap
                    urls.extend([url.find("loc").text for url in soup.find_all("url")])
                logger.info(f"[{self.name}] Trouvé {len(urls)} URLs dans les sitemaps")
            else:
                response = httpx.get(self.sitemap_url, headers={"User-agent":self.ua_generateur.get()}, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "xml")
                    
                # Récupérer toutes les URLs du sitemap
                urls = [url.find("loc").text for url in soup.find_all("url")]
                logger.info(f"[{self.name}] Trouvé {len(urls)} URLs dans le sitemap")
            return urls
    
        except Exception as e:
            logger.error(f"[{self.name}] Erreur lors de la récupération du sitemap {self.sitemap_url}: {e}")
            return None
    
    def get_sitemap_html(self) -> List[str]:
        pass
