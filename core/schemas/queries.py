import graphene
from graphene import Field, ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from core import filters
from core.schemas import types


class Query(ObjectType):
    all_authors = DjangoFilterConnectionField(types.Author, filterset_class=filters.Author)
    author = Field(types.Author, id=graphene.Int())

    all_genres = DjangoFilterConnectionField(types.Genre, filterset_class=filters.Genre)
    genre = Field(types.Genre, id=graphene.Int())

    all_publishers = DjangoFilterConnectionField(types.Publisher, filterset_class=filters.Publisher)
    publisher = Field(types.Publisher, id=graphene.Int())

    all_books = DjangoFilterConnectionField(types.Book, filterset_class=filters.Book)
    book = relay.Node.Field(types.Book)
