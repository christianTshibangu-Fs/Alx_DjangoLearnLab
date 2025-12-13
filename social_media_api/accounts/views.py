from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterSerializer, ProfileUpdateSerializer
from .models import CustomUser

# Create your views here.


# Vue d'Enregistrement (Création d'un nouvel utilisateur)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny] # Tout le monde peut s'enregistrer
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Étape 2: Retourner le token après l'enregistrement réussi
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# Vue de Gestion du Profil (Détail et Mise à Jour)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    # Seuls les utilisateurs authentifiés peuvent accéder à leur profil
    permission_classes = [permissions.IsAuthenticated] 

    # Surcharge pour garantir que l'utilisateur ne peut voir/modifier que son propre profil
    def get_object(self):
        return self.request.user