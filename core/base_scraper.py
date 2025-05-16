# -*- coding: utf-8 -*-
"""
Classe de base abstraite pour tous les scrapers
"""

from abc import ABC, abstractmethod
from typing import List
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Classe de base abstraite pour tous les scrapers"""
    
    def __init__(self, ua_generateur, name: str, sitemap_url: str) -> None:
        """
        Initialise un nouveau scraper
        
        Args:
            name (str): Nom du scraper (ex: 'bnp', 'jll')
            sitemap_url (str): URL de la sitemap XML ou HTML
        """
        self.ua_generateur = ua_generateur
        self.name = name
        self.sitemap_url = sitemap_url
        self.results = []
    
    @abstractmethod
    def get_sitemap_xml(self) -> List[str]:
        """
        Récupère les URLs depuis le ou les sitemaps XML
        
        Returns:
            urls (List[str]): Liste de chaînes de caractères représentant les urls à scraper
        """
        pass
    
    @abstractmethod
    def get_sitemap_html(self) -> List[str]:
        """
        Récupère les URLs depuis le ou les sitemaps HTML
        
        Returns:
            urls (List[str]): Liste de chaînes de caractères représentant les urls à scraper
        """
        pass
    
    @abstractmethod
    def scrape_listing(self, url: str) -> dict:
        """
        Scrape les données d'une annonce à partir de son url
        
        Args:
            urls (str): Chaîne de caractères représentant l'url à scraper
        Retruns:
            data (dict): Dictionnaire de chaînes de caractères avec les informations de chaque offre scrapée
        """
        pass
    
    @abstractmethod
    def filtre_idf_bureaux(self, urls: list) -> list:
        """
        Filtre les URLs pour supprimer les bureaux hors IDF

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper
        Returns:
            filtered_urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        pass
    
    def choix_sitemap(self) -> None:
        """
        Choisi le mode d'extraction de la sitemap en fonction de son type xml ou html
        """
        url = next(iter(self.sitemap_url.keys())) if isinstance(self.sitemap_url, dict) else self.sitemap_url

        if url.endswith(".xml"):
            return self.get_sitemap_xml()
        else:
            return self.get_sitemap_html()
    
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
            urls = self.choix_sitemap()
            print(urls)
            if hasattr(self, "filtre_idf_bureaux") and callable(getattr(self, "filtre_idf_bureaux")):
                url_filtrees = self.filtre_idf_bureaux(urls)
            else:
                url_filtrees = urls
            
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
