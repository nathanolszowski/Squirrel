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
                logger.info("Récupération des urls depuis plusieurs sitemaps XML")
                for actif, url in self.sitemap_url.items():
                    with httpx.Client(follow_redirects=True) as client:
                        response = client.get(url, headers={"User-agent":self.ua_generateur.get()}, timeout=REQUEST_TIMEOUT)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, "xml")
                    
                    # Récupérer toutes les URLs du sitemap
                    urls.extend([url.find("loc").text for url in soup.find_all("url")])
                logger.info(f"[{self.name}] Trouvé {len(urls)} URLs dans les sitemaps")
            else:
                logger.info("Récupération des urls depuis la XML")
                with httpx.Client(follow_redirects=True) as client:
                    response = client.get(self.sitemap_url, headers={"User-agent":self.ua_generateur.get()}, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "xml")
                # Récupérer toutes les URLs du sitemap
                urls = [self.sitemap_url.find("loc").text for self.sitemap_url in soup.find_all("url")]
                logger.info(f"[{self.name}] Trouvé {len(urls)} URLs dans le sitemap")
            return urls
    
        except Exception as e:
            logger.error(f"[{self.name}] Erreur lors de la récupération du sitemap {self.sitemap_url}: {e}")
            return None
    
    def get_sitemap_html(self) -> List[str]:
        pass

    def get_sitemap_api(self) -> List[str]:
        pass