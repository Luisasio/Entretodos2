from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .forms import LoginAlumnoForm, LoginFacilitadorForm
from administracion.models import Alumno, Facilitador

# -------------------- ADMIN --------------------

def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Asegura que no haya datos de sesión de alumno o facilitador
            request.session.pop('alumno_id', None)
            request.session.pop('facilitador_id', None)

            login(request, user)  # Django maneja sesión con request.user
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'autenticacion/login_admin.html')


def logout_admin(request):
    logout(request)  # Cierra solo sesión del admin
    return redirect('login_admin')

# -------------------- ALUMNO --------------------

def login_alumno(request):
    if request.method == 'POST':
        form = LoginAlumnoForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            try:
                alumno = Alumno.objects.get(correo=correo)
                if check_password(contrasena, alumno.contrasena):
                    # Limpia solo sesiones de otros roles (no usa logout)
                    request.session.pop('facilitador_id', None)
                    request.session.pop('_auth_user_id', None)  # por si está logueado como admin
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
    request.session.pop('alumno_id', None)  # Solo elimina clave del alumno
    return redirect('login_alumno')

# -------------------- FACILITADOR --------------------

def login_facilitador(request):
    if request.method == 'POST':
        form = LoginFacilitadorForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            try:
                facilitador = Facilitador.objects.get(correo=correo)
                if check_password(contrasena, facilitador.contrasena):
                    # Limpia solo sesiones de otros roles (no usa logout)
                    request.session.pop('alumno_id', None)
                    request.session.pop('_auth_user_id', None)  # por si está logueado como admin
                    request.session['facilitador_id'] = facilitador.id
                    return redirect('inicio_facilitador')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except Facilitador.DoesNotExist:
                messages.error(request, 'No existe un facilitador con ese correo.')
    else:
        form = LoginFacilitadorForm()

    return render(request, 'autenticacion/login_facilitador.html', {'form': form})


def logout_facilitador(request):
    request.session.pop('facilitador_id', None)  # Solo elimina clave del facilitador
    return redirect('login_facilitador')
