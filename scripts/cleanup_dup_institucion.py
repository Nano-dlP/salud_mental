
# scripts/cleanup_dup_institucion.py
# Remove duplicate ExpedienteInstitucion entries
# Duplicates are defined as having the same expediente, institucion, and rol
# Para ejecutar este script, usa el shell de Django:
# python manage.py shell < scripts/cleanup_dup_institucion.py

from django.db.models import Count
from expediente.models import ExpedienteInstitucion

dups = (ExpedienteInstitucion.objects
        .values('expediente_id','institucion_id','rol')
        .annotate(c=Count('id'))
        .filter(c__gt=1))

for d in dups:
    qs = (ExpedienteInstitucion.objects
          .filter(expediente_id=d['expediente_id'], institucion_id=d['institucion_id'], rol=d['rol'])
          .order_by('id'))
    keep = qs.first()
    to_delete = qs.exclude(pk=keep.pk)
    print(f"Keeping id {keep.pk}, would delete {to_delete.count()} duplicates for expediente={d['expediente_id']} institucion={d['institucion_id']} rol={d['rol']}")
    # Para borrar realmente, descomenta la siguiente línea:
    #to_delete.delete()

