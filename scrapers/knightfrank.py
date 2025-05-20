# -*- coding: utf-8 -*-
"""
Scraper pour KNIGHT FRANK
"""

import logging
import httpx
import re
from typing import List
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import SITEMAPS, REQUEST_TIMEOUT, USER_AGENT
from config.selectors import KNIGHTFRANK_SELECTORS

logger = logging.getLogger(__name__)

class KNIGHTFRANKScraper(RequestsScraper):#Transformer
    """Scraper pour le site CBRE qui hérite de la classe RequestsScraper"""
    
    def __init__(self, ua_generateur) -> None:
        super().__init__(ua_generateur, "KNIGHTFRANK", SITEMAPS["KNIGHTFRANK"])
        self.selectors = KNIGHTFRANK_SELECTORS
        self.base_url = "https://www.knightfrank.fr"
           
    def scrape_listing(self, url: str) -> dict:
        """
        Scrape une annonce KNIGHT FRANK en implémentant la méthode de la classe mère RequestsScraper
        
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
                "reference" : self.safe_select_text(soup, self.selectors["reference"])
                #"contrat": contrat,
                #"actif" : actif,
                #"disponibilite" :self.safe_select_text(soup, self.selectors["disponibilite"]),
                #"surface" : self.safe_select_text(soup, self.selectors["surface"]),
                #"division" : self.safe_select_text(soup, self.selectors["division"]),
                #"adresse" : self.safe_select_text(soup, self.selectors["adresse"]),
                #"contact" : self.safe_select_text(soup, self.selectors["contact"]),
                #"accroche" : self.safe_select_text(soup, self.selectors["accroche"]),
                #"amenagements" : " ".join([self.safe_select_text(soup, self.selectors["amenagements"]),
                                           #self.safe_select_text(soup, self.selectors["prestations"])]),
                #"prix_global" : self.safe_select_text(soup, self.selectors["prix_global"])
            }
            return data
            
        except Exception as e:
            logger.error(f"[self.name] Erreur scraping des données pour {url}: {e}")
            return None
                    
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
            response = httpx.get(url, headers={"User-agent":self.ua_generateur.get()}, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            
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