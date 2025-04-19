from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import LoginAlumnoForm, LoginFacilitadorForm
from administracion.models import Alumno, Facilitador
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
            # Asegura que no haya datos de sesión del alumno
            if 'alumno_id' in request.session:
                del request.session['alumno_id']

            login(request, user)  # Django maneja sesión con 'request.user'
            return redirect('dashboard')
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
                    request.session.flush()  # Limpia toda la sesión anterior
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
    request.session.pop('alumno_id', None)
    return redirect('login_alumno')

def login_facilitador(request):
    if request.method == 'POST':
        form = LoginFacilitadorForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            try:
                facilitador = Facilitador.objects.get(correo=correo)
                if check_password(contrasena, facilitador.contrasena):
                    request.session.flush()  # limpia otras sesiones
                    request.session['facilitador_id'] = facilitador.id
                    return redirect('inicio_facilitador')  # asegúrate de tener esta URL
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except Facilitador.DoesNotExist:
                messages.error(request, 'No existe un facilitador con ese correo.')
    else:
        form = LoginFacilitadorForm()
    return render(request, 'autenticacion/login_facilitador.html', {'form': form})

def logout_facilitador(request):
    request.session.pop('facilitador_id', None)
    return redirect('login_facilitador')