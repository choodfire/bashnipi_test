import json

from graphene_django.utils.testing import GraphQLTestCase

from core import models


class TestGenre(GraphQLTestCase):
    def setUp(self) -> None:
        self.genre = models.Genre.objects.create(name='genre')

    def test_list(self) -> None:
        response = self.query(
            """
            query {
              allGenres{
                edges{
                  node{
                    id
                    name
                  }
                }
              }
            }
            """,
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['data']['allGenres']['edges']), models.Genre.objects.count())

    def test_retrieve(self) -> None:
        response = self.query(
            """
            query {
              allGenres(id:1){
                edges{
                  node{
                    id
                    name
                  }
                }
              }
            }
            """,
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['data']['allGenres']['edges']), 1)
        self.assertEqual(content['data']['allGenres']['edges'][0]['node']['name'], self.genre.name)

    def test_create(self) -> None:
        response = self.query(
            """
            mutation createGenre {
              createGenre(name: "new_name"){
                genre{
                  id
                  name
                }
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Genre.objects.count(), 2)
        self.assertEqual(models.Genre.objects.last().name, 'new_name')

    def test_update(self) -> None:
        response = self.query(
            """
            mutation updateGenre {
              updateGenre(id: 1, name: "new_name") {
                genre{
                  id
                  name
                }
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Genre.objects.count(), 1)
        self.assertEqual(models.Genre.objects.first().name, 'new_name')

    def test_delete(self) -> None:
        response = self.query(
            """
            mutation deleteGenre {
              deleteGenre(id: "1") {
                success
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Genre.objects.count(), 0)
