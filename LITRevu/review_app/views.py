
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth import get_user_model


User = get_user_model()

@login_required
def home(request):
    #afficher le feed des reviews et demande de review

    #gestion du nombre de page
    return render(request, 'review_app/home.html')


@login_required
def follow_user(request):
    message = ""

    if request.method == 'POST':
        username = request.POST.get('username')
        action = request.POST.get('action')
        # on vérifie que l'utilisateur existe :
        try :
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            message = f"L'utilisateur '{username}' n'existe pas."
        else:
            # arreter de suivre
            if action == "unfollow":
                request.user.follows.remove(target_user)
                message = f"Vous ne suivez plus {username}."

            # Empêcher de se suivre soi-même
            elif target_user == request.user:
                message = "Vous ne pouvez pas vous suivre vous-même."

            # Vérifier si déjà suivi
            elif request.user.follows.filter(id=target_user.id).exists():
                message = f"Vous suivez déjà {username}."

            else:
                request.user.follows.add(target_user)
                message = f"{username} a été ajouté à vos abonnements."

    context = {
        'message': message,
        'follows': request.user.follows.all(),  # mes abonnements
        'followers': request.user.followers.all(),  # mes abonnés
    }
    return render(request, 'review_app/follow.html', {'context': context})





# class UserFollows(models.Model):
#     # Your UserFollows model definition goes here
#
#     class Meta:
#         # ensures we don't get multiple UserFollows instances
#         # for unique user-user_followed pairs
#         unique_together = ('user', 'followed_user', )









# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.conf import settings
# from django.db import models
#
#
# class Ticket(models.Model):
#     # Your Ticket model definition goes here
#     pass
#
#
# class Review(models.Model):
#     ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
#     rating = models.PositiveSmallIntegerField(
#         # validates that rating must be between 0 and 5
#         validators=[MinValueValidator(0), MaxValueValidator(5)])
#     headline = models.CharField(max_length=128)
#     body = models.CharField(max_length=8192, blank=True)
#     user = models.ForeignKey(
#         to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     time_created = models.DateTimeField(auto_now_add=True)
#
#

