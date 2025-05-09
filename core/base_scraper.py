# -*- coding: utf-8 -*-
"""
Classe de base abstraite pour tous les scrapers
"""

from abc import ABC, abstractmethod
import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Classe de base abstraite pour tous les scrapers"""
    
    def __init__(self, name: str, sitemap_url: str) -> None:
        """
        Initialise un nouveau scraper
        
        Args:
            name (str): Nom du scraper (ex: 'bnp', 'jll')
            sitemap_url (str): URL du sitemap XML
        """
        self.name = name
        self.sitemap_url = sitemap_url
        self.results = []
    
    @abstractmethod
    def get_sitemap_xml(self) -> None:
        """Récupère les URLs depuis le sitemap"""
        pass
    
    @abstractmethod
    def scrape_listing(self, url: str) -> None:
        """Scrape une annonce individuelle"""
        pass
    
    @abstractmethod
    def filtre_idf_bureaux(self, urls: list) -> None:
        """Filtre les URLs en fonction de la sitemap pour supprimer les bureaux hors IDF"""
        pass
    
    def safe_select_text(self, soup: BeautifulSoup, selector: str) -> str:
        """
        Extrait le texte d'un élément HTML de manière sécurisée

        Args:
            soup (BeautifulSoup): Objet BeautifulSoup représentant le contenu HTML de la page à requêter
            selector (str): Chaîne de caractère représentant l'élément CSS à requêter et qui provient du fichier settings.py
        Returns:
            (str): Chaîne de caractères représentant la valeur du sélécteur requêté sinon la valeur "N/A"
        """
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else "N/A"
    
    def run(self) -> None:
        """Exécute le programme complet"""
        try:
            logger.info(f"[{self.name.upper()}] Début du scraping")
            urls = self.get_sitemap_xml()
            url_filtrees = self.filtre_idf_bureaux(urls)

            for url in url_filtrees[:5]:
                try:
                    result = self.scrape_listing(url)
                    if result:
                        self.results.append(result)
                except Exception as e:
                    logger.error(f"[{self.name.upper()}] Erreur lors de la récupération de {url}: {e}")
            
            logger.info(f"[{self.name.upper()}] Fin du scraping. {len(self.results)} résultats collectés.")
            return self.results
            
        except Exception as e:
            logger.error(f"[{self.name.upper()}] Erreur importante lors du scraping : {e}")
            return []
