from django import forms
from home.models import User


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def clean(self):
        return self.cleaned_data


class UserRegisterForm(forms.ModelForm):
    repeat_password = forms.PasswordInput()
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'sex', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        return self.cleaned_data