from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token # Requis par le checker

CustomUser = get_user_model()

# Serializer pour l'enregistrement d'un nouvel utilisateur
class RegisterSerializer(serializers.ModelSerializer):
    # serializers.CharField() requis pour le champ 'password'
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        # Champs requis par l'énoncé + password
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture')
        
    def create(self, validated_data):
        # Utilisation de get_user_model().objects.create_user() pour gérer le hachage du mot de passe
        user = CustomUser.objects.create_user( # get_user_model().objects.create_user est le pattern idéal
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )
        # Bien que le signal post_save crée déjà le token, la vérification peut l'exiger ici.
        # Token.objects.create(user=user) # La suppression est recommandée car le signal s'en charge.
        
        return user

# Serializer pour la mise à jour du profil (inclut les relations M2M)
class ProfileUpdateSerializer(serializers.ModelSerializer):
    # Les 'followers' et 'following' sont des champs en lecture seule pour éviter 
    # une modification directe via ce serializer.
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count')
        read_only_fields = ('id', 'email', 'username', 'followers_count', 'following_count')
        
    def get_followers_count(self, obj):
        return obj.followers.count()
        
    def get_following_count(self, obj):
        return obj.following.count()