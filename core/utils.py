import httpagentparser
from .models import ClienteLog

def registrar_cliente(request):
    # IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    # User Agent
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    try:
        parsed = httpagentparser.simple_detect(user_agent)
        sistema_operativo = parsed[0]
        navegador = parsed[1]
    except:
        sistema_operativo = 'Desconocido'
        navegador = 'Desconocido'

    # URL actual
    url = request.build_absolute_uri()

    # Referer
    referer = request.META.get('HTTP_REFERER', '')

    # Usuario (si está autenticado)
    usuario = request.user if request.user.is_authenticated else None

    # Guardar log
    ClienteLog.objects.create(
        usuario=usuario,
        ip=ip,
        navegador=navegador,
        sistema_operativo=sistema_operativo,
        user_agent=user_agent,
        url=url,
        referer=referer or None
    )
