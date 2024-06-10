import json
from datetime import date

from graphene_django.utils.testing import GraphQLTestCase

from core import models


class TestAuthor(GraphQLTestCase):
    def setUp(self) -> None:
        self.author = models.Author.objects.create(
            surname='surname', first_name='first_name', patronymic='patronymic', birthday=date.today()
        )

    def test_list(self) -> None:
        response = self.query(
            """
            query {
              allAuthors{
                edges{
                  node{
                    id
                    surname
                    firstName
                    patronymic
                    birthday
                  }
                }
              }
            }
            """,
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['data']['allAuthors']['edges']), models.Author.objects.count())

    def test_retrieve(self) -> None:
        response = self.query(
            """
            query {
              allAuthors(id:"1"){
                edges{
                  node{
                    id
                    surname
                    firstName
                    patronymic
                    birthday
                  }
                }
              }
            }
            """,
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['data']['allAuthors']['edges']), 1)
        self.assertEqual(content['data']['allAuthors']['edges'][0]['node']['surname'], self.author.surname)

    def test_create(self) -> None:
        response = self.query(
            """
            mutation createAuthor {
              createAuthor(surname: "new_surname", firstName:"fn", patronymic:"p", birthday:"2024-01-01"){
                author{
                  id
                  surname
                  firstName
                  patronymic
                  birthday
                }
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Author.objects.count(), 2)
        self.assertEqual(models.Author.objects.last().first_name, 'fn')

    def test_update(self) -> None:
        response = self.query(
            """
            mutation updateAuthor {
              updateAuthor(id: 1, surname: "new_surname") {
                author{
                  id
                  surname
                }
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Author.objects.count(), 1)
        self.assertEqual(models.Author.objects.first().surname, 'new_surname')

    def test_delete(self) -> None:
        response = self.query(
            """
            mutation deleteAuthor {
              deleteAuthor(id: "1") {
                success
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Author.objects.count(), 0)
