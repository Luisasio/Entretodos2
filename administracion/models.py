from django.db import models

# Create your models here.
from django.db import models

class Alumno(models.Model):
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    correo = models.CharField(max_length=250)
    contrasena = models.CharField(max_length=250)
    telefono = models.BigIntegerField(max_length=10)
    clave = models.CharField(max_length=255, unique=True)
    curp = models.CharField(max_length=255, unique=True)
    sexo = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"  

class Facilitador(models.Model):
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    correo = models.CharField(max_length=250)
    contrasena = models.CharField(max_length=250)
    telefono = models.BigIntegerField(max_length=10)
    clave = models.CharField(max_length=255, unique=True)
    curp = models.CharField(max_length=255, unique=True)
    sexo = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"  

class Periodo(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"{self.fecha_inicio} - {self.fecha_fin}"  

class Curso(models.Model):
    nombre_curso = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    cupos = models.IntegerField(blank=True, null=True)
    grupo = models.CharField(max_length=255)
    facilitador = models.ForeignKey(Facilitador, on_delete=models.CASCADE, null=True, blank=True) 
    periodo = models.ForeignKey(Periodo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre_curso  

class Taller(models.Model):
    nombre_taller = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    grupo = models.CharField(max_length=255)
    facilitador = models.ForeignKey(Facilitador, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_taller  

class Diplomado(models.Model):
    nombre_diplomado = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    grupo = models.CharField(max_length=255)
    facilitador = models.ForeignKey(Facilitador, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_diplomado  

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE, null=True, blank=True)
    diplomado = models.ForeignKey(Diplomado, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.alumno} - {self.estado}"
