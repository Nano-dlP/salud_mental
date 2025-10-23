import logging
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

EXCLUDE_PREFIXES = ("/static", "/media", "/favicon.ico", "/robots.txt")  # ajustar según necesidad

def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

class BlockIPMiddleware(MiddlewareMixin):
    """
    Middleware que bloquea peticiones desde IPs marcadas en cache (blocked_ip:<ip>).
    Ponlo lo más arriba posible en MIDDLEWARE para evitar trabajo innecesario.
    """
    def process_request(self, request):
        try:
            path = request.path or ""
            # excluir prefijos que no queremos bloquear (opcional)
            if any(path.startswith(p) for p in EXCLUDE_PREFIXES):
                return None

            ip = _get_client_ip(request)
            if not ip:
                return None

            blocked_key = f"blocked_ip:{ip}"
            if cache.get(blocked_key):
                logger.info("Bloqueando petición desde IP bloqueada: %s path=%s", ip, path)
                # Puedes devolver una página personalizada o HttpResponseForbidden
                return HttpResponseForbidden("Tu IP ha sido temporalmente bloqueada por demasiados intentos fallidos.")
        except Exception:
            logger.exception("Error comprobando bloqueo de IP")
        return None