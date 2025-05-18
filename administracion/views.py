from datetime import datetime
from io import BytesIO
from django.contrib import messages
from django.http import FileResponse
from reportlab.lib.pagesizes import letter, landscape
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, Q
from reportlab.pdfgen import canvas

from administracion.forms import CursoForm, DiplomadoForm, PeriodoForm, RegisterForm, TallerForm, EditarCursoForm, EditarTallerForm, EditarDiplomadoForm
from administracion.models import Alumno, Inscripcion, Periodo, Taller, Diplomado,Facilitador
from administracion.models import Curso
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from inicio.forms import EditarAlumnoForm, RegistroAlumnoForm, RegistroFacilitadorForm,EditarFacilitadorForm


# esto es para la validacion del admin al querer agregar un facilitador que choquen sus horarios
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


# --------------------------------------------------------------------------------------------------

#validacion de la sede y el aula, que no sea en el mismo lugar, 4 validaciones, la hora, el aula, la fecha y el lugar
from django.db.models import Q

def conflicto_salon_presencial(nuevo):
    if nuevo.modalidad != 'presencial':
        return False

    cursos = Curso.objects.filter(modalidad='presencial', lugar__iexact=nuevo.lugar.strip(), aula__iexact=nuevo.aula.strip())
    talleres = Taller.objects.filter(modalidad='presencial', lugar__iexact=nuevo.lugar.strip(), aula__iexact=nuevo.aula.strip())
    diplomados = Diplomado.objects.filter(modalidad='presencial', lugar__iexact=nuevo.lugar.strip(), aula__iexact=nuevo.aula.strip())

    grupos = list(cursos) + list(talleres) + list(diplomados)

    for existente in grupos:
        if not set(nuevo.dias).intersection(set(existente.dias or [])):
            continue
        if nuevo.hora_inicio < existente.hora_fin and existente.hora_inicio < nuevo.hora_fin:
            return True
    return False






# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'administracion/dashboard.html')


def cursos(request):
    cursos = Curso.objects.filter(finalizado=False)  # Solo cursos activos
    return render(request, 'administracion/cursos.html', {'cursos': cursos})


def facilitadores(request):
    return render(request, 'administracion/facilitadores.html')

def agregar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            facilitador = nuevo.facilitador

            if conflicto_salon_presencial(nuevo):
                messages.error(request, "Ya existe un grupo presencial con el mismo lugar, aula y horario.")
            elif facilitador and conflicto_horario_facilitador(nuevo, facilitador):
                messages.error(request, "El facilitador ya tiene asignado otro grupo con un horario o día que se empalma.")
            else:
                nuevo.save()
                messages.success(request, "Curso creado exitosamente.")
                return redirect('cursos')
    else:
        form = CursoForm()

    periodos = Periodo.objects.all()
    return render(request, 'administracion/agregar_curso.html', {
        'form': form,
        'periodos_data': [
            {
                'id': p.id,
                'inicio': p.fecha_inicio.strftime('%Y-%m-%d'),
                'fin': p.fecha_fin.strftime('%Y-%m-%d'),
            } for p in periodos
        ]
    })




def periodos(request):
    periodos = Periodo.objects.all()  # Obtener todos los periodos
    return render(request, 'administracion/periodos.html', {'periodos': periodos})

def agregar_periodo(request):
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('periodos')  # Redirige a la lista de periodos
    else:
        form = PeriodoForm()
    
    return render(request, 'administracion/agregar_periodo.html', {'form': form})

def editar_periodo(request, periodo_id):
    periodo = get_object_or_404(Periodo, id=periodo_id)
    
    if request.method == 'POST':
        form = PeriodoForm(request.POST, instance=periodo)
        if form.is_valid():
            form.save()
            return redirect('periodos')
    else:
        form = PeriodoForm(instance=periodo)
    
    return render(request, 'administracion/agregar_periodo.html', {
        'form': form,
        'editar': True,
        'periodo': periodo
    })

def eliminar_periodo(request, periodo_id):
    periodo = get_object_or_404(Periodo, id=periodo_id)
    
    if request.method == 'POST':
        periodo.delete()
        return redirect('periodos')
    
    return render(request, 'administracion/eliminar_periodo.html', {
        'periodo': periodo
    })

def editar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == "POST":
        form = EditarCursoForm(request.POST, instance=curso)
        if form.is_valid():
            nuevo = form.save(commit=False)
            facilitador = nuevo.facilitador

            if facilitador and conflicto_horario_facilitador(nuevo, facilitador):
                messages.error(request, "El facilitador ya tiene asignado otro grupo con un horario o día que se empalma.")
            else:
                nuevo.save()
                messages.success(request, "Curso actualizado correctamente.")
                return redirect('cursos')
    else:
        form = EditarCursoForm(instance=curso)

    return render(request, 'administracion/editar_curso.html', {'form': form, 'curso': curso})



def eliminar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    if request.method == "POST":
        curso.delete()
        return redirect('cursos')  # Redirige a la lista de cursos después de eliminar

    return render(request, 'administracion/eliminar_curso.html', {'curso': curso})

def talleres(request):
    talleres = Taller.objects.filter(finalizado=False)  # Solo talleres activos
    return render(request, 'administracion/talleres.html', {'talleres': talleres})

def talleres_finalizados(request):
    talleres = Taller.objects.filter(finalizado=True)
    return render(request, 'administracion/talleres_finalizados.html', {'talleres': talleres})

# funciones para agreagar taller

def agregar_taller(request):
    if request.method == "POST":
        form = TallerForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            facilitador = nuevo.facilitador

            if facilitador and conflicto_horario_facilitador(nuevo, facilitador):
                messages.error(request, "El facilitador ya tiene asignado otro grupo con un horario o día que se empalma.")
            elif conflicto_salon_presencial(nuevo):
                messages.error(request, "Ya existe un grupo presencial en ese mismo lugar, aula, día y horario.")
            else:
                nuevo.save()
                messages.success(request, "Taller creado exitosamente")
                return redirect('talleres')
    else:
        form = TallerForm()

    periodos = Periodo.objects.all()
    return render(request, 'administracion/agregar_taller.html', {
        'form': form,
        'periodos_data': [
            {
                'id': p.id,
                'inicio': p.fecha_inicio.strftime('%Y-%m-%d'),
                'fin': p.fecha_fin.strftime('%Y-%m-%d'),
            } for p in periodos
        ]
    })



    # return render(request, 'administracion/agregar_taller.html', {'form': form})




def editar_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)

    if request.method == "POST":
        form = EditarTallerForm(request.POST, instance=taller)
        if form.is_valid():
            nuevo = form.save(commit=False)
            facilitador = nuevo.facilitador

            if facilitador and conflicto_horario_facilitador(nuevo, facilitador):
                messages.error(request, "El facilitador ya tiene asignado otro grupo con un horario o día que se empalma.")
            else:
                nuevo.save()
                messages.success(request, "Taller actualizado correctamente.")
                return redirect('talleres')
    else:
        form = EditarTallerForm(instance=taller)

    return render(request, 'administracion/editar_taller.html', {'form': form, 'taller': taller})


def eliminar_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)
    
    if request.method == "POST":
        taller.delete()
        return redirect('talleres')  # Redirigir a la lista de talleres

    return render(request, 'administracion/eliminar_taller.html', {'taller': taller})

# esto es la logica para publicar el curso o taller
@require_POST
def publicar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.publicado = True
    curso.save()
    return redirect('cursos')

@require_POST
def publicar_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)
    taller.publicado = True
    taller.save()
    return redirect('talleres')
# logica para despublicarlo si hay algun error
@require_POST
def despublicar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.publicado = False
    curso.save()
    return redirect('cursos')

@require_POST
def despublicar_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)
    taller.publicado = False
    taller.save()
    return redirect('talleres')

@require_POST
def despublicar_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id)
    diplomado.publicado = False
    diplomado.save()
    return redirect('diplomados')

@require_POST
def publicar_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id)
    diplomado.publicado = True
    diplomado.save()
    return redirect('diplomados')

def diplomados(request):
    diplomados = Diplomado.objects.filter(finalizado=False)  # Solo diplomados activos
    return render(request, 'administracion/diplomados.html', {'diplomados': diplomados})

def diplomados_finalizados(request):
    diplomados = Diplomado.objects.filter(finalizado=True)
    return render(request, 'administracion/diplomados_finalizados.html', {'diplomados': diplomados})



def agregar_diplomado(request):
    if request.method == 'POST':
        form = DiplomadoForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            facilitador = nuevo.facilitador

            if facilitador and conflicto_horario_facilitador(nuevo, facilitador):
                messages.error(request, "El facilitador ya tiene asignado otro grupo con un horario o día que se empalma.")
            elif conflicto_salon_presencial(nuevo):
                messages.error(request, "Ya existe un grupo presencial en ese mismo lugar, aula, día y horario.")
            else:
                nuevo.save()
                messages.success(request, "Diplomado creado exitosamente")
                return redirect('diplomados')
    else:
        form = DiplomadoForm()

    periodos = Periodo.objects.all()
    return render(request, 'administracion/agregar_diplomado.html', {
        'form': form,
        'periodos_data': [
            {
                'id': p.id,
                'inicio': p.fecha_inicio.strftime('%Y-%m-%d'),
                'fin': p.fecha_fin.strftime('%Y-%m-%d'),
            } for p in periodos
        ]
    })

    
    # return render(request, 'administracion/agregar_diplomado.html', {'form': form})

def editar_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id)

    if request.method == "POST":
        form = EditarDiplomadoForm(request.POST, instance=diplomado)
        if form.is_valid():
            nuevo = form.save(commit=False)
            facilitador = nuevo.facilitador

            if facilitador and conflicto_horario_facilitador(nuevo, facilitador):
                messages.error(request, "El facilitador ya tiene asignado otro grupo con un horario o día que se empalma.")
            else:
                nuevo.save()
                messages.success(request, "Diplomado actualizado correctamente.")
                return redirect('diplomados')
    else:
        form = EditarDiplomadoForm(instance=diplomado)

    return render(request, 'administracion/editar_diplomado.html', {'form': form, 'diplomado': diplomado})


def eliminar_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id)
    
    if request.method == "POST":
        diplomado.delete()
        return redirect('diplomados')  # Redirigir a la lista de talleres

    return render(request, 'administracion/eliminar_diplomado.html', {'diplomados': diplomado})

def alumnos(request):
    alumnos = Alumno.objects.all()

    for alumno in alumnos:
        inscripciones_activas = Inscripcion.objects.filter(
            alumno=alumno,
            estado='Inscrito'
        ).filter(Q(curso__isnull=False) | Q(taller__isnull=False) | Q(diplomado__isnull=False))

        alumno.estado_inscripcion = 'Inscrito' if inscripciones_activas.exists() else 'No inscrito'

    return render(request, 'administracion/alumnos.html', {'alumnos': alumnos})


def agregar_alumno(request):
    if request.method == 'POST':
        form = RegistroAlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alumnos')
    else:
        form = RegistroAlumnoForm()

    return render(request, 'administracion/agregar_alumno.html', {'form': form})

def editar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)

    if request.method == 'POST':
        form = EditarAlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('alumnos')
    else:
        form = EditarAlumnoForm(instance=alumno)

    return render(request, 'administracion/editar_alumno.html', {
        'form': form,
        'alumno': alumno
    })

def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)

    if request.method == "POST":
        alumno.delete()
        return redirect('alumnos')

    return render(request, 'administracion/eliminar_alumno.html', {'alumno': alumno})

@require_POST
def finalizar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.finalizado = True
    curso.save()

    # Cambiar estado a "Finalizado" para alumnos inscritos en ese curso
    Inscripcion.objects.filter(curso=curso).update(estado='Finalizado', finalizado=True)

    return redirect('cursos')


def cursos_finalizados(request):
    cursos = Curso.objects.filter(finalizado=True).order_by('-fecha_fin')
    return render(request, 'administracion/cursos_finalizados.html', {'cursos': cursos})


@require_POST
def finalizar_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)
    taller.finalizado = True
    taller.save()

    # Cambiar estado a "Finalizado" para alumnos inscritos en ese taller
    Inscripcion.objects.filter(taller=taller).update(estado='Finalizado', finalizado=True)

    return redirect('talleres')

@require_POST
def finalizar_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id)
    diplomado.finalizado = True
    diplomado.save()

    # Cambiar estado a "Finalizado" para alumnos inscritos en ese diplomado
    Inscripcion.objects.filter(diplomado=diplomado).update(estado='Finalizado', finalizado=True)

    return redirect('diplomados')

from administracion.models import Curso, Taller, Diplomado, Inscripcion

def inscripciones_admin(request):
    # Cursos con al menos un alumno inscrito
    cursos = Curso.objects.filter(inscripcion__curso__isnull=False).distinct()
    talleres = Taller.objects.filter(inscripcion__taller__isnull=False).distinct()
    diplomados = Diplomado.objects.filter(inscripcion__diplomado__isnull=False).distinct()

    total_cursos = cursos.count()
    total_talleres = talleres.count()
    total_diplomados = diplomados.count()

    total_alumnos_cursos = Inscripcion.objects.filter(curso__isnull=False).count()
    total_alumnos_talleres = Inscripcion.objects.filter(taller__isnull=False).count()
    total_alumnos_diplomados = Inscripcion.objects.filter(diplomado__isnull=False).count()

    return render(request, 'administracion/inscripciones_admin.html', {
        'total_cursos': total_cursos,
        'total_talleres': total_talleres,
        'total_diplomados': total_diplomados,
        'total_alumnos_cursos': total_alumnos_cursos,
        'total_alumnos_talleres': total_alumnos_talleres,
        'total_alumnos_diplomados': total_alumnos_diplomados,
    })

def ver_cursos(request):
    cursos = Curso.objects.filter(finalizado=False).annotate(
        total_inscritos=Count('inscripcion')
    )
    return render(request, 'administracion/ver_curso.html', {'ver_curso': cursos})

def ver_talleres(request):
    talleres = Taller.objects.filter(finalizado=False).annotate(
        total_inscritos=Count('inscripcion')
    )
    return render(request, 'administracion/ver_taller.html', {'ver_taller': talleres})

def ver_diplomados(request):
    diplomados = Diplomado.objects.filter(finalizado=False).annotate(
        total_inscritos=Count('inscripcion')
    )
    return render(request, 'administracion/ver_diplomado.html', {'ver_diplomado': diplomados})
# funcion de conficto de horario
def hay_conflicto_horario(nuevo, existente):
    if not nuevo or not existente:
        return False
    if not set(nuevo.dias).intersection(set(existente.dias or [])):
        return False
    return (
        nuevo.hora_inicio < existente.hora_fin and
        existente.hora_inicio < nuevo.hora_fin
    )



def ver_alumnos_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    query = request.GET.get('q', '')

    inscripciones = Inscripcion.objects.filter(curso=curso)

    if query:
        inscripciones = inscripciones.filter(
            Q(alumno__nombres__icontains=query) |
            Q(alumno__apellido_paterno__icontains=query) |
            Q(alumno__apellido_materno__icontains=query) |
            Q(alumno__clave_alumno__icontains=query) |
            Q(alumno__telefono__icontains=query)
        )

    return render(request, 'administracion/ver_alumnos_curso.html', {
        'curso': curso,
        'inscripciones': inscripciones,
        'query': query
    })

def ver_alumnos_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)
    query = request.GET.get('q', '')

    inscripciones = Inscripcion.objects.filter(taller=taller)

    if query:
        inscripciones = inscripciones.filter(
            Q(alumno__nombres__icontains=query) |
            Q(alumno__apellido_paterno__icontains=query) |
            Q(alumno__apellido_materno__icontains=query) |
            Q(alumno__clave_alumno__icontains=query) |
            Q(alumno__telefono__icontains=query)
        )

    return render(request, 'administracion/ver_alumnos_taller.html', {
        'taller': taller,
        'inscripciones': inscripciones,
        'query': query
    })

def ver_alumnos_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id)
    query = request.GET.get('q', '')

    inscripciones = Inscripcion.objects.filter(diplomado=diplomado)

    if query:
        inscripciones = inscripciones.filter(
            Q(alumno__nombres__icontains=query) |
            Q(alumno__apellido_paterno__icontains=query) |
            Q(alumno__apellido_materno__icontains=query) |
            Q(alumno__clave_alumno__icontains=query) |
            Q(alumno__telefono__icontains=query)
        )

    return render(request, 'administracion/ver_alumnos_diplomado.html', {
        'diplomado': diplomado,
        'inscripciones': inscripciones,
        'query': query
    })


@require_POST
def dar_de_baja_curso(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    curso = inscripcion.curso  # Guardamos el curso antes de borrar

    if curso:
        curso.cupos += 1
        curso.save()

    inscripcion.delete()
    messages.success(request, "Alumno dado de baja exitosamente.")

    return redirect('ver_alumnos_curso', curso_id=curso.id)

@require_POST
def dar_de_baja_taller(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    taller = inscripcion.taller  # Guardamos el taller antes de borrar

    if taller:
        taller.cupos += 1
        taller.save()

    inscripcion.delete()
    messages.success(request, "Alumno dado de baja exitosamente.")

    return redirect('ver_alumnos_taller', taller_id=taller.id)

@require_POST
def dar_de_baja_diplomado(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    diplomado = inscripcion.diplomado  # Guardamos el diplomado antes de borrar

    if diplomado:
        diplomado.cupos += 1
        diplomado.save()

    inscripcion.delete()
    messages.success(request, "Alumno dado de baja exitosamente.")

    return redirect('ver_alumnos_diplomado', diplomado_id=diplomado.id)

def dar_de_alta_alumno_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    query = request.GET.get('q', '')
    alumnos = Alumno.objects.all()
    disponibles = []

    for alumno in alumnos:
        inscripciones = alumno.inscripcion_set.filter(estado="Inscrito")
        conflicto = any(hay_conflicto_horario(curso, i.curso or i.taller or i.diplomado) for i in inscripciones)

        if alumno.restriccion_libre:
            if not conflicto:
                disponibles.append(alumno)
        else:
            tiene_curso_o_taller = inscripciones.filter(Q(curso__isnull=False) | Q(taller__isnull=False)).exists()
            if not tiene_curso_o_taller and not conflicto:
                disponibles.append(alumno)

    if not disponibles:
        messages.info(request, "No hay alumnos disponibles. Todos los alumnos tienen curso/taller activo o conflicto de horario.")

    if query:
        disponibles = [a for a in disponibles if query.lower() in a.nombres.lower()
                       or query.lower() in a.apellido_paterno.lower()
                       or query.lower() in a.apellido_materno.lower()
                       or query.lower() in a.clave_alumno.lower()
                       or query.lower() in a.telefono.lower()]

    return render(request, 'administracion/dar_de_alta_alumno_curso.html', {
        'curso': curso,
        'alumnos_disponibles': disponibles,
        'query': query
    })


def dar_de_alta_alumno_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)
    query = request.GET.get('q', '')
    alumnos = Alumno.objects.all()
    disponibles = []

    for alumno in alumnos:
        inscripciones = alumno.inscripcion_set.filter(estado="Inscrito")
        conflicto = any(hay_conflicto_horario(taller, i.curso or i.taller or i.diplomado) for i in inscripciones)

        if alumno.restriccion_libre:
            if not conflicto:
                disponibles.append(alumno)
        else:
            tiene_curso_o_taller = inscripciones.filter(Q(curso__isnull=False) | Q(taller__isnull=False)).exists()
            if not tiene_curso_o_taller and not conflicto:
                disponibles.append(alumno)

    if not disponibles:
        messages.info(request, "No hay alumnos disponibles. Todos tienen curso/taller activo o conflicto de horario.")

    if query:
        disponibles = [a for a in disponibles if query.lower() in a.nombres.lower()
                       or query.lower() in a.apellido_paterno.lower()
                       or query.lower() in a.apellido_materno.lower()
                       or query.lower() in a.clave_alumno.lower()
                       or query.lower() in a.telefono.lower()]

    return render(request, 'administracion/dar_de_alta_alumno_taller.html', {
        'taller': taller,
        'alumnos_disponibles': disponibles,
        'query': query
    })

def dar_de_alta_alumno_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id)
    query = request.GET.get('q', '')
    alumnos = Alumno.objects.all()
    disponibles = []

    for alumno in alumnos:
        inscripciones = alumno.inscripcion_set.filter(estado="Inscrito")
        conflicto = any(hay_conflicto_horario(diplomado, i.curso or i.taller or i.diplomado) for i in inscripciones)

        if alumno.restriccion_libre:
            if not conflicto:
                disponibles.append(alumno)
        else:
            tiene_diplomado = inscripciones.filter(diplomado__isnull=False).exists()
            if not tiene_diplomado and not conflicto:
                disponibles.append(alumno)

    if not disponibles:
        messages.info(request, "No hay alumnos disponibles. Todos tienen un diplomado activo o conflicto de horario.")

    if query:
        disponibles = [a for a in disponibles if query.lower() in a.nombres.lower()
                       or query.lower() in a.apellido_paterno.lower()
                       or query.lower() in a.apellido_materno.lower()
                       or query.lower() in a.clave_alumno.lower()
                       or query.lower() in a.telefono.lower()]

    return render(request, 'administracion/dar_de_alta_alumno_diplomado.html', {
        'diplomado': diplomado,
        'alumnos_disponibles': disponibles,
        'query': query
    })

@require_POST
def alta_alumno_taller(request, taller_id, alumno_id):
    taller = get_object_or_404(Taller, id=taller_id)
    alumno = get_object_or_404(Alumno, id=alumno_id)

    if taller.cupos > 0:
        Inscripcion.objects.create(alumno=alumno, taller=taller, estado="Inscrito")
        taller.cupos -= 1
        taller.save()
        messages.success(request, "Alumno inscrito exitosamente.")
    else:
        messages.error(request, "No hay cupos disponibles.")

    return redirect('dar_de_alta_alumno_taller', taller_id=taller.id)


@require_POST
def alta_alumno_curso(request, curso_id, alumno_id):
    curso = get_object_or_404(Curso, id=curso_id)
    alumno = get_object_or_404(Alumno, id=alumno_id)

    if curso.cupos > 0:
        Inscripcion.objects.create(alumno=alumno, curso=curso, estado="Inscrito")
        curso.cupos -= 1
        curso.save()
        messages.success(request, "Alumno inscrito exitosamente.")
    else:
        messages.error(request, "No hay cupos disponibles.")

    return redirect('dar_de_alta_alumno', curso_id=curso.id)

def alta_alumno_diplomado(request, diplomado_id, alumno_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id)
    alumno = get_object_or_404(Alumno, id=alumno_id)

    if diplomado.cupos > 0:
        Inscripcion.objects.create(alumno=alumno, diplomado=diplomado, estado="Inscrito")
        diplomado.cupos -= 1
        diplomado.save()
        messages.success(request, "Alumno inscrito exitosamente.")
    else:
        messages.error(request, "No hay cupos disponibles.")

    return redirect('dar_de_alta_alumno_diplomado', diplomado_id=diplomado.id)

@require_POST
def toggle_restriccion_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    alumno.restriccion_libre = not alumno.restriccion_libre
    alumno.save()
    return redirect('alumnos')

#esta es la funcion para poder descargar la lista de alumnos inscritos en un curso y la plantilla
def generar_pdf_alumnos(inscripciones, titulo):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Datos del encabezado
    entidad = inscripciones[0].curso if hasattr(inscripciones[0], 'curso') and inscripciones[0].curso else \
              inscripciones[0].taller if hasattr(inscripciones[0], 'taller') and inscripciones[0].taller else \
              inscripciones[0].diplomado

    now = datetime.now()
    fecha_hora = now.strftime("%d/%m/%Y %I:%M %p")  # Formato: 16/05/2025 03:20 PM

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, height - 40, f"Nombre del {titulo.lower()}: {getattr(entidad, f'nombre_{titulo.lower()}')}")
    pdf.drawString(40, height - 55, f"Nombre del facilitador: {entidad.facilitador}")
    pdf.drawString(40, height - 70, f"Grupo: {entidad.grupo}")
    pdf.drawString(40, height - 85, f"Periodo: {entidad.periodo}")
    pdf.drawString(500, height - 40, f"Generado: {fecha_hora}")

    # Tabla
    y = height - 120
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(40, y, "Clave única")
    pdf.drawString(110, y, "Alumno")
    pdf.drawString(260, y, "Clave escolar")
    pdf.drawString(350, y, "CURP")
    pdf.drawString(480, y, "Correo")
    pdf.drawString(620, y, "Teléfono")
    pdf.line(40, y - 2, 750, y - 2)

    pdf.setFont("Helvetica", 8)
    for ins in inscripciones:
        alumno = ins.alumno
        y -= 20
        if y < 40:
            pdf.showPage()
            y = height - 40
        pdf.drawString(40, y, alumno.clave_alumno)
        pdf.drawString(110, y, f"{alumno.nombres} {alumno.apellido_paterno} {alumno.apellido_materno}")
        pdf.drawString(260, y, alumno.clave)
        pdf.drawString(350, y, alumno.curp)
        pdf.drawString(480, y, alumno.correo)
        pdf.drawString(620, y, str(alumno.telefono))

    pdf.save()
    buffer.seek(0)
    return buffer

def descargar_lista_alumnos_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    inscripciones = Inscripcion.objects.filter(curso=curso)
    buffer = generar_pdf_alumnos(inscripciones, "Curso")
    return FileResponse(buffer, as_attachment=True, filename="lista_curso.pdf")

def descargar_lista_alumnos_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)
    inscripciones = Inscripcion.objects.filter(taller=taller)
    buffer = generar_pdf_alumnos(inscripciones, "Taller")
    return FileResponse(buffer, as_attachment=True, filename="lista_taller.pdf")

def descargar_lista_alumnos_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id)
    inscripciones = Inscripcion.objects.filter(diplomado=diplomado)
    buffer = generar_pdf_alumnos(inscripciones, "Diplomado")
    return FileResponse(buffer, as_attachment=True, filename="lista_diplomado.pdf")

def historial_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    historial = Inscripcion.objects.filter(alumno=alumno, finalizado=True)

    return render(request, 'administracion/historial_alumno.html', {
        'alumno': alumno,
        'historial': historial
    })

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

# @login_required
def administrador(request):
    usuario = request.user  # Este es el administrador con sesión activa
    return render(request, 'administracion/perfil_admin.html', {
        'usuario': usuario
    })

def agregar_admin(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.is_superuser = True
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}!')
            return redirect('administrador')  # o 'agregar_admin' si quieres volver al mismo formulario
    else:
        form = RegisterForm()
    return render(request, 'administracion/agregar_admin.html', {'form': form})


class CambiarContrasenaView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'administracion/cambiar_contrasena.html'
    success_url = reverse_lazy('perfil_admin')  # o a donde quieras redirigir después
    login_url = 'login_admin'

    def form_valid(self, form):
        messages.success(self.request, "Contraseña actualizada correctamente.")
        return super().form_valid(form)
    
#esta parte es de los facilitadores su formulario y logica
def agregar_facilitador(request):
    if request.method == 'POST':
        form = RegistroFacilitadorForm(request.POST)
        if form.is_valid():
            form.save()  # ya hace el cifrado en el método save del form
            return redirect('facilitadores')  # o la vista/listado que tengas
    else:
        form = RegistroFacilitadorForm()

    return render(request, 'administracion/agregar_facilitador.html', {'form': form})

#esto es para que se vean el listado de los facilitadores
def lista_facilitadores(request):
    facilitadores = Facilitador.objects.all()
    
    return render(request, 'administracion/facilitadores.html', {'facilitadores': facilitadores})
#esta logica es para editar a los facilitadores
def editar_facilitador(request, facilitador_id):
    facilitador = get_object_or_404(Facilitador, id=facilitador_id)
    if request.method == 'POST':
        form = EditarFacilitadorForm(request.POST, instance=facilitador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Facilitador actualizado correctamente.')
            return redirect('facilitadores')
    else:
        form = EditarFacilitadorForm(instance=facilitador)
    return render(request, 'administracion/editar_facilitador.html', {'form': form, 'facilitador': facilitador})

#esto es para eliminar a los facilitadores
def eliminar_facilitador(request, facilitador_id):
    facilitador = get_object_or_404(Facilitador, id=facilitador_id)
    if request.method == 'POST':
        facilitador.delete()
        messages.success(request, 'Facilitador eliminado correctamente.')
        return redirect('facilitadores')
    return render(request, 'administracion/eliminar_facilitador.html', {'facilitador': facilitador})