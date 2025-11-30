from django.urls import path, include
from .views import BookListCreateView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),  
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]    