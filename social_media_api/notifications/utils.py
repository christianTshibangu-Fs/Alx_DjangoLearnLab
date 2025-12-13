from django.contrib.contenttypes.models import ContentType
from django.db import models
from .models import Notification
from django.conf import settings

CustomUser = settings.AUTH_USER_MODEL

def create_notification(recipient: CustomUser, actor: CustomUser, verb: str, target: models.Model):
    """
    Crée une instance de Notification.
    
    Args:
        recipient: L'utilisateur qui recevra la notification.
        actor: L'utilisateur qui a déclenché l'action.
        verb: Le verbe décrivant l'action (e.g., 'aimé', 'commenté', 'suivi').
        target: L'objet cible de l'action (e.g., un Post, un Comment).
    """
    # Empêcher l'utilisateur de se notifier lui-même, sauf si l'action est spécifique (e.g. follow)
    if recipient == actor:
        # On pourrait ajouter ici une logique pour des cas spécifiques où l'auto-notification est autorisée
        return 

    # Récupérer le ContentType de l'objet cible
    target_content_type = ContentType.objects.get_for_model(target)
    
    # Créer et sauvegarder la notification
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=target_content_type,
        object_id=target.pk
    )