Type de champs en graphene 

import graphene

graphene.String
graphene.Int
graphene.Float
graphene.Boolean
graphene.ID
graphene.types.datetime.Date
graphene.types.datetime.DateTime
graphene.types.datetime.Time
graphene.types.json.JSONString
graphene.Field(graphene.String)
graphene.Enum('Episode', [('NEWHOPE', 4), ('EMPIRE', 5), ('JEDI', 6)])
