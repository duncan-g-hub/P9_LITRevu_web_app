from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings

from . import forms


def login_page(request):
    """
    Affiche et traite le formulaire de connexion.

    Args:
        request (HttpRequest): Requête HTTP entrante.

    Returns:
        HttpResponse: Redirige vers 'feed' si la connexion réussit,
            sinon retourne la page de connexion avec le formulaire
            et un éventuel message d'erreur.
    """
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})


def signup_page(request):
    """
        Affiche et traite le formulaire d'inscription.

        Args:
            request (HttpRequest): Requête HTTP entrante.

        Returns:
            HttpResponse: Redirige vers 'login' si l'inscription réussit,
                sinon retourne la page d'inscription avec le formulaire
                et un éventuel message d'erreur.
    """
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})


def logout_user(request):
    """
        Déconnecte l'utilisateur.

        Args:
            request (HttpRequest): Requête HTTP entrante.

        Returns:
            HttpResponse: Redirige vers la page de connexion.
    """
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)
