import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def nettoyer_reference(ref: str, pattern: str) -> str:
    if not isinstance(ref, str):
        return ref
    ref = ref.replace(" ", "")
    return re.sub(pattern, "", ref, flags=re.IGNORECASE).strip()


def nettoyer_prix(prix: str) -> str:
    if not isinstance(prix, str):
        return prix
    return prix.replace(" ", "").replace("\n", "").strip()


def nettoyer_disponibilite(val: str) -> str:
    if not isinstance(val, str):
        return val
    val = val.replace(" ", "").replace("\n", "")
    return re.sub(r"(?i)^Disponibilité\s*:\s*", "", val).strip()


def appliquer_nettoyage_specifique(df: pd.DataFrame) -> pd.DataFrame:
    def nettoyer_ligne(row):
        logger.info("Lancement du nettoyage du dictionnaire d'offres")
        confrere = row["confrere"]

        if confrere == "BNP":
            row["reference"] = nettoyer_reference(
                row.get("reference", ""), r"^Référence\s*:\s*"
            )

        elif confrere == "CBRE":
            row["reference"] = nettoyer_reference(
                row.get("reference", ""), r"^Offre\s*"
            )

        elif confrere == "CUSHMAN":
            row["reference"] = nettoyer_reference(
                row.get("reference", ""), r"^Réf\s*:\s*"
            )
            row["prix_global"] = nettoyer_prix(row.get("prix_global", ""))

        elif confrere == "KNIGHTFRANK":
            row["disponibilite"] = nettoyer_disponibilite(row.get("disponibilite", ""))
            row["prix_global"] = re.sub(
                r"(?i)^(loyer|prix)\s*:\s*",
                "",
                nettoyer_prix(row.get("prix_global", "")),
            )

        elif confrere == "SAVILLS":
            row["surface"] = row.get("surface", "").replace("sq feet", "m²")

        elif confrere == "ARTHURLOYD":
            row["prix_global"] = re.sub(
                r"(?i)^(loyer|prix)\s*:\s*",
                "",
                nettoyer_prix(row.get("prix_global", "")),
            )

        return row

    return df.apply(nettoyer_ligne, axis=1)
