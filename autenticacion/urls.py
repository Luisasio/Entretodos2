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
]