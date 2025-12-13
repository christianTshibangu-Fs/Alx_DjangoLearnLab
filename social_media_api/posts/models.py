from django.db import models
from django.conf import settings # Pour référencer le modèle utilisateur personnalisé

# Create your models here.

class Post(models.Model):
    """
    Représente un post publié par un utilisateur.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts', # Accès facile aux posts d'un utilisateur (user.posts.all())
        verbose_name="Auteur"
    )
    title = models.CharField(max_length=255, verbose_name="Titre du Post")
    content = models.TextField(verbose_name="Contenu")
    
    # Horodatage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Afficher les plus récents en premier
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.title} by {self.author.username}"

class Comment(models.Model):
    """
    Représente un commentaire sur un post spécifique.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments', # Accès facile aux commentaires d'un post (post.comments.all())
        verbose_name="Post Parent"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments', # Accès facile aux commentaires d'un utilisateur (user.comments.all())
        verbose_name="Auteur du Commentaire"
    )
    content = models.TextField(verbose_name="Contenu du Commentaire")
    
    # Horodatage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Afficher les commentaires chronologiquement
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"

    def __str__(self):
        # Troncature du contenu pour l'affichage lisible
        return f"Comment by {self.author.username} on post {self.post.id}: {self.content[:30]}..."