from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import LibraryDetailView, list_books

urlpatterns = [
    # Vue d'Inscription (utilise la vue personnalisée)
    path('register/', views.register, name='register'),
    
    # Vue de Connexion (utilise la vue intégrée de Django)
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Vue de Déconnexion (utilise la vue intégrée de Django)
    path('logout/', LogoutView.as_view(templete_name='relationship_app/login/'), name='logout'),
    
    # Vous devriez également avoir un chemin racine pour tester les redirections
    # path('', views.home_page, name='home'), 
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]

