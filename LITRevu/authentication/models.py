from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # modele user de base, on laisse la possiblité d'ajouter des champs supplémentaire avec AbstractUser)

    #gestion des abonnées et abbonnements
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)