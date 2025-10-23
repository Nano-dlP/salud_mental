import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Nombre de la clave/estructura usada para listar IPs bloqueadas en Redis
BLOCKED_IPS_SET = "blocked_ips:set"
BLOCKED_KEY_PREFIX = "blocked_ip:"

# Intentar usar django-redis para acceder directamente a Redis y mantener un set
try:
    from django_redis import get_redis_connection
    _have_redis = True
except Exception:
    _have_redis = False


def add_blocked_ip(ip, block_time=None):
    """
    Marcar una IP como bloqueada también en la estructura listable (Redis set).
    block_time se ignora aquí; la expiración sigue siendo controlada por la clave blocked_ip:<ip>.
    """
    try:
        # Guardar la clave de bloqueo en cache si es necesario (aquí asumimos que ya se puso en cache por signals)
        # Añadir a set para poder listar
        if _have_redis:
            conn = get_redis_connection("default")
            conn.sadd(BLOCKED_IPS_SET, ip)
        else:
            # Si no hay acceso a Redis, no podemos mantener un set compartido.
            # Como fallback no hacemos nada: get_blocked_ips() devolverá None.
            logger.debug("No hay django_redis; no se añadió IP al set listable")
    except Exception:
        logger.exception("Error añadiendo IP al set de bloqueadas")


def remove_blocked_ip(ip):
    """
    Elimina el bloqueo de la IP: borra la clave de bloqueo en cache y la elimina del set si es posible.
    """
    try:
        # Borrar la clave de bloqueo en cache (si existe)
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
    """
    Devuelve una lista de IPs bloqueadas o None si no es posible listar
    (por ejemplo si no se tiene acceso directo a Redis).
    """
    try:
        if _have_redis:
            conn = get_redis_connection("default")
            members = conn.smembers(BLOCKED_IPS_SET) or set()
            # members vienen como bytes; convertir a str
            return sorted({m.decode("utf-8") if isinstance(m, bytes) else str(m) for m in members})
        else:
            # No es posible listar con la API de cache; devolver None para indicar que no hay listado disponible.
            return None
    except Exception:
        logger.exception("Error obteniendo lista de IPs bloqueadas")
        return None