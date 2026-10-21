"""Configuration settings for the AI Readiness Simulation Game."""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Ollama (embeddings locaux ; et LLM si llm_provider == "ollama")
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "qwen2.5:14b"
    # bge-m3 remplace nomic-embed-text : modele multilingue, nettement plus
    # discriminant sur des textes juridiques en francais (test comparatif :
    # 3/3 questions reussies contre 2/3, marge moyenne 0,285 contre 0,025).
    embed_model: str = "bge-m3"

    # Fournisseur du LLM de raisonnement : "groq" (API, modeles a poids
    # ouverts, rapide) ou "ollama" (local, lent sans carte graphique).
    llm_provider: str = "groq"
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    # Modele principal (simulations finales) et modele rapide (essais) :
    # leurs quotas journaliers sont distincts.
    groq_model: str = "openai/gpt-oss-120b"
    groq_model_fast: str = "openai/gpt-oss-20b"

    # Paths
    base_dir: Path = Path(__file__).resolve().parents[2]  # racine du depot
    data_dir: Path = base_dir / "data"
    chromadb_dir: Path = base_dir / "bd" / "chromadb"
    docs_dir: Path = data_dir / "docs"
    framework_dir: Path = base_dir / "bd" / "framework"
    input_docs_dir: Path = base_dir / "bd" / "InputDocs"
    db_path: Path = data_dir / "game.db"

    # ChromaDB collections
    kb_main_collection: str = "kb_main"
    kb_decisions_collection: str = "kb_decisions"
    kb_framework_collection: str = "kb_framework"

    # Chunking
    chunk_size: int = 256
    chunk_overlap: int = 30

    # Scoring
    maturity_scale_min: float = 0.0
    maturity_scale_max: float = 5.0
    similarity_threshold: float = 0.7

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_prefix = "AIREADY_"
        # Secrets (cle Groq) lus depuis un fichier .env non versionne.
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
