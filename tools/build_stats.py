#!/usr/bin/env python3
"""Agrège les citations des éditions et le registre des sources en statistiques
déterministes, écrites dans data/STATS.md.

Bibliothèque standard uniquement — aucune dépendance pip.
Usage : python tools/build_stats.py

Le calcul est exposé via `compute_stats()` pour être réutilisé (ex. aperçu HTML
par tools/preview_stats.py) sans dupliquer la logique.
"""

import csv
import glob
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone

# --- Seuils d'alerte (documentés) -----------------------------------------
SEUIL_ORIENTATION = 50.0  # % : une orientation au-delà = concentration signalée
SEUIL_PAYS = 60.0         # % : un pays au-delà = concentration signalée
TOP_SOURCES = 15          # nombre de sources affichées dans le classement

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
REGISTRY = os.path.join(DATA_DIR, "registry.csv")
CITATIONS_GLOB = os.path.join(DATA_DIR, "citations", "*.json")
OUT = os.path.join(DATA_DIR, "STATS.md")


def load_registry():
    reg = {}
    with open(REGISTRY, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            sid = (row.get("id") or "").strip()
            if sid:
                reg[sid] = {k: (v or "").strip() for k, v in row.items()}
    return reg


def load_citations():
    editions = []
    for path in sorted(glob.glob(CITATIONS_GLOB)):
        with open(path, encoding="utf-8") as f:
            editions.append(json.load(f))
    return editions


def pct(n, total):
    return (100.0 * n / total) if total else 0.0


def compute_stats(reg, editions):
    """Retourne un dict de compteurs/agrégats — source unique de vérité."""
    total = 0
    par_pays = Counter()
    par_orientation = Counter()
    par_type = Counter()
    par_sujet = Counter()
    par_emplacement = Counter()
    par_role = Counter()
    par_source = Counter()           # (source_id, nom) -> nb citations
    par_mois = defaultdict(Counter)  # mois -> Counter
    mois_editions = defaultdict(int)
    mois_pays = defaultdict(set)
    mois_orient = defaultdict(set)
    hors_registre = Counter()
    a_verifier = set()
    dates = []

    for ed in editions:
        date = ed.get("date", "")
        dates.append(date)
        mois = date[:7]
        mois_editions[mois] += 1
        for c in ed.get("citations", []):
            total += 1
            sid = c.get("source_id", "")
            meta = reg.get(sid)
            if meta is None:
                hors_registre[sid] += 1
                pays = orient = typ = "(hors registre)"
                nom = sid
            else:
                pays = meta.get("pays", "")
                orient = meta.get("orientation", "")
                typ = meta.get("type", "")
                nom = meta.get("nom", sid)
                if orient == "a-verifier":
                    a_verifier.add(sid)
            par_pays[pays] += 1
            par_orientation[orient] += 1
            par_type[typ] += 1
            par_sujet[c.get("sujet", "?")] += 1
            par_emplacement[c.get("emplacement", "?")] += 1
            par_role[c.get("role", "?")] += 1
            par_source[(sid, nom)] += 1
            par_mois[mois]["citations"] += 1
            mois_pays[mois].add(pays)
            mois_orient[mois].add(orient)

    dates = [d for d in dates if d]
    return {
        "total": total,
        "par_pays": par_pays,
        "par_orientation": par_orientation,
        "par_type": par_type,
        "par_sujet": par_sujet,
        "par_emplacement": par_emplacement,
        "par_role": par_role,
        "par_source": par_source,
        "par_mois": par_mois,
        "mois_editions": mois_editions,
        "mois_pays": mois_pays,
        "mois_orient": mois_orient,
        "hors_registre": hors_registre,
        "a_verifier": a_verifier,
        "reg": reg,
        "n_editions": len(editions),
        "dates": dates,
        "periode": f"{min(dates)} → {max(dates)}" if dates else "—",
    }


def alertes_list(s):
    """Liste des alertes (qualité + concentration), réutilisable."""
    total, reg = s["total"], s["reg"]
    out = []
    for sid, n in s["hors_registre"].items():
        out.append(f"⚠️ Source hors registre : `{sid}` ({n} citation(s)) — ajouter une ligne dans registry.csv.")
    for sid in sorted(s["a_verifier"]):
        nom = reg.get(sid, {}).get("nom", sid)
        out.append(f"🔎 Orientation à vérifier : {nom} (`{sid}`) — à trancher dans registry.csv.")
    for orient, n in s["par_orientation"].most_common():
        p = pct(n, total)
        if orient not in ("factuel", "a-verifier", "(hors registre)") and p > SEUIL_ORIENTATION:
            out.append(f"📊 Concentration d'orientation : `{orient}` = {p:.1f} % (seuil {SEUIL_ORIENTATION:.0f} %).")
    for pays, n in s["par_pays"].most_common():
        p = pct(n, total)
        if pays not in ("(hors registre)", "International") and p > SEUIL_PAYS:
            out.append(f"🌍 Concentration géographique : `{pays}` = {p:.1f} % (seuil {SEUIL_PAYS:.0f} %).")
    return out


def _bar(p):
    return "█" * int(round(p / 5.0))  # 1 bloc ≈ 5 %


def _table(title, counter, total):
    lines = [f"### {title}", "", "| Valeur | Citations | Part | |", "|---|---:|---:|---|"]
    for value, n in counter.most_common():
        p = pct(n, total)
        lines.append(f"| {value or '—'} | {n} | {p:.1f} % | {_bar(p)} |")
    lines.append("")
    return "\n".join(lines)


def render_markdown(s):
    total = s["total"]
    genere = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = []
    out.append("# Statistiques des sources citées")
    out.append("")
    out.append(f"*Fichier généré automatiquement par `tools/build_stats.py` — ne pas éditer à la main. Dernière génération : {genere}.*")
    out.append("")
    out.append("## Résumé")
    out.append("")
    out.append(f"- **Période couverte** : {s['periode']}")
    out.append(f"- **Éditions analysées** : {s['n_editions']}")
    out.append(f"- **Citations totales** : {total}")
    out.append(f"- **Sources distinctes citées** : {len({sid for (sid, _) in s['par_source']})}")
    out.append(f"- **Pays distincts** : {len(s['par_pays'])}")
    out.append(f"- **Orientations distinctes** : {len(s['par_orientation'])}")
    out.append("")
    out.append("## Alertes")
    out.append("")
    al = alertes_list(s)
    if al:
        out.extend(f"- {a}" for a in al)
    else:
        out.append("Aucune alerte : pas de source hors registre, pas d'orientation `a-verifier`, pas de concentration au-delà des seuils.")
    out.append("")
    out.append(f"*Seuils : orientation > {SEUIL_ORIENTATION:.0f} %, pays unique > {SEUIL_PAYS:.0f} % (hors `International`). « factuel » est exclu du calcul de concentration politique.*")
    out.append("")
    out.append("## Répartitions")
    out.append("")
    out.append(_table("Par pays d'origine", s["par_pays"], total))
    out.append(_table("Par orientation politique", s["par_orientation"], total))
    out.append(_table("Par type de source", s["par_type"], total))
    out.append(_table("Par sujet (France / Monde)", s["par_sujet"], total))
    out.append(_table("Par emplacement (lien formel / mention)", s["par_emplacement"], total))
    out.append(_table("Par rôle (fait / analyse / opinion)", s["par_role"], total))
    out.append(f"## Sources les plus citées (top {TOP_SOURCES})")
    out.append("")
    out.append("| Source | Citations | Part |")
    out.append("|---|---:|---:|")
    for (sid, nom), n in s["par_source"].most_common(TOP_SOURCES):
        out.append(f"| {nom} | {n} | {pct(n, total):.1f} % |")
    out.append("")
    out.append("## Évolution mensuelle")
    out.append("")
    out.append("| Mois | Éditions | Citations | Pays distincts | Orientations distinctes |")
    out.append("|---|---:|---:|---:|---:|")
    for mois in sorted(s["par_mois"]):
        out.append(f"| {mois} | {s['mois_editions'][mois]} | {s['par_mois'][mois]['citations']} | {len(s['mois_pays'][mois])} | {len(s['mois_orient'][mois])} |")
    out.append("")
    return "\n".join(out)


def main():
    s = compute_stats(load_registry(), load_citations())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(render_markdown(s))
    print(f"STATS.md genere : {s['total']} citations, {s['n_editions']} edition(s) -> {OUT}")


if __name__ == "__main__":
    main()
