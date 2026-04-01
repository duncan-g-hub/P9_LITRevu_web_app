from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings


class Ticket(models.Model):
    """
    Modèle représentant une demande de critique.

    Hérite de Model (django.db.models).

    Attributes:
        title (CharField): Titre du ticket
        description (CharField): Description du ticket
        image (ImageField): Image de l'oeuvre lié au ticket (optionnelle)
        time_created (DateTimeField): Date de création du ticket (automatique)
        author (ForeignKey): Auteur du ticket, relation plusieurs à un vers User
        closed (BooleanField): Ticket fermé ou non. Défaut : False
    """
    title = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False, blank=True)


class Review(models.Model):
    """
    Modèle représentant une critique d'une oeuvre.

    Hérite de Model (django.db.models).

    Attributes:
        ticket (ForeignKey): Ticket associé, relation plusieurs à un vers Ticket
        rating (PositiveSmallIntegerField): Note de l'oeuvre, entre 0 et 5
        headline (CharField): Titre de la critique
        body (TextField): Contenu textuel de la critique
        author (ForeignKey): Auteur de la critique, relation plusieurs à un vers User
        time_created (DateTimeField): Date de création de la critique (automatique)
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField()
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """
    Modèle représentant la relation d'abonnement entre deux utilisateurs.

    Attributes:
        user (ForeignKey): L'utilisateur qui suit.
        followed_user (ForeignKey): L'utilisateur qui est suivi.

    Meta:
        unique_together: Empêche qu'un utilisateur suive deux fois le même utilisateur.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')