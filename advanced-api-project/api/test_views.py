from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITests(APITestCase):
    """
    Suite de tests pour les endpoints de l'API Book.
    Teste le CRUD, les permissions, le filtrage, la recherche et le tri.
    """

    def setUp(self):
        """
        Configuration initiale exécutée avant CHAQUE test.
        Crée un utilisateur, un auteur et des livres de test.
        """
        # 1. Création d'un utilisateur pour l'authentification
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # 2. Création d'un auteur (nécessaire pour la ForeignKey)
        self.author = Author.objects.create(name="George Orwell")
        
        # 3. Création de livres de test
        self.book1 = Book.objects.create(
            title="1984", 
            publication_year=1949, 
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Animal Farm", 
            publication_year=1945, 
            author=self.author
        )

        # 4. URLs (Utilise les noms définis dans api/urls.py)
        # Assurez-vous que les noms correspondent à ceux de votre urls.py
        self.list_url = reverse('book-list-create') 
        self.detail_url = reverse('book-detail-update-destroy', args=[self.book1.id])

    # --- TESTS CRUD (Create, Read, Update, Delete) ---

    def test_list_books(self):
        """Vérifie que la liste des livres est récupérée correctement (Public)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # On a créé 2 livres dans setUp

    def test_create_book_authenticated(self):
        """Vérifie qu'un utilisateur connecté peut créer un livre."""
        self.client.login(username='testuser', password='password')
        data = {
            'title': 'Homage to Catalonia',
            'publication_year': 1938,
            'author': self.author.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'Homage to Catalonia')

    def test_update_book_authenticated(self):
        """Vérifie qu'un utilisateur connecté peut modifier un livre."""
        self.client.login(username='testuser', password='password')
        data = {
            'title': '1984 (Updated)',
            'publication_year': 1949,
            'author': self.author.id
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, '1984 (Updated)')

    def test_delete_book_authenticated(self):
        """Vérifie qu'un utilisateur connecté peut supprimer un livre."""
        self.client.login(username='testuser', password='password')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # --- TESTS DE PERMISSIONS ---

    def test_create_book_unauthenticated(self):
        """Vérifie qu'un utilisateur NON connecté NE PEUT PAS créer un livre."""
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        # Pas de login effectué
        response = self.client.post(self.list_url, data, format='json')
        # Doit retourner 403 Forbidden (ou 401 selon la config)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 

    def test_delete_book_unauthenticated(self):
        """Vérifie qu'un utilisateur NON connecté NE PEUT PAS supprimer un livre."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- TESTS FILTRAGE, RECHERCHE ET TRI ---

    def test_filter_books_by_year(self):
        """Teste le filtrage par année de publication."""
        # Filtre pour l'année 1949 (seulement book1)
        response = self.client.get(self.list_url, {'publication_year': 1949})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_search_books(self):
        """Teste la fonctionnalité de recherche (SearchFilter)."""
        # Recherche "Animal"
        response = self.client.get(self.list_url, {'search': 'Animal'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Animal Farm')

    def test_ordering_books(self):
        """Teste le tri des résultats (OrderingFilter)."""
        # Tri par titre (A-Z) : Animal Farm devrait être premier, 1984 deuxième
        # (Les chiffres viennent parfois avant les lettres selon la DB, 
        # mais testons par année pour être sûr).
        
        # Tri par année de publication décroissante (plus récent au plus ancien)
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], '1984')       # 1949
        self.assertEqual(response.data[1]['title'], 'Animal Farm') # 1945