
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from administracion.models import Alumno
from .serializers import AlumnoLoginSerializer

class AlumnoLoginAPIView(APIView):
    def post(self, request):
        correo = request.data.get('correo')
        contrasena = request.data.get('contrasena')

        try:
            alumno = Alumno.objects.get(correo=correo)

            if check_password(contrasena, alumno.contrasena):
                serializer = AlumnoLoginSerializer(alumno)
                return Response(serializer.data)
            else:
                return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)

        except Alumno.DoesNotExist:
            return Response({'error': 'Correo no encontrado'}, status=status.HTTP_404_NOT_FOUND)



# autenticacion/api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from administracion.models import Inscripcion
from .serializers import InscripcionUnificadaSerializer

class InscripcionesAlumnoAPIView(APIView):
    def get(self, request, alumno_id):
        inscripciones = Inscripcion.objects.filter(alumno_id=alumno_id)
        serializer = InscripcionUnificadaSerializer(inscripciones, many=True)
        return Response(serializer.data)
