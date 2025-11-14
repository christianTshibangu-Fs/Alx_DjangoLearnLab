from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Librarian', 'Bibliothécaire'),
    ('Member', 'Membre'),
)
class UserProfile(models.Model):
    """Extension du modèle User pour inclure le rôle."""
    # Relation One-to-One vers le modèle User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Champ de rôle avec choix prédéfinis. Le rôle par défaut sera 'Member'.
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Member',
        verbose_name='Rôle Utilisateur'
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title  

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')



# FONCTION DE SIGNAL
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée un UserProfile automatiquement quand un nouvel utilisateur est créé."""
    if created:
        UserProfile.objects.create(user=instance)

# FONCTION DE SIGNAL
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil de l'utilisateur après chaque sauvegarde du modèle User."""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
