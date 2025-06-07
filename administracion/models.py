from django.db import models
import uuid
# Create your models here.
from django.db import models
from multiselectfield import MultiSelectField


# parte para agregar los dias
DIAS_SEMANA = [
    ('lunes', 'Lunes'),
    ('martes', 'Martes'),
    ('miercoles', 'Miércoles'),
    ('jueves', 'Jueves'),
    ('viernes', 'Viernes'),
]

class Alumno(models.Model):
    clave_alumno = models.CharField(max_length=255, unique=True, null=True, blank=True)
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    correo = models.CharField(max_length=250)
    contrasena = models.CharField(max_length=250)
    telefono = models.BigIntegerField()
    clave = models.CharField(max_length=255) # esta es la clave de la escuela
    curp = models.CharField(max_length=18, unique=True)
    sexo = models.CharField(max_length=250)
    token_recuperacion = models.CharField(max_length=64, blank=True, null=True)
    restriccion_libre = models.BooleanField(default=False, help_text="Permitir que el alumno se inscriba sin restricciones")
    estado = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)



    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"

    def save(self, *args, **kwargs):
        if not self.clave_alumno:
            self.clave_alumno = self._generar_clave_unica()
        super().save(*args, **kwargs)

    def _generar_clave_unica(self):
        while True:
            clave = uuid.uuid4().hex[:10].upper()  # Por ejemplo: 'A1B2C3D4E5'
            if not Alumno.objects.filter(clave_alumno=clave).exists():
                return clave

class Facilitador(models.Model):
    clave_facilitador = models.CharField(max_length=255, unique=True, null=True, blank=True)
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    correo = models.CharField(max_length=250)
    contrasena = models.CharField(max_length=250)
    telefono = models.BigIntegerField()
    clave = models.CharField(max_length=255)
    curp = models.CharField(max_length=18, unique=True)
    sexo = models.CharField(max_length=150)
    token_recuperacion = models.CharField(max_length=64, null=True, blank=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"

    def save(self, *args, **kwargs):
        if not self.clave_facilitador:
            self.clave_facilitador = self._generar_clave_unica()
        super().save(*args, **kwargs)

    def _generar_clave_unica(self):
        while True:
            clave = uuid.uuid4().hex[:10].upper()  # Ejemplo: 'A1B2C3D4E5'
            if not Facilitador.objects.filter(clave_facilitador=clave).exists():
                return clave

class Periodo(models.Model):
    nombre_periodo = models.CharField(max_length=255,null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre_periodo 


class Curso(models.Model):
    nombre_curso = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    cupos = models.IntegerField(blank=True, null=True)
    grupo = models.CharField(max_length=255, unique=True)
    modalidad = models.CharField(max_length=255,null=True, blank=True)
    duracion = models.IntegerField(blank=True, null=True)
    facilitador = models.ForeignKey(Facilitador, on_delete=models.CASCADE, null=True, blank=True) 
    periodo = models.ForeignKey(Periodo, on_delete=models.SET_NULL, null=True, blank=True)
    publicado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)
    lugar = models.CharField(max_length=255, null=True, blank=True)
    aula = models.CharField(max_length=255, null=True, blank=True)
    dias = MultiSelectField(choices=DIAS_SEMANA, blank=True, default=list)




    def __str__(self):
        return self.nombre_curso  

class Taller(models.Model):
    nombre_taller = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    cupos = models.IntegerField(blank=True, null=True)
    grupo = models.CharField(max_length=255, unique=True)
    modalidad = models.CharField(max_length=255, null=True, blank=True)
    duracion = models.IntegerField(blank=True, null=True)
    facilitador = models.ForeignKey(Facilitador, on_delete=models.CASCADE, null=True, blank=True) 
    periodo = models.ForeignKey(Periodo, on_delete=models.SET_NULL, null=True, blank=True)
    publicado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)
    lugar = models.CharField(max_length=255, null=True, blank=True)
    aula = models.CharField(max_length=255, null=True, blank=True)
    dias = MultiSelectField(choices=DIAS_SEMANA, blank=True, default=list)




    def __str__(self):
        return self.nombre_taller  

class Diplomado(models.Model):
    nombre_diplomado = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    cupos = models.IntegerField(blank=True, null=True)
    grupo = models.CharField(max_length=255, unique=True)
    modalidad = models.CharField(max_length=255, null=True, blank=True)
    duracion = models.IntegerField(blank=True, null=True)
    facilitador = models.ForeignKey(Facilitador, on_delete=models.CASCADE, null=True, blank=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)
    lugar = models.CharField(max_length=255, null=True, blank=True)
    aula = models.CharField(max_length=255, null=True, blank=True)
    dias = MultiSelectField(choices=DIAS_SEMANA, blank=True, default=list)




    def __str__(self):
        return self.nombre_diplomado  

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE, null=True, blank=True)
    diplomado = models.ForeignKey(Diplomado, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=255)
    finalizado = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.alumno} - {self.estado}"

class DiplomadoLanding(models.Model):
    titulo = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='diplomados_landing/')
    destinatarios = models.TextField(null=True)
    introduccion = models.TextField(null=True)
    nivel = models.CharField(max_length=100, null=True, blank=True)
    proposito = models.TextField(null=True)
    particulares = models.TextField(null=True)
    recursos = models.TextField(null=True)
    duracion = models.CharField(max_length=255, null=True, blank=True)
    modalidad = models.CharField(max_length=255, null=True, blank=True)
    costo = models.TextField(null=True, blank=True)
    participantes = models.CharField(max_length=255, null=True, blank=True)
    responsable = models.CharField(max_length=255, null=True, blank=True)
    programa_pdf = models.FileField(upload_to='diplomados_landing/programas/', null=True, blank=True)


    class Meta:
        db_table = 'diplomados_landing'
        verbose_name = 'Diplomado en Landing'
        verbose_name_plural = 'Diplomados en Landing'

    def __str__(self):
        return self.titulo
    
class ModuloDiplomado(models.Model):
    diplomado = models.ForeignKey(DiplomadoLanding, related_name='modulos', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo

class TallerLanding(models.Model):
    titulo = models.CharField(max_length=200, null=True, blank=True)
    descripcion_corta = models.TextField()
    imagen = models.ImageField(upload_to='taller_landing/')
    subtitulo =models.CharField(max_length=200, null=True, blank=True)
    descripcion_larga = models.TextField(null=True,blank=True)
    responsable =models.CharField(max_length=200, null=True, blank=True)
    duracion = models.CharField(max_length=255, null=True, blank=True)
    programa_pdf = models.FileField(upload_to='taller_landing/programas/', null=True, blank=True)

    class Meta:
        db_table = 'taller_landing'
        verbose_name = 'Taller en Landing'
        verbose_name_plural = 'Talleres en Landing'

    def __str__(self):
        return self.titulo
    
class SesionTaller(models.Model):
    taller = models.ForeignKey(TallerLanding, on_delete=models.CASCADE, related_name='sesiones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    class Meta:
        verbose_name = 'Sesión del Taller'
        verbose_name_plural = 'Sesiones del Taller'

    def __str__(self):
        return self.titulo
    
class CursoLanding(models.Model):
    titulo = models.CharField(max_length=200, null=True, blank=True)
    descripcion_corta = models.TextField()
    imagen = models.ImageField(upload_to='cursos_landing/')
    subtitulo =models.CharField(max_length=200, null=True, blank=True)
    descripcion_larga = models.TextField(null=True,blank=True)
    responsable =models.CharField(max_length=200, null=True, blank=True)
    duracion = models.CharField(max_length=255, null=True, blank=True)
    programa_pdf = models.FileField(upload_to='curso_landing/programas/', null=True, blank=True)


    class Meta:
        db_table = 'cursos_landing'
        verbose_name = 'Cursos en Landing'
        verbose_name_plural = 'Cursos en Landing'

    def __str__(self):
        return self.titulo
    
class SesionCurso(models.Model):
    curso = models.ForeignKey(CursoLanding, on_delete=models.CASCADE, related_name='sesiones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    class Meta:
        verbose_name = 'Sesión del Curso'
        verbose_name_plural = 'Sesiones del Curso'

    def __str__(self):
        return self.titulo
    
class Noticia(models.Model):
    titulo = models.CharField(max_length=200, null=True, blank=True)
    imagen = models.ImageField(upload_to='noticias/')


#parte de las resvistas para que se vean bien en la landing
class Revista(models.Model):
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='revistas/')
    pdf = models.FileField(upload_to='revistas_pdfs/')
    fecha_publicacion = models.DateField()

    def __str__(self):
        return self.titulo
