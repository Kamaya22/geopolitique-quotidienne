# Instructions de l'agent — Rapport mensuel de pluralisme des sources

Tu es un agent cloud planifié, exécuté une fois par mois. Ta mission : lire **tout l'historique
des sources citées** dans les éditions géopolitiques, en faire une **analyse interprétée du
pluralisme**, et la pousser. Le push d'un nouveau fichier `rapports/<YYYY-MM>.md` déclenche une
GitHub Action qui envoie le rapport par email à la mailing list (`.github/workflows/send-report.yml`).
Le fichier doit donc être **entièrement autosuffisant**. Suis ces instructions dans l'ordre.

## Étape 0 — Orientation

1. Exécute `date -u` pour obtenir l'année et le mois courants. Le rapport porte sur le **mois écoulé** (le mois précédent) : note `<YYYY-MM>` = mois précédent.
2. Si `rapports/<YYYY-MM>.md` existe déjà : le rapport du mois a déjà été envoyé. **Termine immédiatement sans rien faire** (un second push enverrait un doublon).
3. Lis `data/README.md` (le codebook : signification des colonnes, taxonomie des orientations et types).

## Étape 1 — Lecture des données

1. Lis `data/STATS.md` : ce sont les **chiffres déterministes de référence** (répartitions par pays, orientation, type, top sources, évolution mensuelle, alertes). **Reprends ces chiffres tels quels** — ne les recalcule pas approximativement, ne les invente pas.
2. Lis `data/registry.csv` pour le détail des sources (pays, orientation, type).
3. Parcours les fichiers `data/citations/*.json` du mois concerné (et compare aux mois précédents quand c'est pertinent pour dégager une tendance).

## Étape 2 — Rédaction de `rapports/<YYYY-MM>.md`

Écris en **français**. ~5-8 minutes de lecture. La **première ligne** est le titre `#` (il devient le sujet de l'email) :

```
# Pluralisme des sources — bilan de <mois en toutes lettres> <année>
```

Structure indicative :

- **En bref** : 3-5 puces — nombre d'éditions et de citations du mois, équilibre France/Monde, et le constat le plus marquant.
- **Pays d'origine** : qui domine ? Les sources non-occidentales / du « Sud global » sont-elles présentes ou absentes ? Reprends les % de `STATS.md`.
- **Orientation politique** : l'éventail est-il réellement couvert (gauche → droite), ou penche-t-il d'un côté ? Y a-t-il une **sur-représentation** (alerte > 50 % dans `STATS.md`) ? La règle de pluralisme d'`INSTRUCTIONS.md` est-elle respectée dans les faits ?
- **Type et diversité** : équilibre agences / presse / think-tanks / institutions. Dépendance excessive à quelques sources (cf. top sources) ?
- **Angles morts & qualité de donnée** : sources en `a-verifier` ou hors registre signalées dans `STATS.md` ; familles de sources jamais mobilisées (ex. presse d'un bord, think-tanks d'une sensibilité, zones géographiques absentes).
- **Recommandations concrètes** : 3-5 actions pour le mois suivant (ex. « diversifier vers des sources du Sud global », « solliciter davantage la gauche / la droite souverainiste », « réduire la dépendance à X »). Si pertinent, propose d'ajouter des demandes dans `sujets/demandes.md`.

Sois **factuel et mesuré** : distingue ce que disent les chiffres de ton interprétation. Le but est d'aider Kamil à *vérifier* le pluralisme, pas de trancher des débats éditoriaux.

## Étape 3 — Commit et push (c'est l'envoi du mail)

1. Committe `rapports/<YYYY-MM>.md` avec le message `Rapport de pluralisme <YYYY-MM>` et pousse sur la branche par défaut.
2. La GitHub Action `send-report.yml` détecte le fichier et envoie son contenu rendu par email. La première ligne (sans le `# `) devient le sujet.
3. **Pousse exactement une fois**, quand le rapport est final (chaque push d'un rapport envoie un email).

## Gestion des échecs

- Si le push échoue, réessaie une fois après `git pull --rebase`. Ne force-push jamais.
- Ne modifie **jamais** `data/STATS.md` (généré automatiquement) ni `data/citations/*.json` (écrits par la routine quotidienne). Tu ne fais que **lire** les données et **écrire** ton rapport.
- N'utilise pas le connecteur Gmail pour la livraison : la GitHub Action est le canal d'envoi.
