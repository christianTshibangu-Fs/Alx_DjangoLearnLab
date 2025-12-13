from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


CustomUser = settings.AUTH_USER_MODEL

class Notification(models.Model):
    """
    Modèle représentant une notification pour un utilisateur.
    Utilise GenericForeignKey pour pouvoir cibler différents types d'objets (Post, Comment, etc.).
    """
    
    # L'utilisateur qui reçoit la notification
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    
    # L'utilisateur qui a effectué l'action (e.g., l'utilisateur qui a liké)
    actor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='actions_made')
    
    # Description de l'action (e.g., 'aimé', 'commenté', 'suivi')
    verb = models.CharField(max_length=255)
    
    # Champ GenericForeignKey pour lier à l'objet cible (Post, Comment, User, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    
    # Statut et horodatage
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.actor.username} {self.verb} {self.target} à {self.timestamp.strftime('%Y-%m-%d %H:%M')}"