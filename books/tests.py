from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Author, Genre, Book


class AuthorTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_author_creation(self):
        url = reverse('author-list')
        data = {
            'name': 'Test Author',
            'date_of_birth': '2000-01-01',
            'date_of_death': '2022-03-15',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_author_detail(self):
        author = Author.objects.create(
            name='Test Author',
            date_of_birth='2000-01-01',
            date_of_death='2022-03-15',
        )
        url = reverse('author-detail', args=[author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], 'Test Author')
        self.assertEqual(response.data['date_of_birth'], '2000-01-01')
        self.assertEqual(response.data['date_of_death'], '2022-03-15')

    def test_author_update(self):
        author = Author.objects.create(name='Test Author')
        url = reverse('author-detail', args=[author.id])
        data = {
            'name': 'Updated Author',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Author.objects.get(id=author.id).name, 'Updated Author')

    def test_author_deletion(self):
        author = Author.objects.create(name='Test Author')
        url = reverse('author-detail', args=[author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(id=author.id)


class GenreTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_genre(self):
        url = reverse('genre-list')
        data = {
            'name': 'Test Genre',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_genre_detail(self):
        genre = Genre.objects.create(name='Test Genre')
        url = reverse('genre-detail', args=[genre.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], 'Test Genre')

    def test_update_genre(self):
        genre = Genre.objects.create(name='Test Genre')
        url = reverse('genre-detail', args=[genre.id])
        data = {
            'name': 'Updated Genre',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Genre.objects.get(id=genre.id).name, 'Updated Genre')

    def test_delete_genre(self):
        genre = Genre.objects.create(name='Test Genre')
        url = reverse('genre-detail', args=[genre.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Genre.DoesNotExist):
            Genre.objects.get(id=genre.id)


class BookTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_book(self):
        author = Author.objects.create(name='Test Author')
        genre = Genre.objects.create(name='Test Genre')
        url = reverse('book-list')
        data = {
            'title': 'Test Book',
            'authors': [author.id],
            'description': 'Test description',
            'publish_date': '2023-10-19',
            'genres': [genre.id],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_book_detail(self):
        author = Author.objects.create(name='Test Author')
        genre = Genre.objects.create(name='Test Genre')
        book = Book.objects.create(
            title='Test Book',
            publish_date='2023-10-19',
        )
        book.authors.add(author)
        book.genres.add(genre)
        url = reverse('book-detail', args=[book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['description'], 'Test description')
        self.assertEqual(response.data['publish_date'], '2023-10-19')

    def test_update_book(self):
        author = Author.objects.create(name='Test Author')
        genre = Genre.objects.create(name='Test Genre')
        book = Book.objects.create(
            title='Test Book',
            publish_date='2023-10-19',
        )
        book.authors.add(author)
        book.genres.add(genre)
        url = reverse('book-detail', args=[book.id])
        data = {
            'title': 'Updated Book',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Book.objects.get(id=book.id).title, 'Updated Book')

    def test_delete_book(self):
        author = Author.objects.create(name='Test Author')
        genre = Genre.objects.create(name='Test Genre')
        book = Book.objects.create(
            title='Test Book',
            publish_date='2023-10-19',
        )
        book.authors.add(author)
        book.genres.add(genre)
        url = reverse('book-detail', args=[book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book.id)
