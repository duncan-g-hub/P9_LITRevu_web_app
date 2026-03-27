from django.contrib import admin
from authentication.models import User

# Enregistrement du modèle User dans l'interface d'administration
admin.site.register(User)
