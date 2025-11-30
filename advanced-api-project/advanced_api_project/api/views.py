from django.shortcuts import render
from rest_framework.generics import ListAPIView
# Create your views here.

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

