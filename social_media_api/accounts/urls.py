from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token # DRF Login View
from .views import RegisterView, ProfileView

urlpatterns = [
    # Étape 3: Enregistrement (/register)
    # Retourne le token après la création de l'utilisateur
    path('register/', RegisterView.as_view(), name='register'),
    
    # Étape 3: Login (/login)
    # DRF fournit la vue obtain_auth_token qui prend username/password et retourne le token
    path('login/', obtain_auth_token, name='login'),
    
    # Étape 3: Gestion du Profil (/profile)
    # Permet de voir (GET) et mettre à jour (PUT/PATCH) le profil de l'utilisateur connecté
    path('profile/', ProfileView.as_view(), name='profile-management'),
]