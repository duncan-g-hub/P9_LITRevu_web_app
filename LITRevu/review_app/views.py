
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth import get_user_model

from .models import Ticket, Review

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



@login_required
def add_ticket(request):
    # if form is valid ; if request = post ; gestion auteur ; date
    form = forms.TicketForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            ticket = form.save(commit=False) # objet Ticket créé mais pas sauvegardé
            ticket.author = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'review_app/add_ticket.html', {'form': form})






@login_required
def edit_ticket(request, ticket_id):
    # if form is valid ; if request = post ; gestion auteur ; date
    ticket = Ticket.objects.get(id=ticket_id)
    form = forms.TicketForm(request.POST or None, request.FILES or None, instance=ticket)
    context = {'ticket': ticket, 'form': form}
    if request.method == 'POST':
        if form.is_valid():
            ticket.save()
            return redirect('posts')
    return render(request, 'review_app/edit_ticket.html', {'context': context})

@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'review_app/delete_ticket.html', {'ticket': ticket})


@login_required
def add_review(request):
    # if form is valid ; if request = post ; gestion auteur ; date ; ticket
    form = forms.ReviewForm(request.POST)
    return render(request, 'review_app/add_review.html', {'form': form})


@login_required
def edit_review(request, review_id):
    # if form is valid ; if request = post ; gestion auteur ; date ; ticket
    review = Review.objects.get(id=review_id)
    form = forms.ReviewForm(request.POST or None, request.FILES or None, instance=review)
    context = {'review': review, 'form': form}
    return render(request, 'review_app/edit_review.html', {'context': context})


@login_required
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 'review_app/delete_review.html', {'review': review})




@login_required
def posts(request):
    tickets = Ticket.objects.filter(author=request.user)
    reviews = Review.objects.filter(author=request.user)
    context = {'tickets': tickets, 'reviews': reviews}
    return render(request, 'review_app/posts.html', {'context': context})