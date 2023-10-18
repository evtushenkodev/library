import uuid

from django.db import models
from django.db.models import UniqueConstraint


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='author')
    description = models.TextField(null=True)
    publish_date = models.DateField()
    genres = models.ManyToManyField(Genre, related_name='genres')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['title'], name='unique_book_title')
        ]

    def __str__(self):
        authors = ", ".join([str(author) for author in self.authors.all()])
        genres = ", ".join([str(genre) for genre in self.genres.all()])
        return f'{self.title}, автор: {authors}, жанр: {genres}'
