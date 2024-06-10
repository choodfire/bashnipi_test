import json

from graphene_django.utils.testing import GraphQLTestCase

from core import models


class TestPublisher(GraphQLTestCase):
    def setUp(self) -> None:
        self.publisher = models.Publisher.objects.create(name='publisher')

    def test_list(self) -> None:
        response = self.query(
            """
            query {
              allPublishers{
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
        self.assertEqual(len(content['data']['allPublishers']['edges']), models.Publisher.objects.count())

    def test_retrieve(self) -> None:
        response = self.query(
            """
            query {
              allPublishers(id:1){
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
        self.assertEqual(len(content['data']['allPublishers']['edges']), 1)
        self.assertEqual(content['data']['allPublishers']['edges'][0]['node']['name'], self.publisher.name)

    def test_create(self) -> None:
        response = self.query(
            """
            mutation createPublisher {
              createPublisher(name: "new_name"){
                publisher{
                  id
                  name
                }
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Publisher.objects.count(), 2)
        self.assertEqual(models.Publisher.objects.last().name, 'new_name')

    def test_update(self) -> None:
        response = self.query(
            """
            mutation updatePublisher {
              updatePublisher(id: 1, name: "new_name") {
                publisher{
                  id
                  name
                }
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Publisher.objects.count(), 1)
        self.assertEqual(models.Publisher.objects.first().name, 'new_name')

    def test_delete(self) -> None:
        response = self.query(
            """
            mutation deletePublisher {
              deletePublisher(id: "1") {
                success
              }
            }
            """,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Book.objects.count(), 0)
