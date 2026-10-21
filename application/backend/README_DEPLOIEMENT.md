# MinorShield — Backend (FastAPI) — Notice de mise en route

Backend de détection de contenu inapproprié (API REST). Base de données **SQLite**
(un seul fichier `minorshield.db`, créé automatiquement au premier démarrage).

---

## 1. Prérequis système

- **Python 3.11**
- **Tesseract OCR** + langues française et anglaise (obligatoire pour l'analyse de texte) :
  ```bash
  # Debian / Ubuntu
  sudo apt update
  sudo apt install -y tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng
  ```

> Windows : installer Tesseract depuis https://github.com/UB-Mannheim/tesseract/wiki
> (le code pointe automatiquement sur `C:\Program Files\Tesseract-OCR\tesseract.exe`).

## 2. Installation

```bash
cd Server
python3 -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configuration

Le fichier **`.env`** est déjà fourni (clés incluses). Vérifier surtout :
- `API_KEY` : **doit rester identique** à la valeur codée dans les apps Android
  (`CHANGE_ME`), sinon les téléphones ne se connectent plus.
- `PUBLIC_URL` : mettre l'URL publique du nouveau serveur (pour le webhook Monetbil).
- `ENVIRONMENT` : `development` en test ; `production` impose `API_KEY` non vide,
  `ENABLE_DOCS=false` et `ALLOWED_ORIGINS` sans `*`.

Base persistante : par défaut la base est le fichier `minorshield.db` dans `Server/`.
Sur un serveur privé le disque est persistant → rien à configurer. Pour choisir un
autre emplacement : variable `DATABASE_URL=sqlite:////chemin/absolu/minorshield.db`.

## 4. Lancement

```bash
# Test rapide
python main.py                    # écoute sur $HOST:$PORT (défaut 0.0.0.0:8081)

# Production (recommandé)
uvicorn main:app --host 0.0.0.0 --port 8081
```

Mettre derrière un **service systemd** + **nginx** (reverse proxy HTTPS) pour la prod.
Vérifier ensuite : `http://<serveur>:8081/api/v1/health` → doit renvoyer
`{"status":"ok", ... "models_loaded":true}`.

## 5. Côté applications Android

Le backend ayant changé d'adresse, il faut mettre la **nouvelle URL** dans les 2 apps
(constante `BASE_URL` de `ParentApiClient.kt` et `ChildApiClient.kt`) puis **regénérer
les APK**. (Étape séparée, non incluse ici.)

---

## Notes

- **NudeNet** télécharge son modèle au premier démarrage (accès Internet requis une fois).
- Analyse **texte/violence** : nécessite `OPENAI_API_KEY` (et éventuellement
  `HUGGINGFACE_TOKEN` en secours). Un **lexique local** (`app/data/lexique_cmr.txt`)
  complète la détection et fonctionne même sans IA.
- **Notifications push** (optionnel) : renseigner `FIREBASE_CREDENTIALS_JSON`
  (contenu du compte de service Firebase) — sinon le push est simplement désactivé.
