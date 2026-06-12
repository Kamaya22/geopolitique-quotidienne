# Données de traçabilité des sources

Ce dossier transforme **chaque source citée** dans les éditions en **donnée structurée**,
afin de pouvoir *vérifier* — et non seulement *espérer* — que la couverture reste
pluraliste et diversifiée (pays d'origine, orientation politique, type) au fil du temps.

## Fichiers

| Fichier | Rôle | Écrit par |
|---|---|---|
| `registry.csv` | Registre canonique des sources et de leurs attributs. **C'est le fichier que Kamil audite et corrige.** | Agent (ajouts), Kamil (corrections) |
| `citations/<YYYY-MM-DD>.json` | Toutes les citations d'une édition (1 fichier par édition). | Agent, le jour de l'édition |
| `STATS.md` | Tableaux statistiques **déterministes** régénérés à chaque push. **Ne pas éditer à la main.** | `tools/build_stats.py` (GitHub Action) |

La séparation des rôles est volontaire : l'**agent** (jugement) *extrait et étiquette*,
le **script** (précision) *agrège et compte*. Les chiffres sont donc reproductibles et
vérifiables, indépendamment du modèle.

## `registry.csv` — colonnes

`id,nom,type,pays,orientation,notes`

- **id** — slug `kebab-case` unique, clé de jointure avec les citations (`le-figaro`, `ifri`, `chatham-house`). Ne jamais renommer un `id` existant (cela casserait l'historique).
- **nom** — nom affiché de la source.
- **type** — une valeur parmi :
  - `agence` — agence de presse (AFP, Reuters, AP)
  - `presse` — média / journal / chaîne d'information
  - `revue` — revue d'analyse (ex. Le Grand Continent, Le Monde diplomatique)
  - `think-tank` — institut d'études / groupe de réflexion
  - `institution` — institution officielle, OIG, organisme public, cabinet d'étude (ONU, UE, INSEE, AIE, AIEA…)
  - `media-etat` — média d'État non indépendant (RT, CGTN, Press TV…) — **jamais source factuelle**, uniquement « point de vue officiel » étiqueté
- **pays** — pays d'origine en français (`France`, `États-Unis`, `Royaume-Uni`, `Allemagne`, `Espagne`, `Iran`…). Pour les organisations intergouvernementales (ONU, UE, OTAN, OCDE, FMI, AIE, AIEA…), utiliser **`International`**.
- **orientation** — orientation éditoriale / politique, selon une **taxonomie fixe** :
  - presse / revue : `extreme-gauche` · `gauche` · `centre-gauche` · `centre` · `centre-droit` · `droite` · `droite-souverainiste`
  - agence / institution : `factuel` (réputée neutre / vocation factuelle)
  - think-tank : `liberal` · `droite-liberale` · `centre` · `centre-gauche` · `gauche` · `independant`
  - **`a-verifier`** — valeur spéciale : l'agent était **incertain**. Ces lignes sont **remontées en tête de `STATS.md`** pour que Kamil tranche. Mettre `a-verifier` plutôt que deviner.
- **notes** — justification courte du classement / base méthodologique (optionnel). Contenant des virgules → **entourer de guillemets doubles** dans le CSV.

## Audit (Kamil)

L'étiquetage pays/orientation est **subjectif et faillible**. Le registre est conçu pour être
relu : ouvre `registry.csv` (tableur ou éditeur), corrige une `orientation` ou un `pays` que
tu juges erroné, traite les lignes `a-verifier`, puis pousse. Au prochain push, `STATS.md` se
recalcule avec tes corrections. **Tu gardes le dernier mot.**

## `citations/<date>.json` — schéma

```json
{
  "date": "2026-06-12",
  "sujet_fr": "intitulé court du sujet France",
  "sujet_monde": "intitulé court du sujet Monde",
  "citations": [
    {
      "source_id": "le-grand-continent",
      "sujet": "Monde",
      "emplacement": "pour-aller-plus-loin",
      "role": "analyse",
      "url": "https://...",
      "titre": "Titre de l'article",
      "date_source": "2026-04-08"
    }
  ]
}
```

- **source_id** — doit exister dans `registry.csv` (sinon la citation est comptée mais signalée « hors registre » dans `STATS.md`).
- **sujet** — `FR` ou `Monde`.
- **emplacement** — `pour-aller-plus-loin` (lien formel) ou `texte` (mention dans le corps).
- **role** — `fait` · `analyse` · `opinion`.
- **url / titre / date_source** — `null` si absent (mentions inline sans lien). `date_source` au format `YYYY-MM-DD` ou `YYYY-MM`.

Une même source citée plusieurs fois donne **plusieurs entrées** (chaque mention compte).
