import django_filters as filters
from django.db.models import Q, QuerySet

from core import models


class Book(filters.FilterSet):
    order_by = filters.OrderingFilter(
        fields=(
            'title',
            'release_date',
            'author',
        ),
    )
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = filters.CharFilter(method='filter_author')

    class Meta:
        model = models.Book
        fields = ('id', 'title', 'release_date', 'author', 'genres', 'publisher')

    def filter_author(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(
            Q(author__surname__icontains=value)
            | Q(author__first_name__icontains=value)
            | Q(author__patronymic__icontains=value)
        )


class Publisher(filters.FilterSet):
    order_by = filters.OrderingFilter(
        fields=('name',),
    )
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.Publisher
        fields = (
            'id',
            'name',
        )


class Genre(filters.FilterSet):
    order_by = filters.OrderingFilter(
        fields=('name',),
    )
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.Genre
        fields = (
            'id',
            'name',
        )


class Author(filters.FilterSet):
    order_by = filters.OrderingFilter(
        fields=(
            'surname',
            'first_name',
            'patronymic',
        ),
    )
    fio = filters.CharFilter(method='filter_fio')
    birthday_from = filters.CharFilter(field_name='birthday', lookup_expr='gt', label='День рождения с')
    birthday_to = filters.DateFilter(field_name='birthday', lookup_expr='lt', label='День рождения по')

    class Meta:
        model = models.Author
        fields = ('id', 'surname', 'first_name', 'patronymic', 'birthday', 'birthday_from', 'birthday_to', 'fio')

    def filter_fio(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(
            Q(surname__icontains=value) | Q(first_name__icontains=value) | Q(patronymic__icontains=value)
        )
