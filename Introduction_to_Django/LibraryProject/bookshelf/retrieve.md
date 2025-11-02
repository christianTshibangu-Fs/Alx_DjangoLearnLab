Command Python (Django shell) :

    from bookshelf.models import Book
    book = Book.objects.get(id=1)
    print(f"Title : {book.title}")
    print(f"Author : {book.author}"
    print(f"Year : {book.publication_year}"))

Output :
    Title : 1984
    Author : George Orwell
    Year : 1949