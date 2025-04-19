from django import forms

class LoginAlumnoForm(forms.Form):
    correo = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo'}))
    contrasena = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'}), label="Contraseña")

class LoginFacilitadorForm(forms.Form):
    correo = forms.EmailField(label="Correo",  widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo'}) )
    contrasena = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'}), label="Contraseña")