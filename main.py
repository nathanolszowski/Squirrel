# -*- coding: utf-8 -*-
"""
Point d'entrée principal du scraper
"""

import logging
from datetime import datetime
import pandas as pd

# from scrapers.jll import JLLScraper /!/ En panne - Ne pas utiliser /!/
from scrapers.bnp import BNPScraper
from scrapers.cbre import CBREScraper
from scrapers.alexbolton import ALEXBOLTONScraper
from scrapers.cushman import CUSHMANScraper
from scrapers.arthurloyd import ARTHURLOYDScraper
from scrapers.savills import SAVILLSScraper
from scrapers.knightfrank import KNIGHTFRANKScraper


from utils.export import export_json
from utils.logging_config import setup_logging
from utils.user_agent import Rotator, ListUserAgent
from config.settings import PROXY
from utils.data_pipeline import appliquer_nettoyage_specifique


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

    ua_liste = ListUserAgent(PROXY)
    ua_generateur = Rotator(ua_liste.obtenir_liste())

    # Liste des scrapers à exécuter
    scrapers = [
        BNPScraper(ua_generateur, PROXY),
        # JLLScraper(ua_generateur, PROXY) /!/ En panne - Ne pas utiliser /!/
        # CBREScraper(ua_generateur, PROXY),
        # ALEXBOLTONScraper(ua_generateur, PROXY),
        CUSHMANScraper(ua_generateur, PROXY),
        # KNIGHTFRANKScraper(ua_generateur, PROXY),
        # ARTHURLOYDScraper(ua_generateur, PROXY),
        # SAVILLSScraper(ua_generateur, PROXY)
        # Ajouter les autres scrapers ici
    ]

    all_resultats = []

    # Exécution des scrapers
    debut_chrono = datetime.now()
    logger.info(f"Le programme a démarré à {debut_chrono}")
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
        dataFrame = pd.DataFrame(all_resultats)
        logger.info("Lancement du nettoyage du dictionnaire d'offres")
        dataFrame = appliquer_nettoyage_specifique(dataFrame)
        export_json(dataFrame)

    logger.info("Le programme de scraping est terminé")
    fin_chrono = datetime.now()
    chrono = fin_chrono - debut_chrono
    logger.info(
        f"Le programme a terminé à {fin_chrono}. Le programme s'est executé en {chrono}"
    )


if __name__ == "__main__":
    main()
