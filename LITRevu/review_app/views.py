from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Ticket, Review

User = get_user_model()


@login_required
def feed(request):
    """
    Affiche le flux principal de l'utilisateur connecté, paginé par 5 éléments.
    Récupère les tickets et critiques des utilisateurs suivis ainsi que
    les critiques liées aux tickets de l'utilisateur, triés par date décroissante.
        Args:
            request (HttpRequest): Requête HTTP entrante.

        Returns:
            HttpResponse: Page de flux via le template feed.html,
            avec les tickets et critiques paginés.
    """
    follows = request.user.follows.all()

    followed_users = []
    for follow in follows:
        followed_users.append(follow)
    followed_users.append(request.user)

    tickets = Ticket.objects.filter(author__in=followed_users)
    reviews = Review.objects.filter(Q(author__in=followed_users) | Q(ticket__author=request.user))

    items = []
    for ticket in tickets:
        ticket.type = 'TICKET'
        items.append(ticket)
    for review in reviews:
        review.type = 'REVIEW'
        items.append(review)

    context = sorted(items, key=lambda x: x.time_created, reverse=True)

    # gestion du nombre de page
    paginator = Paginator(context, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'review_app/feed.html', {'page_obj': page_obj})


@login_required
def follow_user(request):
    """
    Affiche la page des abonnements et traite l'ajout d'un nouvel abonnement pour l'utilisateur connecté.

    Affiche les abonnements et abonnés de l'utilisateur connecté.
    En GET, tente d'abonner l'utilisateur à un autre via son nom d'utilisateur.
    En POST, empêche de se suivre soi-même ou de suivre un utilisateur déjà suivi.
        Args:
            request (HttpRequest): Requête HTTP entrante.

        Returns:
            HttpResponse: Page des abonnements via le template follow.html,
            avec la liste des abonnements, abonnés et un message de retour.
    """
    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        # on vérifie que l'utilisateur existe :
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            message = f"L'utilisateur '{username}' n'existe pas."
        else:
            # Empêcher de se suivre soi-même
            if target_user == request.user:
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


login_required


def unfollow_user(request):
    """Traite la suppression d'un abonnement.

    En GET, désabonne l'utilisateur connecté d'un autre utilisateur
    via son nom d'utilisateur.
    En POST, redirige si l'utilisateur cible n'existe pas ou n'est pas suivi.

    Args:
        request (HttpRequest): Requête HTTP entrante.

    Returns:
        HttpResponseRedirect: Redirige vers la page des abonnements ('follow').
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            # arreter de suivre en controllant si il y a bien un suivi
            if request.user.follows.filter(id=target_user.id).exists():
                request.user.follows.remove(target_user)
    return redirect('follow')


@login_required
def add_ticket(request):
    """Affiche et traite le formulaire de création d'un ticket.

    En GET, affiche le formulaire vide.
    En POST, valide le formulaire, assigne l'auteur à l'utilisateur connecté,
    sauvegarde le ticket puis redirige vers le flux.

    Args:
        request (HttpRequest): Requête HTTP entrante.

    Returns:
        HttpResponse: Formulaire de création via le template add_ticket.html,
            ou redirige vers 'feed' après une création réussie.
    """
    form = forms.TicketForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            ticket = form.save(commit=False)  # objet Ticket créé mais pas sauvegardé
            ticket.author = request.user
            ticket.save()
            return redirect('feed')
    return render(request, 'review_app/add_ticket.html', {'form': form})


@login_required
def edit_ticket(request, ticket_id):
    """Affiche et traite le formulaire de modification d'un ticket.

    Vérifie que le ticket appartient à l'utilisateur connecté, sinon redirige vers les posts.
    En GET, affiche le formulaire pré-rempli.
    En POST, valide et sauvegarde les modifications puis redirige vers les posts.

    Args:
        request (HttpRequest): Requête HTTP entrante.
        ticket_id (int): Identifiant du ticket à modifier.

    Returns:
        HttpResponse: Formulaire de modification via le template edit_ticket.html,
            ou redirige vers 'posts' après une modification réussie,
            ou redirige vers 'posts' si l'utilisateur n'est pas l'auteur.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.author != request.user:
        return redirect('posts')
    form = forms.TicketForm(request.POST or None, request.FILES or None, instance=ticket)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request, 'review_app/edit_ticket.html', {'ticket': ticket, 'form': form})


@login_required
def delete_ticket(request, ticket_id):
    """Affiche et traite la confirmation de suppression d'un ticket.

    Vérifie que le ticket appartient à l'utilisateur connecté, sinon redirige vers les posts.
    En GET, affiche la page de confirmation.
    En POST, supprime le ticket puis redirige vers les posts.

    Args:
        request (HttpRequest): Requête HTTP entrante.
        ticket_id (int): Identifiant du ticket à supprimer.

    Returns:
        HttpResponse: Page de confirmation via le template delete_ticket.html,
            ou redirige vers 'posts' après une suppression réussie,
            ou redirige vers 'posts' si l'utilisateur n'est pas l'auteur.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.author != request.user:
        return redirect('posts')
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'review_app/delete_ticket.html', {'ticket': ticket})


@login_required
def add_review_and_ticket(request):
    """Affiche et traite la création simultanée d'un ticket et d'une critique.

    En GET, affiche les deux formulaires vides.
    En POST, valide les deux formulaires, crée le ticket (marqué comme fermé),
    lui associe la critique, assigne l'auteur aux deux objets, puis redirige vers le flux.

    Args:
        request (HttpRequest): Requête HTTP entrante.

    Returns:
        HttpResponse: Page de création via le template add_review_and_ticket.html,
            ou redirige vers 'feed' après une création réussie.
    """
    ticket_form = forms.TicketForm(request.POST or None, request.FILES or None)
    review_form = forms.ReviewForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if ticket_form.is_valid() and review_form.is_valid():
            review = review_form.save(commit=False)  # objet Review créé mais pas sauvegardé
            ticket = ticket_form.save(commit=False)  # objet Ticket créé mais pas sauvegardé

            ticket.author = request.user
            ticket.closed = True
            ticket.save()

            review.author = request.user
            review.ticket = ticket
            review.save()

            return redirect('feed')

    context = {'ticket_form': ticket_form, 'review_form': review_form}
    return render(request, 'review_app/add_review_and_ticket.html', {'context': context})


@login_required
def add_review_from_ticket(request, ticket_id):
    """Affiche et traite la création d'une critique pour un ticket existant.

    En GET, affiche le formulaire de critique avec le ticket associé.
    En POST, valide le formulaire, marque le ticket comme fermé,
    assigne l'auteur à la critique puis redirige vers le flux.

    Args:
        request (HttpRequest): Requête HTTP entrante.
        ticket_id (int): Identifiant du ticket auquel associer la critique.

    Returns:
        HttpResponse: Page de création via le template add_review_from_ticket.html,
            ou redirige vers 'feed' après une création réussie.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = forms.ReviewForm(request.POST or None, request.FILES or None)
    context = {'ticket': ticket, 'review_form': review_form}
    if request.method == 'POST':
        if review_form.is_valid():
            review = review_form.save(commit=False)  # objet Review créé mais pas sauvegardé

            ticket.closed = True
            ticket.save()

            review.author = request.user
            review.ticket = ticket
            review.save()

            return redirect('feed')
    return render(request, 'review_app/add_review_from_ticket.html', {'context': context})


@login_required
def edit_review(request, review_id):
    """Affiche et traite le formulaire de modification d'une critique.

    Vérifie que la critique appartient à l'utilisateur connecté, sinon redirige vers les posts.
    En GET, affiche le formulaire pré-rempli.
    En POST, valide et sauvegarde les modifications puis redirige vers les posts.

    Args:
        request (HttpRequest): Requête HTTP entrante.
        review_id (int): Identifiant de la critique à modifier.

    Returns:
        HttpResponse: Formulaire de modification via le template edit_review.html,
            ou redirige vers 'posts' après une modification réussie,
            ou redirige vers 'posts' si l'utilisateur n'est pas l'auteur.
    """
    review = get_object_or_404(Review, id=review_id)
    if review.author != request.user:
        return redirect('posts')
    form = forms.ReviewForm(request.POST or None, request.FILES or None, instance=review)
    context = {'review': review, 'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request, 'review_app/edit_review.html', {'context': context})


@login_required
def delete_review(request, review_id):
    """Affiche et traite la confirmation de suppression d'une critique.

    Vérifie que la critique appartient à l'utilisateur connecté, sinon redirige vers les posts.
    En GET, affiche la page de confirmation.
    En POST, supprime la critique puis redirige vers les posts.

    Args:
        request (HttpRequest): Requête HTTP entrante.
        review_id (int): Identifiant de la critique à supprimer.

    Returns:
        HttpResponse: Page de confirmation via le template delete_review.html,
            ou redirige vers 'posts' après une suppression réussie,
            ou redirige vers 'posts' si l'utilisateur n'est pas l'auteur.
    """
    review = get_object_or_404(Review, id=review_id)
    if review.author != request.user:
        return redirect('posts')
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 'review_app/delete_review.html', {'review': review})


@login_required
def posts(request):
    """Affiche les tickets et critiques de l'utilisateur connecté, paginés par 5 éléments.

    Récupère uniquement les tickets et critiques dont l'utilisateur est l'auteur,
    triés par date de création décroissante.

    Args:
        request (HttpRequest): Requête HTTP entrante.

    Returns:
        HttpResponse: Page des posts via le template posts.html,
            avec les tickets et critiques paginés.
    """
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

    paginator = Paginator(context, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'review_app/posts.html', {'page_obj': page_obj})
