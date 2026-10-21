# app/services/email_service.py
# Envoi d'e-mails via SMTP (vérification du compte). Fournisseur configurable
# dans le .env (Outlook par défaut, Gmail possible sans changer le code).

import smtplib
from email.mime.text import MIMEText

from loguru import logger

from app.core.config import settings


def smtp_configured() -> bool:
    return bool(settings.SMTP_USER and settings.SMTP_PASSWORD)


def send_verification_email(to_email: str, code: str, name: str | None = None) -> bool:
    """Envoie le code de vérification. Retourne True si l'envoi a réussi."""
    if not smtp_configured():
        logger.warning("SMTP non configuré — e-mail de vérification non envoyé")
        return False

    sender   = settings.SMTP_FROM or settings.SMTP_USER
    greeting = f"Bonjour {name}," if name else "Bonjour,"
    body = (
        f"{greeting}\n\n"
        f"Votre code de vérification MinorShield est : {code}\n\n"
        f"Il expire dans 15 minutes. Saisissez-le dans l'application pour "
        f"activer votre compte.\n\n"
        f"Si vous n'êtes pas à l'origine de cette demande, ignorez cet e-mail.\n\n"
        f"— L'équipe MinorShield"
    )

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "MinorShield - Code de verification"
    msg["From"]    = sender
    msg["To"]      = to_email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(sender, [to_email], msg.as_string())
        logger.info(f"E-mail de vérification envoyé à {to_email}")
        return True
    except Exception as e:
        logger.error(f"Échec envoi e-mail de vérification à {to_email} : {e}")
        return False
