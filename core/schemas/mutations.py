from datetime import date

import graphene

from core import models
from core.schemas import types


class CreateAuthor(graphene.Mutation):
    class Arguments:
        surname = graphene.String(required=True)
        first_name = graphene.String(required=True)
        patronymic = graphene.String(required=True)
        birthday = graphene.types.datetime.Date(required=True)

    author = graphene.Field(types.Author)

    @classmethod
    def mutate(cls, root, info, surname: str, first_name: str, patronymic: str, birthday: date) -> 'CreateAuthor':  # noqa: ANN001
        author = models.Author(surname=surname, first_name=first_name, patronymic=patronymic, birthday=birthday)
        author.save()
        return CreateAuthor(author=author)


class CreateGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(types.Genre)

    @classmethod
    def mutate(cls, root, info, name: str) -> 'CreateGenre':  # noqa: ANN001
        genre = models.Genre(name=name)
        genre.save()
        return CreateGenre(genre=genre)


class CreatePublisher(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    publisher = graphene.Field(types.Publisher)

    @classmethod
    def mutate(cls, root, info, name: str) -> 'CreatePublisher':  # noqa: ANN001
        publisher = models.Publisher(name=name)
        publisher.save()
        return CreatePublisher(publisher=publisher)


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        release_date = graphene.types.datetime.Date(required=True)
        author_id = graphene.Int(required=True)
        genres_id = graphene.List(graphene.Int)
        publisher_id = graphene.Int(required=True)

    book = graphene.Field(types.Book)

    @classmethod
    def mutate(
        cls,
        root,  # noqa: ANN001
        info,  # noqa: ANN001
        title: str,
        release_date: date,
        author_id: int,
        genres_id: list[int],
        publisher_id: int,
    ) -> 'CreatePublisher':
        author = models.Author.objects.get(id=author_id)
        publisher = models.Publisher.objects.get(id=publisher_id)
        genres = models.Genre.objects.filter(id__in=genres_id)

        book = models.Book(title=title, release_date=release_date, author=author, publisher=publisher)
        book.save()
        book.genres.add(*genres)
        return CreateBook(book=book)


class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        surname = graphene.String()
        first_name = graphene.String()
        patronymic = graphene.String()
        birthday = graphene.types.datetime.Date()

    author = graphene.Field(types.Author)

    @classmethod
    def mutate(
        cls,
        root,  # noqa: ANN001
        info,  # noqa: ANN001
        id: int,
        surname: str = None,
        first_name: str = None,
        patronymic: str = None,
        birthday: date = None,
    ) -> 'UpdateAuthor':
        author = models.Author.objects.get(pk=id)
        if surname:
            author.surname = surname
        if first_name:
            author.first_name = first_name
        if patronymic:
            author.patronymic = patronymic
        if birthday:
            author.birthday = birthday
        author.save()
        return UpdateAuthor(author=author)


class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    genre = graphene.Field(types.Genre)

    @classmethod
    def mutate(cls, root, info, id: int, name: str = None) -> 'UpdateGenre':  # noqa: ANN001
        genre = models.Genre.objects.get(pk=id)
        if name:
            genre.name = name
        genre.save()
        return UpdateGenre(genre=genre)


class UpdatePublisher(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    publisher = graphene.Field(types.Publisher)

    @classmethod
    def mutate(cls, root, info, id: int, name: str = None) -> 'UpdatePublisher':  # noqa: ANN001  # noqa: ANN001
        publisher = models.Publisher.objects.get(pk=id)
        if name:
            publisher.name = name
        publisher.save()
        return UpdatePublisher(publisher=publisher)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=False)
        release_date = graphene.types.datetime.Date(required=False)
        author_id = graphene.Int(required=False)
        genres_id = graphene.List(graphene.Int)
        publisher_id = graphene.Int(required=False)

    book = graphene.Field(types.Book)

    @classmethod
    def mutate(
        cls,
        root,  # noqa: ANN001
        info,  # noqa: ANN001
        id: int,
        title: str = None,
        release_date: date = None,
        author_id: int = None,
        genres_id: list[int] = None,
        publisher_id: int = None,
    ) -> 'UpdateBook':  # noqa: ANN001
        book = models.Book.objects.get(id=id)
        if title:
            book.title = title
        if release_date:
            book.release_date = release_date
        if author_id:
            book.author = models.Author.objects.get(id=author_id)
        if publisher_id:
            book.publisher = models.Publisher.objects.get(id=publisher_id)
        if genres_id:
            book.genres.set(models.Genre.objects.filter(id__in=genres_id), clear=True)
        book.save()
        return UpdateBook(book=book)


class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id: int) -> 'DeleteAuthor':  # noqa: ANN001
        author = models.Author.objects.get(pk=id)
        author.delete()
        return DeleteAuthor(success=True)


class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id: int) -> 'DeleteGenre':  # noqa: ANN001
        genre = models.Genre.objects.get(pk=id)
        genre.delete()
        return DeleteGenre(success=True)


class DeletePublisher(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id: int) -> 'DeletePublisher':  # noqa: ANN001
        publisher = models.Publisher.objects.get(pk=id)
        publisher.delete()
        return DeletePublisher(success=True)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id: int) -> 'DeleteBook':  # noqa: ANN001
        book = models.Book.objects.get(pk=id)
        book.delete()
        return DeleteBook(success=True)


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()

    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()

    create_publisher = CreatePublisher.Field()
    update_publisher = UpdatePublisher.Field()
    delete_publisher = DeletePublisher.Field()

    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
