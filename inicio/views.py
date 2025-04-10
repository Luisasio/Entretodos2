from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import RegistroAlumnoForm
from administracion.models import Alumno
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
    alumno = request.session.get("alumno_id")
    if not alumno:
        return redirect('login_alumno')

    cursos = Curso.objects.filter(publicado=True)
    talleres = Taller.objects.filter(publicado=True)
    diplomados = Diplomado.objects.filter(publicado=True)  # 👈 nuevo

    inscripcion_existente = Inscripcion.objects.filter(alumno_id=alumno).first()

    return render(request, 'inscripciones.html', {
        'cursos': cursos,
        'talleres': talleres,
        'diplomados': diplomados,  # 👈 nuevo
        'inscripcion': inscripcion_existente
    })

# esto es para que el alumno se inscriba es decir la logica
def inscribirse(request, tipo, id):
    alumno_id = request.session.get("alumno_id")
    if not alumno_id:
        return redirect('login_alumno')

    ya_inscrito = Inscripcion.objects.filter(alumno_id=alumno_id).first()
    if ya_inscrito:
        messages.warning(request, "Ya estás inscrito a un curso, taller o diplomado.")
        return redirect('inscripciones')

    if tipo == 'curso':
        inscripcion = Inscripcion.objects.create(alumno_id=alumno_id, curso_id=id, estado="Inscrito")
    elif tipo == 'taller':
        inscripcion = Inscripcion.objects.create(alumno_id=alumno_id, taller_id=id, estado="Inscrito")
    elif tipo == 'diplomado':
        inscripcion = Inscripcion.objects.create(alumno_id=alumno_id, diplomado_id=id, estado="Inscrito")
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

    inscripcion = Inscripcion.objects.filter(alumno_id=alumno_id).first()

    return render(request, 'mis_cursos.html', {
        'inscripcion': inscripcion
    })
