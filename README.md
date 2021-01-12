# django-grahene


#Installation

    pip install graphene-django
    
# Umpload Image 

    pip install graphene-file-upload
    
    https://github.com/lmcgartland/graphene-file-upload


PROJET

  1- Settings.py

    INSTALLED_APPS = [
        ...
       'graphene_django',
    ]

    ......

    GRAPHENE = {
        'SCHEMA': 'mon_projet.schema.schema'
    }
    
   2-urls.py
    
    from django.conf.urls import url, include
    from django.contrib import admin

    from graphene_django.views import GraphQLView

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^graphql$', GraphQLView.as_view(graphiql=True)),
    ]
    
  3 - schema.py
    
    import graphene

    import mon_application.schema


    class Query(mon_application.schema.Query, graphene.ObjectType):
        # This class will inherit from multiple Queries
        # as we begin to add more apps to our project
        pass

    schema = graphene.Schema(query=Query)
    
    class Mutation(mon_application.schema.Mutation, graphene.ObjectType):
    pass

    schema = graphene.Schema(query=Query,mutati on=Mutation)


APPLICATION 

1 - Models
    
          from django.db import models


          class Category(models.Model):
              name = models.CharField(max_length=100)

              def __str__(self):
                  return self.name


          class Ingredient(models.Model):
              name = models.CharField(max_length=100)
              notes = models.TextField()
              category = models.ForeignKey(
                  Category, related_name='ingredients', on_delete=models.CASCADE)

            def __str__(self):
                return self.name
                
# Methode 1 

pip install django-filter

#APPLICATION/schema.py

      import graphene
      from graphene import relay, ObjectType
      from graphene_django import DjangoObjectType
      from graphene_django.filter import DjangoFilterConnectionField

      from ingredients.models import Category, Ingredient


       Graphene will automatically map the Category model's fields onto the CategoryNode.
       This is configured in the CategoryNode's Meta class (as you can see below)
      class CategoryNode(DjangoObjectType):
          class Meta:
              model = Category
              filter_fields = ['name', 'ingredients']
              interfaces = (relay.Node, )


      class IngredientNode(DjangoObjectType):
          class Meta:
              model = Ingredient
              # Allow for some more advanced filtering here
              filter_fields = {
                  'name': ['exact', 'icontains', 'istartswith'],
                  'notes': ['exact', 'icontains'],
                  'category': ['exact'],
                  'category__name': ['exact'],
              }
              interfaces = (relay.Node, )


        class Query(graphene.ObjectType):
          category = relay.Node.Field(CategoryNode)
          all_categories = DjangoFilterConnectionField(CategoryNode)

          ingredient = relay.Node.Field(IngredientNode)
          all_ingredients = DjangoFilterConnectionField(IngredientNode)

  Test of query
    
               1- query {
                    allIngredients {
                      edges {
                        node {
                          id,
                          name
                        }
                      }
                    }
                  }

               2- query {
            allCategories {
              edges {
                node {
                  name,
                  ingredients {
                    edges {
                      node {
                        name
                      }
                    }
                  }
                }
              }
            }
          }

     
  ## METHODE 2
  
  2- schema.py
  
    import graphene

    from graphene_django.types import DjangoObjectType

    from cookbook.ingredients.models import Category, Ingredient


    class CategoryType(DjangoObjectType):
        class Meta:
            model = Category


    class IngredientType(DjangoObjectType):
        class Meta:
            model = Ingredient


    class Query(object):
        all_categories = graphene.List(CategoryType)
        all_ingredients = graphene.List(IngredientType)

        def resolve_all_categories(self, info, **kwargs):
            return Category.objects.all()

        def resolve_all_ingredients(self, info, **kwargs):
            # We can easily optimize query count in the resolve method
            return Ingredient.objects.select_related('category').all()
            
            
       #Exemple Test
       
       1- query {
          allIngredients {
            id
            name
           }
         }
         
         2- query {
                allIngredients {
                  id
                  name
                  category {
                      id
                      name
                    }
                }
              }

       


Lien 2 : https://stackabuse.com/building-a-graphql-api-with-django/


## avoid crsftoken error

    from django.views.decorators.csrf import csrf_exempt
    
    urlpatterns = [
    # ...
    path('...', csrf_exempt(views.myfonct) ),
   
    ]
