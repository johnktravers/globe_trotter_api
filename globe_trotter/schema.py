import graphene

import trips.schema

class Query(trips.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
