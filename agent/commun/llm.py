"""Acces unique au modele de langage (LLM) de raisonnement.

Tous les agents passent par ``chat_json`` : changer de fournisseur
(Groq <-> Ollama) se fait ici, sans toucher aux agents.

- ``groq``   : API compatible OpenAI, modeles a poids ouverts (gpt-oss),
               rapide. Necessite AIREADY_GROQ_API_KEY dans .env.
- ``ollama`` : modele local (code de reference UIT) ; lent sans GPU.

Les quotas Groq (offre gratuite) sont limites par jour : en cas de
depassement (HTTP 429), on attend puis on retente, avant d'abandonner
proprement avec un message explicite.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Optional

from agent.commun.config import settings

logger = logging.getLogger(__name__)

_groq_client = None
_ollama_client = None


def _groq():
    global _groq_client
    if _groq_client is None:
        if not settings.groq_api_key:
            raise RuntimeError(
                "Cle Groq absente : renseignez AIREADY_GROQ_API_KEY dans le fichier .env"
            )
        from openai import OpenAI
        _groq_client = OpenAI(api_key=settings.groq_api_key, base_url=settings.groq_base_url)
    return _groq_client


def _ollama():
    global _ollama_client
    if _ollama_client is None:
        import ollama
        _ollama_client = ollama.Client(host=settings.ollama_base_url)
    return _ollama_client


# Offre gratuite Groq : une requete ne peut pas depasser 8 000 jetons PAR MINUTE,
# en comptant la reponse maximale demandee. On garde une marge.
REQUEST_TOKEN_BUDGET = 7600


def estimate_tokens(text: str) -> int:
    """Estimation prudente : ~3 caracteres par jeton pour du francais juridique."""
    return len(text) // 3 + 1


def model_name(fast: bool = False) -> str:
    """Nom du modele effectivement utilise (pour les journaux d'audit)."""
    if settings.llm_provider == "groq":
        return settings.groq_model_fast if fast else settings.groq_model
    return settings.llm_model


@dataclass
class LLMResult:
    """Reponse du LLM et informations utiles au journal d'audit."""
    text: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    seconds: float = 0.0
    # « length » : la reponse a ete coupee par la limite de longueur.
    finish_reason: str = ""

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


def chat_json(
    system: str,
    user: str,
    fast: bool = False,
    temperature: float = 0.3,
    max_tokens: int = 4096,
    retries: int = 3,
) -> str:
    """Envoie un message au LLM et renvoie sa reponse brute (JSON attendu).

    ``fast=True`` utilise le petit modele (quota separe), pour les essais.
    """
    return chat(system, user, fast=fast, temperature=temperature,
                max_tokens=max_tokens, retries=retries).text


def chat(
    system: str,
    user: str,
    fast: bool = False,
    temperature: float = 0.3,
    max_tokens: int = 4096,
    retries: int = 3,
    reasoning_effort: Optional[str] = "low",
) -> LLMResult:
    """Comme ``chat_json``, mais renvoie aussi le modele et les jetons consommes.

    ``reasoning_effort`` (modeles gpt-oss sur Groq) : la reflexion interne du
    modele consomme du quota ; on la limite par defaut. Le raisonnement
    enregistre dans le journal d'audit est celui que l'agent explicite dans sa
    reponse, pas cette reflexion interne.
    """
    provider = settings.llm_provider
    model = model_name(fast)

    for attempt in range(1, retries + 1):
        start = time.time()
        try:
            if provider == "groq":
                extra = {}
                if reasoning_effort and "gpt-oss" in model:
                    extra["reasoning_effort"] = reasoning_effort
                resp = _groq().chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format={"type": "json_object"},
                    **extra,
                )
                usage = resp.usage
                return LLMResult(
                    text=resp.choices[0].message.content or "",
                    model=model,
                    prompt_tokens=getattr(usage, "prompt_tokens", 0) or 0,
                    completion_tokens=getattr(usage, "completion_tokens", 0) or 0,
                    seconds=round(time.time() - start, 2),
                    finish_reason=resp.choices[0].finish_reason or "",
                )

            # Ollama (comportement du code de reference UIT)
            resp = _ollama().chat(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                options={"temperature": temperature, "num_predict": max_tokens, "num_ctx": 8192},
                format="json",
            )
            return LLMResult(
                text=resp["message"]["content"],
                model=model,
                prompt_tokens=resp.get("prompt_eval_count", 0) or 0,
                completion_tokens=resp.get("eval_count", 0) or 0,
                seconds=round(time.time() - start, 2),
            )

        except Exception as e:  # noqa: BLE001 - on journalise et on retente
            msg = str(e)
            low = msg.lower()
            rate_limited = "429" in msg or "rate limit" in low
            # Coupures reseau passageres : frequentes sur une connexion instable.
            network = any(k in low for k in ("connection", "timeout", "timed out", "502", "503", "504"))
            if (rate_limited or network) and attempt < retries:
                wait = (20 if rate_limited else 5) * attempt
                logger.warning("%s (%s) - nouvel essai dans %ss",
                               "Quota LLM atteint" if rate_limited else "Coupure reseau", model, wait)
                time.sleep(wait)
                continue
            logger.error("Appel LLM echoue (%s, %s) : %s", provider, model, msg)
            raise

    raise RuntimeError("Appel LLM impossible apres plusieurs essais")
