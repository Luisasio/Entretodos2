from functools import wraps
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import RegistroAlumnoForm, RegistroFacilitadorForm
from administracion.models import Alumno, DiplomadoLanding, Facilitador, ModuloDiplomado, Noticia, SesionCurso, SesionTaller, TallerLanding, CursoLanding
from django.db.models import Q
from django.contrib import messages
from administracion.models import Curso, Taller, Inscripcion, Diplomado







#estas son las vistas de la pagina web
def index(request):
    diplomados = DiplomadoLanding.objects.all()
    talleres = TallerLanding.objects.all()
    cursos =CursoLanding.objects.all()
    noticias = Noticia.objects.all()
    return render(request, 'index.html', {
        'diplomados': diplomados,
        'talleres': talleres,
        'cursos': cursos,
        'noticias': noticias
    })

def historia(request):
    return render(request, 'historia.html')

#diplomados
def diplomado_desarrollo(request):
    return render(request, 'diplomado_desarrollo.html')

def diplomado_literatura(request):
    return render(request, 'diplomado_literatura.html')

def diplomado_paz(request):
    return render(request, 'diplomado_paz.html')

def diplomado_tic(request):
    return render(request, 'diplomado_tic.html')
#-------------------
#talleres
def taller_creacion_literaria(request):
    return render(request, 'taller_creacion_literaria.html')
def taller_cuento(request):
    return render(request, 'taller_cuento.html')
def taller_danza(request):
    return render(request, 'taller_danza.html')
def taller_fotografia(request):
    return render(request, 'taller_fotografia.html')
def taller_huerto(request):
    return render(request, 'taller_huerto.html')
def taller_musica_coral(request):
    return render(request, 'taller_musica_coral.html')
def taller_ofimatica(request):
    return render(request, 'taller_ofimatica.html')
def taller_pintura(request):
    return render(request, 'taller_pintura.html')
def taller_teatro(request):
    return render(request, 'taller_teatro.html')
#-----------------------
#cursos
def curso_cultura_paz(request):
    return render(request, 'curso_cultura_paz.html')
def curso_felicidad(request):
    return render(request, 'curso_felicidad.html')
def curso_poesia(request):
    return render(request, 'curso_poesia.html')
def curso_rostro_humano(request):
    return render(request, 'curso_rostro_humano.html')
def curso_socioemocionales(request):
    return render(request, 'curso_socioemocionales.html')
def curso_tic(request):
    return render(request, 'curso_tic.html')


# esto es la validacion del conflicto de horario en la parte de la vista del facilitador

def conflicto_horario_facilitador(nuevo, facilitador):
    from administracion.models import Curso, Taller, Diplomado

    # Obtener todos los cursos, talleres y diplomados del facilitador, excluyendo el actual si ya existe
    cursos = Curso.objects.filter(facilitador=facilitador).exclude(id=getattr(nuevo, 'id', None))
    talleres = Taller.objects.filter(facilitador=facilitador).exclude(id=getattr(nuevo, 'id', None))
    diplomados = Diplomado.objects.filter(facilitador=facilitador).exclude(id=getattr(nuevo, 'id', None))

    for existente in list(cursos) + list(talleres) + list(diplomados):
        if not set(nuevo.dias).intersection(set(existente.dias or [])):
            continue
        if nuevo.hora_inicio < existente.hora_fin and existente.hora_inicio < nuevo.hora_fin:
            return True
    return False





  
#esta vista es para el registro de alumnos
def registro_alumno(request):
    if request.method == 'POST':
        form = RegistroAlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login_alumno')
    else:
        form = RegistroAlumnoForm()
    return render(request, 'registro.html', {'form': form})

def inicio(request):
    alumno_id = request.session.get("alumno_id")
    if not alumno_id:
        return redirect('login_alumno')

    alumno = Alumno.objects.get(id=alumno_id)

    inscripciones = Inscripcion.objects.filter(
        alumno=alumno,
        estado='Inscrito'
    ).filter(Q(curso__isnull=False) | Q(taller__isnull=False) | Q(diplomado__isnull=False))

    return render(request, 'inicio.html', {
        'alumno': alumno,
        'inscripciones': inscripciones,
    })


# esta es la parte para que el alumno vea la parte de los cursos y talleres
def inscripciones(request):
    alumno_id = request.session.get("alumno_id")
    if not alumno_id:
        return redirect('login_alumno')

    alumno = Alumno.objects.get(id=alumno_id)
    inscripciones = Inscripcion.objects.filter(alumno_id=alumno_id, estado="Inscrito")

    # Listado de cursos/talleres/diplomados ya inscritos
    inscritos_cursos = inscripciones.filter(curso__isnull=False).values_list('curso_id', flat=True)
    inscritos_talleres = inscripciones.filter(taller__isnull=False).values_list('taller_id', flat=True)
    inscritos_diplomados = inscripciones.filter(diplomado__isnull=False).values_list('diplomado_id', flat=True)

    query = request.GET.get('q', '')

    # Función local para filtrar sin conflicto
    def sin_conflicto(queryset):
        resultado = []
        for nuevo in queryset:
            conflicto = False
            for ins in inscripciones:
                actual = ins.curso or ins.taller or ins.diplomado
                if nuevo.dias and set(nuevo.dias).intersection(actual.dias or []):
                    if nuevo.hora_inicio < actual.hora_fin and actual.hora_inicio < nuevo.hora_fin:
                        conflicto = True
                        break
            if not conflicto:
                resultado.append(nuevo)
        return resultado

    cursos = Curso.objects.filter(publicado=True, cupos__gt=0, finalizado=False)\
        .exclude(id__in=inscritos_cursos)
    if query:
        cursos = cursos.filter(Q(nombre_curso__icontains=query) | Q(grupo__icontains=query))
    cursos = sin_conflicto(cursos)

    talleres = Taller.objects.filter(publicado=True, cupos__gt=0, finalizado=False)\
        .exclude(id__in=inscritos_talleres)
    if query:
        talleres = talleres.filter(Q(nombre_taller__icontains=query) | Q(grupo__icontains=query))
    talleres = sin_conflicto(talleres)

    diplomados = Diplomado.objects.filter(publicado=True, cupos__gt=0, finalizado=False)\
        .exclude(id__in=inscritos_diplomados)
    if query:
        diplomados = diplomados.filter(Q(nombre_diplomado__icontains=query) | Q(grupo__icontains=query))
    diplomados = sin_conflicto(diplomados)

    tiene_curso_o_taller = inscripciones.filter(Q(curso__isnull=False) | Q(taller__isnull=False)).exists()
    tiene_diplomado = inscripciones.filter(diplomado__isnull=False).exists()
    bloqueado = not alumno.restriccion_libre and tiene_curso_o_taller and tiene_diplomado

    return render(request, 'inscripciones.html', {
        'alumno': alumno,
        'cursos': cursos,
        'talleres': talleres,
        'diplomados': diplomados,
        'tiene_curso_o_taller': tiene_curso_o_taller,
        'tiene_diplomado': tiene_diplomado,
        'bloqueado': bloqueado,
        'query': query
    })


# parte de la validacion que dijo luis "Verificar que el alumno no tenga choques de horarios"

def hay_conflicto_horario(inscripcion_existente, nuevo, dias_nuevo):
    dias_existente = inscripcion_existente.dias or []
    
    # Verifica si hay al menos un día en común
    if not set(dias_existente).intersection(dias_nuevo):
        return False

    # Verifica cruce de horas
    return (
        nuevo.hora_inicio < inscripcion_existente.hora_fin and
        inscripcion_existente.hora_inicio < nuevo.hora_fin
    )


# esto es para que el alumno se inscriba es decir la logica
def inscribirse(request, tipo, id):
    alumno_id = request.session.get("alumno_id")
    if not alumno_id:
        return redirect('login_alumno')

    alumno = Alumno.objects.get(id=alumno_id)
    inscripciones = Inscripcion.objects.filter(alumno_id=alumno_id)

    if not alumno.restriccion_libre:
        tiene_curso_o_taller = inscripciones.filter(
            estado__iexact="Inscrito"
        ).filter(Q(curso__isnull=False) | Q(taller__isnull=False)).exists()

        tiene_diplomado = inscripciones.filter(
            estado__iexact="Inscrito", diplomado__isnull=False
        ).exists()

        if tiene_curso_o_taller and tipo in ['curso', 'taller']:
            messages.warning(request, "Ya estás inscrito a un curso o taller. Solo puedes inscribirte a un diplomado.")
            return redirect('inscripciones')

        if tiene_diplomado and tipo == 'diplomado':
            messages.warning(request, "Ya estás inscrito a un diplomado. No puedes inscribirte a otro.")
            return redirect('inscripciones')

        if tiene_diplomado and tiene_curso_o_taller:
            messages.warning(request, "Ya estás inscrito a un diplomado y un curso/taller. No puedes inscribirte a más.")
            return redirect('inscripciones')

    # PASA LA REGLA → inscribirse
    if tipo == 'curso':
        curso = Curso.objects.get(id=id)

        # Validación de conflicto de horario y días
        for ins in inscripciones.filter(estado="Inscrito"):
            existente = ins.curso or ins.taller or ins.diplomado
            if hay_conflicto_horario(existente, curso, curso.dias):
                messages.error(request, "Conflicto de horario y días con otra inscripción activa.")
                return redirect('inscripciones')

        if not curso.facilitador:
            messages.error(request, "Este curso aún no tiene un facilitador asignado.")
            return redirect('inscripciones')
        if curso.cupos and curso.cupos > 0:
            Inscripcion.objects.create(alumno_id=alumno_id, curso=curso, estado="Inscrito")
            curso.cupos -= 1
            curso.save()
        else:
            messages.error(request, "El curso ya no tiene cupos disponibles.")
            return redirect('inscripciones')

    elif tipo == 'taller':
        taller = Taller.objects.get(id=id)

        # Validación de conflicto de horario y días
        for ins in inscripciones.filter(estado="Inscrito"):
            existente = ins.curso or ins.taller or ins.diplomado
            if hay_conflicto_horario(existente, taller, taller.dias):
                messages.error(request, "Conflicto de horario y días con otra inscripción activa.")
                return redirect('inscripciones')

        if not taller.facilitador:
            messages.error(request, "Este taller aún no tiene un facilitador asignado.")
            return redirect('inscripciones')
        if taller.cupos and taller.cupos > 0:
            Inscripcion.objects.create(alumno_id=alumno_id, taller=taller, estado="Inscrito")
            taller.cupos -= 1
            taller.save()
        else:
            messages.error(request, "El taller ya no tiene cupos disponibles.")
            return redirect('inscripciones')

    elif tipo == 'diplomado':
        diplomado = Diplomado.objects.get(id=id)

        # Validación de conflicto de horario y días
        for ins in inscripciones.filter(estado="Inscrito"):
            existente = ins.curso or ins.taller or ins.diplomado
            if hay_conflicto_horario(existente, diplomado, diplomado.dias):
                messages.error(request, "Conflicto de horario y días con otra inscripción activa.")
                return redirect('inscripciones')

        if not diplomado.facilitador:
            messages.error(request, "Este diplomado aún no tiene un facilitador asignado.")
            return redirect('inscripciones')
        if diplomado.cupos and diplomado.cupos > 0:
            Inscripcion.objects.create(alumno_id=alumno_id, diplomado=diplomado, estado="Inscrito")
            diplomado.cupos -= 1
            diplomado.save()
        else:
            messages.error(request, "El diplomado ya no tiene cupos disponibles.")
            return redirect('inscripciones')

    messages.success(request, "¡Inscripción exitosa!")
    return redirect('mis_cursos')



#esto es para ver los cursos inscitos:
def mis_cursos(request):
    alumno_id = request.session.get("alumno_id")
    if not alumno_id:
        return redirect('login_alumno')

    inscripciones = Inscripcion.objects.filter(alumno_id=alumno_id)

    alumno = Alumno.objects.get(id=alumno_id)

    return render(request, 'mis_cursos.html', {
        'inscripciones': inscripciones,
        'alumno': alumno
    })


def cargar_facilitador(vista_funcion):
    @wraps(vista_funcion)
    def funcion_envuelta(request, *args, **kwargs):
        facilitador_id = request.session.get("facilitador_id")
        if not facilitador_id:
            return redirect('login_facilitador')  # Asegúrate que esta URL exista

        try:
            facilitador = Facilitador.objects.get(id=facilitador_id)
        except Facilitador.DoesNotExist:
            return redirect('login_facilitador')

        request.facilitador = facilitador  # Puedes acceder desde request en la vista si lo necesitas

        # Ejecuta la vista pasando el contexto automáticamente
        response = vista_funcion(request, *args, **kwargs)
        if isinstance(response, dict):  # Si la vista retorna un dict, agregamos el facilitador
            response.setdefault('facilitador', facilitador)
            return render(request, response.pop('template'), response)
        return response

    return funcion_envuelta


def inicio_facilitador(request):
    facilitador_id = request.session.get("facilitador_id")
    if not facilitador_id:
        return redirect('login_facilitador')

    facilitador = Facilitador.objects.get(id=facilitador_id)

    cursos = Curso.objects.filter(facilitador=facilitador)
    talleres = Taller.objects.filter(facilitador=facilitador)
    diplomados = Diplomado.objects.filter(facilitador=facilitador)

    return render(request, 'inicio_facilitador.html', {
        'facilitador': facilitador,
        'cursos': cursos,
        'talleres': talleres,
        'diplomados': diplomados
    })

def registro_facilitador(request):
    if request.method == 'POST':
        form = RegistroFacilitadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login_facilitador')
    else:
        form = RegistroFacilitadorForm()
    return render(request, 'registro_facilitador.html', {'form': form})


@cargar_facilitador
def impartir_cursos(request):
    query = request.GET.get('q', '')
    facilitador = request.facilitador

    cursos = Curso.objects.filter(facilitador__isnull=True, publicado=True, finalizado=False)
    talleres = Taller.objects.filter(facilitador__isnull=True, publicado=True, finalizado=False)
    diplomados = Diplomado.objects.filter(facilitador__isnull=True, publicado=True, finalizado=False)

    # Obtener asignaciones actuales
    cursos_asignados = Curso.objects.filter(facilitador=facilitador)
    talleres_asignados = Taller.objects.filter(facilitador=facilitador)
    diplomados_asignados = Diplomado.objects.filter(facilitador=facilitador)

    asignados = list(cursos_asignados) + list(talleres_asignados) + list(diplomados_asignados)

    # Función para detectar conflicto
    def hay_conflicto(nuevo):
        for existente in asignados:
            if not set(nuevo.dias).intersection(set(existente.dias or [])):
                continue
            if nuevo.hora_inicio < existente.hora_fin and existente.hora_inicio < nuevo.hora_fin:
                return True
        return False

    # Aplicar el filtro
    cursos = [c for c in cursos if not hay_conflicto(c)]
    talleres = [t for t in talleres if not hay_conflicto(t)]
    diplomados = [d for d in diplomados if not hay_conflicto(d)]

    # Filtrar por búsqueda si hay query
    if query:
        cursos = [c for c in cursos if query.lower() in c.nombre_curso.lower() or query.lower() in c.grupo.lower()]
        talleres = [t for t in talleres if query.lower() in t.nombre_taller.lower() or query.lower() in t.grupo.lower()]
        diplomados = [d for d in diplomados if query.lower() in d.nombre_diplomado.lower() or query.lower() in d.grupo.lower()]

    return render(request, 'impartir_cursos.html', {
        'cursos': cursos,
        'talleres': talleres,
        'diplomados': diplomados,
        'facilitador': facilitador,
        'query': query
    })



@cargar_facilitador
def tomar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, facilitador__isnull=True)
    if conflicto_horario_facilitador(curso, request.facilitador):
        messages.error(request, "Ya tienes asignado otro grupo con un horario o día que se empalma.")
        return redirect('impartir_cursos')

    curso.facilitador = request.facilitador
    curso.save()
    messages.success(request, "Curso asignado correctamente.")
    return redirect('impartir_cursos')


@cargar_facilitador
def tomar_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id, facilitador__isnull=True)

    if conflicto_horario_facilitador(taller, request.facilitador):
        messages.error(request, "Ya tienes asignado otro grupo con un horario o día que se empalma.")
        return redirect('impartir_cursos')

    taller.facilitador = request.facilitador
    taller.save()
    messages.success(request, "Taller asignado correctamente.")
    return redirect('impartir_cursos')

@cargar_facilitador
def tomar_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id, facilitador__isnull=True)

    if conflicto_horario_facilitador(diplomado, request.facilitador):
        messages.error(request, "Ya tienes asignado otro grupo con un horario o día que se empalma.")
        return redirect('impartir_cursos')

    diplomado.facilitador = request.facilitador
    diplomado.save()
    messages.success(request, "Diplomado asignado correctamente.")
    return redirect('impartir_cursos')



@cargar_facilitador
def mis_grupos(request):
    facilitador_id = request.session.get('facilitador_id')

    cursos = Curso.objects.filter(facilitador_id=facilitador_id)
    talleres = Taller.objects.filter(facilitador_id=facilitador_id)
    diplomados = Diplomado.objects.filter(facilitador_id=facilitador_id)

    return render(request, 'mis_grupos.html', {
        'cursos': cursos,
        'talleres': talleres,
        'diplomados': diplomados,
        'facilitador': request.facilitador

    })
@cargar_facilitador
def lista_de_alumnos(request, tipo, id):
    if tipo == 'curso':
        grupo = get_object_or_404(Curso, id=id, facilitador=request.facilitador)
        inscripciones = Inscripcion.objects.filter(curso=grupo)
        nombre = grupo.nombre_curso
    elif tipo == 'taller':
        grupo = get_object_or_404(Taller, id=id, facilitador=request.facilitador)
        inscripciones = Inscripcion.objects.filter(taller=grupo)
        nombre = grupo.nombre_taller
    elif tipo == 'diplomado':
        grupo = get_object_or_404(Diplomado, id=id, facilitador=request.facilitador)
        inscripciones = Inscripcion.objects.filter(diplomado=grupo)
        nombre = grupo.nombre_diplomado
    else:
        return redirect('mis_grupos_facilitador')

    return render(request, 'lista_de_alumnos.html', {
        'inscripciones': inscripciones,
        'grupo': grupo.grupo,
        'nombre': nombre,
        'tipo': tipo
    })


#esto es simplemente para que se envie el correo
from django.core.mail import send_mail

def contacto_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        cuerpo = f"""
        Nuevo mensaje de contacto:
        
        Nombre: {nombre} {apellido}
        Correo: {email}
        
        Mensaje:
        {mensaje}
        """

        send_mail(
            subject='Mensaje desde formulario de contacto',
            message=cuerpo,
            from_email=email,
            recipient_list=['correopruebadjango196@gmail.com'],  # puede ser tu propio correo
            fail_silently=False,
        )

        messages.success(request, 'Tu mensaje fue enviado correctamente.')
        return redirect('index')  # o la ruta que corresponda

    return render(request, 'index.html')  # si es solo render normal


def diplomado_detalle(request, id):
    diplomado = get_object_or_404(DiplomadoLanding, id=id)
    modulos = ModuloDiplomado.objects.filter(diplomado=diplomado)
    
    return render(request, 'diplomado_detalles.html', {
        'diplomado': diplomado,
        'modulos': modulos
    })

def taller_detalle(request,id):
    taller = get_object_or_404(TallerLanding, id=id)
    sesiones = SesionTaller.objects.filter(taller=taller)

    return render(request, 'taller_detalles.html', {
        'taller': taller,
        'sesiones' : sesiones
    })

def curso_detalles(request,id):
    curso = get_object_or_404(CursoLanding, id = id)
    sesiones = SesionCurso.objects.filter(curso=curso)

    return render(request, 'curso_detalles.html', {
        'curso': curso,
        'sesiones' : sesiones
    })