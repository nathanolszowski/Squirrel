# -*- coding: utf-8 -*-
"""
Scraper pour SAVILLS
"""

import logging
import httpx
import json
from typing import Union
from core.requests_scraper import RequestsScraper
from config.settings import SITEMAPS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class SAVILLSScraper(RequestsScraper):
    """Scraper pour le site SAVILLS qui hérite de la classe RequestsScraper"""

    def __init__(self, ua_generateur, proxy) -> None:
        super().__init__(ua_generateur, proxy, "SAVILLS", SITEMAPS["SAVILLS"])

        self.base_url = "https://search.savills.com"
        self.ua_generateur = ua_generateur
        self.proxy = proxy
        self.api_url = "https://livev6-searchapi.savills.com/Data/SearchByUrl"
        self.property_url = "https://search.savills.com/fr/fr/bien-immobilier-details/"

    def obtenir_sitemap_api(self) -> Union[list[str], list[None]]:
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
                        follow_redirects=True,
                        timeout=REQUEST_TIMEOUT,
                    ) as client:
                        reponse = client.post(self.api_url, data=params_url)
                    reponse.raise_for_status()
                    data = reponse.json()
                    # Extraire et sécuriser le nombre de pages
                    paging_info = (
                        data.get("Results", {}).get("PagingInfo", {}).get("PageCount")
                    )
                    if isinstance(paging_info, int) and paging_info > 0:
                        nb_pages_resultats = paging_info
                    else:
                        logger.warning(
                            f"[{self.name}] Aucune page trouvée pour {actif}"
                        )
                        break  # sortir de la boucle while

                    logger.info(
                        f"[{self.name}] Page {page} / {nb_pages_resultats} pour {actif}"
                    )
                    offres = data.get("Results", {}).get("Properties", [])
                    for offre in offres:
                        contrat = offre.get("SizeDescription", "")
                        contrat_map = {
                            "louer": "Location",
                            "vendre": "Vente",
                        }
                        contrat = next(
                            (
                                label
                                for key, label in contrat_map.items()
                                if key in contrat
                            ),
                            "N/A",
                        )
                        offre_detail = {
                            "confrere": self.name,
                            "url": self.property_url
                            + offre.get("ExternalPropertyIDFormatted", ""),
                            "reference": offre.get("ExternalPropertyIDFormatted", ""),
                            "url_image": offre.get("ImagesGallery")[0].get(
                                "ImageUrl_L", ""
                            ),
                            "actif": (
                                offre.get("PropertyTypes", [{}])[0].get("Caption", "")
                                if isinstance(offre.get("PropertyTypes"), list)
                                and len(offre.get("PropertyTypes")) > 0
                                else ""
                            ),
                            "contrat": contrat,
                            "disponibilite": (
                                offre.get("ByUnit", [{}])[0].get("Disponibilité", "")
                                if isinstance(offre.get("ByUnit"), list)
                                and len(offre.get("ByUnit")) > 0
                                else ""
                            ),
                            "surface": offre.get("SizeFormatted", ""),
                            "adresse": offre.get("AddressLine2", ""),
                            "latitude": offre.get("Latitude", ""),
                            "longitude": offre.get("Longitude", ""),
                            "contact": offre.get("PrimaryAgent", {}).get(
                                "AgentName", ""
                            ),
                            "accroche": offre.get("Description", ""),
                            "amenagements": (
                                offre.get("LongDescription", [{}])[0].get("Body", "")
                                if isinstance(offre.get("LongDescription"), list)
                                and len(offre.get("LongDescription")) > 0
                                else ""
                            ),
                            "prix_global": offre.get("DisplayPriceText", ""),
                        }

                        resultats.append(offre_detail)
                    page += 1

                except Exception as e:
                    logger.error(f"[{self.name}] Erreur page {page}: {e}")
                    return []
        return resultats

    # Obligé d'appeler la méthode ci-dessous car implémentée dans la classe abstraite BaseScraper
    def filtre_urls(self, urls: list[str]) -> list[str]:
        pass
