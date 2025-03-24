from django.shortcuts import redirect, render

from administracion.forms import CursoForm, PeriodoForm
from administracion.models import Periodo
from administracion.models import Curso
# from django.contrib.auth.decorators import login_required


# Create your views here.
# @login_required
def dashboard(request):
    return render(request, 'administracion/dashboard.html')

def cursos(request):
    cursos = Curso.objects.all()  # Obtener todos los cursos
    return render(request, 'administracion/cursos.html', {'cursos': cursos})

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