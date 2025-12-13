from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q # Pour des requêtes complexes
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


# Create your views here.


# --- Permissions Personnalisées (Step 3) ---

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser uniquement les propriétaires de l'objet à l'éditer ou le supprimer.
    Les requêtes GET, HEAD, OPTIONS sont toujours autorisées (lecture seule).
    """
    def has_object_permission(self, request, view, obj):
        # La permission de lecture est toujours autorisée pour les requêtes sûres (GET, HEAD, OPTIONS).
        if request.method in permissions.SAFE_METHODS:
            return True

        # Les permissions d'écriture ne sont autorisées que si l'utilisateur est l'auteur de l'objet.
        return obj.author == request.user

# --- Pagination (Step 5) ---

class StandardResultsPagination(PageNumberPagination):
    """Configuration de la pagination pour les listes."""
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

# --- ViewSets (Steps 3 & 5) ---

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les Posts. 
    Inclus la création, lecture, mise à jour, suppression, pagination et filtrage.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsPagination
    
    # Permissions : lecture pour tous, écriture/modification pour les authentifiés/propriétaires
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] 
    
    # Filtrage (Step 5): Permet la recherche par titre ou contenu
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content'] # Champs sur lesquels la recherche est appliquée (e.g., ?search=mot_cle)
    ordering_fields = ['created_at', 'title'] # Champs pour le tri (e.g., ?ordering=-created_at)

    def perform_create(self, serializer):
        """Associe automatiquement l'utilisateur connecté comme auteur lors de la création."""
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les Commentaires. 
    Inclus la création, lecture, mise à jour, suppression, et l'association au post.
    """
    serializer_class = CommentSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] 
    
    # Le queryset est ajusté pour filtrer les commentaires par Post ID dans `get_queryset`
    # Ceci est requis car les commentaires sont généralement imbriqués ou filtrés par post.

    def get_queryset(self):
        """Retourne uniquement les commentaires pour un post spécifique s'il est fourni dans l'URL."""
        # Récupère 'post_pk' si la route a été définie comme imbriquée (voir urls.py)
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return Comment.objects.filter(post_id=post_pk)
        
        # Si non imbriqué, retourne tous les commentaires (pour /comments/)
        return Comment.objects.all()
        
    def perform_create(self, serializer):
        """Associe automatiquement l'utilisateur connecté comme auteur et le post parent."""
        
        # Récupère le Post parent si la route est imbriquée (Post/1/comments/)
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        
        # Sauvegarde l'objet Comment en définissant l'auteur et le post
        serializer.save(author=self.request.user, post=post)

       
# --- NOUVEAU : Vue du Flux d'Actualité (Feed) ---

class UserFeedView(generics.ListAPIView):
    """
    Génère le flux d'actualité pour l'utilisateur connecté.
    Affiche les posts des utilisateurs suivis, triés par date de création récente.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        # Récupère l'utilisateur connecté
        user = self.request.user
        
        # 1. Identifier les utilisateurs que l'utilisateur actuel suit (IDs)
        # On utilise le related_name 'following' défini dans le modèle CustomUser
        followed_users = user.following.all()
        
        # 2. Filtrer les posts : Inclure uniquement les posts dont l'auteur fait partie des utilisateurs suivis
        # Optionnel: On peut aussi inclure ses propres posts (décommenter si désiré)
        # followed_users_ids = list(followed_users.values_list('id', flat=True))
        # followed_users_ids.append(user.id) # Ajouter l'utilisateur lui-même
        
        queryset = Post.objects.filter(author__in=followed_users).order_by()
        
        return queryset