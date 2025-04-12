from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cursos/', views.cursos, name='cursos'),
    path('facilitadores', views.facilitadores, name = 'facilitadores'),
    path('cursos/agregar/', views.agregar_curso, name='agregar_curso'),
    path('periodos/', views.periodos, name='periodos'),
    path('periodos/agregar/', views.agregar_periodo, name='agregar_periodo'),
    path('periodos/editar/<int:periodo_id>/', views.editar_periodo, name='editar_periodo'),
    path('periodos/eliminar/<int:periodo_id>/', views.eliminar_periodo, name='eliminar_periodo'),
    path('cursos/editar/<int:curso_id>/', views.editar_curso, name='editar_curso'),
    path('cursos/eliminar/<int:curso_id>/', views.eliminar_curso, name='eliminar_curso'),
    path('talleres/', views.talleres, name='talleres'),
    path('talleres/agregar/', views.agregar_taller, name='agregar_taller'),
    path('talleres/editar/<int:taller_id>/', views.editar_taller, name='editar_taller'),
    path('talleres/eliminar/<int:taller_id>/', views.eliminar_taller, name='eliminar_taller'),
    path('diplomados/', views.diplomados, name='diplomados'),
    path('diplomados/agregar/', views.agregar_diplomado, name='agregar_diplomado'),
    path('diplomados/editar/<int:diplomado_id>/', views.editar_diplomado, name='editar_diplomado'),
    path('diplomados/eliminar/<int:diplomado_id>/', views.eliminar_diplomado, name='eliminar_diplomado'),
    path('alumnos/', views.alumnos, name='alumnos'),
    path('alumnos/agregar/', views.agregar_alumno, name='agregar_alumno'),
    path('alumnos/<int:alumno_id>/editar/', views.editar_alumno, name='editar_alumno'),
    path('alumnos/<int:alumno_id>/eliminar/', views.eliminar_alumno, name='eliminar_alumno'),


    # url para la publicacion de cursos y talleres
    path('publicar-curso/<int:curso_id>/', views.publicar_curso, name='publicar_curso'),
    path('publicar-taller/<int:taller_id>/', views.publicar_taller, name='publicar_taller'),
    path ('publicar-diplomado/<int:diplomado_id>/', views.publicar_diplomado, name='publicar_diplomado'),
    # esto es para despublicarlo
    path('despublicar-curso/<int:curso_id>/', views.despublicar_curso, name='despublicar_curso'),
    path('despublicar-taller/<int:taller_id>/', views.despublicar_taller, name='despublicar_taller'),
    path('despublicar-diplomado/<int:diplomado_id>/', views.despublicar_diplomado, name='despublicar_diplomado'),
]