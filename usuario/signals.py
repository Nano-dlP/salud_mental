import logging
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

from .blocked_ips import add_blocked_ip

logger = logging.getLogger(__name__)

ATTEMPT_LIMIT = getattr(settings, "IP_BLOCK_ATTEMPT_LIMIT", 3)
ATTEMPT_WINDOW = getattr(settings, "IP_BLOCK_ATTEMPT_WINDOW", 5 * 60)
BLOCK_TIME = getattr(settings, "IP_BLOCK_TIME", 60 * 60)
BLOCKED_KEY_PREFIX = "blocked_ip:"
ATTEMPTS_KEY_PREFIX = "login_attempts:"


def _get_client_ip(request):
    if request is None:
        return None
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@receiver(user_login_failed)
def handle_login_failed(sender, credentials, request, **kwargs):
    """
    Incrementa contador de intentos por IP y, si alcanza ATTEMPT_LIMIT, bloquea la IP.
    Además agrega la IP al set listable usando add_blocked_ip.
    """
    try:
        ip = _get_client_ip(request)
        if not ip:
            return

        attempts_key = f"{ATTEMPTS_KEY_PREFIX}{ip}"
        blocked_key = f"{BLOCKED_KEY_PREFIX}{ip}"

        # Si ya está bloqueada, no hacemos nada
        if cache.get(blocked_key):
            logger.debug("Intento desde IP ya bloqueada: %s", ip)
            return

        attempts = cache.get(attempts_key, 0) + 1
        cache.set(attempts_key, attempts, timeout=ATTEMPT_WINDOW)

        logger.info("Login fallido #%d desde IP %s", attempts, ip)

        if attempts >= ATTEMPT_LIMIT:
            cache.set(blocked_key, True, timeout=BLOCK_TIME)
            # Añadir al set listable (Redis) para que la admin view pueda listar
            try:
                add_blocked_ip(ip)
            except Exception:
                logger.exception("No se pudo añadir IP %s al set de bloqueadas", ip)
            try:
                cache.delete(attempts_key)
            except Exception:
                logger.exception("No se pudo borrar el contador de intentos para %s", ip)

            logger.warning("IP %s bloqueada por %d segundos tras %d intentos fallidos", ip, BLOCK_TIME, ATTEMPT_LIMIT)
    except Exception:
        logger.exception("Error en handle_login_failed")