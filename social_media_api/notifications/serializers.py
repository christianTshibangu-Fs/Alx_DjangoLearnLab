from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Serializer simple pour l'utilisateur acteur (afin d'éviter les boucles d'import)
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username',)

class NotificationSerializer(serializers.ModelSerializer):
    # Utiliser le serializer simple pour l'acteur
    actor = ActorSerializer(read_only=True)
    
    # Afficher le nom du modèle cible (e.g., 'Post' ou 'Comment')
    target_model = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id', 
            'actor', 
            'verb', 
            'target_model',
            'object_id', 
            'timestamp', 
            'is_read'
        )
        read_only_fields = fields

    def get_target_model(self, obj):
        # Retourne le nom de la classe du modèle cible
        if obj.target:
            return obj.target.__class__.__name__
        return None