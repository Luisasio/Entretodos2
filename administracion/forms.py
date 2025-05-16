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
            'facilitador', 'periodo','lugar', 'aula', 'dias'
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
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cede Paulo Friere'}),
            'aula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Aula 4, Salon ...'}),
            'dias': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ej. Lunes, Miércoles y Viernes'}),

        }
    # para añadir la parte de presencial
    def clean(self):
        cleaned_data = super().clean()
        modalidad = cleaned_data.get('modalidad')
        
        # es para que el campo no se envie si esta vacio
        if not cleaned_data.get('dias'):
            self.add_error('dias', 'Este campo es obligatorio.')

        if modalidad == 'presencial':
            if not cleaned_data.get('lugar'):
                self.add_error('lugar', 'Este campo es obligatorio en modalidad presencial.')
            if not cleaned_data.get('aula'):
                self.add_error('aula', 'Este campo es obligatorio en modalidad presencial.')
        return cleaned_data

    # validacion para la fecha de periodo
    def clean(self):
        cleaned_data = super().clean()
        periodo = cleaned_data.get('periodo')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if periodo and fecha_inicio and fecha_fin:
            if not (periodo.fecha_inicio <= fecha_inicio <= periodo.fecha_fin):
                self.add_error('fecha_inicio', f'La fecha de inicio debe estar entre {periodo.fecha_inicio} y {periodo.fecha_fin}.')

            if not (periodo.fecha_inicio <= fecha_fin <= periodo.fecha_fin):
                self.add_error('fecha_fin', f'La fecha de fin debe estar entre {periodo.fecha_inicio} y {periodo.fecha_fin}.')

            if fecha_inicio > fecha_fin:
                self.add_error('fecha_fin', 'La fecha de fin no puede ser anterior a la fecha de inicio.')

        return cleaned_data
    
    # validacion para que no se repita grupo
    def clean_grupo(self):
        grupo = self.cleaned_data.get('grupo')
        if Curso.objects.filter(grupo__iexact=grupo).exists():
            raise forms.ValidationError("Ya existe un curso con ese grupo. Usa un grupo diferente.")
        return grupo
    # es para arreglar el input de facilitador
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


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
                  'modalidad', 'duracion', 'facilitador', 'periodo','lugar', 'aula', 'dias'
                  ]
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
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cede Paulo Friere'}),
            'aula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Aula 4, Salon ...'}),
            'dias': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ej. Lunes, Miércoles y Viernes'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        modalidad = cleaned_data.get('modalidad')
        
        if not cleaned_data.get('dias'):
            self.add_error('dias', 'Este campo es obligatorio.')

        if modalidad == 'presencial':
            if not cleaned_data.get('lugar'):
                self.add_error('lugar', 'Este campo es obligatorio en modalidad presencial.')
            if not cleaned_data.get('aula'):
                self.add_error('aula', 'Este campo es obligatorio en modalidad presencial.')
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        periodo = cleaned_data.get('periodo')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if periodo and fecha_inicio and fecha_fin:
            if not (periodo.fecha_inicio <= fecha_inicio <= periodo.fecha_fin):
                self.add_error('fecha_inicio', f'La fecha de inicio debe estar entre {periodo.fecha_inicio} y {periodo.fecha_fin}.')

            if not (periodo.fecha_inicio <= fecha_fin <= periodo.fecha_fin):
                self.add_error('fecha_fin', f'La fecha de fin debe estar entre {periodo.fecha_inicio} y {periodo.fecha_fin}.')

            if fecha_inicio > fecha_fin:
                self.add_error('fecha_fin', 'La fecha de fin no puede ser anterior a la fecha de inicio.')

        return cleaned_data
    
    def clean_grupo(self):
        grupo = self.cleaned_data.get('grupo')
        if Taller.objects.filter(grupo__iexact=grupo).exists():
            raise forms.ValidationError("Ya existe un taller con ese grupo. Usa un grupo diferente.")
        return grupo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')



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
                  'modalidad', 'duracion', 'facilitador', 'periodo'
                  ,'lugar', 'aula', 'dias']
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
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cede Paulo Friere'}),
            'aula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Aula 4, Salon ...'}),
            'dias': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ej. Lunes, Miércoles y Viernes'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        modalidad = cleaned_data.get('modalidad')
        
        if not cleaned_data.get('dias'):
            self.add_error('dias', 'Este campo es obligatorio.')

        if modalidad == 'presencial':
            if not cleaned_data.get('lugar'):
                self.add_error('lugar', 'Este campo es obligatorio en modalidad presencial.')
            if not cleaned_data.get('aula'):
                self.add_error('aula', 'Este campo es obligatorio en modalidad presencial.')
        return cleaned_data


    def clean(self):
        cleaned_data = super().clean()
        periodo = cleaned_data.get('periodo')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if periodo and fecha_inicio and fecha_fin:
            if not (periodo.fecha_inicio <= fecha_inicio <= periodo.fecha_fin):
                self.add_error('fecha_inicio', f'La fecha de inicio debe estar entre {periodo.fecha_inicio} y {periodo.fecha_fin}.')

            if not (periodo.fecha_inicio <= fecha_fin <= periodo.fecha_fin):
                self.add_error('fecha_fin', f'La fecha de fin debe estar entre {periodo.fecha_inicio} y {periodo.fecha_fin}.')

            if fecha_inicio > fecha_fin:
                self.add_error('fecha_fin', 'La fecha de fin no puede ser anterior a la fecha de inicio.')

        return cleaned_data
    
    def clean_grupo(self):
        grupo = self.cleaned_data.get('grupo')
        if Diplomado.objects.filter(grupo__iexact=grupo).exists():
            raise forms.ValidationError("Ya existe un diplomado con ese grupo. Usa un grupo diferente.")
        return grupo
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'