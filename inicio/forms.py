from django import forms
from administracion.models import Alumno, Facilitador
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import re


class RegistroAlumnoForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    SEXO_CHOICES = [
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
        ('Otro', 'Otro'),
    ]
    sexo = forms.ChoiceField(choices=SEXO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Alumno
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno', 'correo',
            'contrasena', 'telefono', 'clave', 'curp', 'sexo', 'estado', 'municipio'
        ]
        labels = {
            'clave': 'CCT (clave de trabajo)',
        }

    def clean_curp(self):
        curp = self.cleaned_data.get('curp', '')
        if not re.match(r'^[A-Za-z0-9]+$', curp):
            raise ValidationError('La CURP solo puede contener letras y números.')
        if len(curp) > 18:
            raise ValidationError('La CURP no debe tener más de 18 caracteres.')
        return curp

    def clean_telefono(self):
        telefono = str(self.cleaned_data.get('telefono', ''))
        if not re.fullmatch(r'\d{10}', telefono):
            raise ValidationError('El teléfono debe contener exactamente 10 dígitos numéricos.')
        return telefono


    def save(self, commit=True):
        alumno = super().save(commit=False)
        alumno.contrasena = make_password(self.cleaned_data['contrasena'])
        if commit:
            alumno.save()
        return alumno


class EditarAlumnoForm(forms.ModelForm):
    SEXO_CHOICES = [
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
        ('Otro', 'Otro'),
    ]
    sexo = forms.ChoiceField(choices=SEXO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Alumno
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno', 'correo',
            'telefono', 'clave', 'curp', 'sexo', 'estado', 'municipio'
        ]
        labels = {
            'clave': 'CCT (clave de trabajo)',
        }



# registro del facilitador
class RegistroFacilitadorForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    SEXO_CHOICES = [
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
        ('Otro', 'Otro'),
    ]
    sexo = forms.ChoiceField(choices=SEXO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Facilitador
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno', 'correo',
            'contrasena', 'telefono', 'clave', 'curp', 'sexo', 'estado', 'municipio'
        ]
        labels = {
            'clave': 'CCT (clave de trabajo)',
        }

    def clean_curp(self):
        curp = self.cleaned_data.get('curp', '')
        if not re.fullmatch(r'[A-Za-z0-9]{1,18}', curp):
            raise ValidationError('El CURP solo debe contener letras y números (máximo 18 caracteres).')
        return curp

    def clean_telefono(self):
        telefono = str(self.cleaned_data.get('telefono', ''))
        if not re.fullmatch(r'\d{10}', telefono):
            raise ValidationError('El teléfono debe contener exactamente 10 dígitos numéricos.')
        return telefono

    def save(self, commit=True):
        facilitador = super().save(commit=False)
        facilitador.contrasena = make_password(self.cleaned_data['contrasena'])
        if commit:
            facilitador.save()
        return facilitador
    

class EditarFacilitadorForm(forms.ModelForm):
    SEXO_CHOICES = [
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
        ('Otro', 'Otro'),
    ]
    sexo = forms.ChoiceField(choices=SEXO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Facilitador
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno', 'correo',
            'telefono', 'clave', 'curp', 'sexo', 'estado', 'municipio'
        ]
        labels = {
            'clave': 'CCT (clave de trabajo)',
        }
