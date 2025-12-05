from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Post
from .forms import PostForm


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

@login_required
def profile(request):

    if request.method == 'POST':
        # On instancie les formulaires avec les données envoyées (request.POST) 
        # et les fichiers (request.FILES pour l'image)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Votre compte a été mis à jour !')
            return redirect('profile') # Redirection pour éviter la resoumission du formulaire (Post/Redirect/Get pattern)

    else:
        # Requête GET : On pré-remplit les formulaires avec les infos actuelles de l'utilisateur
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'blog/profile.html', context)

# 1. ListView (Liste tous les posts - Public)
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-published_date'] # Ordre : plus récent en premier
    paginate_by = 5 # Optionnel : ajoute la pagination

# 2. DetailView (Détail d'un post - Public)
class PostDetailView(DetailView):
    model = Post
    # Cherche blog/post_detail.html par défaut

# 3. CreateView (Créer un post - Authentifié seulement)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    # Cherche blog/post_form.html par défaut
    success_url = '/' # Redirige vers la page d'accueil après la création

    # Étape 5 : Surcharge de form_valid pour définir l'auteur automatiquement
    def form_valid(self, form):
        form.instance.author = self.request.user # Définit l'auteur comme l'utilisateur actuellement connecté
        return super().form_valid(form)

# 4. UpdateView (Modifier un post - Auteur seulement + Authentifié)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    # Cherche blog/post_form.html par défaut

    # Surcharge de form_valid pour définir l'auteur (même si c'est une mise à jour)
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

    # Étape 5 : Test de permission pour s'assurer que l'utilisateur est l'auteur
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# 5. DeleteView (Supprimer un post - Auteur seulement + Authentifié)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # Cherche blog/post_confirm_delete.html par défaut
    success_url = '/' # Redirige vers la page d'accueil après la suppression

    # Étape 5 : Test de permission pour s'assurer que l'utilisateur est l'auteur
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def post(request):
    pass



