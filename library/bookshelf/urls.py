from django.urls import path
from .views import BookListViewCreateView

urlpatterns = [
    path('api/books/', BookListViewCreateView.as_view(), name='book-list-create'), 
]