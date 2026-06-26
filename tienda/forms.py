from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = ("username", "email")

  
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("❌ Este correo ya está registrado en otra cuenta.")
        return email



class PerfilUsuarioForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    
    password_actual = forms.CharField(
        label="Contraseña Actual (Requerida para guardar)",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña actual'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError("❌ Este correo ya está siendo usado por otro usuario.")
        return email

   
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.user.id).exists():
            raise forms.ValidationError("❌ Este nombre de usuario ya está ocupado. Elige otro.")
        return username

    
    def clean_password_actual(self):
        password = self.cleaned_data.get('password_actual')
        if not self.user.check_password(password):
            raise forms.ValidationError("❌ La contraseña ingresada es incorrecta.")
        return password