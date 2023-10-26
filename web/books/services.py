from .models import Book, Author, Genre


class AuthorService:
    @classmethod
    def create_or_update_author(cls, instance, author_data):
        name = author_data.get('name')

        if Author.objects.filter(name=name).exclude(id=instance.id if instance else None).exists():
            return None, {'detail': 'Автор с таким именем уже существует'}
        if instance:
            for field in ['name', 'date_of_birth', 'date_of_death']:
                if field in author_data:
                    setattr(instance, field, author_data[field])
            instance.save()
            author = instance
        else:
            author = Author.objects.create(**author_data)
        return author, None


class GenreService:
    @classmethod
    def create_or_update_genre(cls, instance, genre_data):
        name = genre_data.get('name')

        if Genre.objects.filter(name=name).exclude(id=instance.id if instance else None).exists():
            return None, {'detail': 'Жанр с таким именем уже существует.'}

        if instance:
            instance.name = name
            instance.save()
            genre = instance
        else:
            genre = Genre.objects.create(**genre_data)
        return genre, None


class BookService:
    @classmethod
    def create_or_update_book(cls, instance, book_data, authors, genres):
        title = book_data.get('title')
        if title:
            if Book.objects.filter(title=title).exclude(id=instance.id if instance else None).exists():
                return None, {'detail': 'Книга с таким названием уже существует'}

        if instance:
            for field in ['title', 'description', 'publish_date']:
                if field in book_data:
                    setattr(instance, field, book_data[field])
            instance.save()
            book = instance
        else:
            # Если это создание новой книги
            book = Book.objects.create(**book_data)

        author_errors, genre_errors = cls.validate_authors_and_genres(authors, genres)
        if author_errors or genre_errors:
            return None, {'detail': 'Ошибка валидации.', 'errors': {'authors': author_errors, 'genres': genre_errors}}

        for author_name in authors:
            if author_name not in author_errors:
                author = Author.objects.get(name=author_name)
                book.authors.add(author)

        for genre_name in genres:
            if genre_name not in author_errors:
                genre = Genre.objects.get(name=genre_name)
                book.genres.add(genre)

        return book, None

    @classmethod
    def validate_authors_and_genres(cls, authors, genres):
        author_errors = []
        genre_errors = []

        author_exists = Author.objects.filter(name__in=authors).values_list('name', flat=True)
        for author_name in authors:
            if author_name not in author_exists:
                author_errors.append(f"Автор с именем '{author_name}' не найден в базе данных.")

        genre_exists = Genre.objects.filter(name__in=genres).values_list('name', flat=True)
        for genre_name in genres:
            if genre_name not in genre_exists:
                genre_errors.append(f"Жанр с именем '{genre_name}' не найден в базе данных.")

        return author_errors, genre_errors
