Command Python (Django shell) :

    from bookshelf.models import Book
    book = Book.objects.get(title="1984")
    book.title = "nineteen Eighty-Four"
    book.save()
    print(Book.objects.get(id=book1.id).title)

Output :
    Nineteen Eighty-Four