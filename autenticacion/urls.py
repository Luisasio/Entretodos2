from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_admin, name='logout_admin'),
]