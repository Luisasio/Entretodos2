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
    #urls para facilitadores
    path('inicio-facilitador/', views.inicio_facilitador, name='inicio_facilitador'),
    path('registro-facilitador/', views.registro_facilitador, name='registro_facilitador'),
    path('impartir-cursos/', views.impartir_cursos, name='impartir_cursos'),
    path('impartir/curso/<int:curso_id>/', views.tomar_curso, name='tomar_curso'),
    path('impartir/taller/<int:taller_id>/', views.tomar_taller, name='tomar_taller'),
    path('impartir/diplomado/<int:diplomado_id>/', views.tomar_diplomado, name='tomar_diplomado'),
    path('mis-grupos/', views.mis_grupos, name='mis_grupos'),
    path('mis-grupos/<str:tipo>/<int:id>/alumnos/', views.lista_de_alumnos, name='lista_de_alumnos'),


]

