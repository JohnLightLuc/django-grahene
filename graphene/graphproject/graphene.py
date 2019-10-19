
#METHODE 1

#Installation

pip install graphene-django


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
    
    3 - schemma.py
    
    import graphene

    import mon_application.schema


    class Query(mon_application.schema.Query, graphene.ObjectType):
        # This class will inherit from multiple Queries
        # as we begin to add more apps to our project
        pass

    schema = graphene.Schema(query=Query)


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

       

        
        
