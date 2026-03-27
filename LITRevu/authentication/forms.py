from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    """
    Formulaire pour la connection d'un utilisateur.
    Hérite de Form (django.forms)
    """
    username = forms.CharField(max_length=63, label='', widget=forms.TextInput(
        attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(max_length=63, label='', widget=forms.PasswordInput(
        attrs={'placeholder': "Mot de passe"}))


class SignupForm(UserCreationForm):
    """
    Formulaire d'inscription d'un nouvel utilisateur.
    Hérite de UserCreationForm (django.contrib.auth.forms).
    """
    class Meta(UserCreationForm.Meta):
        """Métadonnées du formulaire : modèle utilisé et champs affichés."""
        model = get_user_model()
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        """Initialise le formulaire d'inscription.

        Appelle le constructeur parent puis personnalise les champs
        username, password1 et password2 : ajout de placeholders,
        suppression des labels et des textes d'aide.

        Args:
            *args: Arguments positionnels transmis au constructeur parent (UserCreationForm).
            **kwargs: Arguments nommés transmis au constructeur parent (UserCreationForm).
        """
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
