from django.db.models import QuerySet
from django.views.generic import ListView, TemplateView

from core import filters, models


class Author(ListView):
    template_name = 'core/author.html'
    model = models.Author

    def get_filters(self) -> filters:
        return filters.Author(self.request.GET)

    def get_queryset(self) -> QuerySet:
        return self.get_filters().qs

    def get_context_data(self, *, object_list: list = None, **kwargs: dict) -> dict:
        context = super().get_context_data()
        context['filters'] = self.get_filters()

        return context


class Publisher(ListView):
    template_name = 'core/publisher.html'
    model = models.Publisher

    def get_filters(self) -> filters:
        return filters.Publisher(self.request.GET)

    def get_queryset(self) -> QuerySet:
        return self.get_filters().qs

    def get_context_data(self, *, object_list: list = None, **kwargs: dict) -> dict:
        context = super().get_context_data()
        context['filters'] = self.get_filters()

        return context


class Book(ListView):
    template_name = 'core/book.html'
    model = models.Book

    def get_filters(self) -> filters:
        return filters.Book(self.request.GET)

    def get_queryset(self) -> QuerySet:
        return self.get_filters().qs

    def get_context_data(self, *, object_list: list = None, **kwargs: dict) -> dict:
        context = super().get_context_data()
        context['filters'] = self.get_filters()

        return context


class Genre(ListView):
    template_name = 'core/genre.html'
    model = models.Genre

    def get_filters(self) -> filters:
        return filters.Genre(self.request.GET)

    def get_queryset(self) -> QuerySet:
        return self.get_filters().qs

    def get_context_data(self, *, object_list: list = None, **kwargs: dict) -> dict:
        context = super().get_context_data()
        context['filters'] = self.get_filters()

        return context


class Index(TemplateView):
    template_name = 'core/index.html'
