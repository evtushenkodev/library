from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Author, Book, Genre
from .serializers import AuthorSerializer, BookSerializer, GenreSerializer
from .services import BookService, AuthorService, GenreService


class AuthorListCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        author, error_response = AuthorService.create_or_update_author(None, request.data)

        if error_response:
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(author)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        author, error_response = AuthorService.create_or_update_author(instance, request.data)

        if error_response:
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(author)
        return Response(serializer.data)


class GenreListCreateView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        genre, error_response = GenreService.create_or_update_genre(None, request.data)

        if error_response:
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(genre)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GenreDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        author, error_response = GenreService.create_or_update_genre(instance, request.data)

        if error_response:
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(author)
        return Response(serializer.data)


class BookListCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            authors_data = request.data.pop('authors', [])
            genres_data = request.data.pop('genres', [])
            book, error_response = BookService.create_or_update_book(
                None, request.data, authors_data, genres_data
            )

            if error_response:
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        title = request.query_params.get('title')
        if title:
            books = Book.objects.filter(title__icontains=title)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)


class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        authors_data = request.data.get('authors', [])
        genres_data = request.data.get('genres', [])

        book, error_response = BookService.create_or_update_book(
            instance, request.data, authors_data, genres_data
        )

        if error_response:
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(book)
        return Response(serializer.data)
