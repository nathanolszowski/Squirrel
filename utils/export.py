# -*- coding: utf-8 -*-
"""
Fonctions d'export des résultats sous format JSON
"""

import json
from datetime import datetime
import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)


def export_json(data: pd.DataFrame, log_dir: str = "exports") -> None:
    """
    Exporte les résultats au format JSON

    Args:
        data (pd.DataFrame): Le DataFrame à exporter.
        output_path (str): Le chemin du fichier de sortie (.json).
    """

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        # Créer le nom du fichier de log avec horodatage
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")
        log_file = os.path.join(log_dir, f"{now}.json")

        data = data.to_dict(orient="records")

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Exportation réussie de {len(data)} résultats")

    except Exception as e:
        logger.error(f"Erreur lors de l'export des données au format JSON: {e}")
