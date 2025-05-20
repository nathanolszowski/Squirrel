# -*- coding: utf-8 -*-
"""
Classe de base abstraite pour tous les scrapers
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import logging
import httpx
from config.settings import REQUEST_TIMEOUT
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
    def filtre_idf_bureaux(self, urls: list) -> list:
        """
        Filtre les URLs pour supprimer les bureaux hors IDF

        Args:
            urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper
        Returns:
            filtered_urls (list[str]): Liste de chaînes de caractères représentant les urls à scraper après filtrage des urls bureaux régions
        """
        pass
    
    def scrape_listing(self, url: str) -> dict:
        """
        Scrape les données d'une annonce depuis une url
        
        Hooks à surcharger par les instances si besoin spécifiques :
            - post_traitement_hook()
        
        Args:
            urls (str): Chaîne de caractères représentant l'url à scraper
        Retruns:
            data (dict): Dictionnaire avec les informations de chaque offre scrapée
        """
        try:
            logger.info(f"[{self.name.upper()}] Début du scraping des données pour chacune des offres")
            response = httpx.get(url, headers={"User-agent":self.ua_generateur.get()}, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extraction des données
            data = {
                "confrere" : self.name,
                "url": url,
                "reference" : self.safe_select_text(soup, self.selectors["reference"]),
                "contrat": self.safe_select_text(soup, self.selectors["contrat"]),
                "actif" : self.safe_select_text(soup, self.selectors["actif"]),
                "disponibilite" : self.safe_select_text(soup, self.selectors["disponibilite"]),
                "surface" : self.safe_select_text(soup, self.selectors["surface"]),
                "division" : self.safe_select_text(soup, self.selectors["division"]),
                "adresse" : self.safe_select_text(soup, self.selectors["adresse"]),
                "contact" : self.safe_select_text(soup, self.selectors["contact"]),
                "accroche" : self.safe_select_text(soup, self.selectors["accroche"]),
                "amenagements" : self.safe_select_text(soup, self.selectors["amenagements"]),
                "prix_global" : self.safe_select_text(soup, self.selectors["prix_global"])
            }
            # Fonction de post-traitement si besoin spécifique pour certains champs du dictionnaire
            self.post_traitement_hook(data, soup, url)
            return data
        
        except Exception as e:
            logger.error(f"[{self.name}] Erreur scraping des données pour {url}: {e}")
            return None
        
    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> Optional[dict]:
        """Fonction de post-traitement à surcharger si besoin spécifique pour certains champs du dictionnaire"""
        pass
    
    def choix_sitemap(self) -> str:
        """
        Choisi le mode d'extraction de la sitemap en fonction de son type xml ou html
        """
        url = next(iter(self.sitemap_url.keys())) if isinstance(self.sitemap_url, dict) else self.sitemap_url

        if url.endswith(".xml"):
            logger.info(f"[{self.sitemap_url}] Utilisation de la méthode XML")
            return self.get_sitemap_xml()
        else:
            logger.info(f"[{self.sitemap_url}] Utilisation de la méthode HTML")
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
        if selector == "None" :
            return "N/A"
        
        try:
            el = soup.select_one(selector)
            return el.get_text(strip=True) if el else "N/A"
        
        except Exception as e:
            logger.error(f"[{self.name}] Erreur dans safe_select_text avec selector='{selector}': {e}")
            return "N/A"
    
    def run(self) -> None:
        """Exécute le programme complet"""
        try:
            logger.info(f"[{self.name.upper()}] Début du scraping")
            urls = self.choix_sitemap()

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
