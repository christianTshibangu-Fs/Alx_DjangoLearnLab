from relationship_app.models import Author, Book, Library, Librarian
from django.db.models import QuerySet

def query_all_books_by_author(author_name: str) -> QuerySet[Book]:
    """
    Récupère tous les livres écrits par un auteur spécifique.
    (Utilisation de la relation ForeignKey inversée)
    """
    try:
        # 1. Trouver l'auteur par son nom
        author = Author.objects.get(name=author_name)
        
        # 2. Utiliser le 'related_name' ('books') pour accéder aux livres
        books = author.books.all()
        
        print(f"\n--- Requête 1: Livres de {author_name} ---")
        if books.exists():
            for book in books:
                print(f"  - {book.title}")
        else:
            print(f"  - Aucun livre trouvé pour {author_name}.")
        return books
    except Author.DoesNotExist:
        print(f"\n--- Erreur: Auteur '{author_name}' non trouvé. ---")
        return Book.objects.none()


def list_all_books_in_library(library_name: str) -> QuerySet[Book]:
    """
    Liste tous les livres contenus dans une bibliothèque spécifique.
    (Utilisation de la relation ManyToMany)
    """
    try:
        # 1. Trouver la bibliothèque par son nom
        library = Library.objects.get(name=library_name)
        
        # 2. Accéder aux livres via le ManyToManyField
        books = library.books.all()
        
        print(f"\n--- Requête 2: Livres dans {library_name} ---")
        if books.exists():
            for book in books:
                print(f"  - {book.title} (by {book.author.name})")
        else:
            print(f"  - Aucun livre trouvé dans {library_name}.")
        return books
    except Library.DoesNotExist:
        print(f"\n--- Erreur: Bibliothèque '{library_name}' non trouvée. ---")
        return Book.objects.none()


def retrieve_librarian_for_library(library_name: str) -> Librarian | None:
    """
    Récupère le bibliothécaire responsable d'une bibliothèque.
    (Utilisation de la relation OneToOne)
    """
    print(f"\n--- Requête 3: Bibliothécaire pour {library_name} ---")
    try:
        # 1. Récupérer l'instance de la bibliothèque (qui est la clé primaire du bibliothécaire)
        library = Library.objects.get(name=library_name)
        
        # 2. Utiliser la relation OneToOne inversée (le nom du modèle est l'attribut par défaut)
        # Note : Si vous définissez 'library' comme PK sur Librarian, vous pouvez accéder directement.
        librarian = Librarian.objects.get(pk=library.pk)
        
        print(f"  - Bibliothécaire : {librarian.name}")
        print(f"  - ID Bibliothèque : {librarian.library_id}")
        return librarian
    except Library.DoesNotExist:
        print(f"  - Erreur: Bibliothèque '{library_name}' non trouvée.")
        return None
    except Librarian.DoesNotExist:
        print(f"  - Erreur: Aucun bibliothécaire trouvé pour '{library_name}'.")
        return None

def setup_data():
    """Crée des données de test pour exécuter les requêtes."""
    print("--- Configuration des données de test ---")
    # 1. Auteurs
    author_orwell, _ = Author.objects.get_or_create(name='George Orwell')
    author_huxley, _ = Author.objects.get_or_create(name='Aldous Huxley')

    # 2. Livres
    book_1984, _ = Book.objects.get_or_create(title='1984', author=author_orwell)
    book_animal_farm, _ = Book.objects.get_or_create(title='Animal Farm', author=author_orwell)
    book_brave_new_world, _ = Book.objects.get_or_create(title='Brave New World', author=author_huxley)

    # 3. Bibliothèques
    library_central, created_central = Library.objects.get_or_create(name='Central Library')
    library_west, created_west = Library.objects.get_or_create(name='West Branch')

    # 4. Association Livres/Bibliothèques (ManyToMany)
    if created_central:
        library_central.books.add(book_1984, book_animal_farm, book_brave_new_world)
    if created_west:
        library_west.books.add(book_1984, book_brave_new_world)
        
    # 5. Bibliothécaires (OneToOne)
    Librarian.objects.get_or_create(name='Jane Smith', library=library_central)
    Librarian.objects.get_or_create(name='John Doe', library=library_west)
    print("Données de base créées.")


def run_queries():
    """Exécute toutes les fonctions de requête."""
    setup_data()
    
    # Exécution des requêtes demandées
    query_all_books_by_author("George Orwell")
    list_all_books_in_library("Central Library")
    retrieve_librarian_for_library("Central Library")

if __name__ == '__main__':
    # Ceci est un script de démonstration. 
    # Normalement, il serait exécuté après l'initialisation de l'environnement Django.
    print("Veuillez exécuter ce script via le Django shell ou un setup de test.")
    # Pour l'environnement de test automatisé, l'appel à run_queries() serait fait ici 
    # après la configuration de l'environnement Django.
