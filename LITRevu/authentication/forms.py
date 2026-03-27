from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='', widget=forms.TextInput(
        attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(max_length=63, label='', widget=forms.PasswordInput(
        attrs={'placeholder': "Mot de passe"}))


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': "Nom d'utilisateur",
        })
        self.fields['username'].label = ''

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Mot de passe',
        })
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirmer le mot de passe',
        })
        self.fields['password2'].label = ''

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
