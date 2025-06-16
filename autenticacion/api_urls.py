

from django.urls import path
from .api_views import AlumnoLoginAPIView
from .api_views import InscripcionesAlumnoAPIView

urlpatterns = [
    path('alumno/login/', AlumnoLoginAPIView.as_view()),
    path('alumno/<int:alumno_id>/inscripciones/', InscripcionesAlumnoAPIView.as_view()),
]
