from graphene import Schema

from core.schemas.mutations import Mutation
from core.schemas.queries import Query

schema = Schema(query=Query, mutation=Mutation)
