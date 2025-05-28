# -*- coding: utf-8 -*-
"""
Scraper pour SAVILLS
"""

import logging
import httpx
from typing import Union
from core.requests_scraper import RequestsScraper
from config.settings import SITEMAPS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class SAVILLSScraper(RequestsScraper):
    """Scraper pour le site SAVILLS qui hérite de la classe RequestsScraper"""

    def __init__(self, ua_generateur) -> None:
        super().__init__(ua_generateur, "SAVILLS", SITEMAPS["SAVILLS"])

        self.base_url = "https://search.savills.com"
        self.api_url = "https://livev6-searchapi.savills.com/Data/SearchByUrl"
        self.property_url = "https://search.savills.com/fr/fr/bien-immobilier-details/"

    def get_sitemap_api(self) -> Union[list[str], list[None]]:
        """Méthode de récupération les URLs depuis le ou les sitemaps API qui surcharge celle de la classe abstraite BaseScraper

        Returns:
            urls (list[str]): Représente les urls à scraper depuis le format API
        """
        # Initialise le header avec le mini infos nécessaire pour acceder au site
        header_search_url = {
            "gpscountrycode": "fr",
            "gpslanguagecode": "fr",
            "origin": self.base_url,
            "user-agent": self.ua_generateur.get(),
        }
        resultats = []
        # Pour chaque url de la liste de sitemap, récupérer le détail des offres
        for actif, url in self.sitemap_url.items():
            page = 1
            nb_pages_resultats = 1
            while page <= nb_pages_resultats:
                params = f"{url}&Page={page}"
                params_url = {
                    "url": params,
                }
                try:
                    with httpx.Client(
                        proxy=self.proxy,
                        headers=header_search_url,
                        json=params_url,
                        follow_redirects=True,
                        timeout=REQUEST_TIMEOUT,
                    ) as client:
                        reponse = client.post(self.api_url)
                    reponse.raise_for_status()

                    nb_pages_resultats = reponse.json()["Results"]["PagingInfo"][
                        "PageCount"
                    ]
                    offres = reponse.json()["Results"]["Properties"]

                    for offre in offres:
                        offre_detail = {
                            "confrere": self.name,
                            "url": self.property_url
                            + offre["ExternalPropertyIDFormatted"],
                            "reference": offre["ExternalPropertyIDFormatted"],
                            "actif": offre["PropertyTypes"]["Caption"],
                            "disponibilite": offre["ByUnit"][0]["Disponibilité"],
                            "surface": offre["SizeFormatted"],
                            "adresse": offre["AddressLine2"],
                            "contact": offre["PrimaryAgent"]["AgentName"],
                            "accroche": offre["Description"],
                            "amenagements": offre["LongDescription"]["Body"],
                            "prix_global": offre["DisplayPriceText"],
                        }
                        resultats.append(offre_detail)
                    page += 1
                except Exception as e:
                    logger.error(
                        f"[{self.name}] Erreur scraping des données pour {url}: {e}"
                    )
                    return []
        return resultats

    # Obligé d'appeler la méthode ci-dessous car implémentée dans la classe abstraite BaseScraper
    def filtre_urls(self, urls: list[str]) -> list[str]:
        pass
