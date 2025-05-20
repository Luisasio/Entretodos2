from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_admin, name='logout_admin'),
    #esto es para el login del alumno
    path('login-alumno/', views.login_alumno, name='login_alumno'),
    path('logout-alumno/', views.logout_alumno, name='logout_alumno'),
    #esto es para el login del facilitador
    path('login-facilitador/', views.login_facilitador, name='login_facilitador'),
    path('logout-facilitador/', views.logout_facilitador, name='logout_facilitador'),

# restablecer contraseña alumno
   path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
   path('restablecer-contrasena/<str:token>/', views.restablecer_contrasena, name='restablecer_contrasena'),

# restablecer contraseña facilitador
path('recuperar-contrasena-facilitador/', views.recuperar_contrasena_facilitador, name='recuperar_contrasena_facilitador'),
path('restablecer-contrasena-facilitador/<str:token>/', views.restablecer_contrasena_facilitador, name='restablecer_contrasena_facilitador'),


]