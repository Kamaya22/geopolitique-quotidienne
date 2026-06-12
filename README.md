# Géopolitique quotidienne — 15 minutes par jour

Automatisation personnelle : chaque jour à ~7h00 (Europe/Paris), un agent Claude planifié dans le cloud produit une lecture d'environ 15 minutes sur la géopolitique liée à l'actualité — **moitié sur un sujet France, moitié sur un sujet Monde** — et l'envoie par email à la mailing list. Sources exclusivement issues du journalisme de référence et d'instituts d'études géopolitiques sérieux, avec une règle stricte de **pluralisme** : chaque sujet présente plusieurs points de vue et bords politiques, nommés et étiquetés.

## Fonctionnement

- **Routine cloud Claude** : s'exécute tous les jours (cron `0 5 * * *` UTC ≈ 7h00 Paris). Elle clone ce repo, lit `INSTRUCTIONS.md` et le suit intégralement.
- **Chaque jour** : l'agent choisit un sujet France et un sujet Monde dans l'actualité récente (en évitant les répétitions grâce à `sujets/history.md`), rédige l'édition (`editions/<YYYY-MM-DD>.md`) et la pousse sur GitHub.
- **Envoi de l'email** : la GitHub Action `.github/workflows/send-reading.yml` détecte chaque nouvelle édition poussée et l'envoie par email (SMTP Gmail) au destinataire défini par la variable de repo `MAIL_TO` (la mailing list ; à défaut, kamilmahmal22@gmail.com). Secrets requis dans le repo : `MAIL_USERNAME` (adresse Gmail) et `MAIL_APP_PASSWORD` (mot de passe d'application Google, créé sur https://myaccount.google.com/apppasswords). Le connecteur Gmail de claude.ai ne sait que créer des brouillons : il n'est pas utilisé pour la livraison.

## Mailing list

Les éditions sont envoyées au Google Group **geopolitique-quotidienne@googlegroups.com**. S'abonner / se désabonner : https://groups.google.com/g/geopolitique-quotidienne (chaque mail du groupe contient aussi un lien de désabonnement). Pour changer de destinataire, modifier la variable `MAIL_TO` du repo (Settings → Secrets and variables → Actions → Variables) — aucun commit nécessaire.

## Traçabilité et statistiques des sources

Pour pouvoir **vérifier** (et pas seulement espérer) que la couverture reste pluraliste dans la durée, chaque source citée est enregistrée comme donnée structurée dans `data/` :

- **`data/registry.csv`** — registre canonique des sources, étiquetées par **pays**, **orientation politique** et **type**. C'est le fichier que tu **audites et corriges** : ouvre-le, rectifie un classement erroné, traite les lignes marquées `a-verifier`, puis pousse. Voir `data/README.md` pour la taxonomie complète. **Tu gardes le dernier mot sur l'étiquetage.**
- **`data/citations/<date>.json`** — toutes les sources citées par une édition (liens « Pour aller plus loin » **et** mentions dans le texte), écrites par l'agent le jour même.
- **`data/STATS.md`** — tableaux statistiques **déterministes** (par pays, orientation, type, top sources, évolution mensuelle, alertes de concentration), régénérés automatiquement à chaque push par la GitHub Action `build-stats.yml`. Fichier généré : ne pas l'éditer à la main.
- **Rapport mensuel** : une routine cloud mensuelle (instructions dans `RAPPORT_MENSUEL.md`) lit ces données et envoie par email une **analyse interprétée du pluralisme** (`rapports/<YYYY-MM>.md`, envoyé via `send-report.yml`).

## Comment piloter

- **Demander un sujet précis** : éditer `sujets/demandes.md` (depuis GitHub web, l'app mobile GitHub, ou ce dossier local). L'agent traite la demande en priorité dans la prochaine édition, puis l'efface.
- **Ajuster le format, la durée, les sources** : éditer `INSTRUCTIONS.md` — la routine relit ce fichier à chaque exécution, aucun changement de la routine elle-même n'est nécessaire.
- **Auditer / corriger l'étiquetage des sources** : éditer `data/registry.csv` (pays, orientation, type) — `STATS.md` se recalcule au prochain push.
- **Renvoyer la dernière édition** : lancer manuellement le workflow `Send daily geopolitics reading by email` (onglet Actions → Run workflow).

## Structure

```
INSTRUCTIONS.md          — instructions de l'agent quotidien (format, sources, pluralisme, traçabilité)
RAPPORT_MENSUEL.md       — instructions de la routine mensuelle (rapport de pluralisme)
sujets/demandes.md       — demandes de sujets pour les prochaines éditions (éditable à tout moment)
sujets/history.md        — sujets déjà traités (anti-répétition)
editions/<date>.md       — archive des éditions quotidiennes
data/README.md           — codebook : colonnes du registre et taxonomie des sources
data/registry.csv        — registre canonique des sources (auditable)
data/citations/<date>.json — sources citées par chaque édition
data/STATS.md            — statistiques déterministes (généré automatiquement)
rapports/<YYYY-MM>.md    — rapports mensuels de pluralisme
tools/build_stats.py     — génère data/STATS.md à partir des citations + registre
```

## Gestion des routines

Les routines se gèrent sur https://claude.ai/code/routines (activer/désactiver, supprimer, voir les exécutions) :
- **Quotidienne** (`INSTRUCTIONS.md`) : produit l'édition du jour.
- **Mensuelle** (`RAPPORT_MENSUEL.md`, cron `0 6 1 * *` ≈ 8h Paris le 1er du mois) : produit le rapport de pluralisme. À créer sur la même base que la routine quotidienne (même PAT GitHub fine-grained), en pointant l'agent vers `RAPPORT_MENSUEL.md`.
