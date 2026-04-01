from django import forms

from review_app.models import Review, Ticket


class TicketForm(forms.ModelForm):
    """
    Formulaire de création et modification d'un Ticket.
    Hérite de ModelForm (django.forms).
    Un ticket correspond à une demande de critique.
    """
    title = forms.CharField(label="Titre")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    image = forms.ImageField(label="Image", required=False)

    class Meta:
        """Métadonnées du formulaire : modèle utilisé et champs affichés."""
        model = Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    """
    Formulaire de création et modification d'une Review.
    Hérite de ModelForm (django.forms).
    """
    headline = forms.CharField(label="Titre")
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect,
        label="Note")
    body = forms.CharField(label="Commentaire", widget=forms.Textarea)

    class Meta:
        """Métadonnées du formulaire : modèle utilisé et champs affichés."""
        model = Review
        fields = ("headline", "rating", "body")
