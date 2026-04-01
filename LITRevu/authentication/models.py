from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    """
    Modèle utilisateur personnalisé, permettant l'ajout de nouveaux champs.

    Hérite de AbstractUser (django.contrib.auth.models).
    """
    pass
