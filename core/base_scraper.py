# -*- coding: utf-8 -*-
"""
Classe de base abstraite pour tous les scrapers
"""

from abc import ABC, abstractmethod
from typing import Union
import logging
import httpx
from config.settings import REQUEST_TIMEOUT
from bs4 import BeautifulSoup
from utils.user_agent import Rotator

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Classe de base abstraite pour l'initialisation des scrapers"""

    def __init__(
        self,
        user_agent_generateur: Rotator,
        proxy: str,
        nom_site: str,
        sitemap: list[str],
    ) -> None:
        """Instanciation d'un scraper depuis la classe abstraite BaseScraper

        Args:
            user_agent_generateur (str): Réprésente le générateur d'user-agents à utiliser dans les requêtes
            proxy (str): Représente le lien vers le proxy à utiliser dans les requêtes
            name (str): Représente le nom du site à scraper
            sitemap (list[str]): Réprésente le format d'extraction et la ou les urls des sites à scraper ex: ["XML", "Url"] ou ["XML", {"Type1":"Url", "Type2":"Url"}]
        """
        self.ua_generateur = user_agent_generateur
        self.proxy = proxy
        self.name = nom_site
        self.format_sitemap = sitemap[0]
        self.sitemap_url = sitemap[1]
        self.resultats_offres = []

    @abstractmethod
    def obtenir_sitemap_xml(self) -> list[str]:
        """Récupère les URLs depuis le ou les sitemaps XML

        Returns:
            list[str]: Représente les urls à scraper depuis le format XML
        """
        pass

    @abstractmethod
    def obtenir_sitemap_html(self) -> list[str]:
        """Récupère les URLs depuis le ou les sitemaps HTML

        Returns:
            list[str]: Représente les urls à scraper depuis le format HTML
        """
        pass

    @abstractmethod
    def obtenir_sitemap_api(self) -> list[str]:
        """Récupère les URLs depuis le ou les sitemaps API

        Returns:
            list[str]: Représente les urls à scraper depuis le format API
        """
        pass

    @abstractmethod
    def filtre_urls(self, urls: list[str]) -> list[str]:
        """Filtre les URLs selon les règles spécifiques de chaque scraper

        Args:
            urls (list[str]): Représente les urls avant filtrage

        Returns:
            list[str]: Représente les urls après filtrage
        """
        pass

    def choix_methode_extraction(self) -> list[str]:
        """
        Choisi le mode d'extraction de la sitemap en fonction de son type xml ou html

        Returns:
            list[str]: Liste de chaîne de caractères représentants les urls à scraper
        """
        logger.info("Choix de la méthode d'extraction")

        if self.format_sitemap == "XML":
            logger.info(f"[{self.sitemap_url}] Utilisation de la méthode XML")
            return self.obtenir_sitemap_xml()
        elif self.format_sitemap == "API":
            logger.info(f"[{self.sitemap_url}] Utilisation de la méthode API")
            return self.obtenir_sitemap_api()
        elif self.format_sitemap == "URL":
            logger.info(f"[{self.sitemap_url}] Utilisation de la méthode HTML")
            return self.obtenir_sitemap_html()
        else:
            raise ValueError(
                f"Le format de la sitemap : {self.format_sitemap} n'est pas supporté"
            )

    def rechercher_donnees_offre(self, url: str) -> Union[dict[str], dict[None]]:
        """Récupère les informations d'une offre à partir de son url

        * Hooks à surcharger par les instances si besoin spécifiques :
            - post_traitement_hook()

        Args:
            url (str): Représentant l'url à scraper

        Returns:
            dict[str]: Dictionnaire avec les informations de l'offre scrapée depuis l'url
        """
        try:
            with httpx.Client(
                proxy=self.proxy,
                headers={"User-agent": self.ua_generateur.get()},
                timeout=REQUEST_TIMEOUT,
                follow_redirects=True,
            ) as client:
                reponse = client.get(url)
            reponse.raise_for_status()
            soup = BeautifulSoup(reponse.text, "html.parser")

            # Extraction des données
            data = {
                "confrere": self.name,
                "url": url,
                "reference": self.safe_select_text(soup, self.selectors["reference"]),
                "contrat": self.safe_select_text(soup, self.selectors["contrat"]),
                "actif": self.safe_select_text(soup, self.selectors["actif"]),
                "disponibilite": self.safe_select_text(
                    soup, self.selectors["disponibilite"]
                ),
                "surface": (self.safe_select_text(soup, self.selectors["surface"])),
                "division": (
                    self.safe_select_text(soup, self.selectors["division"])
                    if self.selectors["division"] != "None"
                    else None
                ),
                "adresse": self.safe_select_text(soup, self.selectors["adresse"]),
                "contact": self.safe_select_text(soup, self.selectors["contact"]),
                "accroche": self.safe_select_text(soup, self.selectors["accroche"]),
                "amenagements": self.safe_select_text(
                    soup, self.selectors["amenagements"]
                ),
                "url_image": self.safe_select_text(soup, self.selectors["url_image"]),
                "latitude": self.safe_select_text(soup, self.selectors["latitude"]),
                "longitude": self.safe_select_text(soup, self.selectors["longitude"]),
                "prix_global": self.safe_select_text(
                    soup, self.selectors["prix_global"]
                ),
            }

            # Fonction de post-traitement si besoin spécifique pour certains champs du dictionnaire
            self.post_traitement_hook(data, soup, url)
            return data

        except Exception as e:
            logger.error(f"[{self.name}] Erreur scraping des données pour {url}: {e}")
            return {}

    def post_traitement_hook(
        self, data: dict[str], soup: BeautifulSoup, url: str
    ) -> None:
        """Méthode de post-traitement à surcharger si besoin spécifique pour certains champs du dictionnaire

        Args:
            data (dict[str]): Représente les données de l'offre à scraper
            soup (BeautifulSoup): Représente le parser lié à la page html de l'offre à scraper
            url (str): Représente l'url de l'offre à scraper
        """
        pass

    def safe_select_text(self, soup: BeautifulSoup, selector: str) -> str:
        """
        Extrait le texte d'un élément HTML de manière sécurisée depuis un élément BeautifulSoup

        Args:
            soup (BeautifulSoup): Représente le contenu HTML de la page à scraper
            selector (str): Représente l'élément CSS à requêter et qui provient du fichier settings.py
        Returns:
            (str): Représente la valeur du sélécteur requêté sinon la valeur "N/A"
        """
        if selector == "None":
            return "N/A"

        try:
            element_selector = soup.select_one(selector)
            return element_selector.get_text(strip=True) if element_selector else "N/A"

        except Exception as e:
            logger.error(
                f"[{self.name}] Erreur dans safe_select_text avec selector='{selector}': {e}"
            )
            return "N/A"

    def run(self) -> Union[list[str], None]:
        """Méthode pour lancer le scraper"""
        try:
            logger.info(
                f"[{self.name.upper()}] Début du programme de scraping des offres immobilières"
            )
            urls = self.choix_methode_extraction()
            # Filtrer seulement si la méthode est implémentée
            if hasattr(self, "filtre_urls") and callable(getattr(self, "filtre_urls")):
                url_filtrees = self.filtre_urls(urls)
            else:
                url_filtrees = urls
            # Il n'est pas nécessaire de boucler sur la liste en passant par API pour l'instant
            if self.format_sitemap == "API":
                self.resultats_offres = urls
                logger.info(
                    f"[{self.name.upper()}] Fin du scraping. {len(self.resultats_offres)} résultats collectés."
                )
                return self.resultats_offres
            else:
                logger.info(
                    f"[{self.name.upper()}] Début du scraping des données pour chacune des offres"
                )
                nb_urls = len(url_filtrees)
                for url in url_filtrees[:5]:
                    try:
                        resultats = self.rechercher_donnees_offre(url)
                        if resultats:
                            self.resultats_offres.append(resultats)
                        logger.info(
                            f"[{self.name.upper()}] Recherche des données en cours - {url_filtrees.index(url)}/{nb_urls}"
                        )
                    except Exception as e:
                        logger.error(
                            f"[{self.name.upper()}] Erreur lors de la récupération de {url}: {e}"
                        )

                logger.info(
                    f"[{self.name.upper()}] Fin du scraping. {len(self.resultats_offres)} résultats collectés."
                )
                return self.resultats_offres

        except Exception as e:
            logger.error(
                f"[{self.name.upper()}] Erreur importante lors du scraping : {e}"
            )
            return []
