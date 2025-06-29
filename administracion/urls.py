from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('facilitadores', views.facilitadores, name = 'facilitadores'),
    path('periodos/', views.periodos, name='periodos'),
    #periodos
    path('periodos/agregar/', views.agregar_periodo, name='agregar_periodo'),
    path('periodos/editar/<int:periodo_id>/', views.editar_periodo, name='editar_periodo'),
    # path('periodos/eliminar/<int:periodo_id>/', views.eliminar_periodo, name='eliminar_periodo'),
    path('periodos/suprimir/<int:periodo_id>/', views.suprimir_periodo, name='suprimir_periodo'),

    #cursos
    path('cursos/', views.cursos, name='cursos'),
    path('cursos/agregar/', views.agregar_curso, name='agregar_curso'),
    path('cursos/editar/<int:curso_id>/', views.editar_curso, name='editar_curso'),
    path('cursos/eliminar/<int:curso_id>/', views.eliminar_curso, name='eliminar_curso'),
    path('cursos/<int:curso_id>/finalizar/', views.finalizar_curso, name='finalizar_curso'),
    path('cursos/finalizados/', views.cursos_finalizados, name='cursos_finalizados'),
    #talleres
    path('talleres/', views.talleres, name='talleres'),
    path('talleres/agregar/', views.agregar_taller, name='agregar_taller'),
    path('talleres/editar/<int:taller_id>/', views.editar_taller, name='editar_taller'),
    path('talleres/eliminar/<int:taller_id>/', views.eliminar_taller, name='eliminar_taller'),
    path('talleres/<int:taller_id>/finalizar/', views.finalizar_taller, name='finalizar_taller'),
    path('talleres-finalizados/', views.talleres_finalizados, name='talleres_finalizados'),

    #diplomados
    path('diplomados/', views.diplomados, name='diplomados'),
    path('diplomados/agregar/', views.agregar_diplomado, name='agregar_diplomado'),
    path('diplomados/editar/<int:diplomado_id>/', views.editar_diplomado, name='editar_diplomado'),
    path('diplomados/eliminar/<int:diplomado_id>/', views.eliminar_diplomado, name='eliminar_diplomado'),
    path('diplomados/<int:diplomado_id>/finalizar/', views.finalizar_diplomado, name='finalizar_diplomado'),
    path('diplomados-finalizados/', views.diplomados_finalizados, name='diplomados_finalizados'),

    #alumnos
    path('alumnos/', views.alumnos, name='alumnos'),
    path('alumnos/agregar/', views.agregar_alumno, name='agregar_alumno'),
    path('alumnos/<int:alumno_id>/editar/', views.editar_alumno, name='editar_alumno'),
    # path('alumnos/<int:alumno_id>/eliminar/', views.eliminar_alumno, name='eliminar_alumno'),
    path('alumnos/suprimir/<int:alumno_id>/', views.suprimir_alumno, name='suprimir_alumno'),

    path('alumnos/<int:alumno_id>/historial/', views.historial_alumno, name='historial_alumno'),

    # facilitadores
    path('facilitadores/agregar/', views.agregar_facilitador, name='agregar_facilitador'),
    path('facilitadores/', views.lista_facilitadores, name='facilitadores'),
    path('facilitadores/editar/<int:facilitador_id>/', views.editar_facilitador, name='editar_facilitador'),
    path('facilitadores/suprimir/<int:facilitador_id>/', views.suprimir_facilitador, name='suprimir_facilitador'),
    path('grupos/', views.grupos, name='grupos'),



    

    # inscripciones
    path('inscripciones_admin/', views.inscripciones_admin, name='inscripciones_admin'),
    path('inscripciones_admin/ver-cursos/', views.ver_cursos, name='ver_cursos'),
    path('inscripciones_admin/ver-talleres/', views.ver_talleres, name='ver_talleres'),
    path('inscripciones_admin/ver-diplomados/', views.ver_diplomados, name='ver_diplomados'),
    path('cursos/<int:curso_id>/alumnos/', views.ver_alumnos_curso, name='ver_alumnos_curso'),
    path('talleres/<int:taller_id>/alumnos/', views.ver_alumnos_taller, name='ver_alumnos_taller'),
    path('diplomados/<int:diplomado_id>/alumnos/', views.ver_alumnos_diplomado, name='ver_alumnos_diplomado'),
    path('inscripciones/<int:inscripcion_id>/baja/', views.dar_de_baja_curso, name='dar_de_baja_curso'),
    path('inscripciones/<int:inscripcion_id>/baja-taller/', views.dar_de_baja_taller, name='dar_de_baja_taller'),
    path('inscripciones/<int:inscripcion_id>/baja-diplomado/', views.dar_de_baja_diplomado, name='dar_de_baja_diplomado'),
    path('cursos/<int:curso_id>/alumnos/alta/', views.dar_de_alta_alumno_curso, name='dar_de_alta_alumno'),
    path('talleres/<int:taller_id>/alumnos/alta/', views.dar_de_alta_alumno_taller, name='dar_de_alta_alumno_taller'),
    path('diplomados/<int:diplomado_id>/alumnos/alta/', views.dar_de_alta_alumno_diplomado, name='dar_de_alta_alumno_diplomado'),
    path('cursos/<int:curso_id>/alumnos/<int:alumno_id>/inscribir/', views.alta_alumno_curso, name='alta_alumno_curso'),
    path('talleres/<int:taller_id>/alumnos/<int:alumno_id>/inscribir/', views.alta_alumno_taller, name='alta_alumno_taller'),
    path('diplomados/<int:diplomado_id>/alumnos/<int:alumno_id>/inscribir/', views.alta_alumno_diplomado, name='alta_alumno_diplomado'),
    path('alumnos/<int:alumno_id>/toggle-restriccion/', views.toggle_restriccion_alumno, name='toggle_restriccion_alumno'),
    path('cursos/<int:curso_id>/descargar/', views.descargar_lista_alumnos_curso, name='descargar_lista_curso'),
    path('talleres/<int:taller_id>/descargar/', views.descargar_lista_alumnos_taller, name='descargar_lista_taller'),
    path('diplomados/<int:diplomado_id>/descargar/', views.descargar_lista_alumnos_diplomado, name='descargar_lista_diplomado'),

    #admin
    path('administrador/', views.administrador, name = 'administrador'),
    path('administrador/agregar-admin', views.agregar_admin, name = 'agregar_admin'),
    path('cambiar-contrasena/', views.CambiarContrasenaView.as_view(), name='cambiar_contrasena'),


    #publicaciones
    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('publicaciones/cursos/', views.publicaciones_cursos, name='publicaciones_cursos'),
    path('publicaciones/cursos/agregar-diplomado/', views.agregar_diplomado_inicio, name='agregar_diplomado_inicio'),
    path('publicaciones/cursos/agregar-taller/', views.agregar_taller_inicio, name='agregar_taller_inicio'),
    path('publicaciones/cursos/agregar-curso/', views.agregar_curso_inicio, name='agregar_curso_inicio'),
    path('publicaciones/noticias', views.publicaciones_noticias, name= 'publicaciones_noticias'),
    path('publicaciones/agregar-noticia/', views.agregar_noticia, name='agregar_noticia'),
    path('noticias/editar/<int:pk>/', views.editar_noticia, name='editar_noticia'),
    path('noticias/eliminar/<int:pk>/', views.eliminar_noticia, name='eliminar_noticia'),



    #editar publicaciones
    path('diplomados-landing/<int:pk>/editar/', views.editar_diplomado_landing, name='editar_diplomado_landing'),
    path('talleres-landing/editar/<int:pk>/', views.editar_taller_inicio, name='editar_taller_inicio'),
    path('cursos-landing/editar/<int:pk>/', views.editar_curso_inicio, name='editar_curso_inicio'),


    #eliminar publicaciones
    path('diplomados-landing/eliminar/<int:pk>/', views.eliminar_diplomado_landing, name='eliminar_diplomado_landing'),
    path('talleres-landing/eliminar/<int:pk>/', views.eliminar_taller_inicio, name='eliminar_taller_inicio'),
    path('cursos-landing/eliminar/<int:pk>/', views.eliminar_curso_inicio, name='eliminar_curso_inicio'),



    #esto es parte de la landing para que haya un apartado donde te lleve a las revistas
    path('revistas/', views.publicaciones_revistas, name='publicaciones_revistas'),

    # Agregar una nueva revista
    path('revistas/agregar/', views.agregar_revista, name='agregar_revista'),

    # Editar una revista
    path('revistas/editar/<int:revista_id>/', views.editar_revista, name='editar_revista'),

    # Eliminar una revista
    path('revistas/eliminar/<int:revista_id>/', views.eliminar_revista, name='eliminar_revista'),











    # url para la publicacion de cursos y talleres
    path('publicar-curso/<int:curso_id>/', views.publicar_curso, name='publicar_curso'),
    path('publicar-taller/<int:taller_id>/', views.publicar_taller, name='publicar_taller'),
    path ('publicar-diplomado/<int:diplomado_id>/', views.publicar_diplomado, name='publicar_diplomado'),
    # esto es para despublicarlo
    path('despublicar-curso/<int:curso_id>/', views.despublicar_curso, name='despublicar_curso'),
    path('despublicar-taller/<int:taller_id>/', views.despublicar_taller, name='despublicar_taller'),
    path('despublicar-diplomado/<int:diplomado_id>/', views.despublicar_diplomado, name='despublicar_diplomado'),


]