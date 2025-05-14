# -*- coding: utf-8 -*-
"""
Fonctions pour gérer les user_agents
"""

import random
from functools import cached_property
from typing import List
from time import time
from ua_parser import user_agent_parser
import logging

logger = logging.getLogger(__name__)

class UserAgent:
    """Classe de base pour tous les user-agents"""
   
    def __init__(self, user_agent: str) -> None:
        """
        Initialise un nouvel user-agent
        
        Args:
            user-agent (str): Châine de caractère représentant un Nom d'user-agent, par exemple : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        """
        self.string: str = user_agent
        # Parse la string user-agent
        self.parsed_string: str = user_agent_parser.Parse(user_agent)
        self.last_used: int = time()

    # Récupère le nom du browser
    @cached_property
    def browser(self) -> str:
        return self.parsed_string["user_agent"]["family"]

    # Récupère la version du browser
    @cached_property
    def browser_version(self) -> int:
        return int(self.parsed_string["user_agent"]["major"])

    # Récupére le système d'exploitation
    @cached_property
    def os(self) -> str:
        return self.parsed_string["os"]["family"]

    # Retourne la valeur string de l'user-agent actuel
    def __str__(self) -> str:
        return self.string
    
class Rotator:
    """Classe de base pour tous le générateur d'user-agent"""
    
    def __init__(self, user_agents: List[UserAgent]) -> None:
        """
        Initialise un nouveau générateur d'user-agent
        
        Args:
            user-agents (list[str]): Liste de chaînes représentant des user-agents, par exemple : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        """
        # Add User-Agent strings to the UserAgent container
        logger.info("Initialisation du sélecteur d'user-agent")
        self.user_agents = [UserAgent(ua) for ua in user_agents]
        
    # Add weight for each User-Agent
    def weigh_user_agent(self, user_agent: UserAgent) -> int:
        """
        Notation d'un user-agent selon ses caractéristiques
        
        Args:
            user_agent (UserAgent): Objet représentant un user-agent
        Returns:
            (int): Notation de l'user-agent en cours d'analyse
        """
        weight = 1000

        # Add higher weight for less used User-Agents
        if user_agent.last_used:
            _seconds_since_last_use = time() - user_agent.last_used
            weight += _seconds_since_last_use

        # Add higher weight based on the browser
        if user_agent.browser == "Chrome":
            weight += 100
        if user_agent.browser == "Firefox" or "Edge":
            weight += 50
        if user_agent.browser == "Chrome Mobile" or "Firefox Mobile":
            weight += 0

        # Add higher weight for higher browser versions
        if user_agent.browser_version:
            weight += user_agent.browser_version * 10

        # Add higher weight based on the OS type
        if user_agent.os == "Windows":
            weight += 150
        if user_agent.os == "Mac OS X":
            weight += 100
        if user_agent.os in ["Linux", "Ubuntu"]:
            weight -= 50
        if user_agent.os == "Android":
            weight -= 100
        return weight

    def get(self)-> str:
        """
        Retourne un user-agent qui aura été choisi selon sa notation et sa dernière date d'utilisation

        Returns:
            (str): Retourne un user-agent qui aura été choisi selon sa notation et sa dernière date d'utilisation
        """
        # Note tous les user-agents
        logger.info("Récupération d'un user_agent")
        user_agent_weights = []
        for user_agent in self.user_agents :
            user_agent_weights.append(self.weigh_user_agent(user_agent))
        logger.info("Les user-agents ont été notés")

        # Sélectionne un user-agent
        user_agent = random.choices(
            self.user_agents,
            weights=user_agent_weights,
            k=1,
        )[0]

        # Met à jour l'attribut de dernière utilisation
        user_agent.last_used = time()
        logger.info(f"Un nouvel user_agent a été sélectionné {user_agent}")
        return str(user_agent)