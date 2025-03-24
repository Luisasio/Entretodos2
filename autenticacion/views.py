from django.shortcuts import render

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