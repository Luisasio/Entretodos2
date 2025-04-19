from functools import wraps
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import RegistroAlumnoForm, RegistroFacilitadorForm
from administracion.models import Alumno, Facilitador
from django.db.models import Q
from django.contrib import messages
from administracion.models import Curso, Taller, Inscripcion, Diplomado

def index(request):
  
    return render(request, 'index.html')
  
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
    alumno_id = request.session.get('alumno_id')
    if not alumno_id:
        return redirect('login_alumno')
    alumno = Alumno.objects.get(id=alumno_id)
    return render(request, 'inicio.html', {'alumno': alumno})


# esta es la parte para que el alumno vea la parte de los cursos y talleres
def inscripciones(request):
    alumno_id = request.session.get("alumno_id")
    if not alumno_id:
        return redirect('login_alumno')

    alumno = Alumno.objects.get(id=alumno_id)

    cursos = Curso.objects.filter(publicado=True, cupos__gt=0, finalizado=False)
    talleres = Taller.objects.filter(publicado=True, cupos__gt=0)
    diplomados = Diplomado.objects.filter(publicado=True, cupos__gt=0)

    inscripciones = Inscripcion.objects.filter(alumno_id=alumno_id)

    tiene_curso_o_taller = inscripciones.filter(estado__iexact="Inscrito").filter(Q(curso__isnull=False) | Q(taller__isnull=False)).exists()
    tiene_diplomado = inscripciones.filter(
    estado__iexact="Inscrito", diplomado__isnull=False
    ).exists()

    bloqueado = not alumno.restriccion_libre and tiene_curso_o_taller and tiene_diplomado

    return render(request, 'inscripciones.html', {
        'alumno': alumno,
        'cursos': cursos,
        'talleres': talleres,
        'diplomados': diplomados,
        'tiene_curso_o_taller': tiene_curso_o_taller,
        'tiene_diplomado': tiene_diplomado,
        'bloqueado': bloqueado
    })



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


        if tiene_curso_o_taller and tipo in ['curso', 'taller', 'diplomado']:
            messages.warning(request, "Ya estás inscrito a un curso o taller. No puedes inscribirte a más.")
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
        if curso.cupos and curso.cupos > 0:
            Inscripcion.objects.create(alumno_id=alumno_id, curso=curso, estado="Inscrito")
            curso.cupos -= 1
            curso.save()
        else:
            messages.error(request, "El curso ya no tiene cupos disponibles.")
            return redirect('inscripciones')

    elif tipo == 'taller':
        taller = Taller.objects.get(id=id)
        if taller.cupos and taller.cupos > 0:
            Inscripcion.objects.create(alumno_id=alumno_id, taller=taller, estado="Inscrito")
            taller.cupos -= 1
            taller.save()
        else:
            messages.error(request, "El taller ya no tiene cupos disponibles.")
            return redirect('inscripciones')

    elif tipo == 'diplomado':
        diplomado = Diplomado.objects.get(id=id)
        if diplomado.cupos and diplomado.cupos > 0:
            Inscripcion.objects.create(alumno_id=alumno_id, diplomado=diplomado, estado="Inscrito")
            diplomado.cupos -= 1
            diplomado.save()
        else:
            messages.error(request, "El diplomado ya no tiene cupos disponibles.")
            return redirect('inscripciones')

    else:
        messages.error(request, "Tipo de inscripción no válido.")
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

    return render(request, 'inicio_facilitador.html', {'facilitador': facilitador})

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
    
    cursos = Curso.objects.filter(facilitador__isnull=True, publicado=True, finalizado=False)
    talleres = Taller.objects.filter(facilitador__isnull=True, publicado=True)
    diplomados = Diplomado.objects.filter(facilitador__isnull=True, publicado=True)

    return render(request, 'impartir_cursos.html', {
        'cursos': cursos,
        'talleres': talleres,
        'diplomados': diplomados,
        'facilitador': request.facilitador
    })

@cargar_facilitador
def tomar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, facilitador__isnull=True)
    curso.facilitador = request.facilitador
    curso.save()
    messages.success(request, "Curso asignado correctamente.")
    return redirect('impartir_cursos')

@cargar_facilitador
def tomar_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id, facilitador__isnull=True)
    taller.facilitador = request.facilitador
    taller.save()
    messages.success(request, "Taller asignado correctamente.")
    return redirect('impartir_cursos')

@cargar_facilitador
def tomar_diplomado(request, diplomado_id):
    diplomado = get_object_or_404(Diplomado, id=diplomado_id, facilitador__isnull=True)
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