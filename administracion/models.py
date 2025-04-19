from django.db import models
import uuid
# Create your models here.
from django.db import models

class Alumno(models.Model):
    clave_alumno = models.CharField(max_length=255, unique=True, null=True, blank=True)
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    correo = models.CharField(max_length=250)
    contrasena = models.CharField(max_length=250)
    telefono = models.BigIntegerField()
    clave = models.CharField(max_length=255, unique=True) # esta es la clave de la escuela
    curp = models.CharField(max_length=255, unique=True)
    sexo = models.CharField(max_length=250)
    restriccion_libre = models.BooleanField(default=False, help_text="Permitir que el alumno se inscriba sin restricciones")


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
    clave = models.CharField(max_length=255, unique=True)
    curp = models.CharField(max_length=255, unique=True)
    sexo = models.CharField(max_length=150)

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
    grupo = models.CharField(max_length=255)
    modalidad = models.CharField(max_length=255,null=True, blank=True)
    duracion = models.IntegerField(blank=True, null=True)
    facilitador = models.ForeignKey(Facilitador, on_delete=models.CASCADE, null=True, blank=True) 
    periodo = models.ForeignKey(Periodo, on_delete=models.SET_NULL, null=True, blank=True)
    publicado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)


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
    grupo = models.CharField(max_length=255)
    modalidad = models.CharField(max_length=255, null=True, blank=True)
    duracion = models.IntegerField(blank=True, null=True)
    facilitador = models.ForeignKey(Facilitador, on_delete=models.CASCADE, null=True, blank=True) 
    periodo = models.ForeignKey(Periodo, on_delete=models.SET_NULL, null=True, blank=True)
    publicado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)


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
    grupo = models.CharField(max_length=255)
    modalidad = models.CharField(max_length=255, null=True, blank=True)
    duracion = models.IntegerField(blank=True, null=True)
    facilitador = models.ForeignKey(Facilitador, on_delete=models.CASCADE, null=True, blank=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)



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
