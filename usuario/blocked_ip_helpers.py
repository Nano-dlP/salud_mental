import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

BLOCKED_IPS_SET = "blocked_ips:set"
BLOCKED_KEY_PREFIX = "blocked_ip:"

try:
    from django_redis import get_redis_connection
    _have_redis = True
except Exception:
    _have_redis = False


def add_blocked_ip(ip, block_time=None):
    try:
        if _have_redis:
            conn = get_redis_connection("default")
            conn.sadd(BLOCKED_IPS_SET, ip)
        else:
            logger.debug("No hay django_redis; no se añadió IP al set listable")
    except Exception:
        logger.exception("Error añadiendo IP al set de bloqueadas")


def remove_blocked_ip(ip):
    try:
        cache.delete(f"{BLOCKED_KEY_PREFIX}{ip}")
    except Exception:
        logger.exception("Error borrando la clave de bloqueo en cache para %s", ip)

    try:
        if _have_redis:
            conn = get_redis_connection("default")
            conn.srem(BLOCKED_IPS_SET, ip)
        else:
            logger.debug("No hay django_redis; no se puede eliminar IP del set listable")
    except Exception:
        logger.exception("Error eliminando IP del set listable")


def get_blocked_ips():
    try:
        if _have_redis:
            conn = get_redis_connection("default")
            members = conn.smembers(BLOCKED_IPS_SET) or set()
            return sorted({m.decode("utf-8") if isinstance(m, bytes) else str(m) for m in members})
        else:
            return None
    except Exception:
        logger.exception("Error obteniendo lista de IPs bloqueadas")
        return None
