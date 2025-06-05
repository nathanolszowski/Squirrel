# -*- coding: utf-8 -*-
"""
Point d'entrée principal du scraper
"""

import logging

# from scrapers.bnp import BNPScraper
from scrapers.jll import JLLScraper

# from scrapers.cbre import CBREScraper
# from scrapers.alexbolton import ALEXBOLTONScraper
# from scrapers.cushman import CUSHMANScraper
# from scrapers.arthurloyd import ARTHURLOYDScraper
# from scrapers.savills import SAVILLSScraper
# from scrapers.knightfrank import KNIGHTFRANKScraper


from utils.export import export_json
from utils.logging_config import setup_logging
from utils.user_agent import Rotator, ListUserAgent


def main():
    """Fonction principale"""

    # Configuration du logging avec fichier horodaté
    log_file = setup_logging()
    logger = logging.getLogger(__name__)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("seleniumwire").setLevel(logging.WARNING)
    logger.info(
        f"Démarrage du programme de scraping. Les logs seront conservés dans ce fichier: {log_file}"
    )

    PROXY = ""

    ua_liste = ListUserAgent(PROXY)
    ua_generateur = Rotator(ua_liste.obtenir_liste())

    # Liste des scrapers à exécuter
    scrapers = [
        # BNPScraper(ua_generateur, PROXY),
        JLLScraper(ua_generateur, PROXY)
        # CBREScraper(ua_generateur, PROXY),
        # ALEXBOLTONScraper(ua_generateur, PROXY),
        # CUSHMANScraper(ua_generateur, PROXY),
        # KNIGHTFRANKScraper(ua_generateur, PROXY),
        # ARTHURLOYDScraper(ua_generateur, PROXY),
        # SAVILLSScraper(ua_generateur, PROXY)
        # Ajouter les autres scrapers ici
    ]

    all_resultats = []

    # Exécution des scrapers
    for scraper in scrapers:
        try:
            logger.info(f"Démarrage du scraper {scraper.name.upper()} ...")
            resultats = scraper.run()

            if resultats:
                all_resultats.extend(resultats)
                logger.info(
                    f"Récupération de {len(resultats)} résultats pour le scraper {scraper.name}"
                )

        except Exception as e:
            logger.error(f"Erreur de lancement pour {scraper.name} : {e}")

    if all_resultats:
        export_json(all_resultats)

    logger.info("Le programme de scraping est terminé")


if __name__ == "__main__":
    main()
