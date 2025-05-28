# -*- coding: utf-8 -*-
"""
Classe de base pour les scrapers utilisant requests
"""

import logging
import httpx
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from config.settings import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class RequestsScraper(BaseScraper):
    """Classe de base pour les scrapers utilisant httpx et qui hérite de la classe abstraite BaseScraper"""

    def __init__(
        self,
        ua_generateur,
        proxy,
        name: str,
        sitemap_url: str,
        timeout=REQUEST_TIMEOUT,
    ) -> None:
        """Instanciation d'un scraper Requests depuis la classe abstraite BaseScraper"""
        super().__init__(ua_generateur, proxy, name, sitemap_url)
        self.driver = None
        self.timeout = timeout

    def get_sitemap_xml(self) -> list[str]:
        """
        Récupère les URLs depuis le ou les sitemaps XML en surchageant la méthode de la classe abstraite BaseScraper

        Returns:
            list[str]: Liste de chaînes de caractères représentant les urls à scraper
        """
        logger.info("Récupération des urls depuis le ou les sitemaps XML")
        try:
            urls = []
            if isinstance(self.sitemap_url, dict):
                logger.info("Récupération des urls depuis plusieurs sitemaps XML")
                for actif, url in self.sitemap_url.items():
                    with httpx.Client(
                        proxy=self.proxy,
                        headers={"User-agent": self.ua_generateur.get()},
                        timeout=REQUEST_TIMEOUT,
                        follow_redirects=True,
                    ) as client:
                        reponse = client.get(url)
                    reponse.raise_for_status()
                    soup = BeautifulSoup(reponse.content, "xml")
                    urls.extend([url.find("loc").text for url in soup.find_all("url")])
                logger.info(
                    f"[{self.name}] Trouvé {len(urls)} URLs dans les sitemaps XML"
                )
            else:
                logger.info("Récupération des urls depuis la sitemap XML")
                with httpx.Client(
                    proxy=self.proxy,
                    headers={"User-agent": self.ua_generateur.get()},
                    timeout=REQUEST_TIMEOUT,
                    follow_redirects=True,
                ) as client:
                    reponse = client.get(self.sitemap_url)
                reponse.raise_for_status()
                soup = BeautifulSoup(reponse.content, "xml")
                urls = [
                    self.sitemap_url.find("loc").text
                    for self.sitemap_url in soup.find_all("url")
                ]
                logger.info(
                    f"[{self.name}] Trouvé {len(urls)} URLs dans le sitemap XML"
                )
            return urls

        except Exception as e:
            logger.error(
                f"[{self.name}] Erreur lors de la récupération du sitemap {self.sitemap_url}: {e}"
            )
            return []

    def get_sitemap_html(self) -> list[str]:
        pass

    def get_sitemap_api(self) -> list[str]:
        pass
