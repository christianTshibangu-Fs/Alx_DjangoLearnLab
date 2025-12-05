from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.


def home_page(request):
    return render(request, 'blog/home.html')

# Vue d'inscription personnalisée
def register(request):
    """Gère l'inscription de nouveaux utilisateurs."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Connecte l'utilisateur immédiatement après l'inscription
            login(request, user)
            # Redirige vers la page d'accueil ou une autre page après l'inscription
            return redirect('/') 
    else:
        form = UserCreationForm()
    
    # Rend le template 'register.html' en passant le formulaire
    return render(request, 'blog/register.html', {'form': form})
