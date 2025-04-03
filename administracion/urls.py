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
]