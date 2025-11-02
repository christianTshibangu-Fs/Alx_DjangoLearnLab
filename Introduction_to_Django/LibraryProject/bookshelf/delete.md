Command Python (Django shell) :

    from bookshelf.models import Book
    book = Book.objects.get(author="George Orwell")
    book.delete()

Output :
    <QuerySet []>