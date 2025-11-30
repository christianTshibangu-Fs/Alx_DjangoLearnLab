from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer # Assurez-vous d'avoir un BookSerializer fonctionnel

# Create your views here.

# --- Vues pour le Modèle Book ---

# Mixin d'autorisation par défaut : Lecture pour tous, Écriture pour les connectés.
DEFAULT_PERMISSION_CLASSES = [IsAuthenticatedOrReadOnly]

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Ajoutez des filtres si nécessaire
    search_fields = ['title', 'author', 'publication_year']  # Champs à rechercher
    ordering_fields = ['published_date', 'title']  # Champs pour le tri

#  Vue pour Créer (POST /books/)
class BookCreateView(generics.CreateAPIView):
    """
    Gère la récupération de la liste complète des livres et la création d'un nouveau livre.
    (Combine ListView et CreateView)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = DEFAULT_PERMISSION_CLASSES 

# Vue pour Détail (GET), Mise à jour (PUT/PATCH) et Suppression (DELETE)
class BookDetailView(generics.RetrieveAPIView):
    """
    Gère la récupération, la modification ou la suppression d'un seul livre par ID (PK).
    (Combine DetailView, UpdateView et DeleteView)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk' # Définit le champ de recherche dans l'URL (par défaut à 'pk')
    permission_classes = DEFAULT_PERMISSION_CLASSES

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    permission_classes = DEFAULT_PERMISSION_CLASSES

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    permission_classes = DEFAULT_PERMISSION_CLASSES 

