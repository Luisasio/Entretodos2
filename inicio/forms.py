from django import forms
from administracion.models import Alumno, Facilitador
from django.contrib.auth.hashers import make_password

class RegistroAlumnoForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Alumno
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno', 'correo',
            'contrasena', 'telefono', 'clave', 'curp', 'sexo'
        ]

    def save(self, commit=True):
        alumno = super().save(commit=False)
        alumno.contrasena = make_password(self.cleaned_data['contrasena'])  # Contraseña cifrada
        if commit:
            alumno.save()
        return alumno

class EditarAlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno', 'correo',
            'telefono', 'clave', 'curp', 'sexo'
        ]

class RegistroFacilitadorForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Facilitador
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno', 'correo',
            'contrasena', 'telefono', 'clave', 'curp', 'sexo'
        ]

    def save(self, commit=True):
        facilitador = super().save(commit=False)
        facilitador.contrasena = make_password(self.cleaned_data['contrasena'])
        if commit:
            facilitador.save()
        return facilitador