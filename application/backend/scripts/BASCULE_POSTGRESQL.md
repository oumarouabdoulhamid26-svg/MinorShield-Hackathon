# Bascule SQLite → PostgreSQL — procédure

Tout a été préparé et testé en local (PostgreSQL 16, 2 179 lignes migrées,
13 tests passés). Il ne reste que la bascule en production.

**Durée estimée : 30 minutes.** Interruption de service : ~5 minutes.

---

## Pré-requis

- Le responsable serveur a lancé `deploy/install_postgres.sh`.
- Il a renvoyé la ligne `DATABASE_URL=postgresql+psycopg2://…`.

---

## Étape 1 — Sauvegarder l'existant (impératif)

Sur le serveur, avant toute chose :

```bash
cp Server/data/minorshield.db Server/data/minorshield.db.avant-postgres
```

C'est le filet de sécurité : en cas de problème, on revient à cette base.

## Étape 2 — Déployer le nouveau code

Le code livré contient déjà :

- `psycopg2-binary` et `alembic` dans `requirements.txt` ;
- `app/core/database.py` compatible SQLite **et** PostgreSQL ;
- `scripts/migrate_sqlite_to_postgres.py`.

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Étape 3 — Créer le schéma dans PostgreSQL

Toujours avec l'ancienne `DATABASE_URL` (SQLite) **inchangée** dans le `.env`,
on crée les tables côté PostgreSQL :

```bash
DATABASE_URL="<URL_POSTGRES>" python -c "from app.core.database import init_db; init_db()"
```

## Étape 4 — Migrer les données (simulation d'abord)

```bash
python scripts/migrate_sqlite_to_postgres.py --sqlite data/minorshield.db --postgres "<URL_POSTGRES>" --dry-run
```

Vérifier les nombres de lignes annoncés, puis lancer la migration réelle :

```bash
python scripts/migrate_sqlite_to_postgres.py --sqlite data/minorshield.db --postgres "<URL_POSTGRES>" --truncate
```

Le script affiche une vérification finale `source -> cible` pour chaque table.
**Ne pas continuer si un écart est signalé.**

## Étape 5 — Basculer la configuration

Dans `Server/.env`, remplacer la ligne :

```
DATABASE_URL=sqlite:///./data/minorshield.db
```

par la ligne PostgreSQL fournie par le responsable serveur.

## Étape 6 — Redémarrer et vérifier

Redémarrer le service, puis contrôler :

```bash
curl -s https://minorshield.nolate.cm/health
```

Puis, depuis l'application parent : se connecter avec un compte existant,
vérifier que les enfants et l'historique des détections apparaissent bien.

---

## Retour arrière (si problème)

La bascule est réversible : remettre l'ancienne ligne `DATABASE_URL`
(SQLite) dans le `.env` et redémarrer. Les données SQLite n'ont jamais été
modifiées — le script lit la base sans jamais y écrire.

---

## Après la bascule

- **Conserver le fichier SQLite au moins 2 semaines** avant de le supprimer.
- Vérifier au bout d'un jour que la sauvegarde automatique tourne :

```bash
ls -lh /var/backups/minorshield
```

---

## Ce qui a été testé en local

| Vérification | Résultat |
|---|---|
| Création du schéma sur PostgreSQL | 4 tables, colonnes identiques à SQLite |
| Migration des données | 9 parents · 5 enfants · 2 164 détections · 1 abonnement — aucune perte |
| Conversion des booléens (0/1 → true/false) | correcte |
| Conversion des dates (texte → TIMESTAMP) | correcte, aucun NULL inattendu |
| Accents français (UTF-8) | préservés |
| Inscription / connexion / appairage / réglages | fonctionnels |
| Avertissements illimités (valeur 0) | fonctionnel |
| Suite de tests du projet | 13 tests passés |
