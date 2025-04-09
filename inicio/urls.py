from django.urls import path
from . import views

urlpatterns = [

  path('', views.index, name='index'),
   path('registro/', views.registro_alumno, name='registro_alumno'),
   path('inicio/', views.inicio, name='inicio'),
    # esto es las url de las inscripciones
     path('inscripciones/', views.inscripciones, name='inscripciones'),
    path('inscribirse/<str:tipo>/<int:id>/', views.inscribirse, name='inscribirse'),
    path('mis-cursos/', views.mis_cursos, name='mis_cursos'),
]

