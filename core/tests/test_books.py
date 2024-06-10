import json
from datetime import date

from graphene_django.utils.testing import GraphQLTestCase

from core import models


class TestBook(GraphQLTestCase):
    def setUp(self) -> None:
        self.author = models.Author.objects.create(
            surname='surname', first_name='first_name', patronymic='patronymic', birthday=date.today()
        )
        self.publisher = models.Publisher.objects.create(name='publisher')
        self.genre = models.Genre.objects.create(name='genre')

        self.book = models.Book.objects.create(
            author=self.author, publisher=self.publisher, title='title', release_date=date.today()
        )
        self.book.genres.add(self.genre.id)

    def test_list(self) -> None:
        response = self.query(
            """
            query {
              allBooks{
                edges{
                  node{
                    id
                    title
                  }
                }
              }
            }
            """,
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['data']['allBooks']['edges']), models.Book.objects.count())

    def test_retrieve(self) -> None:
        response = self.query(
            """
            query {
              allBooks(id:1){
                edges{
                  node{
                    id
                    title
                  }
                }
              }
            }
            """,
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['data']['allBooks']['edges']), 1)
        self.assertEqual(content['data']['allBooks']['edges'][0]['node']['title'], self.book.title)

    def test_create(self) -> None:
        response = self.query(
            """
            mutation createBook{
              createBook(authorId:1, title:"title2", releaseDate:"1999-10-01", genresId:[1], publisherId:1) {
                    book {
                        author {
                          id
                        }
                        title
                        releaseDate
                        genres {
                          edges {
                            node {
                              id
                            }
                          }
                        }
                        publisher{
                          id
                        }
                    }
                }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Book.objects.count(), 2)
        self.assertEqual(models.Book.objects.last().title, 'title2')

    def test_update(self) -> None:
        response = self.query(
            """
            mutation updateBook {
              updateBook(id: 1, title: "new_title") {
                book{
                  id
                  title
                }
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Book.objects.count(), 1)
        self.assertEqual(models.Book.objects.first().title, 'new_title')

    def test_delete(self) -> None:
        response = self.query(
            """
            mutation updateBook {
              deleteBook(id: "1") {
                success
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Book.objects.count(), 0)
