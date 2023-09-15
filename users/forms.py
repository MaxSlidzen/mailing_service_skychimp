from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserUpdateForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserLoginForm(StyleFormMixin, AuthenticationForm):

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_username(self):
        cleaned_data = self.cleaned_data['username']

        if User.objects.filter(email=cleaned_data, is_active=False).exists():
            raise forms.ValidationError('Активность аккаунта приостановлена. Проверьте электронную почту.')

        return cleaned_data
