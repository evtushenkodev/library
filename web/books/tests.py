from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Author, Genre, Book


class AuthorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_author = Author.objects.create(
            name='Test Author',
            date_of_birth='2000-01-01',
            date_of_death='2022-03-15',
        )

    def test_author_creation(self):
        url = reverse('author-list')
        data = {
            'name': 'New Test Author',
            'date_of_birth': '2000-01-01',
            'date_of_death': '2022-03-15',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_author_detail(self):
        url = reverse('author-detail', args=[self.test_author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], 'Test Author')
        self.assertEqual(response.data['date_of_birth'], '2000-01-01')
        self.assertEqual(response.data['date_of_death'], '2022-03-15')

    def test_author_update(self):
        url = reverse('author-detail', args=[self.test_author.id])
        data = {
            'name': 'Updated Author',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Author.objects.get(id=self.test_author.id).name, 'Updated Author')

    def test_author_deletion(self):
        url = reverse('author-detail', args=[self.test_author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(id=self.test_author.id)


class GenreTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_genre = Genre.objects.create(name='Test Genre')

    def test_create_genre(self):
        url = reverse('genre-list')
        data = {
            'name': 'New Test Genre',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_genre_detail(self):
        url = reverse('genre-detail', args=[self.test_genre.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Genre')

    def test_update_genre(self):
        url = reverse('genre-detail', args=[self.test_genre.id])
        data = {
            'name': 'Updated Genre',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Genre.objects.get(id=self.test_genre.id).name, 'Updated Genre')

    def test_delete_genre(self):
        url = reverse('genre-detail', args=[self.test_genre.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Genre.DoesNotExist):
            Genre.objects.get(id=self.test_genre.id)


class BookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Author Name')
        self.genre = Genre.objects.create(name='Genre Name')

    def test_create_book(self):
        url = reverse('book-list')
        data = {
            'title': 'Test Book',
            'description': 'Test description',
            'publish_date': '2023-10-19',
            'authors': [self.author.name],
            'genres': [self.genre.name],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_book_detail(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            publish_date='2023-10-19',
        )
        book.authors.add(self.author)
        book.genres.add(self.genre)
        url = reverse('book-detail', args=[book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['description'], 'Test description')
        self.assertEqual(response.data['publish_date'], '2023-10-19')

    def test_update_book(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            publish_date='2023-10-19',
        )
        book.authors.add(self.author)
        book.genres.add(self.genre)
        url = reverse('book-detail', args=[book.id])
        data = {
            'title': 'Updated Book',
            'description': 'Updated description',
            'authors': [self.author.name],
            'genres': [self.genre.name],
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Book.objects.get(id=book.id).title, 'Updated Book')

    def test_delete_book(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            publish_date='2023-10-19',
        )
        book.authors.add(self.author)
        book.genres.add(self.genre)
        url = reverse('book-detail', args=[book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book.id)
