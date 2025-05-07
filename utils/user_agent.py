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
   
    def __init__(self, string) -> None:
        self.string: str = string
        # Parse the User-Agent string
        self.parsed_string: str = user_agent_parser.Parse(string)
        self.last_used: int = time()

    # Get the browser name
    @cached_property
    def browser(self) -> str:
        return self.parsed_string["user_agent"]["family"]

    # Get the browser version
    @cached_property
    def browser_version(self) -> int:
        return int(self.parsed_string["user_agent"]["major"])

    # Get the operation system
    @cached_property
    def os(self) -> str:
        return self.parsed_string["os"]["family"]

    # Return the actual user agent string
    def __str__(self) -> str:
        return self.string
    
class Rotator:
    
    def __init__(self, user_agents: List[UserAgent]):
        # Add User-Agent strings to the UserAgent container
        self.user_agents = [UserAgent(ua) for ua in user_agents]

    # Add weight for each User-Agent
    def weigh_user_agent(self, user_agent: UserAgent):
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

    def get(self):
        # Weigh all User-Agents
        logger.info("Récupération d'un user_agent")
        user_agent_weights = []
        for user_agent in self.user_agents :
            user_agent_weights.append(self.weigh_user_agent(user_agent))
        print("Tous les users on été pesés")

        # Select a random User-Agent
        user_agent = random.choices(
            self.user_agents,
            weights=user_agent_weights,
            k=1,
        )[0]
        print(f"{user_agent} a été trouvé")
        # Update the last used time when selecting a User-Agent
        user_agent.last_used = time()
        logger.info("Un nouvel user_agent a été sélectionné")
        return str(user_agent)