# -*- coding: utf-8 -*-
"""
Scraper pour KNIGHT FRANK
"""

import logging
import re
from typing import List
from bs4 import BeautifulSoup
from core.selenium_scraper import SeleniumScraper
from config.settings import SITEMAPS
from config.selectors import KNIGHTFRANK_SELECTORS

logger = logging.getLogger(__name__)

class KNIGHTFRANKScraper(SeleniumScraper):
    """Scraper pour le site CBRE qui hérite de la classe RequestsScraper"""
    
    def __init__(self, ua_generateur, proxy) -> None:
        super().__init__(ua_generateur, proxy, "KNIGHTFRANK", SITEMAPS["KNIGHTFRANK"])
        self.selectors = KNIGHTFRANK_SELECTORS
        self.base_url = "https://www.knightfrank.fr"
           
    def post_traitement_hook(self, data: dict, soup: BeautifulSoup, url: str) -> dict:
        # Surcharger la méthode obtenir le contrat
        contrat_map = {
            "location": "Location",
            "vente": "Vente",
        }
        data["contrat"] = next((label for key, label in contrat_map.items() if key in url), "N/A")
        # Surcharger la méthode obtenir l'actif
        data["actif"] = "Bureaux"
        # Déterminer l'adresse
                    
    def trouver_formater_urls_offres(self, soup) -> list:
        """Permet de formater les urls lors de la méthode get_sitemap_html"""
        div_parent = soup.select_one("#listCards > div")
        if not div_parent:
            print("Pas d'élément listCards trouvé")
            return []

        offres = div_parent.find_all("div", class_=re.compile("cardOffreListe"))
        liens = [offre.find("a", class_="infosCard") for offre in offres if offre.find("a", class_="infosCard")]
        hrefs = [self.base_url + lien['href'] for lien in liens if liens and lien.has_attr('href')]
        return hrefs
    
    def navigation_page(self, url):
        """Permet de naviguer entre les différentes pages d'offres"""
        urls =[]
        while url:
            soup= self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            urls += self.trouver_formater_urls_offres(soup)
            
            div_parent = soup.select_one("body > main > section > div.container.pagination.py-5 > div")
            if div_parent:
                suivant = div_parent.find_all("a", attrs={"aria-label": "Next"})
                if suivant:
                    href = suivant[0].get("href")
                    url = self.base_url + href
                else:
                    url = None
        return urls
    
    def get_sitemap_html(self) -> List[str]:
        """
        Navigue de la première à la dernière page en implémentant la méthode de la classe abstraite BaseScraper
        
        Returns:
            urls (List[str]): Liste de chaînes de caractères représentant les urls à scraper
        """
        logger.info("Récupération des urls depuis le ou les sitemap HTML")
        try:
            urls = []
            if isinstance(self.sitemap_url, dict):
                for contrat, url in self.sitemap_url.items():
                    urls += self.navigation_page(url)
                logger.info(f"[{self.name}] Trouvé {len(urls)} URLs dans les sitemaps")
            else:
                urls = self.navigation_page(self.sitemap_url)
                logger.info(f"[{self.name}] Trouvé {len(urls)} URLs dans les sitemaps")
            return urls

        except Exception as e:
            logger.error(f"[{self.name}] Erreur lors de la récupération du sitemap {self.sitemap_url}: {e}")
            return None

    #Obligé de l'appeler car classe abstraite
    def filtre_idf_bureaux(self, urls: list) -> List[str]:
        return urls