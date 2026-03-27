from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé, permettant l'ajout de nouveaux champs.

    Hérite de AbstractUser (django.contrib.auth.models).

    Attributes:
        follows (ManyToManyField): Utilisateurs suivis par cet utilisateur.
            La relation est asymétrique : suivre quelqu'un n'implique pas
            d'être suivi en retour.
    """
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
