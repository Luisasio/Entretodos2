from django import forms
from .models import Diplomado, Facilitador, Periodo, Taller
from .models import Curso
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['nombre_periodo','fecha_inicio', 'fecha_fin']
        widgets = {
            'nombre_periodo': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Escriba el nombre que recibira el periodo'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CursoForm(forms.ModelForm):
    facilitador = forms.ModelChoiceField(
        queryset=Facilitador.objects.all(),
        required=False,
        empty_label="Sin facilitador"
    )

    class Meta:
        model = Curso
        fields = [
            'nombre_curso', 'descripcion', 'fecha_inicio', 'fecha_fin',
            'hora_inicio', 'hora_fin', 'cupos', 'grupo',
            'modalidad', 'duracion',  # 👈 nuevos campos
            'facilitador', 'periodo'
        ]
        MODALIDAD_CHOICES = [
        ('virtual', 'Virtual'),
        ('presencial', 'Presencial'),
        ]
        widgets = {
            'nombre_curso': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control custom-input'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(
                choices=[('virtual', 'Virtual'), ('presencial', 'Presencial')],
                attrs={'class': 'form-control'}
            ),  
            'duracion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'En horas'}),  # 👈 entrada numérica
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'facilitador': forms.Select(attrs={'class': 'form-control'}),
        }


class TallerForm(forms.ModelForm):
    facilitador = forms.ModelChoiceField(
        queryset=Facilitador.objects.all(),
        required=False,
        empty_label="Sin facilitador"
    )

    class Meta:
        model = Taller
        fields = ['nombre_taller', 'descripcion', 'fecha_inicio', 'fecha_fin',
                  'hora_inicio', 'hora_fin', 'cupos', 'grupo',
                  'modalidad', 'duracion', 'facilitador', 'periodo']
        widgets = {
            'nombre_taller': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control custom-input'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(
                choices=[('virtual', 'Virtual'), ('presencial', 'Presencial')],
                attrs={'class': 'form-control'}
            ),
            'duracion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'En horas'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'facilitador': forms.Select(attrs={'class': 'form-control'}),
        }



class DiplomadoForm(forms.ModelForm):
    facilitador = forms.ModelChoiceField(
        queryset=Facilitador.objects.all(),
        required=False,
        empty_label="Sin facilitador"
    )

    class Meta:
        model = Diplomado
        fields = ['nombre_diplomado', 'descripcion', 'fecha_inicio', 'fecha_fin',
                  'hora_inicio', 'hora_fin', 'cupos', 'grupo',
                  'modalidad', 'duracion', 'facilitador', 'periodo']
        widgets = {
            'nombre_diplomado': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control custom-input'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(
                choices=[('virtual', 'Virtual'), ('presencial', 'Presencial')],
                attrs={'class': 'form-control'}
            ),
            'duracion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'En horas'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'facilitador': forms.Select(attrs={'class': 'form-control'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'