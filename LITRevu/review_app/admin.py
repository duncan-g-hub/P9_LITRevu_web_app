from django.contrib import admin
from review_app.models import Ticket, Review

# Enregistrement du modèle User dans l'interface d'administration
admin.site.register(Ticket)
admin.site.register(Review)
