from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q 
from .models import Post, Comment, Like # Import de Like
from .serializers import PostSerializer, CommentSerializer
from notifications.utils import create_notification # Import NOUVEAU

# --- Permissions Personnalisées ---

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser uniquement les propriétaires de l'objet à l'éditer ou le supprimer.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

# --- Pagination ---

class StandardResultsPagination(PageNumberPagination):
    """Configuration de la pagination pour les listes."""
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

# --- ViewSets ---

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les Posts. 
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] 
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content'] 
    ordering_fields = ['created_at', 'title'] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les Commentaires. 
    """
    serializer_class = CommentSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] 

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return Comment.objects.filter(post_id=post_pk)
        return Comment.objects.all()
        
    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        comment = serializer.save(author=self.request.user, post=post)
        
        # Création de notification pour l'auteur du post
        if post.author != self.request.user:
            create_notification(
                recipient=post.author, 
                actor=self.request.user, 
                verb='commenté', 
                target=comment # L'objet commenté
            )

# --- Vue du Flux d'Actualité (Feed) ---

class UserFeedView(generics.ListAPIView):
    """
    Génère le flux d'actualité pour l'utilisateur connecté.
    Affiche les posts des utilisateurs suivis, triés par date de création récente.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        user = self.request.user
        followed_users = user.following.all()
        
        # Retourne les posts des utilisateurs suivis
        queryset = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        
        return queryset

# --- NOUVEAU : Vues pour Liker/Unliker un Post (Step 2) ---

class LikePostView(generics.GenericAPIView):
    """Permet à l'utilisateur de liker un post."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        # Tenter de créer l'objet Like
        try:
            Like.objects.create(post=post, user=user)
            
            # Création de notification pour l'auteur du post
            if post.author != user:
                create_notification(
                    recipient=post.author, 
                    actor=user, 
                    verb='aimé', 
                    target=post # L'objet aimé
                )
            
            return Response({"detail": "Post liké avec succès."}, status=status.HTTP_201_CREATED)
        
        except Exception:
            # Gère le cas où l'utilisateur a déjà liké le post (unique_together contrainte)
            return Response({"detail": "Vous avez déjà liké ce post."}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(generics.DestroyAPIView):
    """Permet à l'utilisateur de retirer son like d'un post."""
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all() # Le queryset est utilisé pour get_object

    def get_object(self):
        # Récupère le Like spécifique basé sur le post_id (pk) et l'utilisateur
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        
        try:
            # Tente de trouver l'objet Like existant
            like_instance = Like.objects.get(post=post, user=self.request.user)
            return like_instance
        except Like.DoesNotExist:
            self.handle_exception(
                Response({"detail": "Vous n'avez pas encore liké ce post."}, status=status.HTTP_404_NOT_FOUND)
            )

    def delete(self, request, *args, **kwargs):
        try:
            # Appelle get_object pour vérifier l'existence et l'appartenance
            self.get_object().delete()
            return Response({"detail": "Like retiré avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            # Gère l'exception levée par handle_exception dans get_object si Like non trouvé
            return e.args[0]