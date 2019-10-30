from django.contrib import admin

# Register your models here.
# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class ActorAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class MovieAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'year')
    list_filter = ('id', 'title', 'year')
    raw_id_fields = ('actors',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Actor, ActorAdmin)
_register(models.Movie, MovieAdmin)
