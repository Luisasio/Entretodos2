from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .forms import LoginAlumnoForm, LoginFacilitadorForm
from administracion.models import Alumno, Facilitador


# esto tambien es para el restablecer contraseña
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.urls import reverse

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
                    # Solo limpia lo necesario (no toca admin)
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
    request.session.pop('alumno_id', None)  # Solo quita la del alumno
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
                    # Solo limpia lo necesario (no toca admin)
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
    request.session.pop('facilitador_id', None)  # Solo quita la del facilitador
    return redirect('login_facilitador')


#restablecer contraseña alumno
def recuperar_contrasena(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        try:
            alumno = Alumno.objects.get(correo=correo)
            token = get_random_string(length=32)

            alumno.token_recuperacion = token
            alumno.save()

            url = request.build_absolute_uri(reverse('restablecer_contrasena', args=[token]))
            mensaje = render_to_string('correo/recuperar_contrasena.txt', {
                'nombre': alumno.nombres,
                'url': url
            })

            send_mail(
                'Recuperación de contraseña',
                mensaje,
                'no-responder@entretodos.com',
                [alumno.correo],
                fail_silently=False
            )
            messages.success(request, 'Te hemos enviado un enlace para restablecer tu contraseña.')
            return redirect('login_alumno')

        except Alumno.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta con ese correo.')

    return render(request, 'autenticacion/recuperar_contrasena.html')


def restablecer_contrasena(request, token):
    try:
        alumno = Alumno.objects.get(token_recuperacion=token)
    except Alumno.DoesNotExist:
        messages.error(request, 'Enlace inválido o caducado.')
        return redirect('login_alumno')

    if request.method == 'POST':
        nueva = request.POST.get('nueva_contrasena')
        confirmar = request.POST.get('confirmar_contrasena')
        if nueva != confirmar:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            alumno.contrasena = make_password(nueva)
            alumno.token_recuperacion = None  # invalidar token
            alumno.save()
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('login_alumno')

    return render(request, 'autenticacion/restablecer_contrasena.html', {'token': token})





#recuperar contraseña del facilitador
# -------------------- RESTABLECER CONTRASEÑA FACILITADOR --------------------

def recuperar_contrasena_facilitador(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        try:
            facilitador = Facilitador.objects.get(correo=correo)
            token = get_random_string(length=32)

            facilitador.token_recuperacion = token
            facilitador.save()

            url = request.build_absolute_uri(reverse('restablecer_contrasena_facilitador', args=[token]))
            mensaje = render_to_string('correo/recuperar_contrasena.txt', {
                'nombre': facilitador.nombres,
                'url': url
            })

            send_mail(
                'Recuperación de contraseña (Facilitador)',
                mensaje,
                'no-responder@entretodos.com',
                [facilitador.correo],
                fail_silently=False
            )
            messages.success(request, 'Te hemos enviado un enlace para restablecer tu contraseña.')
            return redirect('login_facilitador')

        except Facilitador.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta con ese correo.')

    return render(request, 'autenticacion/recuperar_contrasena_facilitador.html')


def restablecer_contrasena_facilitador(request, token):
    try:
        facilitador = Facilitador.objects.get(token_recuperacion=token)
    except Facilitador.DoesNotExist:
        messages.error(request, 'Enlace inválido o caducado.')
        return redirect('login_facilitador')

    if request.method == 'POST':
        nueva = request.POST.get('nueva_contrasena')
        confirmar = request.POST.get('confirmar_contrasena')
        if nueva != confirmar:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            facilitador.contrasena = make_password(nueva)
            facilitador.token_recuperacion = None
            facilitador.save()
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('login_facilitador')

    return render(request, 'autenticacion/restablecer_contrasena_facilitador.html', {'token': token})
