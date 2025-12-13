from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

# Serializer pour l'enregistrement d'un nouvel utilisateur
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # Champs obligatoires pour l'enregistrement (et les nouveaux champs)
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture')
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )
        return user

# Serializer pour la mise à jour du profil (les champs peuvent être optionnels)
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'following')
        read_only_fields = ('id', 'followers', 'following')