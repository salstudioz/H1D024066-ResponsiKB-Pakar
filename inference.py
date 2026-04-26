"""
Mesin Inferensi – Forward Chaining
"""
import logging
from knowledge_base import RULES

logger = logging.getLogger(__name__)


def forward_chaining(selected_symptoms: list) -> list:
    """
    Jalankan inferensi forward chaining.

    Parameters
    ----------
    selected_symptoms : list[str]
        Daftar gejala yang dipilih pengguna.

    Returns
    -------
    list[dict]
        Daftar hasil: [{"rule_id", "diagnosis", "saran"}, ...]
    """
    if not selected_symptoms:
        return []

    facts = set(selected_symptoms)
    results = []
    fired_rules = set()

    changed = True
    iteration = 0

    while changed:
        changed = False
        iteration += 1
        logger.debug(f"Forward chaining iteration {iteration}, facts={facts}")

        for rule in RULES:
            if rule["id"] in fired_rules:
                continue

            conditions = set(rule["conditions"])
            if conditions.issubset(facts):
                fired_rules.add(rule["id"])
                changed = True
                results.append({
                    "rule_id":   rule["id"],
                    "diagnosis": rule["conclusion"]["diagnosis"],
                    "saran":     rule["conclusion"]["saran"],
                })
                logger.info(f"Rule {rule['id']} fired: {rule['conclusion']['diagnosis']}")

    if not results:
        logger.info(f"No rules fired for symptoms: {selected_symptoms}")

    return results
