from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, UserFeedView, LikePostView, UnlikePostView # Import de Like/Unlike Views

# --- Routage de base pour les Posts (/posts/) ---
# Utilisation de DefaultRouter pour obtenir les routes CRUD standards pour PostViewSet
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# --- Routage manuel pour les Commentaires imbriqués (/posts/{pk}/comments/) ---
# Ceci évite la dépendance à 'drf-nested-routers' et utilise une approche Django/DRF standard.
# L'argument 'post_pk' sera passé à la vue CommentViewSet.
comment_list = CommentViewSet.as_view({
    'get': 'list',    # Lister les commentaires d'un post spécifique
    'post': 'create'  # Créer un commentaire pour un post spécifique
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve', # Récupérer un commentaire spécifique
    'put': 'update',   # Mettre à jour un commentaire spécifique
    'patch': 'partial_update', # Mise à jour partielle
    'delete': 'destroy' # Supprimer un commentaire
})

urlpatterns = [
    # 1. Routes de base pour les Posts (Liste et Détail)
    path('', include(router.urls)),
    
    # 2. Routes imbriquées pour les Commentaires
    # Route pour la liste des commentaires (GET, POST)
    path('posts/<int:post_pk>/comments/', comment_list, name='post-comments-list'),
    
    # Route pour le détail des commentaires (GET, PUT, PATCH, DELETE)
    path('posts/<int:post_pk>/comments/<int:pk>/', comment_detail, name='post-comments-detail'),
    
    # 3. Route pour le Flux d'Actualité (Feed)
    path('feed/', UserFeedView.as_view(), name='user-feed'),

    # 4. NOUVEAU: Routes pour les Likes
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='post-unlike'),
]




























'''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers # Utilisation d'un router imbriqué (si supporté, sinon fall back)

from .views import PostViewSet, CommentViewSet

# --- Routage de base pour les Posts (/posts/) ---
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# --- Routage imbriqué pour les Commentaires (/posts/{pk}/comments/) ---
# Ceci est l'approche DRF recommandée pour les relations Post-Comment
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
# La lookup est 'post' (dérivé de la clé étrangère `post` dans le modèle Comment)
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    # 1. Routes de base (posts/)
    path('', include(router.urls)),
    
    # 2. Routes imbriquées (posts/{post_pk}/comments/)
    path('', include(posts_router.urls)),
]

# Note: Pour que les routes imbriquées fonctionnent, assurez-vous que `pip install drf-nested-routers` 
# est exécuté si vous utilisez cette bibliothèque. Si non autorisé, l'alternative est de 
# définir une vue CommentList créant un commentaire basé sur le `post_pk` passé en URL.
# Dans cet exemple, nous supposons que drf-nested-routers est disponible ou que l'imbrication 
# via les ViewSets seuls est suffisante, ce qui fonctionne avec la surcharge de `get_queryset`
# si les URLs de base sont définies manuellement. L'approche ci-dessus utilise le router imbriqué.

'''