from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import path

from core import models


class SaveToFileMixin(admin.ModelAdmin):
    change_list_template = 'change_list.html'

    def get_urls(self) -> list:
        urls = super().get_urls()
        urls.insert(0, path('save/', self.save_file, name='applabel_modelname_download-file'))
        return urls

    def save_file(self, request: HttpRequest) -> HttpResponse:
        report = self.model.to_xlsx()

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{self.model._meta.model_name}s.xlsx"'
        report.save(response)
        return response


@admin.register(models.Author)
class Author(SaveToFileMixin, admin.ModelAdmin):
    list_display = ('surname', 'first_name', 'patronymic', 'birthday')
    search_fields = ('surname', 'first_name', 'patronymic', 'birthday')


@admin.register(models.Genre)
class Genre(SaveToFileMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(models.Publisher)
class Publisher(SaveToFileMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(models.Book)
class Book(SaveToFileMixin, admin.ModelAdmin):
    list_display = ('title', 'release_date', 'author', 'publisher')
    search_fields = ('title', 'release_date', 'author', 'publisher')
