from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
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