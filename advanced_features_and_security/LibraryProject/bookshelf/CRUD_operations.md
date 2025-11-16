
1. Create
    from bookshelf.models import Book
    book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
    book.save()
    print(book)

Output :
    1984 by George Orwell (1949)

2. Retrieve

    from bookshelf.models import Book
    book = Book.objects.get(id=1)
    print(f"Title : {book.title}")
    print(f"Author : {book.author}"
    print(f"Year : {book.publication_year}"))

Output :
    Title : 1984
    Author : George Orwell
    Year : 1949

3. Update

    from bookshelf.models import Book
    book = Book.objects.get(title="1984")
    book.title = "nineteen Eighty-Four"
    book.save()
    print(Book.objects.get(id=book1.id).title)

Output :
    Nineteen Eighty-Four


4. Delete

    from bookshelf.models import Book
    book = Book.objects.get(author="George Orwell")
    book.delete()

Output :
    <QuerySet []>