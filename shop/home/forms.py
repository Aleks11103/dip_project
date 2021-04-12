from django import forms
from home.models import User, Comment


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
    password = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput,
    )
    repeat_password = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput,
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'sex', 'role']

    def clean_repeat_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['repeat_password']:
            raise forms.ValidationError('Пароли не совпадают!!!')
        return cd['repeat_password']

    def clean(self):
        return self.cleaned_data


class UserEditForm(forms.ModelForm):
    password = forms.CharField(
        label='Введите пароль',
        required=False,
        widget=forms.PasswordInput,
    )
    repeat_password = forms.CharField(
        label='Повторите пароль',
        required=False,
        widget=forms.PasswordInput,
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'sex', 'birth_date', 'land', 'city')
    
    def clean(self):
        return self.cleaned_data

    def clean_repeat_new_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['repeat_password']:
            raise forms.ValidationError('Пароли не совпадают!!!')
        return cd['repeat_password']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'product', 'user']
        widgets = {
            'product': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }
    
    def clean(self):
        return self.cleaned_data