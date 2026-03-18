from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # modele user de base, on laisse la possiblité d'ajouter des champs supplémentaire avec AbstractUser)

    #gestion des abbonnements et abonnées
    followers = models.ManyToManyField('self', symmetrical=False, verbose_name='followers')
    follows = models.ManyToManyField('self', symmetrical=False, verbose_name='follows')



