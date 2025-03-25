from django import forms
from .models import Facilitador, Periodo
from .models import Curso


class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CursoForm(forms.ModelForm):
    facilitador = forms.ModelChoiceField(
        queryset=Facilitador.objects.all(),
        required=False,  # Permite que el campo sea opcional
        empty_label="Sin facilitador"
    )

    class Meta:
        model = Curso
        fields = ['nombre_curso', 'descripcion', 'fecha_inicio', 'fecha_fin', 'hora_inicio', 'hora_fin', 'cupos', 'grupo', 'facilitador', 'periodo']
        widgets = {
            'nombre_curso': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control custom-input'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'facilitador': forms.Select(attrs={'class': 'form-control'}),
        }
