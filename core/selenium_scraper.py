# -*- coding: utf-8 -*-
"""
Classe de base pour les scrapers utilisant Selenium
"""


import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from .base_scraper import BaseScraper
from config.settings import SELENIUM_OPTIONS, USER_AGENT

logger = logging.getLogger(__name__)

class SeleniumScraper(BaseScraper):
    """Classe de base pour les scrapers utilisant Selenium"""
    
    def __init__(self, name, sitemap_url):
        super().__init__(name, sitemap_url)
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Configure le driver Selenium"""
        options = Options()
        for option in SELENIUM_OPTIONS:
            options.add_argument(option)
        options.add_argument(f"user-agent={USER_AGENT}")
        
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            logger.info(f"[{self.name.upper()}] Le driver Selenium a été initialisé avec succès")
        except Exception as e:
            logger.error(f"[{self.name.upper()}] Erreur pendant l'initialisation du driver Selenium: {e}")
            raise
    
    def get_sitemap_xml(self):
        """Récupère les URLs depuis le ou les sitemaps XML"""
        try:
            urls = []
            if isinstance(self.sitemap_url, dict):
                for actif, url in self.sitemap_url.items():
                    self.driver.get(self.sitemap_url)
                    soup = BeautifulSoup(self.driver.page_source, "xml")
                    urls.extend([url.find("loc").text for url in soup.find_all("url")])
                logger.info(f"[{self.name}] Trouvé {len(urls)} URLs dans les sitemaps")
            else:
                self.driver.get(self.sitemap_url)
                soup = BeautifulSoup(self.driver.page_source, "xml")
                urls = [url.find("loc").text for url in soup.find_all("url")]
                logger.info(f"[{self.name.upper()}] Trouvé {len(urls)} URLs dans le sitemap")
            return urls
        
        except Exception as e:
            logger.error(f"[{self.name.upper()}] Erreur lors de la récupération du sitemap: {self.sitemap_url} {e}")
            return []
    
    def scrape_listing(self, url):
        """
        Scrape une annonce individuelle
        
        Cette méthode doit être surchargée par les classes enfants
        pour implémenter la logique spécifique à chaque site
        """
        raise NotImplementedError("Les sous-classes doivent implémentées la méthode scrape_listing()")
    
    def __del__(self):
        """Nettoie les ressources Selenium"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info(f"[{self.name.upper()}] Le driver Selenium a été fermé avec succès")
            except Exception as e:
                logger.error(f"[{self.name.upper()}] Une erreur est survenue lors de la fermeture du driver Selenium: {e}")
