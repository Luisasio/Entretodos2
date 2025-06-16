from rest_framework import serializers
from administracion.models import Alumno

class AlumnoLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['id', 'nombres', 'apellido_paterno', 'apellido_materno', 'correo', 'curp', 'clave_alumno']







from rest_framework import serializers
from administracion.models import Inscripcion



class InscripcionUnificadaSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()
    descripcion = serializers.SerializerMethodField()
    fecha_inicio = serializers.SerializerMethodField()
    fecha_fin = serializers.SerializerMethodField()
    facilitador = serializers.SerializerMethodField()
    dias = serializers.SerializerMethodField()
    hora_inicio = serializers.SerializerMethodField()
    hora_fin = serializers.SerializerMethodField()

    class Meta:
        model = Inscripcion
        fields = [
            'tipo', 'nombre', 'descripcion',
            'fecha_inicio', 'fecha_fin',
            'facilitador', 'dias', 'hora_inicio', 'hora_fin',
            'estado'
        ]

    def get_tipo(self, obj):
        if obj.curso:
            return "Curso"
        elif obj.taller:
            return "Taller"
        elif obj.diplomado:
            return "Diplomado"
        return "Desconocido"

    def get_nombre(self, obj):
        return obj.curso.nombre_curso if obj.curso else (
               obj.taller.nombre_taller if obj.taller else (
               obj.diplomado.nombre_diplomado if obj.diplomado else ''))

    def get_descripcion(self, obj):
        return obj.curso.descripcion if obj.curso else (
               obj.taller.descripcion if obj.taller else (
               obj.diplomado.descripcion if obj.diplomado else ''))

    def get_fecha_inicio(self, obj):
        return obj.curso.fecha_inicio if obj.curso else (
               obj.taller.fecha_inicio if obj.taller else (
               obj.diplomado.fecha_inicio if obj.diplomado else None))

    def get_fecha_fin(self, obj):
        return obj.curso.fecha_fin if obj.curso else (
               obj.taller.fecha_fin if obj.taller else (
               obj.diplomado.fecha_fin if obj.diplomado else None))

    def get_facilitador(self, obj):
        f = obj.curso.facilitador if obj.curso else (
            obj.taller.facilitador if obj.taller else (
            obj.diplomado.facilitador if obj.diplomado else None))
        return f"{f.nombres} {f.apellido_paterno} {f.apellido_materno}" if f else "Sin asignar"

    def get_dias(self, obj):
        if obj.curso:
            return obj.curso.dias
        elif obj.taller:
            return obj.taller.dias
        elif obj.diplomado:
            return obj.diplomado.dias
        return []

    def get_hora_inicio(self, obj):
        if obj.curso:
            return obj.curso.hora_inicio
        elif obj.taller:
            return obj.taller.hora_inicio
        elif obj.diplomado:
            return obj.diplomado.hora_inicio
        return None

    def get_hora_fin(self, obj):
        if obj.curso:
            return obj.curso.hora_fin
        elif obj.taller:
            return obj.taller.hora_fin
        elif obj.diplomado:
            return obj.diplomado.hora_fin
        return None
