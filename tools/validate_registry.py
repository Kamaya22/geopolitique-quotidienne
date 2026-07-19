#!/usr/bin/env python3
"""Valide la structure de data/registry.csv avant l'agrégation des stats.

Attrape en particulier la cause de l'échec CI historique : une virgule non
échappée dans une cellule (ex. un champ `notes` non entouré de guillemets) qui
crée une colonne surnuméraire. csv.DictReader range alors ces champs en trop
dans une liste, et build_stats.py plantait avec :
    AttributeError: 'list' object has no attribute 'strip'

Bibliothèque standard uniquement — aucune dépendance pip.
Usage : python tools/validate_registry.py   (exit 0 = OK, exit 1 = erreurs)
"""

import csv
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(REPO_ROOT, "data", "registry.csv")

# Schéma attendu (ordre et intitulés exacts de l'en-tête).
EXPECTED_HEADER = ["id", "nom", "type", "pays", "orientation", "notes"]
# Colonnes qui ne doivent jamais être vides.
REQUIRED_FIELDS = ["id", "nom"]


def validate(path=REGISTRY):
    """Retourne la liste des erreurs (chaînes lisibles). Vide = fichier valide."""
    errors = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))

    if not rows:
        return [f"{path} est vide (aucune ligne)."]

    header = rows[0]
    if header != EXPECTED_HEADER:
        errors.append(
            f"En-tête inattendu : {header} ; attendu {EXPECTED_HEADER}."
        )
        # En-tête cassé : le reste des contrôles n'aurait pas de sens.
        return errors

    ncols = len(EXPECTED_HEADER)
    seen_ids = {}
    for lineno, row in enumerate(rows[1:], start=2):
        # Ligne totalement vide -> tolérée (csv l'ignore de toute façon).
        if not row:
            continue
        if len(row) != ncols:
            errors.append(
                f"Ligne {lineno} : {len(row)} champs au lieu de {ncols} "
                f"(virgule non échappée ? entourez la cellule de guillemets) : {row}"
            )
            continue
        record = dict(zip(EXPECTED_HEADER, row))
        for field in REQUIRED_FIELDS:
            if not record[field].strip():
                errors.append(f"Ligne {lineno} : champ « {field} » vide.")
        sid = record["id"].strip()
        if sid:
            if sid in seen_ids:
                errors.append(
                    f"Ligne {lineno} : id « {sid} » déjà défini ligne {seen_ids[sid]}."
                )
            else:
                seen_ids[sid] = lineno
    return errors


def main():
    errors = validate()
    if errors:
        print(f"registry.csv invalide ({len(errors)} erreur(s)) :", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    print("registry.csv valide.")


if __name__ == "__main__":
    main()
