from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render

from administracion.forms import CursoForm, PeriodoForm, TallerForm
from administracion.models import Periodo, Taller
from administracion.models import Curso
# from django.contrib.auth.decorators import login_required


# Create your views here.
# @login_required
def dashboard(request):
    return render(request, 'administracion/dashboard.html')

def cursos(request):
    cursos = Curso.objects.all()  # Obtener todos los cursos
    return render(request, 'administracion/cursos.html', {'cursos': cursos})

def facilitadores(request):
    return render(request, 'administracion/facilitadores.html')

def agregar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cursos')  # Redirigir a la lista de cursos
    else:
        form = CursoForm()
    
    return render(request, 'administracion/agregar_curso.html', {'form': form})

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
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('cursos')  # Redirige a la lista de cursos después de editar
    else:
        form = CursoForm(instance=curso)

    return render(request, 'administracion/editar_curso.html', {'form': form, 'curso': curso})

def eliminar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    if request.method == "POST":
        curso.delete()
        return redirect('cursos')  # Redirige a la lista de cursos después de eliminar

    return render(request, 'administracion/eliminar_curso.html', {'curso': curso})

def talleres(request):
    talleres = Taller.objects.all()
    return render(request, 'administracion/talleres.html', {'talleres': talleres})


def agregar_taller(request):
    if request.method == "POST":
        form = TallerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('talleres')  # Redirigir a la lista de talleres
    else:
        form = TallerForm()

    return render(request, 'administracion/agregar_taller.html', {'form': form})

def editar_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)
    
    if request.method == "POST":
        form = TallerForm(request.POST, instance=taller)
        if form.is_valid():
            form.save()
            return redirect('lista_talleres')  # Redirigir a la lista de talleres
    else:
        form = TallerForm(instance=taller)

    return render(request, 'administracion/editar_taller.html', {'form': form, 'taller': taller})

def eliminar_taller(request, taller_id):
    taller = get_object_or_404(Taller, id=taller_id)
    
    if request.method == "POST":
        taller.delete()
        return redirect('lista_talleres')  # Redirigir a la lista de talleres

    return render(request, 'administracion/eliminar_taller.html', {'taller': taller})

