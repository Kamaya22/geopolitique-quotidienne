# Géopolitique quotidienne — 15 minutes par jour

Automatisation personnelle : chaque jour à ~7h00 (Europe/Paris), un agent Claude planifié dans le cloud produit une lecture d'environ 15 minutes sur la géopolitique liée à l'actualité — **moitié sur un sujet France, moitié sur un sujet Monde** — et l'envoie par email à kamilmahmal22@gmail.com. Sources exclusivement issues du journalisme de référence et d'instituts d'études géopolitiques sérieux, avec une règle stricte de **pluralisme** : chaque sujet présente plusieurs points de vue et bords politiques, nommés et étiquetés.

## Fonctionnement

- **Routine cloud Claude** : s'exécute tous les jours (cron `0 5 * * *` UTC ≈ 7h00 Paris). Elle clone ce repo, lit `INSTRUCTIONS.md` et le suit intégralement.
- **Chaque jour** : l'agent choisit un sujet France et un sujet Monde dans l'actualité récente (en évitant les répétitions grâce à `sujets/history.md`), rédige l'édition (`editions/<YYYY-MM-DD>.md`) et la pousse sur GitHub.
- **Envoi de l'email** : la GitHub Action `.github/workflows/send-reading.yml` détecte chaque nouvelle édition poussée et l'envoie par email (SMTP Gmail). Secrets requis dans le repo : `MAIL_USERNAME` (adresse Gmail) et `MAIL_APP_PASSWORD` (mot de passe d'application Google, créé sur https://myaccount.google.com/apppasswords). Le connecteur Gmail de claude.ai ne sait que créer des brouillons : il n'est pas utilisé pour la livraison.

## Comment piloter

- **Demander un sujet précis** : éditer `sujets/demandes.md` (depuis GitHub web, l'app mobile GitHub, ou ce dossier local). L'agent traite la demande en priorité dans la prochaine édition, puis l'efface.
- **Ajuster le format, la durée, les sources** : éditer `INSTRUCTIONS.md` — la routine relit ce fichier à chaque exécution, aucun changement de la routine elle-même n'est nécessaire.
- **Renvoyer la dernière édition** : lancer manuellement le workflow `Send daily geopolitics reading by email` (onglet Actions → Run workflow).

## Structure

```
INSTRUCTIONS.md       — instructions complètes de l'agent (format, sources, pluralisme, logique)
sujets/demandes.md    — demandes de sujets pour les prochaines éditions (éditable à tout moment)
sujets/history.md     — sujets déjà traités (anti-répétition)
editions/<date>.md    — archive des éditions quotidiennes
```

## Gestion de la routine

La routine se gère sur https://claude.ai/code/routines (activer/désactiver, supprimer, voir les exécutions).
