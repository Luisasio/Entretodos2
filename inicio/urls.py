from django.urls import path
from . import views

urlpatterns = [
  #esto es de la pagina web
    path('', views.index, name='index'),
    #historia web
    path('historia/', views.historia, name='historia'),
    #----------
    #diplomados web
    path('diplomado-desarrollo/', views.diplomado_desarrollo, name='diplomado_desarrollo'),
    path('diplomado_literatura/', views.diplomado_literatura, name='diplomado_literatura'),
    path('diplomado_paz/', views.diplomado_paz, name='diplomado_paz'),
    path('diplomado_tic/', views.diplomado_tic, name='diplomado_tic'),
    #-----------------------
    #talleres web
    path('taller_creacion_literaria/', views.taller_creacion_literaria, name='taller_creacion_literaria'),
    path('taller_cuento/', views.taller_cuento, name='taller_cuento'),
    path('taller_danza/', views.taller_danza, name='taller_danza'),
    path('taller_fotografia/', views.taller_fotografia, name='taller_fotografia'),
    path('taller_huerto/', views.taller_huerto, name='taller_huerto'),
    path('taller_musica_coral/', views.taller_musica_coral, name='taller_musica_coral'),
    path('taller_ofimatica/', views.taller_ofimatica, name='taller_ofimatica'),
    path('taller_pintura/', views.taller_pintura, name='taller_pintura'),
    path('taller_teatro/', views.taller_teatro, name='taller_teatro'),
    #-------------------------------------------
    #Cursos web
    path('curso_cultura_paz/', views.curso_cultura_paz, name='curso_cultura_paz'),
    path('curso_felicidad/', views.curso_felicidad, name='curso_felicidad'),
    path('curso_poesia/', views.curso_poesia, name='curso_poesia'),
    path('curso_rostro_humano/', views.curso_rostro_humano, name='curso_rostro_humano'),
    path('curso_socioemocionales/', views.curso_socioemocionales, name='curso_socioemocionales'),
    path('curso_tic/', views.curso_tic, name='curso_tic'),
    # para enviar el correo
    path('contacto/', views.contacto_view, name='contacto'),







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

