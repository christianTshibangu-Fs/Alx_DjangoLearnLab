from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('L\'Email doit être défini'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('adresse e-mail'), unique=True)
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

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username'] 

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('utilisateur personnalisé')
        verbose_name_plural = _('utilisateurs personnalisés')

    def __str__(self):
        return self.email
    # Note: username, email, password, first_name, last_name, is_active, etc. 
    # sont hérités de AbstractUser.


# Créer un Token DRF automatiquement après la sauvegarde d'un nouvel utilisateur
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)