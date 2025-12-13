from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, ProfileUpdateSerializer

CustomUser = get_user_model()

# Vue d'Enregistrement : Crée l'utilisateur et retourne le token
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Récupérer le token créé par le signal post_save
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# Vue de Gestion du Profil : Détail et Mise à Jour du profil de l'utilisateur connecté
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_object(self):
        # Assure que seul l'utilisateur connecté accède à son propre profil
        return self.request.user

    def get(self, request, *args, **kwargs):
        # Récupère l'objet (utilisateur connecté)
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


# --- NOUVEAU : Vues pour Gérer le Suivi (Follow/Unfollow) ---

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        """Permet à l'utilisateur actuel de suivre l'utilisateur spécifié par user_id."""
        
        # L'utilisateur à suivre
        user_to_follow = get_object_or_404(CustomUser, pk=user_id)
        
        # L'utilisateur qui suit (l'utilisateur connecté)
        current_user = request.user
        
        if current_user == user_to_follow:
            return Response(
                {"detail": "Vous ne pouvez pas vous suivre vous-même."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ajout de la relation de suivi
        current_user.following.add(user_to_follow)
        
        return Response(
            {"detail": f"Vous suivez maintenant {user_to_follow.username}."}, 
            status=status.HTTP_200_OK
        )

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        """Permet à l'utilisateur actuel de ne plus suivre l'utilisateur spécifié par user_id."""
        
        # L'utilisateur à ne plus suivre
        user_to_unfollow = get_object_or_404(CustomUser, pk=user_id)
        
        # L'utilisateur connecté
        current_user = request.user
        
        if current_user == user_to_unfollow:
            return Response(
                {"detail": "Action non applicable."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Suppression de la relation de suivi
        current_user.following.remove(user_to_unfollow)
        
        return Response(
            {"detail": f"Vous ne suivez plus {user_to_unfollow.username}."}, 
            status=status.HTTP_200_OK
        )