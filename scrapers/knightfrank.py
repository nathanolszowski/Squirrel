# -*- coding: utf-8 -*-
"""
Scraper pour KNIGHT FRANK
"""

import logging
import requests
import re
from bs4 import BeautifulSoup
from core.requests_scraper import RequestsScraper
from config.settings import DEPARTMENTS_IDF, SITEMAPS, REQUEST_TIMEOUT, USER_AGENT
from config.selectors import KNIGHTFRANK_SELECTORS

logger = logging.getLogger(__name__)

class KNIGHTFRANKcraper(RequestsScraper):
    """Scraper pour le site CBRE qui hérite de la classe RequestsScraper"""
    
    def __init__(self) -> None:
        super().__init__("KNIGHTFRANK", SITEMAPS["KNIGHTFRANK"])
        self.selectors = KNIGHTFRANK_SELECTORS
           
    def scrape_listing(self, url: str) -> dict:
        """
        Scrape une annonce KNIGHTFRANK
        
        Args:
            urls (str): Chaîne de caractères représentant l'url à scraper
        Retruns:
            data (dict[str]): Dictionnaire de chaînes de caractères avec les informations de chaque offre scrapée
        """
        try:
            logger.info(f"[{self.name.upper()}] Début du scraping des données pour chacune des offres")
            response = requests.get(url, headers={"User-agent":USER_AGENT.get()}, timeout=REQUEST_TIMEOUT)
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
        
    
    def navigation_pages(self, url, url_base, contrat):
        """
        Navigue de la première à la dernière page
        
        Args:
        
        """
        urls = []
        print("Début du scraping des offres " + contrat)
        while url:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
            
            urls += trouver_formater_urls(soup, url_base)
            
            div_parent = soup.select_one("body > main > section > div.container.pagination.py-5 > div")
            if div_parent:
                suivant = div_parent.find_all("a", attrs={"aria-label": "Next"})
                if suivant:
                    href = suivant[0].get("href")
                    url = url_base + href
                else:
                    print(str(len(urls)) + " offres " + contrat + " trouvées chez KTF")
                    url = None
                    
        offres_ktf = []
        print("Début du scraping des données offres " + contrat)
        for url in urls :
            result = scraper(url, url_base, contrat)
            offres_ktf.append(result)
            
        return print("Scraping terminé pour le contrat :" + contrat)
        
            
    def trouver_formater_urls(self, soup, url_base):
        div_parent = soup.select_one("#listCards > div")
        if not div_parent:
            print("Pas d'élément listCards trouvé")
            return []

        offres = div_parent.find_all("div", class_=re.compile("cardOffreListe"))
        liens = [offre.find("a", class_="infosCard") for offre in offres if offre.find("a", class_="infosCard")]
        hrefs = [url_base + lien['href'] for lien in liens if liens and lien.has_attr('href')]
        return hrefs
