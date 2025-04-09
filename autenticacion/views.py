from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import LoginAlumnoForm
from administracion.models import Alumno
from django.contrib import messages
from django.contrib.auth.hashers import check_password

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirige al dashboard si es válido
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'autenticacion/login_admin.html')

def logout_admin(request):
    logout(request)
    return redirect('login_admin')

#registro y logica del Alumno
def login_alumno(request):
    if request.method == 'POST':
        form = LoginAlumnoForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            try:
                alumno = Alumno.objects.get(correo=correo)
                if check_password(contrasena, alumno.contrasena):
                    request.session['alumno_id'] = alumno.id
                    return redirect('inicio')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except Alumno.DoesNotExist:
                messages.error(request, 'No existe un alumno con ese correo.')
    else:
        form = LoginAlumnoForm()
    return render(request, 'autenticacion/login_alumno.html', {'form': form})

def logout_alumno(request):
    request.session.flush()  # Elimina los datos de sesión
    return redirect('login_alumno')
