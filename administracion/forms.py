from django import forms
from .models import CursoLanding, Diplomado, Facilitador, Noticia, Periodo, SesionCurso, SesionTaller, Taller, TallerLanding
from .models import Curso
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from multiselectfield.forms.fields import MultiSelectFormField
from .models import DIAS_SEMANA
from administracion.models import Revista
from django.core.exceptions import ValidationError


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
            'nombre_curso', 'fecha_inicio', 'fecha_fin',
            'hora_inicio', 'hora_fin', 'cupos', 'grupo',
            'modalidad', 'duracion',
            'facilitador', 'periodo','lugar', 'aula', 'dias'
        ]
        MODALIDAD_CHOICES = [
        ('virtual', 'Virtual', ),
        ('presencial', 'Presencial'),
        # ('mixto', 'Mixto'),
        ]
        widgets = {
            'nombre_curso': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            # 'descripcion': forms.Textarea(attrs={'class': 'form-control custom-input'}),
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
        self.fields['dias'].widget = forms.CheckboxSelectMultiple(choices=DIAS_SEMANA)
        for name, field in self.fields.items():
          if name != 'dias':
            field.widget.attrs.setdefault('class', 'form-control')


class TallerForm(forms.ModelForm):
    
    facilitador = forms.ModelChoiceField(
        queryset=Facilitador.objects.all(),
        required=False,
        empty_label="Sin facilitador"
    )

    class Meta:
        model = Taller
        fields = ['nombre_taller', 'fecha_inicio', 'fecha_fin',
                  'hora_inicio', 'hora_fin', 'cupos', 'grupo',
                  'modalidad', 'duracion', 'facilitador', 'periodo','lugar', 'aula', 'dias'
                  ]
        widgets = {
            'nombre_taller': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            # 'descripcion': forms.Textarea(attrs={'class': 'form-control custom-input'}),
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
        self.fields['dias'].widget = forms.CheckboxSelectMultiple(choices=DIAS_SEMANA)
        for name, field in self.fields.items():
          if name != 'dias':
            field.widget.attrs.setdefault('class', 'form-control')



class DiplomadoForm(forms.ModelForm):
    
    facilitador = forms.ModelChoiceField(
        queryset=Facilitador.objects.all(),
        required=False,
        empty_label="Sin facilitador"
    )

    class Meta:
        model = Diplomado
        fields = ['nombre_diplomado', 'fecha_inicio', 'fecha_fin',
                  'hora_inicio', 'hora_fin', 'cupos', 'grupo',
                  'modalidad', 'duracion', 'facilitador', 'periodo'
                  ,'lugar', 'aula', 'dias']
        widgets = {
            'nombre_diplomado': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            # 'descripcion': forms.Textarea(attrs={'class': 'form-control custom-input'}),
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
        self.fields['dias'].widget = forms.CheckboxSelectMultiple(choices=DIAS_SEMANA)
        for name, field in self.fields.items():
          if name != 'dias':
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



class EditarCursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre_curso', 'hora_inicio', 'hora_fin', 'cupos', 'grupo', 'duracion', 'dias', 'facilitador']
        widgets = {
            'nombre_curso': forms.TextInput(attrs={'class': 'form-control'}),
            # 'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'facilitador': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dias'].widget = forms.CheckboxSelectMultiple(choices=DIAS_SEMANA)

class EditarTallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = ['nombre_taller', 'hora_inicio', 'hora_fin', 'cupos', 'grupo', 'duracion', 'dias', 'facilitador']
        widgets = {
            'nombre_taller': forms.TextInput(attrs={'class': 'form-control'}),
            # 'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'facilitador': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dias'].widget = forms.CheckboxSelectMultiple(choices=DIAS_SEMANA)

class EditarDiplomadoForm(forms.ModelForm):
    class Meta:
        model = Diplomado
        fields = ['nombre_diplomado', 'hora_inicio', 'hora_fin', 'cupos', 'grupo', 'duracion', 'dias', 'facilitador']
        widgets = {
            'nombre_diplomado': forms.TextInput(attrs={'class': 'form-control'}),
            # 'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'facilitador': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dias'].widget = forms.CheckboxSelectMultiple(choices=DIAS_SEMANA)

from django import forms
from django.forms import ValidationError, inlineformset_factory
from .models import DiplomadoLanding, ModuloDiplomado

class DiplomadoLandingForm(forms.ModelForm):
    class Meta:
        model = DiplomadoLanding
        fields = [
            'titulo','descripcion','imagen',
            'destinatarios', 'introduccion', 'nivel',
            'proposito', 'particulares', 'recursos',
            'duracion', 'modalidad','costo', 'participantes', 'responsable', 'programa_pdf'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba el titulo del diplomado'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5 , 'placeholder': 'Escriba la descripcion del diplomado', 'style': 'rezise: none;'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'destinatarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2,'placeholder': 'Escriba los destinatarios del diplomado'}),
            'introduccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Escriba la introduccion del diplomado'}),
            'nivel': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba el nivel para este diplomado'}),
            'proposito': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Escriba el proposito general del diplomado'}),
            'particulares': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Escriba los propositos generales del diplomado'}),
            'recursos': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Escriba los recursos tecnicos del diplomado'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba la duracion de este diplomado'}),
            'modalidad': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba la modalidad de este diplomado'}),
            'costo': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba el costo de este diplomado'}),
            'participantes': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba el total de participantes para este diplomado'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba al responsable para este diplomado'}),
            'programa_pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }

class DiplomadoLandingEditForm(forms.ModelForm):
    class Meta:
        model = DiplomadoLanding
        fields = [
            'titulo','descripcion', 'imagen',
            'destinatarios', 'introduccion', 'nivel',
            'proposito', 'particulares', 'recursos',
            'duracion', 'modalidad','costo', 'participantes', 'responsable', 'programa_pdf'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba el titulo del diplomado'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5 , 'placeholder': 'Escriba la descripcion del diplomado', 'style': 'resize: none;'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'destinatarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2,'placeholder': 'Escriba los destinatarios del diplomado'}),
            'introduccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Escriba la introduccion del diplomado'}),
            'nivel': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba el nivel para este diplomado'}),
            'proposito': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Escriba el proposito general del diplomado'}),
            'particulares': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Escriba los propositos generales del diplomado'}),
            'recursos': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Escriba los recursos tecnicos del diplomado'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba la duracion de este diplomado'}),
            'modalidad': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba la modalidad de este diplomado'}),
            'costo': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba el costo de este diplomado'}),
            'participantes': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba el total de participantes para este diplomado'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Escriba al responsable para este diplomado'}),
            'programa_pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }

# sirve para crear un modulos dentro del formulario para el diplomado
class ModuloDiplomadoForm(forms.ModelForm):
    class Meta:
        model = ModuloDiplomado
        fields = ['titulo', 'descripcion']
        widgets = {  # <- ¡CORREGIDO aquí!
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el título del módulo'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escriba la descripción del módulo',
                'style': 'resize: none;'
            }),
        }

ModuloFormSet = inlineformset_factory(
    DiplomadoLanding, ModuloDiplomado,
    form=ModuloDiplomadoForm,
    extra=1, can_delete=True
)

class TallerLandingForm(forms.ModelForm):
    class Meta:
        model = TallerLanding
        fields = [
            'titulo',
            'descripcion_corta',
            'imagen',
            'subtitulo',
            'descripcion_larga',
            'responsable',
            'duracion',
            'programa_pdf',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el título del taller'
            }),
            'descripcion_corta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escriba una descripción corta del taller',
                'style': 'resize: none;'
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el subtítulo del taller'
            }),
            'descripcion_larga': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escriba la descripción larga del taller',
                'style': 'resize: none;'
            }),
            'responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del responsable académico'
            }),
            'duracion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duración total del taller'
            }),
            'programa_pdf': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class TallerLandingEditForm(forms.ModelForm):
    class Meta:
        model = TallerLanding
        fields = [
            'titulo',
            'descripcion_corta',
            'imagen',
            'subtitulo',
            'descripcion_larga',
            'responsable',
            'duracion',
            'programa_pdf',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el título del taller'
            }),
            'descripcion_corta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escriba una descripción corta del taller',
                'style': 'resize: none;'
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el subtítulo del taller'
            }),
            'descripcion_larga': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escriba la descripción larga del taller',
                'style': 'resize: none;'
            }),
            'responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del responsable académico'
            }),
            'duracion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duración total del taller'
            }),
            'programa_pdf': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

class SesionTallerForm(forms.ModelForm):
    class Meta:
        model = SesionTaller
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el título de la sesión'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escriba la descripción de la sesión',
                'style': 'resize: none;'
            }),
        }

SesionFormSet = inlineformset_factory(
    TallerLanding,
    SesionTaller,
    form=SesionTallerForm,
    extra=1,
    can_delete=True
)




class CursoLandingForm(forms.ModelForm):
    class Meta:
        model = CursoLanding
        fields = [
            'titulo',
            'descripcion_corta',
            'imagen',
            'subtitulo',
            'descripcion_larga',
            'responsable',
            'duracion',
            'programa_pdf'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el título del curso'
            }),
            'descripcion_corta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escriba una descripción corta del curso',
                'style': 'resize: none;'
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el subtítulo del curso'
            }),
            'descripcion_larga': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escriba la descripción larga del curso',
                'style': 'resize: none;'
            }),
            'responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del responsable académico'
            }),
            'duracion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duración total del curso'
            }),
            'programa_pdf': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

        
    # def clean_imagen(self):
    #     imagen = self.cleaned_data.get('imagen')
    #     if imagen:
    #         if imagen.size > 5 * 1024 * 1024:  # 5 MB
    #             raise ValidationError("La imagen no debe pesar más de 5MB.")
    #         if not imagen.content_type in ['image/jpeg', 'image/jpg', 'image/png']:
    #             raise ValidationError("Solo se permiten archivos JPEG, JPG o PNG.")
    #     return imagen

    # def clean_programa_pdf(self):
    #     pdf = self.cleaned_data.get('programa_pdf')
    #     if pdf:
    #         if pdf.size > 100 * 1024 * 1024:  # 100 MB
    #             raise ValidationError("El archivo PDF no debe superar los 100MB.")
    #         if not pdf.content_type == 'application/pdf':
    #             raise ValidationError("Solo se permite subir archivos PDF.")
    #     return pdf

class SesionCursoForm(forms.ModelForm):
    class Meta:
        model = SesionCurso
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el título de la sesión'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escriba la descripción de la sesión',
                'style': 'resize: none;'
            }),
        }

SesionFormSet = inlineformset_factory(
    CursoLanding,
    SesionCurso,
    form=SesionCursoForm,
    extra=1,
    can_delete=True
)





class NoticiasForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el título de la noticia'
            }),
        }
    # validacion para las noticias
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')

        if not imagen:
            raise ValidationError("La imagen es obligatoria.")

        # Validar tamaño (5 MB = 5 * 1024 * 1024 bytes)
        if imagen.size > 5 * 1024 * 1024:
            raise ValidationError("La imagen no debe pesar más de 5 MB.")

        # Validar tipo MIME
        valid_mime_types = ['image/jpeg', 'image/png']
        if imagen.content_type not in valid_mime_types:
            raise ValidationError("Solo se permiten imágenes JPEG y PNG.")

        return imagen
    

# Funciones de validación
def validate_image_format(value):
    # Los formatos permitidos (excepto AVIF)
    allowed_formats = ['jpeg', 'png', 'jpg', 'gif', 'bmp', 'tiff', 'webp']
    ext = value.name.split('.')[-1].lower()
    if ext not in allowed_formats:
        raise ValidationError(f"El formato {ext} no es soportado. Solo se permiten {', '.join(allowed_formats)}.")

def validate_image_size(value):
    # Limite de tamaño para la imagen (5MB)
    if value.size > 5 * 1024 * 1024:
        raise ValidationError("La imagen no puede superar los 5MB.")

def validate_pdf_size(value):
    # Limite de tamaño para el PDF (100MB)
    if value.size > 100 * 1024 * 1024:
        raise ValidationError("El PDF no puede superar los 100MB.")

def validate_pdf_format(value):
    # Verificar que el archivo sea PDF
    if value.name.split('.')[-1].lower() != 'pdf':
        raise ValidationError("Solo se permite subir archivos en formato PDF.")

# Formulario de Revista
class RevistaForm(forms.ModelForm):
    class Meta:
        model = Revista
        fields = ['titulo', 'imagen', 'pdf', 'fecha_publicacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la revista'}),
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Campo de fecha
        }

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            validate_image_format(imagen)  # Valida el formato de la imagen
            validate_image_size(imagen)    # Valida el tamaño de la imagen
        return imagen

    def clean_pdf(self):
        pdf = self.cleaned_data.get('pdf')
        if pdf:
            validate_pdf_size(pdf)  # Valida el tamaño del PDF
            validate_pdf_format(pdf)  # Valida que el archivo sea un PDF
        return pdf