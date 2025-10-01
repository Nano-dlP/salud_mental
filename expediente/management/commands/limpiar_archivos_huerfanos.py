import os
from django.core.management.base import BaseCommand
from django.conf import settings
from expediente.models import ExpedienteDocumento

class Command(BaseCommand):
    help = "Elimina archivos huérfanos en la carpeta media/documentos/expedientes"

    def handle(self, *args, **kwargs):
        documentos_path = os.path.join(settings.MEDIA_ROOT, "documentos", "expedientes")

        if not os.path.exists(documentos_path):
            self.stdout.write(self.style.WARNING("La carpeta 'media/documentos/expedientes' no existe."))
            return

        # Archivos que están en la BD (ruta relativa al MEDIA_ROOT)
        archivos_en_bd = set(
            ExpedienteDocumento.objects.exclude(archivo="").values_list("archivo", flat=True)
        )

        # Normalizar: quedarnos solo con el nombre del archivo
        archivos_en_bd = {os.path.basename(str(path)) for path in archivos_en_bd}

        # Archivos realmente presentes en la carpeta
        archivos_en_fs = set(os.listdir(documentos_path))

        # Detectar huérfanos
        huerfanos = archivos_en_fs - archivos_en_bd

        if not huerfanos:
            self.stdout.write(self.style.SUCCESS("No se encontraron archivos huérfanos."))
            return

        # Borrar huérfanos
        for archivo in huerfanos:
            ruta = os.path.join(documentos_path, archivo)
            try:
                os.remove(ruta)
                self.stdout.write(self.style.WARNING(f"Archivo eliminado: {archivo}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"No se pudo eliminar {archivo}: {e}"))

        self.stdout.write(self.style.SUCCESS("Limpieza de archivos huérfanos completada."))
