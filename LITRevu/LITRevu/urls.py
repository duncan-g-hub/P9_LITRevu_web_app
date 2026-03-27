"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import review_app.views

# Définition des patterns d'URL de l'application
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', review_app.views.feed, name='feed'),
    path("posts/", review_app.views.posts, name='posts'),

    path('login/', authentication.views.login_page, name='login'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('logout/', authentication.views.logout_user, name='logout'),

    path('follow/', review_app.views.follow_user, name='follow'),
    path('unfollow/', review_app.views.unfollow_user, name='unfollow'),

    path("ticket/add/", review_app.views.add_ticket, name='add-ticket'),
    path("ticket/edit/<int:ticket_id>/", review_app.views.edit_ticket, name='edit-ticket'),
    path("ticket/delete/<int:ticket_id>/", review_app.views.delete_ticket, name='delete-ticket'),

    path("review/add/", review_app.views.add_review_and_ticket, name='add-review-and-ticket'),
    path("review/add/<int:ticket_id>/", review_app.views.add_review_from_ticket, name='add-review-from-ticket'),
    path("review/edit/<int:review_id>/", review_app.views.edit_review, name='edit-review'),
    path("review/delete/<int:review_id>/", review_app.views.delete_review, name='delete-review'),
]

# En mode développement, sert les fichiers médias depuis MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
