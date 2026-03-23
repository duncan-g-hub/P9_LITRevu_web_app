
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth import get_user_model
from django.db.models import Q


from .models import Ticket, Review

User = get_user_model()

@login_required
def feed(request):
    follows = request.user.follows.all()

    followed_users = []
    for follow in follows:
        followed_users.append(follow)
    followed_users.append(request.user)

    tickets = Ticket.objects.filter(author__in=followed_users)
    reviews = Review.objects.filter(Q(author__in=followed_users) | Q(ticket__author = request.user))

    items = []
    for ticket in tickets:
        ticket.type = 'TICKET'
        items.append(ticket)
    for review in reviews:
        review.type = 'REVIEW'
        items.append(review)

    context = sorted(items, key=lambda x: x.time_created, reverse=True)


    #gestion du nombre de page
    return render(request, 'review_app/feed.html', {'context': context})


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
    form = forms.TicketForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            ticket = form.save(commit=False) # objet Ticket créé mais pas sauvegardé
            ticket.author = request.user
            ticket.save()
            return redirect('feed')
    return render(request, 'review_app/add_ticket.html', {'form': form})




@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.author != request.user:
        return redirect('feed')
    form = forms.TicketForm(request.POST or None, request.FILES or None, instance=ticket)
    context = {'ticket': ticket, 'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request, 'review_app/edit_ticket.html', {'context': context})

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.author != request.user:
        return redirect('feed')
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'review_app/delete_ticket.html', {'ticket': ticket})



@login_required
def add_review_and_ticket(request):
    ticket_form = forms.TicketForm(request.POST or None, request.FILES or None)
    review_form = forms.ReviewForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if ticket_form.is_valid() and review_form.is_valid():
            review = review_form.save(commit=False)  # objet Review créé mais pas sauvegardé
            ticket = ticket_form.save(commit=False)  # objet Ticket créé mais pas sauvegardé

            ticket.author = request.user
            ticket.save()

            review.author = request.user
            review.ticket = ticket
            review.save()

            ticket.closed = True
            ticket.save()
            return redirect('feed')

    context = {'ticket_form': ticket_form, 'review_form': review_form}
    return render(request, 'review_app/add_review_and_ticket.html', {'context': context})


@login_required
def add_review_from_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = forms.ReviewForm(request.POST or None, request.FILES or None)
    context = {'ticket': ticket, 'review_form': review_form}
    if request.method == 'POST':
        if review_form.is_valid():
            review = review_form.save(commit=False)  # objet Review créé mais pas sauvegardé

            review.author = request.user
            review.ticket = ticket
            review.save()
            ticket.closed = True
            ticket.save()
            return redirect('feed')
    return render(request, 'review_app/add_review_from_ticket.html', {'context': context})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review,id=review_id)
    if review.author != request.user:
        return redirect('feed')
    form = forms.ReviewForm(request.POST or None, request.FILES or None, instance=review)
    context = {'review': review, 'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request, 'review_app/edit_review.html', {'context': context})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review,id=review_id)
    if review.author != request.user:
        return redirect('feed')
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 'review_app/delete_review.html', {'review': review})




@login_required
def posts(request):
    tickets = Ticket.objects.filter(author=request.user)
    reviews = Review.objects.filter(author=request.user)

    items = []
    for ticket in tickets:
        ticket.type = 'TICKET'
        items.append(ticket)
    for review in reviews:
        review.type = 'REVIEW'
        items.append(review)

    context = sorted(items, key=lambda x: x.time_created, reverse=True)
    return render(request, 'review_app/posts.html', {'context': context})