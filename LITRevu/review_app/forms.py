from django.contrib.auth import get_user_model
from django import forms

from LITRevu.review_app.models import Review, Ticket


# On crée les formulaires à partir des modele

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "headline", "body")
