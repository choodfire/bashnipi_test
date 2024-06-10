from graphene import relay
from graphene_django import DjangoObjectType

from core import models


class Author(DjangoObjectType):
    class Meta:
        model = models.Author
        interfaces = (relay.Node,)


class Genre(DjangoObjectType):
    class Meta:
        model = models.Genre
        interfaces = (relay.Node,)


class Publisher(DjangoObjectType):
    class Meta:
        model = models.Publisher
        interfaces = (relay.Node,)


class Book(DjangoObjectType):
    class Meta:
        model = models.Book
        interfaces = (relay.Node,)
