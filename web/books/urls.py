from django.urls import path

from .views import (
    AuthorListCreateView, AuthorDetailView, GenreListCreateView, GenreDetailView,
    BookListCreateView, BookDetailView,
)

urlpatterns = [
    path('authors/', AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<uuid:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('genres/', GenreListCreateView.as_view(), name='genre-list'),
    path('genres/<uuid:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<uuid:pk>/', BookDetailView.as_view(), name='book-detail'),
]
