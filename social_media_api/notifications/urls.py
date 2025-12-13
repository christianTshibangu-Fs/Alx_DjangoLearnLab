from django.urls import path
from .views import NotificationListView, MarkAsReadView

urlpatterns = [
    # Récupérer toutes les notifications de l'utilisateur connecté
    path('', NotificationListView.as_view(), name='notification-list'),
    
    # Marquer toutes les notifications comme lues
    path('mark-all-read/', MarkAsReadView.as_view(), name='notification-mark-all-read'),
    
    # Marquer une notification spécifique comme lue
    path('<int:pk>/mark-read/', MarkAsReadView.as_view(), name='notification-mark-read-single'),
]