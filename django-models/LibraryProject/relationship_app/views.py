from django.shortcuts import render
from django.views.generic import DetailView
from .models import Author, Book, Library, Librarian
# Create your views here.

def list_all_books(request):
    books = Book.objects.all().select_related('author')

    context = {
        'books': books
    }   

    return render(request, 'list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('books__author')