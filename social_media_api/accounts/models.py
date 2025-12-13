from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class CustomUser(AbstractUser):
    # Champ bio
    bio = models.TextField(max_length=500, blank=True, null=True)
    
    # Champ profile_picture (utilise un chemin de stockage)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Champ followers (M2M auto-référentiel, symetrical=False)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='following',
        symmetrical=False,  # Permet aux relations d'être unilatérales (je suis A, A ne me suis pas forcément)
        blank=True
    )

    # Note: username, email, password, first_name, last_name, is_active, etc. 
    # sont hérités de AbstractUser.

    def __str__(self):
        return self.username

# Créer un Token DRF automatiquement après la sauvegarde d'un nouvel utilisateur
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)