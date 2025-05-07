# -*- coding: utf-8 -*-
"""
Fonctions pour générer la lsite d'user-agents disponibles
"""
from bs4 import BeautifulSoup
import httpx
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def url_actualise_user_agents ():
    """ Récupère la liste des user-agents à jour et disponible via useragents.io"""
    logger.info("Initialisation de la liste d'user-agents")
    url = "https://useragents.io/sitemaps/useragents.xml"
    request = httpx.get(url, timeout=5)
    soup = BeautifulSoup(request.text, "xml")
    derniere_url_actualise = soup.find_all("sitemap")[-1]
    derniere_url_actualise = derniere_url_actualise.find("loc").text
    return derniere_url_actualise
    
def lister_user_agent (url_actuelle_agents):
    """ Récupère les user_agents string depuis la dernière liste actuelle"""
    liste_agents = httpx.get(url_actuelle_agents)
    sitemap_actuelle_recherche = BeautifulSoup(liste_agents.text, "xml")
    user_agents_liens = [url.find("loc").text for url in sitemap_actuelle_recherche.find_all("url")]
    user_agents=[]
    for url in user_agents_liens :
        response = httpx.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        user_agents.append(soup.select_one("body > div:nth-child(1) > main > h1").get_text())
    logger.info(f"Trouvé {len(user_agents)} user-agents à jour disponibles pour le scraping")
    return user_agents

def verifier_user_agents ():
    derniere_url_actuelle = url_actualise_user_agents ()
    try:
        liste_user_agent = []

        # Vérifie si le cache existe
        if os.path.exists("user_agent.json"):
            with open("user_agent.json", "r", encoding="utf-8") as f:
                contenu = json.load(f)
                url_fichier = next(iter(contenu), None)

                # Si l'URL est la même que celle du sitemap actuel, on utilise le cache
                if url_fichier == derniere_url_actuelle:
                    liste_user_agent = contenu[url_fichier]
                else:
                    # Sinon, on met à jour
                    liste_user_agent = lister_user_agent(derniere_url_actuelle)
                    contenu_actualise = {derniere_url_actuelle: liste_user_agent}
                    with open("user_agent.json", "w", encoding="utf-8") as f:
                        json.dump(contenu_actualise, f, ensure_ascii=False, indent=4)
        else:
            # Fichier JSON inexistant : on récupère et on enregistre
            liste_user_agent = lister_user_agent(derniere_url_actuelle)
            contenu_actualise = {derniere_url_actuelle: liste_user_agent}
            with open("user_agent.json", "w", encoding="utf-8") as f:
                json.dump(contenu_actualise, f, ensure_ascii=False, indent=4)

    except Exception as e:
        logger.error(f"Erreur pendant la vérification du cache des user-agents: {e}")
        raise
    return liste_user_agent