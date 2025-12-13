from rest_framework import serializers
from .models import Post, Comment

# --- Serializer de Commentaire ---
class CommentSerializer(serializers.ModelSerializer):
    # Champ en lecture seule pour afficher le nom d'utilisateur de l'auteur
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'post', 'created_at', 'updated_at'] # L'auteur est défini dans la vue

# --- Serializer de Post ---
class PostSerializer(serializers.ModelSerializer):
    # Champ en lecture seule pour afficher le nom d'utilisateur de l'auteur
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    # Récupérer tous les commentaires du post (en lecture seule)
    # Note: On utilise `source='comments'` car c'est le `related_name` dans le modèle Comment
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_username', 'title', 'content', 
            'created_at', 'updated_at', 'comment_count', 'comments'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at', 'comment_count', 'comments']
        
    def get_comment_count(self, obj):
        """Calcule le nombre de commentaires pour le post."""
        return obj.comments.count()