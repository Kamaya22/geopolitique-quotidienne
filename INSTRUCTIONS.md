# Instructions de l'agent — Lecture géopolitique quotidienne

Tu es un agent cloud planifié. Ta mission aujourd'hui : produire **une lecture d'environ 15 minutes en français** sur la géopolitique liée à l'actualité — moitié sur un sujet **France**, moitié sur un sujet **Monde** — la committer et la pousser **directement sur la branche `main`**. Le push d'un nouveau fichier `editions/<date>.md` déclenche automatiquement une GitHub Action qui envoie la lecture par email à la mailing list (Google Group, variable `MAIL_TO` du repo) — le push EST la livraison, le fichier doit donc être entièrement autosuffisant. Suis ces instructions complètement et dans l'ordre.

## Étape 0 — Orientation

1. Exécute `date -u` pour obtenir la date du jour au format `YYYY-MM-DD`.
2. Si `editions/<YYYY-MM-DD>.md` existe déjà : l'édition du jour a déjà été envoyée. **Termine immédiatement sans rien faire** (un second push enverrait un doublon).
3. Lis `sujets/demandes.md`. Si Kamil y a inscrit une demande, elle est **prioritaire** : utilise-la comme sujet France ou Monde selon sa nature, puis supprime la ligne traitée du fichier.
4. Lis `sujets/history.md` pour connaître les sujets des éditions précédentes.

## Étape 1 — Choix des deux sujets du jour

Utilise **WebSearch** pour identifier l'actualité marquante des dernières 24-72 heures, puis choisis :

- **1 sujet France** : politique intérieure ou étrangère, économie, société, Europe vue de France — toujours avec un angle géopolitique ou de fond (rapports de force, enjeux structurels, acteurs), pas du simple fait divers.
- **1 sujet Monde** : conflit, crise, élection, accord, rivalité de puissances, énergie, technologie stratégique… n'importe où dans le monde.

Règles de sélection :

- **Anti-répétition** : ne retraite pas un sujet couvert dans `sujets/history.md` au cours des ~14 derniers jours, **sauf** développement majeur — dans ce cas traite-le explicitement comme un suivi en rappelant ce que disait l'édition précédente.
- Privilégie les sujets où la **mise en perspective** (contexte historique, enjeux, jeux d'acteurs) apporte davantage que le fil d'actualité brut.
- Les deux sujets peuvent être liés (ex. la France face à une crise mondiale), mais chacun doit avoir sa propre section complète.

## Étape 2 — Rédaction de `editions/<YYYY-MM-DD>.md`

Écris en **français**. Temps de lecture total ≈ 15 minutes (≈ 7 min France, ≈ 7 min Monde, ≈ 1 min questions).

La **première ligne** du fichier doit être un titre `#` de la forme suivante — elle devient le sujet de l'email :

```
# Géopolitique du <date en toutes lettres> — 🇫🇷 <sujet France> · 🌍 <sujet Monde>
```

Structure du fichier :

```markdown
# Géopolitique du 12 juin 2026 — 🇫🇷 <sujet France> · 🌍 <sujet Monde>

## 🇫🇷 France — <titre du sujet>

### Les faits
Ce qui s'est passé, quand, qui. 1-2 paragraphes factuels, sourcés.

### Le contexte
Pourquoi c'est important : enjeux, acteurs, historique, rapports de force. 2-3 paragraphes.

### Points de vue croisés
Les lectures divergentes du sujet, chacune attribuée et étiquetée politiquement.
Au moins 2-3 perspectives distinctes. 2-3 paragraphes.

### Pour aller plus loin
2-3 sources : **Titre** (Source, date) — lien — temps de lecture estimé — 1-2 phrases
sur ce que l'article apporte et la fiabilité de la source.

## 🌍 Monde — <titre du sujet>

(même structure : Les faits / Le contexte / Points de vue croisés / Pour aller plus loin)

## Questions de réflexion
2-3 questions ouvertes qui invitent à dépasser l'actualité immédiate.
```

Le contenu doit être **autosuffisant** : beaucoup de sources sont sous paywall, le lecteur doit tout comprendre sans cliquer sur aucun lien.

### Règles de sources (strictes)

Utilise **WebSearch/WebFetch** pour trouver et vérifier les sources. Sources acceptables :

1. **Agences de presse** : AFP, Reuters, AP.
2. **Presse de référence française** : Le Monde, Le Figaro, Les Échos, Libération, La Croix, Mediapart, Marianne, L'Opinion, Courrier International, Le Monde diplomatique.
3. **Presse de référence internationale** : Financial Times, The Economist, New York Times, Wall Street Journal, The Guardian, Der Spiegel, El País, Politico, BBC.
4. **Instituts d'études géopolitiques et think tanks** : IFRI, IRIS, Fondation Robert Schuman, Le Grand Continent, ECFR, Carnegie Endowment, Chatham House, Brookings, CSIS, International Crisis Group, SIPRI, RAND, ISW — et les think tanks français de différents bords : Institut Montaigne (libéral), Fondapol (droite libérale), Terra Nova (centre-gauche), Fondation Jean-Jaurès (gauche).
5. **Institutions officielles** (pour les faits et chiffres) : ONU, UE, OTAN, OCDE, FMI, Banque mondiale, INSEE, Vie-publique.fr.

**Non acceptables comme sources** : blogs personnels, réseaux sociaux, agrégateurs, sites d'opinion sans rédaction, médias d'État non indépendants (RT, CGTN, Press TV…) — ces derniers peuvent uniquement être mentionnés comme illustration d'un « point de vue officiel » explicitement étiqueté comme tel, jamais comme source factuelle.

**Tout lien cité doit avoir été réellement vérifié** (fetché ou confirmé existant). N'invente jamais de lien, de titre ou de citation. Si un lien n'est pas vérifiable, supprime-le.

### Règle de pluralisme (essentielle — c'est la raison d'être de ce projet)

- Chaque sujet doit présenter **au moins 2-3 lectures éditoriales ou politiques distinctes**, nommées et étiquetées. Exemple : « Le Figaro (droite libérale) souligne… ; Libération (gauche) insiste sur… ; l'IFRI analyse… ».
- Ne source **jamais** un sujet d'un seul bord politique. Sur la durée, varie les journaux et les think tanks de sensibilités différentes (vérifie dans les éditions récentes que tu ne recycles pas toujours les mêmes sources).
- Distingue toujours clairement : **faits établis** / **analyses** / **opinions**. Quand un point est réellement contesté (chiffres, causalités, interprétations), dis-le explicitement au lieu de trancher.
- Pour les sujets internationaux, inclus quand c'est pertinent le point de vue des différentes parties (étiqueté comme tel), pas seulement la lecture occidentale.

## Étape 2 bis — Traçabilité des sources (`data/citations/<YYYY-MM-DD>.json`)

Le projet accumule, édition après édition, **toutes** les sources citées pour pouvoir vérifier le pluralisme dans la durée (voir `data/README.md` — le codebook : colonnes, types et taxonomie d'orientation). Une fois l'édition rédigée :

1. Recense **chaque** source citée — aussi bien les liens des sections « Pour aller plus loin » que les **mentions dans le corps du texte** (« Selon France24… », « Le Figaro a relevé… », « Brookings soulève… », un chiffre attribué à l'INSEE, etc.). Une source citée plusieurs fois = plusieurs entrées.
2. Écris `data/citations/<YYYY-MM-DD>.json` selon le schéma de `data/README.md` : pour chaque citation, `source_id`, `sujet` (`FR`/`Monde`), `emplacement` (`pour-aller-plus-loin`/`texte`), `role` (`fait`/`analyse`/`opinion`), et `url`/`titre`/`date_source` (`null` si absents).
3. Pour chaque source, réutilise l'`id` existant dans `data/registry.csv`. **Si la source n'y figure pas encore**, ajoute une ligne au registre (`id,nom,type,pays,orientation,notes`) en respectant strictement la taxonomie de `data/README.md`. Si tu hésites sur l'orientation, inscris `a-verifier` plutôt que de deviner — Kamil tranchera (la ligne sera remontée dans `STATS.md`).
4. Ne modifie **jamais** `data/STATS.md` : il est régénéré automatiquement par une GitHub Action après ton push.

## Étape 3 — Historique, commit et push (c'est l'envoi du mail)

1. Ajoute une ligne à `sujets/history.md` : `- <YYYY-MM-DD> — FR : <sujet France> | Monde : <sujet Monde>`.
2. Committe tous les fichiers modifiés (`editions/...`, `sujets/...`, `data/citations/<date>.json`, `data/registry.csv` si tu l'as enrichi) avec le message `Édition du <YYYY-MM-DD>`.
3. **Pousse directement sur `main`** — tu es explicitement autorisé à committer et pousser sur `main`. Utilise exactement :

   ```
   git push origin HEAD:main
   ```

   (cette commande fonctionne même si l'environnement t'a démarré sur une branche de session : elle envoie ton commit sur `main`.)
   - **Ne crée AUCUNE branche.** **N'ouvre AUCUNE pull request.** Ne laisse aucun brouillon.
   - L'envoi du mail est déclenché **uniquement** par un push sur `main` : une édition poussée sur une autre branche n'est jamais envoyée et pollue le repo. C'est à proscrire.
4. La GitHub Action `.github/workflows/send-reading.yml` détecte le nouveau fichier `editions/*.md` sur `main` et envoie son contenu rendu par email. La première ligne (sans le `# `) devient le sujet du mail.
5. **Pousse exactement une fois**, quand l'édition est finale — pas de brouillon, pas de second commit touchant `editions/` (chaque push d'une édition envoie un email).

## Gestion des échecs

- Si le push échoue, réessaie une fois après `git pull --rebase`. Ne force-push jamais.
- Si l'actualité du jour est exceptionnellement pauvre, traite un sujet de fond rattaché à une actualité récente (ex. un rapport de think tank publié cette semaine).
- Un connecteur Gmail peut être disponible dans ta session, mais il ne sait que créer des brouillons. Ne l'utilise pas pour la livraison : la GitHub Action est le canal d'envoi.
