from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book, Librarian
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.


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
    return render(request, 'relationship_app/register.html', {'form': form})

# Note: Pour le reste (Login et Logout), nous utilisons directement les vues intégrées de Django dans urls.py.

# Si vous avez besoin d'une page d'accueil simple pour la redirection:
def home_page(request):
    return render(request, 'relationship_app/home.html')

# (Vous devez créer un template home.html si vous utilisez cette fonction)

@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.role == 'Admin')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.role == 'Librarian')    
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.role == 'Member')   
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@permission_required('relationship_app.can_add_book',login_url='login', raise_exception=True)
def book_add(request):

    return render(request, 'relationship_app/book_add.html')

@permission_required('relationship_app.can_change_book', login_url='login', raise_exception=True)
def book_edit(request, pk):
    return render(request, 'relationship_app/book_edit.html ')

    return render(request, 'relationship_app/book_update.html')

@permission_required('relationship_app.can_delete_book', login_url='login', raise_exception=True)
def book_delete(request, pk):
    return render(request, 'relationship_app/book_delete.html')

def list_books(request):
    books = Book.objects.all().select_related('author')

    context = {
        'books': books
    }   
    return render(request ,"relationship_app/list_books.html" , context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = 'library'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('books__author')