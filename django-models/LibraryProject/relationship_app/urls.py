from django.urls import path
from .views import list_all_books, LibraryDetailView

urlpatterns = [
    path('books/', list_all_books, name='list_all_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
