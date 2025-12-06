from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home_page, name='home'), # Home page route
    # You can add more blog-related routes here
    path('register/', views.register, name='register'), # Registration route
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'), # Login route
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), # Logout route
    path('profile/', views.profile, name='profile'), # User profile route   
    #path('post/',views.post, name='posts'), # Post list route

    # ListView (Affiche tous les posts)
    path('post/', views.PostListView.as_view(), name='posts'),
    # DetailView (Détail d'un post spécifique)
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    # CreateView (Créer un nouveau post)
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    # UpdateView (Modifier un post spécifique)
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    # DeleteView (Supprimer un post spécifique)
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    path('posts/int:post_id/comments/new/', views.CommentCreateView.as_view() , name= 'add-comment'),  # Inclure les URLs de l'application de commentaires
    path('comment/int:pk/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/int:pk/update/', views.CommentUpdateView.as_view(), name='comment-update'),
]