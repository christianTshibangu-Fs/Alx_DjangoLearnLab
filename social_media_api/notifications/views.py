from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
# Create your views here.


class NotificationListView(generics.ListAPIView):
    """
    Affiche la liste des notifications pour l'utilisateur connecté.
    Les notifications sont triées par horodatage inverse (plus récentes en premier).
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Récupère uniquement les notifications destinées à l'utilisateur connecté
        return Notification.objects.filter(recipient=self.request.user)

class MarkAsReadView(generics.GenericAPIView):
    """
    Marque une notification spécifique ou toutes les notifications comme lues.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        user = request.user
        
        if pk:
            # Marquer une seule notification comme lue
            try:
                notification = Notification.objects.get(pk=pk, recipient=user)
                notification.is_read = True
                notification.save()
                return Response({"detail": "Notification marquée comme lue."}, status=status.HTTP_200_OK)
            except Notification.DoesNotExist:
                return Response({"detail": "Notification non trouvée."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Marquer TOUTES les notifications non lues comme lues
            count = Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
            return Response({"detail": f"{count} notifications marquées comme lues."}, status=status.HTTP_200_OK)