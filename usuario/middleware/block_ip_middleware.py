from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from usuario.blocked_ip_helpers import get_blocked_ips, BLOCKED_KEY_PREFIX
from django.core.cache import cache

class BlockIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if not ip:
            return None

        # Bloquear IP si está en cache
        if cache.get(f"{BLOCKED_KEY_PREFIX}{ip}"):
            return HttpResponseForbidden(
                "Tu IP ha sido temporalmente bloqueada por demasiados intentos fallidos."
            )

        return None
