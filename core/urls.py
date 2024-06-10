from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from core import views
from core.schemas.schema import schema

app_name = 'core'

urlpatterns = [
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('authors/', views.Author.as_view(), name='authors'),
    path('publishers/', views.Publisher.as_view(), name='publishers'),
    path('genres/', views.Genre.as_view(), name='genres'),
    path('books/', views.Book.as_view(), name='books'),
    path('', views.Index.as_view(), name='index'),
]
