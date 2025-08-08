from django.utils import timezone

def fecha_hora_actual(request):
    return {
        'fecha_hora_actual': timezone.localtime()
    }
