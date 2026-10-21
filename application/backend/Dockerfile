# Dockerfile
# Définit comment construire l'image Docker du serveur MinorShield.

# ── Image de base ─────────────────────────────────────────────────────
# Python 3.11 slim = version légère sans éléments inutiles
FROM python:3.11-slim

# ── Métadonnées ───────────────────────────────────────────────────────
LABEL maintainer="MinorShield"
LABEL version="1.0.0"
LABEL description="API de détection de contenu inapproprié"

# ── Variables d'environnement ─────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1         

# ── Installation des dépendances système ──────────────────────────────
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    tesseract-ocr-eng \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
# ── Dossier de travail ────────────────────────────────────────────────
WORKDIR /app

# ── Copier et installer les dépendances Python ────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ── Copier le code source ─────────────────────────────────────────────
COPY . .

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/logs /app/weights \
    && chown -R appuser:appuser /app \
    && chmod 750 /app \
    && chmod 700 /app/logs

# ── Supprimer le .env s'il a été copié par erreur ─────────────────────
RUN rm -f /app/.env

# ── Port exposé ───────────────────────────────────────────────────────
EXPOSE 8081

USER appuser

# ── Commande de lancement ─────────────────────────────────────────────
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081", "--no-access-log"]
