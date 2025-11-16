from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .form import ExempleForm

# Create your views here.

def home(request):
    return render(request, 'bookshelf/home.html')

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    book = Book.objects.all()
    context = {
        'books': book
    }
    return render(request, 'bookshelf/book_list.html', context)

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        pass
    return render(request, 'bookshelf/book_edit.html')

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        pass
    return render(request, 'bookshelf/book_create.html')

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        pass
    return render(request, 'bookshelf/book_delete.html')

def example_form(request):
    if request.method == 'POST':
        form = ExempleForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ExempleForm()
    return render(request, 'bookshelf/example_form.html', {'form': form})