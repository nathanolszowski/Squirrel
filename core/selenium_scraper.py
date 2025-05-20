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
from config.settings import SELENIUM_OPTIONS, SELENIUM_WAIT_TIME

logger = logging.getLogger(__name__)

class SeleniumScraper(BaseScraper):
    """Classe de base pour les scrapers utilisant Selenium et qui hérite de la classe abstraite BaseScraper"""
    
    def __init__(self, ua_generateur, name: str, sitemap_url: str, timeout=SELENIUM_WAIT_TIME) -> None:
        super().__init__(ua_generateur, name, sitemap_url)
        self.driver = None
        self.timeout = timeout
        self.setup_driver()
    
    def setup_driver(self) -> None:
        """Configure le driver Selenium via les infos du fichier settings.py"""
        options = Options()
        for option in SELENIUM_OPTIONS:
            options.add_argument(option)
        options.add_argument(f"user-agent={self.ua_generateur.get()}")
        
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            logger.info(f"[{self.name.upper()}] Le driver Selenium a été initialisé avec succès")
        except Exception as e:
            logger.error(f"[{self.name.upper()}] Erreur pendant l'initialisation du driver Selenium: {e}")
            raise
    
    def get_sitemap_xml(self) -> list:
        """
        Récupère les URLs depuis le ou les sitemaps XML
        
        Returns:
            urls (list[str]): Liste de chaîne de caractères représentants les urls à scraper
        """
        try:
            urls = []
            if isinstance(self.sitemap_url, dict):
                for actif, url in self.sitemap_url.items():
                    self.driver.get(url)
                    soup = BeautifulSoup(self.driver.page_source, "xml")
                    urls.extend([url.find("loc").text for url in soup.find_all("url")])
                logger.info(f"[{self.name}{actif}] Trouvé {len(urls)} URLs dans les sitemaps")
            else:
                self.driver.get(self.sitemap_url)
                soup = BeautifulSoup(self.driver.page_source, "xml")
                urls = [url.find("loc").text for url in soup.find_all("url")]
                logger.info(f"[{self.name.upper()}] Trouvé {len(urls)} URLs dans le sitemap")
            return urls
        
        except Exception as e:
            logger.error(f"[{self.name.upper()}] Erreur lors de la récupération du sitemap: {self.sitemap_url} {e}")
            return []
    
    def __del__(self) -> None:
        """Nettoie les ressources Selenium"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info(f"[{self.name.upper()}] Le driver Selenium a été fermé avec succès")
            except Exception as e:
                logger.error(f"[{self.name.upper()}] Une erreur est survenue lors de la fermeture du driver Selenium: {e}")

    def get_sitemap_html(self) -> None:
        pass