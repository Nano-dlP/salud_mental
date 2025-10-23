import httpagentparser
from .models import ClienteLog

def registrar_cliente(request):
    # IP: se usa HTTP_X_FORWARDED_FOR si existe (caso detrás de proxy),
    # y se toma el primer valor separado por comas; si no existe se usa REMOTE_ADDR.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    # User Agent: se obtiene la cabecera HTTP_USER_AGENT; por defecto cadena vacía si no existe.
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    try:
        # httpagentparser.simple_detect devuelve (os, browser)
        parsed = httpagentparser.simple_detect(user_agent)
        sistema_operativo = parsed[0]
        navegador = parsed[1]
    except:
        # Si el parser lanza cualquier excepción, se marcan como 'Desconocido'
        sistema_operativo = 'Desconocido'
        navegador = 'Desconocido'

    # URL actual: build_absolute_uri construye la URL completa de la petición
    url = request.build_absolute_uri()

    # Referer: cabecera HTTP_REFERER si existe, sino cadena vacía
    referer = request.META.get('HTTP_REFERER', '')

    # Usuario: si el request tiene user y está autenticado, se guarda el objeto user; si no, None
    usuario = request.user if request.user.is_authenticated else None

    # Guardar log: crea una fila en la tabla ClienteLog con los campos recogidos
    ClienteLog.objects.create(
        usuario=usuario,
        ip=ip,
        navegador=navegador,
        sistema_operativo=sistema_operativo,
        user_agent=user_agent,
        url=url,
        referer=referer or None  # si referer es '' lo convierte a None
    )