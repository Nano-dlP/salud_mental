from django.db import models
from django.contrib.auth.models import User


class ClienteLog(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField()
    navegador = models.CharField(max_length=255)
    sistema_operativo = models.CharField(max_length=255)
    user_agent = models.TextField()
    url = models.URLField(max_length=500)
    referer = models.URLField(max_length=500, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario or self.ip} visitó {self.url} el {self.fecha}"




# Create your models here.
class Auditoria(models.Model):
    estado = models.BooleanField('Estado', default=True)
    fecha_crea = models.DateTimeField('Fecha de creación',  auto_now_add=True, null=True, blank=True)
    fecha_modifica = models.DateTimeField('Fecha de modificación', auto_now=True, null=True, blank=True)
    
    #user_crea = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Usuario creo)
    user_crea = models.ForeignKey(User, verbose_name="Usuario creo registro", on_delete=models.CASCADE, related_name='auditoria_crea', null=True, blank=True)
    user_modifica = models.ForeignKey(User, verbose_name="Usuario modifico registro", on_delete=models.CASCADE, related_name='auditoria_modifica', null=True, blank=True)
    ip = models.GenericIPAddressField('IP', null=True, blank=True)
    
    class Meta:
        abstract=True



class Pais(models.Model):
    pais = models.CharField(max_length=100, blank=True, null=True, verbose_name='País')

    def __str__(self):
        return self.pais
    
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ['pais']



class Provincia(models.Model):
    provincia = models.CharField(max_length=100, verbose_name='Provincia', blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, verbose_name='País', blank=True, null=True, related_name='provincias_pais', default=None)

    def __str__(self):
        return self.provincia
    
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
    

class Genero(models.Model):
    genero = models.CharField('Genero', max_length=50, unique=True)
    
    def __str__(self):
        return self.genero

    class Meta:
        verbose_name='Genero'
        verbose_name_plural='Generos'


class Nivel_Educativo(models.Model):
    nivel_educativo = models.CharField('Nivel Educativo', max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.nivel_educativo

    class Meta:
        verbose_name='Nivel Educativo'
        verbose_name_plural='Niveles Educativos'


class Tipo_Documento(models.Model):
    tipo_documento = models.CharField('Tipo de documento', max_length=50)
    
    def __str__(self):
        return self.tipo_documento
    
    class Meta:
        verbose_name ='Tipo de documento'
        verbose_name_plural = 'Tipos de documentos'


class Sede(models.Model):
    sede = models.CharField('Sede', max_length=50)
    Localidad = models.ForeignKey('Localidad', on_delete=models.CASCADE, verbose_name='Localidad', blank=True, null=True, related_name='sede_localidad')
    
    def __str__(self):
        return self.sede
    
    class Meta:
        verbose_name ='Sede'
        verbose_name_plural = 'Sedes'


class Localidad(models.Model):
    localidad = models.CharField('Localidad', max_length=70, blank=False, null=False)
    nombre_abreviado = models.CharField('Nombre abreviado', max_length=4, blank=True, null=True)
    codigo_area = models.IntegerField('Código de área', blank=True, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, verbose_name='Provincia', blank=True, null=True, related_name='localidades_provincia')


    def __str__(self):
        return self.localidad
    
    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'



class AreaProfesional(models.Model):
    area_profesional = models.CharField('Área profesional', max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.area_profesional
    
    class Meta:
        verbose_name = 'Área profesional'
        verbose_name_plural = 'Áreas profesionales'


class Profesion (models.Model):
    profesion = models.CharField('Profesión', max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.profesion
    
    class Meta:
        verbose_name = 'Profesión'
        verbose_name_plural = 'Profesiones'