from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cursos/', views.cursos, name='cursos'),
    path('cursos/agregar/', views.agregar_curso, name='agregar_curso'),
    path('periodos/', views.periodos, name='periodos'),
    path('periodos/agregar/', views.agregar_periodo, name='agregar_periodo'),
    path('cursos/editar/<int:curso_id>/', views.editar_curso, name='editar_curso'),
    path('cursos/eliminar/<int:curso_id>/', views.eliminar_curso, name='eliminar_curso'),
]