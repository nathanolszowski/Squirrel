# -*- coding: utf-8 -*-
"""
Point d'entrée principal du scraper
"""

import logging
#from scrapers.bnp import BNPScraper
#from scrapers.jll import JLLScraper
#from scrapers.cbre import CBREScraper
#from scrapers.alexbolton import ALEXBOLTONScraper
from scrapers.cushman import CUSHMANScraper
from utils.export import export_json
from utils.logging_config import setup_logging

def main():
    """Fonction principale"""
    
    # Configuration du logging avec fichier horodaté
    log_file = setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Démarrage du programme de scraping. Les logs seront conservés dans ce fichier: {log_file}")
    
    # Liste des scrapers à exécuter
    scrapers = [
        #BNPScraper(),
        #JLLScraper(),
        #CBREScraper(),
        #ALEXBOLTONScraper()
        CUSHMANScraper()
        # Ajouter les autres scrapers ici
    ]
    
    all_results = []
    
    # Exécution des scrapers
    for scraper in scrapers:
        try:
            logger.info(f"Démarrage du scraper {scraper.name.upper()} ...")
            results = scraper.run()
            
            if results:
                all_results.extend(results)
                logger.info(f"Récupération de {len(results)} résultats pour le scraper {scraper.name}")
                
        except Exception as e:
            logger.error(f"Erreur de lancement pour {scraper.name} : {e}")
            
    if all_results :
        export_json(all_results)
        
    logger.info("Le programme de scraping est terminé")

if __name__ == "__main__":
    main()
