from django.contrib import admin
from .models import Movie,Rating


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    fields = ['title', 'description']
    search_fields = ['title']
    list_display = ['title', 'description']
    list_filter = ['title']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    fields = ['user', 'movie', 'stars']
    search_fields = ['user', 'movie']
    list_display = ['user', 'movie']
    list_filter = ['movie']
