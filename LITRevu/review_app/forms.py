from django.contrib.auth import get_user_model
from django import forms


from review_app.models import Review, Ticket


# On crée les formulaires à partir des modele

class TicketForm(forms.ModelForm):
    title = forms.CharField(label="Titre")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    image = forms.ImageField(label="Image", required=False)

    class Meta:
        model = Ticket
        fields = ("title", "description", "image")



class ReviewForm(forms.ModelForm):
    headline = forms.CharField(label="Titre")
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect,
        label = "Note")
    body = forms.CharField(label="Commentaire", widget=forms.Textarea)

    class Meta:
        model = Review
        fields = ("headline", "rating", "body")
